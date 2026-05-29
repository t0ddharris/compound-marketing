/**
 * LinkedIn Page & Post Analytics — CLI script
 * Usage: npx tsx .claude/skills/analytics/scripts/linkedin.ts [command] [period] [limit]
 *   command: posts | followers | overview (default: overview)
 *   period:  7d | 30d | 90d (default: 30d)
 *   limit:   number of posts to show (default: 10)
 *
 * Requires: LINKEDIN_ACCESS_TOKEN, LINKEDIN_ORG_ID in .env
 */
import {
  loadEnv,
  requireEnv,
  parseArgs,
  linkedinGet,
  markdownTable,
  num,
  shortNum,
  pct,
  periodToDates,
  truncate,
  relativeDate,
} from "./lib.js";

loadEnv();
const token = requireEnv("LINKEDIN_ACCESS_TOKEN");
const orgId = requireEnv("LINKEDIN_ORG_ID");
const args = parseArgs({ command: "overview", period: "30d", limit: "10" });
const { start, end } = periodToDates(args.period);
const limit = parseInt(args.limit) || 10;

const orgUrn = `urn:li:organization:${orgId}`;

// ── Follower Count ──────────────────────────────────────────

async function getFollowerCount(): Promise<number> {
  try {
    const data = await linkedinGet<{ firstDegreeSize: number }>(
      `/networkSizes/${encodeURIComponent(orgUrn)}`,
      token,
      { edgeType: "CompanyFollowedByMember" }
    );
    return data.firstDegreeSize ?? 0;
  } catch {
    return -1;
  }
}

// ── Follower Stats (gains over time) ────────────────────────

async function getFollowerStats(): Promise<string[]> {
  const sections: string[] = [];
  try {
    const startMs = new Date(start).getTime();
    const endMs = new Date(end).getTime();

    const data = await linkedinGet<{
      elements?: Array<{
        timeRange: { start: number; end: number };
        followerGains: { organicFollowerGain: number; paidFollowerGain: number };
      }>;
    }>(
      "/organizationalEntityFollowerStatistics",
      token,
      {
        q: "organizationalEntity",
        organizationalEntity: orgUrn,
        "timeIntervals.timeGranularityType": "DAY",
        "timeIntervals.timeRange.start": String(startMs),
        "timeIntervals.timeRange.end": String(endMs),
      }
    );

    if (data.elements && data.elements.length > 0) {
      let totalOrganic = 0;
      let totalPaid = 0;
      for (const el of data.elements) {
        totalOrganic += el.followerGains?.organicFollowerGain ?? 0;
        totalPaid += el.followerGains?.paidFollowerGain ?? 0;
      }

      sections.push(
        markdownTable(
          ["Metric", "Value"],
          [
            ["Organic Followers Gained", num(totalOrganic)],
            ["Paid Followers Gained", num(totalPaid)],
            ["Total New Followers", num(totalOrganic + totalPaid)],
          ]
        )
      );
    }
  } catch (err) {
    sections.push(
      `> Error fetching follower stats: ${err instanceof Error ? err.message : String(err)}`
    );
  }
  return sections;
}

// ── Post Analytics ──────────────────────────────────────────

interface PostElement {
  id: string;
  commentary?: string;
  content?: { article?: { title?: string } };
  publishedAt?: number;
  lifecycleState?: string;
}

interface ShareStat {
  organizationalEntity?: string;
  share?: string;
  totalShareStatistics: {
    shareCount: number;
    clickCount: number;
    likeCount: number;
    commentCount: number;
    impressionCount: number;
    engagement: number;
    uniqueImpressionsCount?: number;
  };
}

async function getPostAnalytics(): Promise<string[]> {
  const sections: string[] = [];

  try {
    // Get recent posts
    const postsData = await linkedinGet<{ elements?: PostElement[] }>(
      "/posts",
      token,
      {
        q: "author",
        author: orgUrn,
        count: String(Math.min(limit * 2, 50)),
        sortBy: "LAST_MODIFIED",
      }
    );

    const posts = postsData.elements ?? [];
    if (posts.length === 0) {
      sections.push("*No posts found.*");
      return sections;
    }

    // Filter to period
    const startMs = new Date(start).getTime();
    const periodPosts = posts
      .filter((p) => (p.publishedAt ?? 0) >= startMs)
      .slice(0, limit);

    if (periodPosts.length === 0) {
      sections.push(`*No posts found in the ${args.period} period.*`);
      return sections;
    }

    // Get share statistics for the org
    const statsData = await linkedinGet<{ elements?: ShareStat[] }>(
      "/organizationalEntityShareStatistics",
      token,
      {
        q: "organizationalEntity",
        organizationalEntity: orgUrn,
      }
    );

    // Aggregate org-level stats
    const orgStats = statsData.elements?.find(
      (e) => e.organizationalEntity === orgUrn && !e.share
    );

    if (orgStats) {
      const s = orgStats.totalShareStatistics;
      sections.push("### Aggregate Page Stats\n");
      sections.push(
        markdownTable(
          ["Metric", "Value"],
          [
            ["Total Impressions", shortNum(s.impressionCount)],
            ["Total Clicks", shortNum(s.clickCount)],
            ["Total Likes", shortNum(s.likeCount)],
            ["Total Comments", shortNum(s.commentCount)],
            ["Total Shares", shortNum(s.shareCount)],
            ["Engagement Rate", pct(s.engagement)],
          ]
        )
      );
      sections.push("");
    }

    // Post-level table
    sections.push(`### Recent Posts (${periodPosts.length})\n`);

    const rows: string[][] = [];
    for (const post of periodPosts) {
      const text =
        post.commentary?.slice(0, 60) ??
        post.content?.article?.title ??
        "(no text)";
      const published = post.publishedAt
        ? relativeDate(new Date(post.publishedAt).toISOString())
        : "-";

      // Try to get per-share stats
      const shareStat = statsData.elements?.find(
        (e) => e.share === post.id
      );
      const s = shareStat?.totalShareStatistics;

      rows.push([
        truncate(text, 50),
        published,
        s ? shortNum(s.impressionCount) : "-",
        s ? shortNum(s.clickCount) : "-",
        s ? shortNum(s.likeCount) : "-",
        s ? num(s.commentCount) : "-",
        s ? pct(s.engagement) : "-",
      ]);
    }

    sections.push(
      markdownTable(
        ["Post", "Date", "Impr.", "Clicks", "Likes", "Comments", "Eng."],
        rows
      )
    );
  } catch (err) {
    sections.push(
      `> Error fetching posts: ${err instanceof Error ? err.message : String(err)}`
    );
  }
  return sections;
}

// ── Main ────────────────────────────────────────────────────

const output: string[] = [];
output.push(`# LinkedIn Analytics (${args.period})`);
output.push(`Period: ${start} to ${end}\n`);

const followers = await getFollowerCount();
if (followers >= 0) {
  output.push(`**Current Followers:** ${num(followers)}\n`);
}

if (args.command === "followers" || args.command === "overview") {
  output.push("## Follower Growth\n");
  output.push(...(await getFollowerStats()));
  output.push("");
}

if (args.command === "posts" || args.command === "overview") {
  output.push("## Post Performance\n");
  output.push(...(await getPostAnalytics()));
}

console.log(output.join("\n"));
