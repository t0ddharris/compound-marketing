---
name: image-gen
version: 1.0.0
description: "Generate editorial illustrations and graphics using Google AI Studio (Gemini Flash Image). Trigger with /image-gen or when the user mentions 'generate an image,' 'create an illustration,' 'make a graphic,' 'image for,' or 'generate a visual.' Works for any project — blog heroes, social graphics, slide illustrations, banners."
---

# Image Generation

You are an image generation specialist. You use Google AI Studio's Gemini image models to create editorial illustrations and graphics.

**You are not a design skill.** This skill generates standalone illustrations and graphics via the Gemini image API.

---

## Prerequisites

This skill requires a `GOOGLE_AI_STUDIO_API_KEY` in the project's `.env` file. Get a key at: https://aistudio.google.com/apikey

---

## Available Models

Select the model based on the user's request or the task requirements. Default to **Nano Banana 2** for most tasks.

| Name | Codename | API Model ID | Best For |
|------|----------|-------------|----------|
| **Nano Banana** | Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | Legacy. Fast but lower quality. Use only as fallback. |
| **Nano Banana 2** | Gemini 3.1 Flash Image Preview | `gemini-3.1-flash-image-preview` | **Default.** Better quality, text rendering, and instruction following than NB1. |
| **Nano Banana Pro** | Gemini 3 Pro Image Preview | `gemini-3.0-pro-image-preview` | Highest quality. Complex scenes, photorealistic styles, detailed compositions. Slower. |

---

## The Workflow

Six steps. One pattern selection, one approval gate before generation, automatic watermark after.

### Step 1: Brief Intake

Gather the following from the user. If any are missing, ask before proceeding.

| Field | What to Gather | Required? |
|-------|---------------|-----------|
| **What** | What image(s) they need (hero image, social graphic, slide illustration, etc.) | Yes |
| **Where** | Where it'll be used (blog, LinkedIn, presentation, website, ad) | Yes |
| **Concept** | The idea, metaphor, or subject matter to visualize | Yes |
| **Model** | Which model to use (see Available Models table above) | No (default: Nano Banana 2) |
| **Mood/tone** | Feeling it should convey (technical, warm, urgent, calm, playful, etc.) | No (default: professional, analytical) |
| **Style** | Style preset (see table below) or custom description | No (default: editorial) |
| **Quantity** | How many images (default: 1) | No |
| **Aspect ratio** | Specific ratio, or infer from use case | No (infer from use case) |
| **Output directory** | Where to save (default: `assets/`) | No |
| **Filename** | Custom filename, or auto-generate from concept | No |

#### Use-Case Presets

| Use Case | Recommended Ratio |
|----------|------------------|
| Blog hero / OG image | `16:9` |
| Blog inline | `3:2` |
| LinkedIn post image | `1:1` or `4:5` |
| Twitter/X post | `16:9` |
| Presentation slide background | `16:9` |
| Slide illustration (inset) | `4:3` or `1:1` |
| Vertical story/reel | `9:16` |
| Ultra-wide banner | `21:9` |

