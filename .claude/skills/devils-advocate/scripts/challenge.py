#!/usr/bin/env python3
"""
Devil's advocate critique via Google Gemini (outside-Anthropic second opinion).

Sends a target (files, pasted text, or a statement) to Gemini with a
devil's-advocate system prompt and returns a structured critique.

Usage:
    # Critique one or more files
    python3 challenge.py --files marketing/plans/pipeline-growth-strategy.md

    # Critique a statement / assumption / decision
    python3 challenge.py --statement "We should lead every homepage test with the tagline 'Full System Visibility' because it outperformed in Q1."

    # Pipe content in
    cat draft.md | python3 challenge.py --stdin --target-type content

    # Add supporting context the critic should read before judging
    python3 challenge.py --files landing/hero.html \\
        --context-files brain/positioning-and-messaging.md brain/truth.md

    # Override model / write to file
    python3 challenge.py --files plan.md --model gemini-3.1-pro-preview \\
        --out marketing/reviews/plan-devils-advocate.md

Requires GOOGLE_AI_STUDIO_API_KEY in env or in the repo's .env file.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_MODEL = "gemini-3.1-pro-preview"

SYSTEM_PROMPT = """\
You are a senior outside advisor acting as a devil's advocate. You are NOT \
part of the team that produced the work below. Your job is to challenge it \
rigorously so the team can pressure-test their thinking before shipping.

You are pointedly adversarial but intellectually honest. You are not \
performatively negative. Weak critiques waste everyone's time.

Follow these rules:

1. STEELMAN FIRST. Before attacking, articulate the strongest version of the \
   opposing view to the work as presented. A sentence or two, not a full \
   essay. This proves you understood it.

2. BE SPECIFIC. Every critique must point to a specific sentence, section, \
   claim, number, code block, or decision. Quote or cite the location. Vague \
   feedback like "this could be clearer" is worse than silence.

3. CHALLENGE REASONING, NOT STYLE. You are probing logic, evidence, \
   assumptions, and risk. Do not rewrite prose for taste. Only flag writing \
   issues when they actively obscure meaning or mislead the reader.

4. PROPOSE, DON'T JUST DESTROY. For every significant weakness, name at \
   least one concrete alternative, counter-framing, or test that would \
   resolve the weakness.

5. SURFACE WHAT'S MISSING. Often the biggest problem is what the work does \
   NOT say: unstated assumptions, missing counter-evidence, skipped \
   stakeholders, unhandled edge cases, survivorship bias, absent failure \
   modes.

6. CALIBRATE YOUR CONFIDENCE. If you don't know enough to judge a claim, \
   say so and name what information would settle it. Do not bluff.

7. RESPECT THE BRIEF. If the context tells you the work is targeting a \
   specific audience, channel, or goal, judge it against that goal. Don't \
   critique a LinkedIn post for not being a whitepaper.

8. NO AI TELLS. Do not write in bullet-heavy consultantese. No "it's not X, \
   it's Y" rhetoric. No "here's the thing." No em-dash abuse. Use short, \
   direct sentences. Weave numbers into prose, don't drop them as \
   stand-alone fragments.

Always return your answer in this exact Markdown structure:

# Devil's advocate review

## Steelman
One paragraph: the strongest honest case FOR the work as written.

## What the work is actually claiming
A short, literal restatement of the main argument, decision, or claim in \
your own words. This is how you make sure you're attacking the real thing \
and not a strawman.

## Specific weaknesses
A numbered list. For each item:
- **Location:** quote or cite the exact place in the work
- **Problem:** what is wrong, missing, or unsupported
- **Why it matters:** the consequence if shipped as-is
- **Fix or test:** the cheapest way to resolve it

Aim for 3-7 weaknesses. More than 7 usually means you are padding; fewer \
than 3 usually means you are being polite.

## Counter-evidence and missing evidence
What evidence would weaken the argument? What evidence SHOULD the work cite \
but doesn't? Name sources, comparisons, or data the team could realistically \
get.

## Alternative framings
One or two genuinely different angles on the same problem, not minor \
rewordings. For each, one sentence on why it might be stronger and one \
sentence on what it would cost.

## Risks and failure modes
If this ships as-is, what are the realistic ways it backfires? Rank by \
likelihood and severity.

