# Nano Banana Prompting Reference

Curated patterns from [awesome-nanobanana-pro](https://github.com/ZeroLu/awesome-nanobanana-pro) and Google's official prompting guide, filtered for editorial illustration use cases (Substack heroes, social graphics, infographics). Portrait/selfie/anime patterns omitted.

---

## Pattern 1: Conceptual Visualization

Interpret an abstract concept as a concrete visual. Works well for thought-leadership hero images.

```text
How engineers see the San Francisco Bridge
```

Takeaway: extremely short prompts that name a concept + a perspective can produce striking editorial images. The model's world knowledge fills in the visual metaphor.

---

## Pattern 2: Literal Interpretation

Give the model a filename or phrase and let it interpret literally.

```text
rare.jpg
```

Takeaway: useful for generating unexpected visual metaphors from a single word or phrase. Good for provocative hero images.

---

## Pattern 3: JSON-Structured Scene Description

Break complex compositions into structured fields. The model parses JSON reliably and produces more coherent results than equivalent free-text at this length.

```json
{
  "intent": "Documentary-style photograph of a specific scene.",
  "frame": {
    "aspect_ratio": "4:3",
    "composition": "Centered medium shot with foreground props for scale.",
    "style_mode": "documentary_realism, texture-focused"
  },
  "subject": {
    "primary_subject": "Description of the main visual element.",
    "visual_details": "Specific colors, materials, textures, positioning.",
    "medium_texture": "How the rendering medium itself should look."
  },
  "environment": {
    "location": "Setting description.",
    "foreground_elements": "Props and objects in the foreground.",
    "background_elements": "What's behind the subject.",
    "atmosphere": "Mood of the environment."
  },
  "lighting": {
    "type": "Lighting setup description.",
    "quality": "Hard/soft, direction, color temperature.",
    "color_temperature": "e.g. 5000K neutral white"
  },
  "camera": {
    "lens": "Focal length.",
    "aperture": "f-stop value.",
    "depth_of_field": "What's sharp, what's soft."
  },
  "negative": {
    "content": "What must NOT appear.",
    "style": "Style attributes to avoid."
  }
}
```

Takeaway: JSON prompts shine for compositions with 3+ distinct concerns (subject + environment + lighting + constraints). For simple single-metaphor images, free text is faster and equally effective.

---

## Pattern 4: Isometric 3D Diorama

Miniature-world style illustrations. Good for system/architecture/concept visuals.

```text
Create a high-detail 3D isometric diorama of [subject], where each [component] is represented as its own miniature platform. Inside each [component], place a stylized, small-scale 3D model of that [component]'s most iconic [element]. Use the same visual style as a cute, polished 3D city diorama: soft pastel colors, clean materials, smooth rounded forms, gentle shadows, and subtle reflections. Each [element] should look like a miniature model, charming, simplified, but clearly recognizable. Include labels in a clean, modern font, floating above or near each model.
```

Takeaway: the "diorama" framing consistently produces clean, readable illustrations of complex systems. Specify "soft pastel colors, clean materials, smooth rounded forms" for the polished look.

---

## Pattern 5: Infographic / Data Visualization

Educational or data-driven visuals with labeled elements.

```text
Create an educational infographic explaining [concept]. Visual Elements: Illustrate the key components: [list them]. Style: Clean, flat vector illustration. Use arrows to show the flow of energy and matter. Labels: Label each element clearly.
```

For financial/flow visualizations (Sankey diagrams, funnels):

```text
[Subject]: A professional Sankey diagram visualizing [data flow].
[Visual Style]: High-fidelity vector infographic, clean minimalist aesthetic, flat design. Light grey or off-white background.
[Color Strategy]: Use [brand color] as the dominant theme. Create harmonious palette with saturated shades for nodes and semi-transparent gradients for flowing paths.
[Composition]: Flow from Left to Right. Paths must appear "silky smooth" with elegant Bezier curves, like liquid ribbons.
[Details]: High resolution, 4k, sharp typography (sans-serif), professional data visualization layout.
```

Takeaway: explicitly requesting "flat vector," "clean minimalist," and "arrows to show flow" produces cleaner infographics than vague style descriptions.

---

## Pattern 6: Magazine Layout / Editorial Spread

Placing content into a physical publication context.

```text
Put this whole text, verbatim, into a photo of a glossy magazine article on a desk, with photos, beautiful typography design, pull quotes and brave formatting.
```

For covers:

```text
A photo of a glossy magazine cover, the cover has the large bold words "[TITLE]". The text is in a serif font, black on white, and fills the view. No other text. In front of the text there is [subject description]. Put the issue number and today's date in the corner along with a barcode and a price. The magazine is on a white shelf against a wall.
```

Takeaway: "glossy magazine" + physical context (desk, shelf) produces realistic editorial mock-ups. Useful for visualizing how content will look in publication.

---

## Pattern 7: Product / Luxury Shot

Floating product with environmental staging.

```text
Product: [description of object/concept]

Scene: Luxury shot floating on [surface] with [decorative elements] arranged around it. [Lighting style] creates reflections and ripples.

Mood & Style: [2-3 adjectives], high-end commercial photography, [camera angle], shallow depth of field with soft bokeh background
```

Takeaway: the Product/Scene/Mood three-part structure works well for any "hero object" composition. Swap the product for a conceptual object (a glowing dashboard, a crumbling silo) for editorial metaphors.

---

## Pattern 8: Smart Outpainting / Composition Rescue

Expanding an existing image to a different aspect ratio.

```text
Zoom out and expand this image to a 16:9 aspect ratio. Seamlessly extend the scenery on both sides. Match the original lighting, weather, and texture perfectly. If there are cut-off objects on the borders, complete them naturally. Do not distort the original center image.
```

Takeaway: useful for adapting images between Substack hero (16:9), social (1:1), and other ratios without regenerating from scratch.

---

## Prompting Principles (from Google's official guide)

1. **Subject**: Be specific about what appears. "Stoic robot barista with glowing blue optics" beats "a robot."
2. **Composition**: Frame the shot explicitly (extreme close-up, wide shot, low angle).
3. **Action**: Describe what's happening, not just what exists.
4. **Location**: Specify the setting even for abstract concepts.
5. **Style**: Name the aesthetic (3D animation, film noir, watercolor, 1990s product photography).
6. **Camera & Lighting**: "Direct the shot like a cinematographer" with f-stop, depth of field, color grading.
7. **Negative constraints**: State what must NOT appear.
8. **Text integration**: Clearly state what text should appear, where, and in what style.
