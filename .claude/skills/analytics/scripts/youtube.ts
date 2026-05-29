/**
 * YouTube Channel & Video Analytics — CLI script
 * Usage: npx tsx .claude/skills/analytics/scripts/youtube.ts [command] [period] [limit]
 *   command: channel | videos (default: channel)
 *   period:  7d | 30d | 90d (default: 30d)
 *   limit:   number of videos to show (default: 10)
 *
 * Requires: YOUTUBE_ACCESS_TOKEN, YOUTUBE_CHANNEL_ID in .env
 */
import {
  loadEnv,
  requireEnv,
  parseArgs,
  youtubeGet,
  markdownTable,
  num,
  shortNum,
  pct,
  periodToDates,
  truncate,
  relativeDate,
} from "./lib.js";

loadEnv();
const accessToken = requireEnv("YOUTUBE_ACCESS_TOKEN");
const channelId = requireEnv("YOUTUBE_CHANNEL_ID");
const args = parseArgs({ command: "channel", period: "30d", limit: "10" });
const { start, end } = periodToDates(args.period);
const limit = parseInt(args.limit) || 10;

// ── Channel Overview ────────────────────────────────────────

interface ChannelStats {
  items?: Array<{
    statistics: {
      viewCount: string;
      subscriberCount: string;
      videoCount: string;
    };
    snippet: { title: string };
  }>;
}

async function getChannelOverview(): Promise<string[]> {
  const sections: string[] = [];

  try {
    const data = await youtubeGet<ChannelStats>(
      "/youtube/v3/channels",
      accessToken,
      {
        part: "statistics,snippet",
        id: channelId,
      }
    );

    const ch = data.items?.[0];
    if (ch) {
      sections.push(`**Channel:** ${ch.snippet.title}\n`);
      sections.push(
        markdownTable(
          ["Metric", "Value"],
          [
            ["Subscribers", num(parseInt(ch.statistics.subscriberCount))],
            ["Total Views", shortNum(parseInt(ch.statistics.viewCount))],
            ["Videos Published", num(parseInt(ch.statistics.videoCount))],
          ]
        )
      );
    }
  } catch (err) {
    sections.push(
      `> Error fetching channel: ${err instanceof Error ? err.message : String(err)}`
    );
  }
  return sections;
}

// ── Analytics Report ────────────────────────────────────────

interface AnalyticsReport {
  columnHeaders: Array<{ name: string }>;
  rows?: Array<Array<string | number>>;
}

async function getChannelAnalytics(): Promise<string[]> {
  const sections: string[] = [];

  try {
    const data = await youtubeGet<AnalyticsReport>(
      "/youtube/analytics/v2/reports",
      accessToken,
      {
        ids: `channel==${channelId}`,
        startDate: start,
        endDate: end,
        metrics:
          "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,comments,shares",
      }
    );

    if (data.rows && data.rows.length > 0) {
      const row = data.rows[0];
      const views = Number(row[0]) || 0;
      const watchMins = Number(row[1]) || 0;
      const avgDuration = Number(row[2]) || 0;
      const subsGained = Number(row[3]) || 0;
      const subsLost = Number(row[4]) || 0;
      const likes = Number(row[5]) || 0;
      const comments = Number(row[6]) || 0;
      const shares = Number(row[7]) || 0;

      const avgMinutes = Math.floor(avgDuration / 60);
      const avgSeconds = Math.round(avgDuration % 60);

      sections.push(
        markdownTable(
          ["Metric", "Value"],
          [
            ["Views", num(views)],
            ["Watch Time (hours)", num(Math.round(watchMins / 60))],
            [
              "Avg View Duration",
              `${avgMinutes}:${String(avgSeconds).padStart(2, "0")}`,
            ],
            ["Subscribers Gained", `+${num(subsGained)}`],
            ["Subscribers Lost", `-${num(subsLost)}`],
            ["Net Subscribers", num(subsGained - subsLost)],
            ["Likes", num(likes)],
            ["Comments", num(comments)],
            ["Shares", num(shares)],
          ]
        )
      );
    } else {
      sections.push("*No analytics data for this period.*");
    }
  } catch (err) {
    sections.push(
      `> Error fetching analytics: ${err instanceof Error ? err.message : String(err)}`
    );
  }
  return sections;
}

// ── Top Videos ──────────────────────────────────────────────

async function getTopVideos(): Promise<string[]> {
  const sections: string[] = [];

  try {
    // Get top videos by views from Analytics API
    const data = await youtubeGet<AnalyticsReport>(
      "/youtube/analytics/v2/reports",
      accessToken,
      {
        ids: `channel==${channelId}`,
        startDate: start,
        endDate: end,
        metrics: "views,estimatedMinutesWatched,likes,comments,subscribersGained",
        dimensions: "video",
        sort: "-views",
        maxResults: String(limit),
      }
    );

    if (data.rows && data.rows.length > 0) {
      // Get video titles
      const videoIds = data.rows.map((r) => String(r[0])).join(",");
      const videosData = await youtubeGet<{
        items?: Array<{
          id: string;
          snippet: { title: string; publishedAt: string };
        }>;
      }>("/youtube/v3/videos", accessToken, {
        part: "snippet",
        id: videoIds,
      });

      const titleMap = new Map<string, { title: string; published: string }>();
      for (const v of videosData.items ?? []) {
        titleMap.set(v.id, {
          title: v.snippet.title,
          published: v.snippet.publishedAt,
        });
      }

      sections.push(
        markdownTable(
          ["Video", "Views", "Watch Hrs", "Likes", "Comments", "Subs+"],
          data.rows.map((row) => {
            const videoId = String(row[0]);
            const info = titleMap.get(videoId);
            const title = info?.title ?? videoId;
            return [
              truncate(title, 45),
              num(Number(row[1]) || 0),
              num(Math.round((Number(row[2]) || 0) / 60)),
              num(Number(row[3]) || 0),
              num(Number(row[4]) || 0),
              num(Number(row[5]) || 0),
            ];
          })
        )
      );
    } else {
      sections.push("*No video data for this period.*");
    }
  } catch (err) {
    sections.push(
      `> Error fetching videos: ${err instanceof Error ? err.message : String(err)}`
    );
  }
  return sections;
}

// ── Main ────────────────────────────────────────────────────

const output: string[] = [];
output.push(`# YouTube Analytics (${args.period})`);
output.push(`Period: ${start} to ${end}\n`);

output.push("## Channel Overview\n");
output.push(...(await getChannelOverview()));
output.push("");

output.push(`## Performance (${args.period})\n`);
output.push(...(await getChannelAnalytics()));
output.push("");

if (args.command === "videos") {
  output.push("## Top Videos\n");
  output.push(...(await getTopVideos()));
}

console.log(output.join("\n"));