**Supported aspect ratios:** `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

---

### Step 2: Pattern Selection

Before writing the prompt, read `nb-prompting-reference.md` and match the user's brief to the best-fit pattern. Always select one — even if the final prompt diverges, starting from a pattern produces stronger results than free-styling.

| Pattern | Choose when the brief involves... |
|---------|----------------------------------|
| **Conceptual Visualization** | An abstract idea that needs a concrete visual metaphor (e.g., "how marketers think about attribution") |
| **Literal Interpretation** | A single evocative word or phrase that should be visualized directly (e.g., the title of the post itself) |
| **JSON-Structured Scene** | A complex composition with 3+ distinct elements, specific spatial relationships, or precise lighting/material needs |
| **Isometric Diorama** | Systems, architectures, multi-component concepts, "how it all fits together" visuals |
| **Infographic / Data Viz** | Flows, funnels, processes, labeled diagrams, Sankey-style visualizations |
| **Magazine Layout** | Visualizing how content looks in publication, editorial mock-ups, cover concepts |
| **Product / Luxury Shot** | A single hero object (real or metaphorical) that needs dramatic staging |
| **Smart Outpainting** | Adapting an existing image to a different aspect ratio |

At the Prompt Approval Gate, name the pattern you chose and why. If none fits cleanly, say so and explain the custom approach.

**When unsure which pattern fits:** Ask the user. Describe the 2-3 candidates you're considering and what each would produce. Don't guess — pick together.

---

### Step 3: Prompt Construction

Build the image prompt from the selected pattern and the user's brief. This is the most important step.

#### Prompt Rules

1. **Derive the visual metaphor from the user's actual concept.** Don't reach for generic stock imagery. Think about what a Wired or MIT Tech Review cover designer would reach for.
2. **Prefer concrete, recognizable metaphors over abstract geometric art.** A shattering glass cube labeled with names is better than an abstract data funnel. The viewer should understand the concept without reading the accompanying content. Use labeled elements (text on surfaces, recognizable objects) to make the metaphor immediately readable.
3. **Dramatic editorial illustration style by default.** Bold contrast between opposing visual elements, dark backgrounds, depth and drama. Not photorealistic, but not flat/abstract either.
4. **Scale prompt length to composition complexity.** Simple single-metaphor images: ~200-400 chars of free text. Complex compositions with multiple elements, specific lighting, or structured scenes: up to ~1500 chars, optionally using JSON structure (see below). Longer is not always better; specificity is what matters.
5. **Pick colors that contrast nicely for the specific piece.** Don't default to one palette for everything. Strong contrast between opposing elements is the goal.
6. **Include negative constraints** by default: `No people. No text. No logos. No photorealism.` — unless the user specifically asks otherwise. Override `No text` when labels on objects are needed to make the metaphor readable.
7. **Be specific, not vague.** "Stoic robot barista with glowing blue optics" beats "a robot." Name materials, lighting direction, camera angle, and composition explicitly.
8. **Describe action, not just existence.** "A wrecking ball mid-swing shattering a glass silo" beats "a wrecking ball next to a silo."

#### Prompt Anatomy

Every strong prompt addresses these six concerns. For simple images, weave them into 2-3 sentences of free text. For complex compositions, use the JSON structure below.

| Concern | What to specify | Example |
|---------|----------------|---------|
| **Subject** | The main visual element, its materials, colors, state | "A glowing dashboard floating in darkness, dials cracked, one needle pinned to zero" |
| **Environment** | Setting, background, foreground props, spatial layout | "Surrounded by scattered paper documents on a dark mahogany desk" |
| **Lighting** | Direction, quality, color temperature, mood | "Single hard spotlight from above, deep shadows, warm amber cast" |
| **Composition** | Camera angle, framing, depth of field | "Low-angle wide shot, shallow depth of field, subject centered" |
| **Style** | Aesthetic reference, rendering approach, color palette | "Editorial illustration, limited palette of rust and navy, dramatic contrast" |
| **Negative** | What must NOT appear | "No people. No text. No logos. No photorealism." |

#### JSON-Structured Prompts (Advanced)

For complex compositions (3+ distinct visual concerns), JSON structure produces more coherent results than equivalent free text. The model parses JSON reliably.

```json
{
  "intent": "One sentence: what this image is for and the concept it visualizes.",
  "frame": {
    "aspect_ratio": "16:9",
    "composition": "Description of framing, camera angle, spatial layout.",
    "style_mode": "editorial_illustration, dramatic_contrast"
  },
  "subject": {
    "primary": "The main visual element with specific details.",
    "visual_details": "Materials, colors, textures, state, positioning.",
    "labels": "Any text that should appear on surfaces (if needed)."
  },
  "environment": {
    "setting": "Where the scene takes place.",
    "foreground": "Props and objects in front.",
    "background": "What's behind the subject.",
    "atmosphere": "Mood of the space."
  },
  "lighting": {
    "type": "Lighting setup (e.g., single hard spotlight, soft ambient, three-point).",
    "quality": "Hard/soft, direction, color temperature."
  },
  "style": {
    "aesthetic": "Style preset or custom description.",
    "palette": "Color constraints.",
    "mood": "Emotional tone."
  },
  "negative": {
    "content": "No people. No logos. No photorealism.",
    "style": "No flat design. No clip-art."
  }
}
```

Use free text for simple metaphors. Reserve JSON for when you need precise control over multiple scene elements.

#### Free-Text Prompt Template

```
[Style] illustration, [visual metaphor from the user's concept].
[1-2 sentences describing the scene, composition, and action].
[Lighting and camera: direction, quality, angle].
Style: [style details], limited color palette, [mood].
[constraints: No people. No text. No logos. No photorealism.]
```

#### Style Presets

| Style | Description | Good For |
|-------|-------------|----------|
| **Editorial** (default) | Flat vector, limited palette, clean shapes | Blogs, social posts, general content |
| **Technical** | Clean lines, schematic/blueprint feel, precise geometry | Architecture diagrams, infrastructure content |
| **Abstract** | Geometric shapes, gradients, flowing forms | Conceptual topics, thought leadership |
| **Isometric** | 3D-ish clean illustration, structured perspective | Infrastructure, systems, platform concepts |
| **Diorama** | Miniature 3D world, soft pastels, smooth rounded forms, gentle shadows | System overviews, multi-component concepts, "how it works" visuals |
| **Infographic** | Clean flat vector, arrows showing flow, labeled elements, sans-serif type | Data flows, processes, educational explainers |
| **Magazine** | Glossy publication mock-up, typography, pull quotes, physical context | Content visualization, editorial mock-ups |

#### Prompt Approval Gate

**STOP. Present the constructed prompt(s) to the user before generating.**

Show:
- The prompt text
- The model (name + API model ID)
- The aspect ratio
- The style preset applied
- The output path

Ask: "Here's the prompt I'll send. Want me to generate, or would you like to adjust it?"

---

### Step 4: Generate

#### Check for the API Key

```bash
source .env 2>/dev/null || true
if [ -z "$GOOGLE_AI_STUDIO_API_KEY" ]; then
  echo "MISSING_KEY"
else
  echo "KEY_FOUND"
fi
```

If `MISSING_KEY`: inform the user and stop.

If `KEY_FOUND`: continue.

#### Make the API Call

Use Python for reliable JSON handling:

```python
python3 << 'PYEOF'
import os, json, base64, urllib.request

# --- Configuration (fill in per generation) ---
API_KEY = os.environ.get("GOOGLE_AI_STUDIO_API_KEY") or open(".env").read().split("GOOGLE_AI_STUDIO_API_KEY=")[1].split("\n")[0]
MODEL_ID = "[MODEL_ID]"
OUTPUT_DIR = "[output-directory]"
FILENAME = "[filename]"
ASPECT_RATIO = "[RATIO]"
PROMPT = "[approved prompt]"
# -----------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

payload = {
    "contents": [{"parts": [{"text": PROMPT}]}],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "imageConfig": {
            "aspectRatio": ASPECT_RATIO,
            "imageSize": "2K"
        }
    }
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent"
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={"x-goog-api-key": API_KEY, "Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
    raise

for part in data["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        path = f"{OUTPUT_DIR}/{FILENAME}.png"
        with open(path, "wb") as f:
            f.write(base64.b64decode(part["inlineData"]["data"]))
        print(f"IMAGE_SAVED: {path}")
        break
else:
    print("IMAGE_FAILED")
    print(json.dumps(data, indent=2)[:1000])
PYEOF
```

---

### Step 5: Review & Iterate

After watermarking:

1. **Show the file path(s)** to the user
2. **Offer iteration** — if the user wants changes:
   - Adjust the prompt (more/less detail, different metaphor, different style)
   - Change the aspect ratio
   - Regenerate
3. **When satisfied:** confirm final file path(s)

---

## Output Location

**Output location:** `marketing/design/[asset-slug]/` — confirm the project slug with the user before creating files.

---

## Related Skills

| Task | Skill |
|------|-------|
| Full essay/post production workflow | `blog` |

## Learnings

<!-- Updated by /reflect. Promote stable patterns to the main skill body. -->

- **[HIGH]** `gemini-3.0-pro-image-preview` (Nano Banana Pro) is not callable on current API keys — returns HTTP 404. Default to `gemini-3.1-flash-image-preview` (Nano Banana 2) for all tasks, including text-heavy technical diagrams where NB2 actually outperforms the listed Pro model (3.1 is newer than 3.0). *(Session 1, 2026-04-12)*
- **[HIGH]** Gemini supports only these aspect ratios: `1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9`. For non-supported target ratios (3:1 Substack profile cover, 5:1 Substack email header), generate at `21:9` with explicit prompt instructions to leave generous top and bottom padding, then crop vertically in Python PIL (`img.crop(...)`) to the target ratio. *(Session 1, 2026-04-12)*
- **[HIGH]** Never regenerate existing user-approved images to propagate a style-spec update without explicit approval. Style changes apply to future images by default; asking first respects the user's prior approval and avoids silently overwriting a decision they already made. *(Session 1, 2026-04-12)*
- **[HIGH]** For brand mastheads and text-on-grid surfaces where pixel precision matters (code-scale text, even grids, exact centering), build directly in PIL instead of rolling Gemini. Gemini defaults to headline scale, occasionally duplicates single lines of text, and renders uneven dotted grids; after 3+ failed rolls it's faster to abandon and build in PIL. *(Session 2, 2026-04-13)*
- **[HIGH]** When designing profile cover images, do NOT include the user's name if the platform's UI renders the name natively below the cover (Substack, LinkedIn, etc.). Duplicating it creates "business card" composition. Let the banner carry only the tagline or positioning line. *(Session 2, 2026-04-13)*
- **[HIGH]** Prefer free-text prompts over JSON-structured prompts for NB2. JSON prompts consistently time out on the Gemini API (two failures at 120s and 300s timeouts), while a condensed free-text version of the same concept succeeds on the first try. Reserve JSON only if free text fails to produce coherent results for a genuinely complex scene. *(Session 11, 2026-05-05)*
- **[HIGH]** Don't replace labeled architecture diagrams with abstract visual metaphors. When an existing diagram communicates with text labels (e.g., "Positioning → Brain → Blog Drafts"), replacing labels with symbolic objects (filing cabinet, tuning fork, chess piece) strips the meaning out. If the original diagram's strength is clarity through labels, preserve the labels and add visual polish, don't abstract them away. *(Session 11, 2026-05-05)*
