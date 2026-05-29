/**
 * HubSpot Landing Page Analytics — CLI script
 * Usage: npx tsx .claude/skills/analytics/scripts/hubspot-pages.ts [period] [limit]
 *   period: 7d | 30d | 90d (default: 30d)
 *   limit:  number of pages to show (default: 10)
 */
import {
  loadEnv,
  requireEnv,
  parseArgs,
  hubspotGet,
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

interface AnalyticsBreakdown {
  [url: string]: {
    "raw-views"?: number;
    visits?: number;
    visitors?: number;
    "new-contacts-count"?: number;
    submissions?: number;
    "bounce-rate"?: number;
    "time-on-page"?: number;
  };
}

interface SourceBreakdown {
  [source: string]: {
    visits?: number;
    "new-contacts-count"?: number;
    submissions?: number;
  };
}

const sections: string[] = [];
sections.push(`# Landing Page Analytics (${args.period})`);
sections.push(`Period: ${start} to ${end}\n`);

// Page breakdown
try {
  const breakdown = await hubspotGet<AnalyticsBreakdown>(
    "/analytics/v2/reports/landing-pages/total",
    token,
    { start, end }
  );

  // Filter out API metadata keys (offset, total, totals, breakdowns)
  const metaKeys = new Set(["offset", "total", "totals", "breakdowns"]);
  let entries = Object.entries(breakdown)
    .filter(([url]) => !metaKeys.has(url))
    .sort((a, b) => (b[1]["raw-views"] ?? 0) - (a[1]["raw-views"] ?? 0))
    .slice(0, limit);

  if (entries.length > 0) {
    const totals = entries.reduce(
      (acc, [, data]) => ({
        views: acc.views + (data["raw-views"] ?? 0),
        submissions: acc.submissions + (data.submissions ?? 0),
        contacts: acc.contacts + (data["new-contacts-count"] ?? 0),
      }),
      { views: 0, submissions: 0, contacts: 0 }
    );

    sections.push("## Summary\n");
    sections.push(
      markdownTable(
        ["Metric", "Value"],
        [
          ["Total Page Views", num(totals.views)],
          ["Total Form Submissions", num(totals.submissions)],
          ["New Contacts", num(totals.contacts)],
          [
            "Overall Conversion Rate",
            totals.views > 0
              ? pct(totals.submissions / totals.views)
              : "N/A",
          ],
        ]
      )
    );

    sections.push("\n## Page Breakdown\n");
    sections.push(
      markdownTable(
        ["Page URL", "Views", "Submissions", "Conv. Rate", "Bounce Rate"],
        entries.map(([url, data]) => {
          const views = data["raw-views"] ?? 0;
          const submissions = data.submissions ?? 0;
          return [
            truncate(url, 50),
            num(views),
            num(submissions),
            views > 0 ? pct(submissions / views) : "N/A",
            data["bounce-rate"] != null ? pct(data["bounce-rate"]) : "N/A",
          ];
        })
      )
    );
  } else {
    sections.push("*No landing page data found for this period.*");
  }
} catch (err) {
  sections.push(
    `> **Error fetching landing page data:** ${err instanceof Error ? err.message : String(err)}`
  );
}

// Traffic source breakdown
try {
  const sources = await hubspotGet<SourceBreakdown>(
    "/analytics/v2/reports/sources/total",
    token,
    { start, end }
  );

  const srcMetaKeys = new Set(["offset", "total", "totals", "breakdowns"]);
  const sourceEntries = Object.entries(sources)
    .filter(([key]) => !srcMetaKeys.has(key))
    .sort((a, b) => (b[1].visits ?? 0) - (a[1].visits ?? 0))
    .slice(0, 10);

  if (sourceEntries.length > 0) {
    sections.push("\n## Traffic Sources\n");
    sections.push(
      markdownTable(
        ["Source", "Visits", "Contacts", "Submissions"],
        sourceEntries.map(([source, data]) => [
          source,
          num(data.visits ?? 0),
          num(data["new-contacts-count"] ?? 0),
          num(data.submissions ?? 0),
        ])
      )
    );
  }
} catch (err) {
  sections.push(
    `> **Error fetching traffic sources:** ${err instanceof Error ? err.message : String(err)}`
  );
}

console.log(sections.join("\n"));
