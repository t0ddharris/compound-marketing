#!/usr/bin/env python3
"""
Generate a YouTube thumbnail with ChatGPT image generation via the Codex CLI
(primary, no API key) or Gemini 3 Pro Image / Nano Banana Pro (backup).

Usage:
    python3 generate_thumbnail.py \
        --headshot path/to/headshot.png \
        --prompt "detailed prompt text" \
        --output path/to/output.png

    With reference image (for iteration):
    python3 generate_thumbnail.py \
        --headshot path/to/headshot.png \
        --reference path/to/previous-thumbnail.png \
        --prompt "edit instruction" \
        --output path/to/output-v2.png

    With example thumbnails from high-performing videos:
    python3 generate_thumbnail.py \
        --headshot path/to/headshot.png \
        --examples path/to/example1.jpg path/to/example2.jpg \
        --prompt "detailed prompt text" \
        --output path/to/output.png

Providers (--provider, default auto):
    codex   Codex CLI logged in with ChatGPT (`codex login`). No API key.
    gemini  GOOGLE_AI_STUDIO_API_KEY or GEMINI_API_KEY must be set.
    auto    Codex if available, falling back to Gemini if Codex is missing or fails.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

# Enable AVIF support — YouTube thumbnails are often AVIF
try:
    import pillow_avif  # noqa: F401
except ImportError:
    pass


def parse_args():
    parser = argparse.ArgumentParser(description="Generate YouTube thumbnail via Codex or Gemini")
    parser.add_argument(
        "--headshot", required=True, nargs="+",
        help="Path(s) to headshot reference image(s)"
    )
    parser.add_argument(
        "--reference", nargs="*", default=[],
        help="Path(s) to additional reference images (e.g., previous thumbnail for iteration)"
    )
    parser.add_argument(
        "--examples", nargs="*", default=[],
        help="Path(s) to example thumbnails from high-performing videos (style inspiration)"
    )
    parser.add_argument(
        "--prompt", required=True,
        help="Detailed prompt for thumbnail generation"
    )
    parser.add_argument(
        "--output", required=True,
        help="Output file path for the generated thumbnail"
    )
    parser.add_argument(
        "--provider", choices=["auto", "codex", "gemini"], default="auto",
        help="Image provider: codex (ChatGPT via Codex CLI), gemini (Nano Banana Pro), or auto"
    )
    parser.add_argument(
        "--no-style", action="store_true",
        help="Skip appending the brand style guide to the prompt"
    )
    return parser.parse_args()


def validate_image_file(path):
    """Check that a file is actually an image, not HTML or other junk from a failed download."""
    p = Path(path)
    if not p.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    # Read first bytes to check for HTML (common when sites block hotlinking)
    with open(p, "rb") as f:
        header = f.read(256)
    if b"<!DOCTYPE" in header or b"<html" in header or b"<HTML" in header:
        print(
            f"Error: '{path}' is an HTML file, not an image. "
            f"The download URL likely returned a web page instead of the actual image. "
            f"Try downloading from a different source.",
            file=sys.stderr,
        )
        sys.exit(1)
    if len(header) < 8:
        print(f"Error: '{path}' is too small to be a valid image ({len(header)} bytes).", file=sys.stderr)
        sys.exit(1)


def resize_if_needed(img, max_edge=2048):
    """Resize image if larger than max_edge on any side."""
    w, h = img.size
    if max(w, h) > max_edge:
        ratio = max_edge / max(w, h)
        new_size = (int(w * ratio), int(h * ratio))
        return img.resize(new_size, Image.LANCZOS)
    return img


def load_dotenv():
    """Load .env file from project root if it exists."""
    env_path = Path(__file__).resolve().parents[3] / ".env"
    if not env_path.exists():
        # Try current working directory
        env_path = Path.cwd() / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())


def codex_available():
    if not shutil.which("codex"):
        return False
    out = subprocess.run(["codex", "login", "status"], capture_output=True, text=True)
    return "ChatGPT" in (out.stdout + out.stderr)


def generate_codex(prompt, image_paths, output_path):
    """Generate via Codex's built-in $imagegen. Images are attached in order (Image 1, 2, ...)."""
    with tempfile.TemporaryDirectory() as tmp:
        cmd = ["codex", "exec", "--skip-git-repo-check", "--sandbox", "workspace-write", "-C", tmp]
        for path in image_paths:
            cmd += ["-i", str(Path(path).resolve())]
        cmd.append("-")
        full = (
            "$imagegen " + prompt + "\n\n"
            "The attached images are, in order, the images the prompt refers to as Image 1, Image 2, etc. "
            "Aspect ratio: 16:9 (YouTube thumbnail). Save the final image as ./thumbnail.png in the current "
            "directory. Do not modify any other files. Reply only with the saved file path."
        )
        result = subprocess.run(cmd, input=full, capture_output=True, text=True, timeout=600)
        produced = Path(tmp) / "thumbnail.png"
        if not produced.exists():
            tail = (result.stdout + result.stderr)[-1500:]
            if "requires a newer version of Codex" in tail:
                tail += "\nRun `codex update` and try again."
            print(f"Codex did not produce an image.\n{tail}", file=sys.stderr)
            return False
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(produced, output_path)
    print(f"Thumbnail saved to: {output_path} (via Codex)")
    return True


