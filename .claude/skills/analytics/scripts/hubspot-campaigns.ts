/**
 * HubSpot Campaign Performance — CLI script
 * Usage: npx tsx .claude/skills/analytics/scripts/hubspot-campaigns.ts [period] [limit]
 *   period: 7d | 30d | 90d | all (default: 30d)
 *   limit:  number of campaigns to show (default: 5)
 */
import {
  loadEnv,
  requireEnv,
  parseArgs,
  hubspotGet,
  markdownTable,
  num,
  periodToDates,
  truncate,
} from "./lib.js";

loadEnv();
const token = requireEnv("HUBSPOT_PRIVATE_APP_TOKEN");
const args = parseArgs({ period: "30d", limit: "5" });
const { start, end } = periodToDates(args.period);
const limit = parseInt(args.limit) || 5;

interface Campaign {
  id: string;
  properties: Record<string, string>;
  createdAt: string;
  updatedAt: string;
}

interface CampaignAsset {
  id: string;
  name: string;
  metrics?: Record<string, number>;
}

const ASSET_TYPES = [
  "MARKETING_EMAIL",
  "LANDING_PAGE",
  "FORM",
  "BLOG_POST",
] as const;

const sections: string[] = [];
sections.push(`# Campaign Performance Report (${args.period})`);
sections.push(`Period: ${start} to ${end}\n`);

try {
  const campaigns = await hubspotGet<{
    total: number;
    results: Campaign[];
  }>("/marketing/v3/campaigns", token, {
    limit: String(limit),
    properties: "hs_name,hs_campaign_status,hs_start_date,hs_end_date",
    sort: "-updatedAt",
  });

  if (!campaigns.results || campaigns.results.length === 0) {
    sections.push("*No campaigns found.*");
    console.log(sections.join("\n"));
    process.exit(0);
  }

  sections.push(`Found ${campaigns.total} campaigns total.\n`);

  // Overview table
  sections.push("## Campaign Overview\n");
  sections.push(
    markdownTable(
      ["Campaign", "Status", "Start", "End"],
      campaigns.results.map((c) => [
        c.properties.hs_name ?? "Unnamed",
        c.properties.hs_campaign_status ?? "-",
        c.properties.hs_start_date ?? "-",
        c.properties.hs_end_date ?? "-",
      ])
    )
  );

  // Per-campaign asset metrics
  for (const campaign of campaigns.results) {
    const campaignName = campaign.properties.hs_name ?? "Unnamed";
    sections.push(`\n### ${campaignName}\n`);

    for (const assetType of ASSET_TYPES) {
      try {
        const assetsResponse = await hubspotGet<{
          results?: CampaignAsset[];
        }>(
          `/marketing/v3/campaigns/${campaign.id}/assets/${assetType}`,
          token,
          { limit: "20", startDate: start, endDate: end }
        );

        const assets = assetsResponse.results;
        if (!assets || assets.length === 0) continue;

        const metricsKeys = new Set<string>();
        for (const asset of assets) {
          if (asset.metrics) {
            for (const key of Object.keys(asset.metrics)) {
              metricsKeys.add(key);
            }
          }
        }

        if (metricsKeys.size > 0) {
          const typeLabel = assetType
            .replace(/_/g, " ")
            .toLowerCase()
            .replace(/\b\w/g, (c) => c.toUpperCase());

          const metricHeaders = Array.from(metricsKeys).map((k) =>
            k
              .replace(/_/g, " ")
              .replace(/\b\w/g, (c) => c.toUpperCase())
          );

          sections.push(`**${typeLabel}s:**\n`);
          sections.push(
            markdownTable(
              ["Asset", ...metricHeaders],
              assets.map((a) => [
                truncate(a.name, 35),
                ...Array.from(metricsKeys).map((k) =>
                  num(a.metrics?.[k] ?? 0)
                ),
              ])
            )
          );
          sections.push("");
        }
      } catch {
        // Asset type not available — skip
      }
    }
  }
} catch (err) {
  sections.push(
    `> **Error fetching campaigns:** ${err instanceof Error ? err.message : String(err)}`
  );
}

sections.push(
  "\n*Note: Revenue attribution requires Marketing Hub Enterprise. Contact/deal counts shown instead.*"
);

console.log(sections.join("\n"));
