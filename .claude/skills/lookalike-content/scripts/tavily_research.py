#!/usr/bin/env python3
"""
Tavily API research script for Lookalike Content skill.

Sends a research query to Tavily's search API and returns structured results
with titles, URLs, and content snippets. Used for trending topic research
and content idea generation.

Usage:
  python tavily_research.py --query "What are the most discussed topics in B2B observability right now?"
  python tavily_research.py --query "trending AI agent frameworks" --output results.json
  python tavily_research.py --query "observability platform engineering" --depth advanced

Output: JSON with the query, results (title, url, content, score), and answer summary.

Requires: TAVILY_API_KEY environment variable (or in .env file)
Install: pip install tavily-python python-dotenv
"""

import argparse
import json
import os
import sys

try:
    from tavily import TavilyClient
except ImportError:
    print("Error: tavily-python not installed. Run: pip install tavily-python")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    # Walk up from script location to find .env at project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..", "..", "..", ".."))
    load_dotenv(os.path.join(project_root, ".env"))
except ImportError:
    pass


def get_api_key():
    """Get Tavily API key from environment."""
    key = os.environ.get("TAVILY_API_KEY")
    if not key:
        print("Error: TAVILY_API_KEY not set. Set it as an environment variable or in a .env file.")
        sys.exit(1)
    return key


def research(query, depth="advanced", max_results=10):
    """Send a research query to Tavily. Returns structured search results."""
    client = TavilyClient(api_key=get_api_key())

    try:
        response = client.search(
            query=query,
            search_depth=depth,
            max_results=max_results,
            include_answer=True,
        )

        result = {
            "query": query,
            "depth": depth,
            "answer": response.get("answer", ""),
            "results": [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                    "score": r.get("score", 0),
                }
                for r in response.get("results", [])
            ],
        }

        return result

    except Exception as e:
        print(f"Error: Tavily API request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Research a topic using Tavily API")
    parser.add_argument("--query", required=True, help="Research query to send to Tavily")
    parser.add_argument("--depth", default="advanced", choices=["basic", "advanced"],
                        help="Search depth: basic (1 credit) or advanced (2 credits, default)")
    parser.add_argument("--max-results", type=int, default=10, help="Max results to return (default: 10)")
    parser.add_argument("--output", help="Output file path (default: stdout)", default=None)

    args = parser.parse_args()

    print(f"Researching: {args.query[:80]}...", file=sys.stderr)
    result = research(args.query, args.depth, args.max_results)
    print(f"Done. {len(result['results'])} results found.", file=sys.stderr)

    output = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Results saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