def main():
    args = parse_args()

    load_dotenv()


    # Build contents: prompt text + headshot images + reference images + examples
    #
    # Image order in contents:
    #   1. Headshot(s)
    #   2. Reference images (logos, icons, previous thumbnails)
    #   3. Example thumbnails (high-performing videos for style inspiration)
    #
    # The prompt should reference these by position (Image 1, Image 2, etc.)
    # Examples are appended last and prefixed with a system note so Gemini
    # knows they're style references, not elements to reproduce exactly.

    prompt = args.prompt

    # Append brand style guide unless --no-style is set
    if not args.no_style:
        style_path = Path(__file__).resolve().parent.parent / "brand-style.md"
        if style_path.exists():
            style_text = style_path.read_text().strip()
            prompt += (
                "\n\nBRAND STYLE GUIDE (follow these rules):\n"
                f"{style_text}"
            )

    if args.examples:
        prompt += (
            "\n\nSTYLE EXAMPLES:\n"
            "The final attached images are thumbnails from high-performing YouTube videos "
            "on this topic. Study their composition, color usage, text placement, and visual "
            "hierarchy — then apply those patterns to create an ORIGINAL thumbnail. "
            "Do NOT copy these thumbnails. Use them as inspiration for what works."
        )

    image_paths = list(args.headshot) + list(args.reference) + list(args.examples)
    for path in image_paths:
        validate_image_file(path)
    output_path = Path(args.output)

    provider = args.provider
    if provider == "auto":
        provider = "codex" if codex_available() else "gemini"
    if provider == "codex":
        if generate_codex(prompt, image_paths, output_path):
            return
        if args.provider == "codex":
            sys.exit(1)
        print("Falling back to Gemini (Nano Banana Pro)...", file=sys.stderr)

    api_key = os.environ.get("GOOGLE_AI_STUDIO_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: no image provider available. Log in to the Codex CLI (`codex login`) "
              "or set GOOGLE_AI_STUDIO_API_KEY.", file=sys.stderr)
        sys.exit(1)

    from google import genai
    from google.genai import types
    client = genai.Client(api_key=api_key)

    contents = [prompt]

    for headshot_path in args.headshot:
        img = resize_if_needed(Image.open(headshot_path))
        contents.append(img)

    for ref_path in args.reference:
        img = resize_if_needed(Image.open(ref_path))
        contents.append(img)

    for ex_path in args.examples:
        img = resize_if_needed(Image.open(ex_path))
        contents.append(img)

    # Generate
    response = client.models.generate_content(
        model="gemini-3-pro-image",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="16:9",
            ),
        ),
    )

    # Process response
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image_saved = False
    text_response = ""

    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data is not None:
            img = part.as_image()
            img.save(str(output_path))
            image_saved = True
            print(f"Thumbnail saved to: {output_path}")
        elif hasattr(part, "text") and part.text is not None:
            text_response += part.text

    if text_response:
        print(f"\nModel notes: {text_response}")

    if not image_saved:
        print("Error: No image was generated in the response.", file=sys.stderr)
        if text_response:
            print(f"Response text: {text_response}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