## Bottom line
One of: SHIP, SHIP WITH FIXES, REWORK, KILL. Then one sentence of reasoning. \
Be willing to say SHIP when the work is actually good. An adversary who \
always says REWORK is useless.
"""


def load_api_key() -> str:
    """Load Gemini key from env or repo .env file."""
    key = os.environ.get("GOOGLE_AI_STUDIO_API_KEY") or os.environ.get(
        "GEMINI_API_KEY"
    )
    if key:
        return key

    for candidate in (Path(".env"), Path(__file__).resolve().parents[4] / ".env"):
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                if line.startswith("GOOGLE_AI_STUDIO_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit(
        "error: no GOOGLE_AI_STUDIO_API_KEY found. Add it to .env or export it "
        "in your shell. Get a key at https://aistudio.google.com/apikey"
    )


def read_files(paths: list[str], label: str) -> str:
    """Concatenate files with clear headers so the model can cite them."""
    chunks = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            sys.exit(f"error: {label} file not found: {p}")
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            sys.exit(f"error: {label} file is not UTF-8 text: {p}")
        chunks.append(f"--- BEGIN {label.upper()} FILE: {p} ---\n{text}\n--- END {label.upper()} FILE: {p} ---")
    return "\n\n".join(chunks)


def build_user_prompt(
    target_type: str,
    target_text: str,
    context_text: str | None,
    note: str | None,
) -> str:
    parts = [f"TARGET TYPE: {target_type}"]
    if note:
        parts.append(f"\nNOTE FROM THE TEAM:\n{note}")
    if context_text:
        parts.append(
            "\nSUPPORTING CONTEXT (read this before judging the work):\n"
            + context_text
        )
    parts.append(
        "\nTHE WORK TO CRITIQUE BEGINS BELOW. Apply the rules from your "
        "instructions and return the review in the required structure.\n\n"
        + target_text
    )
    return "\n".join(parts)


def call_gemini(model: str, api_key: str, system: str, user: str) -> str:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    payload = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.95,
            "maxOutputTokens": 8192,
        },
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        sys.exit(f"error: Gemini API returned {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"error: could not reach Gemini API: {e.reason}")

    try:
        return body["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        sys.exit(
            "error: unexpected response shape from Gemini.\n"
            + json.dumps(body, indent=2)[:2000]
        )


def detect_target_type(files: list[str], explicit: str | None) -> str:
    if explicit:
        return explicit
    if not files:
        return "statement"
    code_exts = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".html", ".css", ".sh"}
    plan_hints = ("/plans/", "plan", "strategy", "roadmap")
    if any(Path(f).suffix.lower() in code_exts for f in files):
        # html inside marketing/ is usually content, not code
        html_only = all(Path(f).suffix.lower() == ".html" for f in files)
        if html_only and any("marketing/" in f for f in files):
            return "content"
        return "code"
    if any(h in f.lower() for f in files for h in plan_hints):
        return "plan"
    return "content"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--files", nargs="*", default=[], help="One or more files to critique")
    parser.add_argument("--stdin", action="store_true", help="Read the target from stdin")
    parser.add_argument("--statement", help="Inline text target (assumption, decision, plan)")
    parser.add_argument(
        "--context-files", nargs="*", default=[],
        help="Supporting context files the critic should read first (e.g. brain/positioning-and-messaging.md)",
    )
    parser.add_argument(
        "--target-type",
        choices=["content", "code", "plan", "assumption", "decision", "statement"],
        help="Hint to the critic about what kind of work this is (auto-detected if omitted)",
    )
    parser.add_argument("--note", help="Short note from the team: audience, goal, constraints")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini model id (default: {DEFAULT_MODEL})")
    parser.add_argument("--out", help="Write the critique to this path (default: stdout)")
    args = parser.parse_args()

    sources = [bool(args.files), args.stdin, bool(args.statement)]
    if sum(sources) == 0:
        sys.exit("error: provide at least one of --files, --stdin, or --statement")
    if sum(sources) > 1:
        sys.exit("error: use only one of --files, --stdin, or --statement")

    if args.files:
        target_text = read_files(args.files, "target")
    elif args.stdin:
        target_text = sys.stdin.read()
        if not target_text.strip():
            sys.exit("error: no input on stdin")
    else:
        target_text = args.statement

    context_text = (
        read_files(args.context_files, "context") if args.context_files else None
    )
    target_type = detect_target_type(args.files, args.target_type)

    api_key = load_api_key()
    user_prompt = build_user_prompt(target_type, target_text, context_text, args.note)
    critique = call_gemini(args.model, api_key, SYSTEM_PROMPT, user_prompt)

    header = (
        f"<!-- devils-advocate critique | model: {args.model} | "
        f"target-type: {target_type} -->\n\n"
    )
    output = header + critique.strip() + "\n"

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output)
        print(f"wrote critique to {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
