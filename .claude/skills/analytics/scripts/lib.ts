import { readFileSync } from "fs";
import { resolve, dirname } from "path";
import { fileURLToPath } from "url";

// ---------------------------------------------------------------------------
// Environment
// ---------------------------------------------------------------------------

/** Load .env from repo root (walks up from script location). */
export function loadEnv(): void {
  let dir = dirname(fileURLToPath(import.meta.url));
  for (let i = 0; i < 10; i++) {
    try {
      const content = readFileSync(resolve(dir, ".env"), "utf-8");
      for (const line of content.split("\n")) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith("#")) continue;
        const eqIdx = trimmed.indexOf("=");
        if (eqIdx === -1) continue;
        const key = trimmed.slice(0, eqIdx).trim();
        const val = trimmed
          .slice(eqIdx + 1)
          .trim()
          .replace(/^["']|["']$/g, "");
        if (key && !process.env[key]) process.env[key] = val;
      }
      return;
    } catch {
      /* no .env here */
    }
    const parent = resolve(dir, "..");
    if (parent === dir) break;
    dir = parent;
  }
}

export function requireEnv(key: string): string {
  const val = process.env[key];
  if (!val) {
    console.error(`Error: ${key} is required. Set it in .env or export it.`);
    process.exit(1);
  }
  return val;
}

// ---------------------------------------------------------------------------
// Arg parsing
// ---------------------------------------------------------------------------

/**
 * Minimal arg parser. Keys of `defaults` define positional order.
 * Supports `--key value` flags and bare positional args.
 */
export function parseArgs(
  defaults: Record<string, string>
): Record<string, string> {
  const args = process.argv.slice(2);
  const result = { ...defaults };
  const keys = Object.keys(defaults);
  let posIdx = 0;

  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      result[key] = args[++i] ?? "";
    } else if (posIdx < keys.length) {
      result[keys[posIdx++]] = args[i];
    }
  }
  return result;
}

// ---------------------------------------------------------------------------
// HTTP helpers
// ---------------------------------------------------------------------------

export async function httpGet<T>(
  url: string,
  headers: Record<string, string>,
  params?: Record<string, string>
): Promise<T> {
  const u = new URL(url);
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== "") u.searchParams.set(k, v);
    }
  }
  const res = await fetch(u.toString(), { headers });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`HTTP ${res.status} on ${u.pathname}: ${body.slice(0, 500)}`);
  }
  return res.json() as Promise<T>;
}

// -- HubSpot ----------------------------------------------------------------

export async function hubspotGet<T>(
  path: string,
  token: string,
  params?: Record<string, string>
): Promise<T> {
  return httpGet<T>(
    `https://api.hubapi.com${path}`,
    { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    params
  );
}

export async function hubspotGetAllPages<T>(
  path: string,
  token: string,
  params?: Record<string, string>,
  maxPages = 5
): Promise<T[]> {
  const results: T[] = [];
  let after: string | undefined;

  for (let page = 0; page < maxPages; page++) {
    const qp: Record<string, string> = { ...params };
    if (after) qp.after = after;

    const response = await hubspotGet<{
      results: T[];
      paging?: { next?: { after: string } };
    }>(path, token, qp);

    results.push(...response.results);
    after = response.paging?.next?.after;
    if (!after) break;
  }
  return results;
}

// -- X / Twitter ------------------------------------------------------------

export async function xGet<T>(
  path: string,
  token: string,
  params?: Record<string, string>
): Promise<T> {
  return httpGet<T>(
    `https://api.x.com/2${path}`,
    { Authorization: `Bearer ${token}` },
    params
  );
}

// -- LinkedIn ---------------------------------------------------------------

export async function linkedinGet<T>(
  path: string,
  token: string,
  params?: Record<string, string>,
  apiVersion = "202401"
): Promise<T> {
  return httpGet<T>(
    `https://api.linkedin.com/rest${path}`,
    {
      Authorization: `Bearer ${token}`,
      "LinkedIn-Version": apiVersion,
      "X-Restli-Protocol-Version": "2.0.0",
    },
    params
  );
}

// -- YouTube ----------------------------------------------------------------

export async function youtubeGet<T>(
  path: string,
  token: string,
  params?: Record<string, string>
): Promise<T> {
  return httpGet<T>(
    `https://www.googleapis.com${path}`,
    { Authorization: `Bearer ${token}` },
    params
  );
}

// ---------------------------------------------------------------------------
// Formatters
// ---------------------------------------------------------------------------

export function markdownTable(headers: string[], rows: string[][]): string {
  if (rows.length === 0) return "*No data.*";
  const widths = headers.map((h, i) =>
    Math.max(h.length, ...rows.map((r) => (r[i] ?? "").length))
  );
  const headerRow = headers.map((h, i) => h.padEnd(widths[i])).join(" | ");
  const separator = widths.map((w) => "-".repeat(w)).join(" | ");
  const dataRows = rows
    .map(
      (row) =>
        `| ${row.map((cell, i) => (cell ?? "").padEnd(widths[i])).join(" | ")} |`
    )
    .join("\n");

  return `| ${headerRow} |\n| ${separator} |\n${dataRows}`;
}

export function pct(ratio: number): string {
  return `${(ratio * 100).toFixed(1)}%`;
}

export function num(n: number): string {
  return n.toLocaleString("en-US");
}

export function shortNum(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}

export function periodToDates(period: string): { start: string; end: string } {
  const now = new Date();
  const end = now.toISOString().split("T")[0]!;
  const daysMap: Record<string, number> = {
    "7d": 7,
    "30d": 30,
    "90d": 90,
    all: 365 * 3,
  };
  const days = daysMap[period] ?? 30;
  const startDate = new Date(now.getTime() - days * 86400000);
  return { start: startDate.toISOString().split("T")[0]!, end };
}

export function truncate(s: string, max: number): string {
  return s.length > max ? s.slice(0, max - 3) + "..." : s;
}

export function relativeDate(iso: string): string {
  const d = new Date(iso);
  const now = new Date();
  const diffDays = Math.floor(
    (now.getTime() - d.getTime()) / 86400000
  );
  if (diffDays === 0) return "today";
  if (diffDays === 1) return "yesterday";
  if (diffDays < 7) return `${diffDays}d ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
  return d.toISOString().split("T")[0]!;
}
