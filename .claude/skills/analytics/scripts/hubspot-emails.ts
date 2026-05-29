/**
 * HubSpot Email Performance — CLI script
 * Usage: npx tsx .claude/skills/analytics/scripts/hubspot-emails.ts [period] [limit]
 *   period: 7d | 30d | 90d | all (default: 30d)
 *   limit:  number of top emails to show (default: 10)
 */
import {
  loadEnv,
  requireEnv,
  parseArgs,
  hubspotGet,
  hubspotGetAllPages,
  markdownTable,
  pct,
  num,
  periodToDates,
  truncate,
} from "./lib.js";

loadEnv();
const token = requireEnv("HUBSPOT_PRIVATE_APP_TOKEN");
const args = parseArgs({ period: "30d", limit: "10" });
const { start, end } = periodToDates(args.period);
const limit = parseInt(args.limit) || 10;

interface AggregateStats {
  aggregate: {
    counters: Record<string, number>;
    ratios: Record<string, number>;
  };
  emails: number[];
}

interface MarketingEmail {
  id: string;
  name: string;
  subject: string;
  publishDate: string;
  stats?: {
    counters: Record<string, number>;
    ratios: Record<string, number>;
  };
}

const sections: string[] = [];
sections.push(`# Email Performance Report (${args.period})`);
sections.push(`Period: ${start} to ${end}\n`);

// Aggregate statistics
try {
  const stats = await hubspotGet<AggregateStats>(
    "/marketing/v3/emails/statistics/list",
    token,
    {
      startTimestamp: new Date(start).toISOString(),
      endTimestamp: new Date(end).toISOString(),
    }
  );

  if (stats.aggregate) {
    const c = stats.aggregate.counters;
    const r = stats.aggregate.ratios;

    sections.push("## Aggregate Metrics\n");
    sections.push(
      markdownTable(
        ["Metric", "Value"],
        [
          ["Sent", num(c.sent ?? 0)],
          ["Delivered", num(c.delivered ?? 0)],
          [
            "Delivery Rate",
            c.sent ? pct((c.delivered ?? 0) / c.sent) : "N/A",
          ],
          ["Opened", num(c.open ?? 0)],
          ["Open Rate", r.openratio != null ? pct(r.openratio) : "N/A"],
          ["Clicked", num(c.click ?? 0)],
          ["Click Rate", r.clickratio != null ? pct(r.clickratio) : "N/A"],
          [
            "CTOR",
            c.open && c.click ? pct(c.click / c.open) : "N/A",
          ],
          ["Bounced", num(c.bounce ?? 0)],
          [
            "Bounce Rate",
            c.sent ? pct((c.bounce ?? 0) / c.sent) : "N/A",
          ],
          ["Unsubscribed", num(c.unsubscribed ?? 0)],
        ]
      )
    );

    sections.push(
      `\n*${num(stats.emails?.length ?? 0)} emails sent in this period.*`
    );
  }
} catch (err) {
  sections.push(
    `> **Error fetching aggregate stats:** ${err instanceof Error ? err.message : String(err)}`
  );
}

// Top performing individual emails
try {
  const emails = await hubspotGetAllPages<MarketingEmail>(
    "/marketing/v3/emails",
    token,
    {
      limit: "50",
      orderBy: "-publishDate",
      statistics: "ab_test_combined",
    }
  );

  const sentEmails = emails
    .filter((e) => e.stats?.counters?.sent && e.stats.counters.sent > 0)
    .sort(
      (a, b) =>
        (b.stats?.ratios?.openratio ?? 0) - (a.stats?.ratios?.openratio ?? 0)
    )
    .slice(0, limit);

  if (sentEmails.length > 0) {
    sections.push("\n## Top Performing Emails (by Open Rate)\n");
    sections.push(
      markdownTable(
        ["Email", "Sent", "Open Rate", "Click Rate", "CTOR"],
        sentEmails.map((e) => {
          const c = e.stats?.counters ?? {};
          const r = e.stats?.ratios ?? {};
          return [
            truncate(e.name, 40),
            num(c.sent ?? 0),
            r.openratio != null ? pct(r.openratio) : "N/A",
            r.clickratio != null ? pct(r.clickratio) : "N/A",
            c.open && c.click ? pct(c.click / c.open) : "N/A",
          ];
        })
      )
    );
  }
} catch (err) {
  sections.push(
    `> **Error fetching individual emails:** ${err instanceof Error ? err.message : String(err)}`
  );
}

console.log(sections.join("\n"));
