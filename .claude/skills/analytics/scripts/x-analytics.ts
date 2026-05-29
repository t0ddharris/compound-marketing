/**
 * X (Twitter) Post Analytics — CLI script
 * Usage: npx tsx .claude/skills/analytics/scripts/x-analytics.ts [command] [period] [limit]
 *   command: posts | profile (default: posts)
 *   period:  7d | 30d | 90d (default: 30d)
 *   limit:   number of tweets to show (default: 20)
 *
 * Requires: X_BEARER_TOKEN, X_USERNAME in .env
 * Note: Requires X Premium+ (or equivalent) for analytics access.
 */
import {
  loadEnv,
  requireEnv,
  parseArgs,
  xGet,
  markdownTable,
  num,
  shortNum,
  pct,
  periodToDates,
  truncate,
  relativeDate,
} from "./lib.js";

loadEnv();
const token = requireEnv("X_BEARER_TOKEN");
const username = process.env.X_USERNAME ?? "your-x-handle";
const args = parseArgs({ command: "posts", period: "30d", limit: "20" });
const { start, end } = periodToDates(args.period);
const limit = parseInt(args.limit) || 20;

// ── Get User ID ─────────────────────────────────────────────

interface XUser {
  id: string;
  name: string;
  username: string;
  public_metrics: {
    followers_count: number;
    following_count: number;
    tweet_count: number;
    listed_count: number;
  };
}

async function getUser(): Promise<XUser> {
  const data = await xGet<{ data: XUser }>(
    `/users/by/username/${username}`,
    token,
    { "user.fields": "public_metrics" }
  );
  return data.data;
}

// ── Get Tweets ──────────────────────────────────────────────

interface XTweet {
  id: string;
  text: string;
  created_at: string;
  public_metrics: {
    retweet_count: number;
    reply_count: number;
    like_count: number;
    quote_count: number;
    bookmark_count: number;
    impression_count: number;
  };
}

async function getTweets(userId: string): Promise<XTweet[]> {
  const allTweets: XTweet[] = [];
  let paginationToken: string | undefined;

  // X API v2 returns max 100 per request
  const perPage = Math.min(limit, 100);

  for (let page = 0; page < 5; page++) {
    const params: Record<string, string> = {
      "tweet.fields": "public_metrics,created_at",
      max_results: String(perPage),
      start_time: new Date(start).toISOString(),
      end_time: new Date(end + "T23:59:59Z").toISOString(),
      exclude: "retweets,replies",
    };
    if (paginationToken) params.pagination_token = paginationToken;

    const data = await xGet<{
      data?: XTweet[];
      meta?: { next_token?: string; result_count: number };
    }>(`/users/${userId}/tweets`, token, params);

    if (data.data) allTweets.push(...data.data);

    paginationToken = data.meta?.next_token;
    if (!paginationToken || allTweets.length >= limit) break;
  }

  return allTweets.slice(0, limit);
}

// ── Main ────────────────────────────────────────────────────

const output: string[] = [];
output.push(`# X (@${username}) Analytics (${args.period})`);
output.push(`Period: ${start} to ${end}\n`);

try {
  const user = await getUser();

  // Profile stats
  const m = user.public_metrics;
  output.push("## Profile\n");
  output.push(
    markdownTable(
      ["Metric", "Value"],
      [
        ["Followers", num(m.followers_count)],
        ["Following", num(m.following_count)],
        ["Total Tweets", num(m.tweet_count)],
        ["Listed", num(m.listed_count)],
      ]
    )
  );
  output.push("");

  if (args.command === "posts" || args.command === "overview") {
    const tweets = await getTweets(user.id);

    if (tweets.length === 0) {
      output.push(`*No original tweets found in the ${args.period} period.*`);
    } else {
      // Aggregate stats
      const totals = tweets.reduce(
        (acc, t) => ({
          impressions: acc.impressions + t.public_metrics.impression_count,
          likes: acc.likes + t.public_metrics.like_count,
          retweets: acc.retweets + t.public_metrics.retweet_count,
          replies: acc.replies + t.public_metrics.reply_count,
          bookmarks: acc.bookmarks + t.public_metrics.bookmark_count,
          quotes: acc.quotes + t.public_metrics.quote_count,
        }),
        { impressions: 0, likes: 0, retweets: 0, replies: 0, bookmarks: 0, quotes: 0 }
      );

      const totalEngagements =
        totals.likes + totals.retweets + totals.replies + totals.quotes + totals.bookmarks;

      output.push(`## Aggregate (${tweets.length} tweets)\n`);
      output.push(
        markdownTable(
          ["Metric", "Value"],
          [
            ["Total Impressions", shortNum(totals.impressions)],
            ["Total Likes", num(totals.likes)],
            ["Total Retweets", num(totals.retweets)],
            ["Total Replies", num(totals.replies)],
            ["Total Bookmarks", num(totals.bookmarks)],
            ["Total Quotes", num(totals.quotes)],
            [
              "Engagement Rate",
              totals.impressions > 0
                ? pct(totalEngagements / totals.impressions)
                : "N/A",
            ],
            [
              "Avg Impressions/Tweet",
              shortNum(Math.round(totals.impressions / tweets.length)),
            ],
          ]
        )
      );

      // Per-tweet breakdown, sorted by impressions
      const sorted = [...tweets].sort(
        (a, b) =>
          b.public_metrics.impression_count - a.public_metrics.impression_count
      );

      output.push("\n## Top Tweets\n");
      output.push(
        markdownTable(
          ["Tweet", "Date", "Impr.", "Likes", "RTs", "Replies", "Eng.%"],
          sorted.map((t) => {
            const pm = t.public_metrics;
            const eng =
              pm.like_count +
              pm.retweet_count +
              pm.reply_count +
              pm.quote_count +
              pm.bookmark_count;
            return [
              truncate(t.text.replace(/\n/g, " "), 50),
              relativeDate(t.created_at),
              shortNum(pm.impression_count),
              num(pm.like_count),
              num(pm.retweet_count),
              num(pm.reply_count),
              pm.impression_count > 0
                ? pct(eng / pm.impression_count)
                : "N/A",
            ];
          })
        )
      );
    }
  }
} catch (err) {
  output.push(
    `> **Error:** ${err instanceof Error ? err.message : String(err)}`
  );
}

console.log(output.join("\n"));
