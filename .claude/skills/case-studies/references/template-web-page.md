# Web Page Template

Use this structure for publishing case studies on the [Company] website or customer-facing web properties. Optimized for SEO, scannability, and conversion.

---

## SEO Metadata

```html
<title>[Customer Name]: [Key Outcome] with the company | Case Study</title>
<meta name="description" content="Learn how [Customer] achieved [key metric] using [Company] for [value proposition]. [Secondary benefit].">
<meta name="keywords" content="[Company], case study, [industry], [product category], [core keyword], [secondary keyword]">
```

**URL slug:** `/case-studies/[customer-name-slugified]`
*Example: `/case-studies/acme-corp-mttr-reduction`*

---

## Page Structure

### Hero Section

```
[CUSTOMER LOGO - if branded]

# [Headline: Outcome-Focused Statement]

[2-3 sentence executive summary capturing the transformation]

[PRIMARY CTA BUTTON: "Sign Up for a Demo"]
```

**Example:**
```
# How Acme Corp Cut MTTR by 75% Without Touching Code

Acme's team went from [before state] across 200+ [systems/teams/locations] to [after state]—without disrupting existing workflows.

[Sign Up for a Demo]
```

---

### Key Metrics Sidebar/Callout

```
┌─────────────────────────────┐
│  KEY RESULTS                │
├─────────────────────────────┤
│  75%     │ Reduction in MTTR │
│  200+    │ Services covered  │
│  <1 hr   │ Time to deploy    │
└─────────────────────────────┘
```

Place this prominently—sidebar on desktop, inline callout on mobile.

---

### Before [Company]

```html
<section class="before-[company]">
  <h2>Before [Company]</h2>

  <p>[Opening paragraph describing their environment and approach]</p>

  <h3>Gaps & Challenges</h3>
  <ul>
    <li>[Gap/challenge 1]</li>
    <li>[Gap/challenge 2]</li>
    <li>[Gap/challenge 3]</li>
  </ul>

  <h3>Business Impact</h3>
  <p>[What these gaps were costing the team and business]</p>

  <blockquote>
    <p>"[Quote capturing the frustration]"</p>
    <cite>— [Name], [Title], [Company]</cite>
  </blockquote>
</section>
```

---

### Why They Chose [Company]

```html
<section class="why-[company]">
  <h2>Why They Chose [Company]</h2>

  <h3>Decision Factors</h3>
  <ul class="feature-list">
    <li>
      <strong>[Factor 1]</strong>
      <span>[Detail]</span>
    </li>
    <li>
      <strong>[Factor 2]</strong>
      <span>[Detail]</span>
    </li>
    <li>
      <strong>[Factor 3]</strong>
      <span>[Detail]</span>
    </li>
  </ul>

  <aside class="stood-out">
    <h4>What Stood Out vs Alternatives</h4>
    <p>[Key differentiator—AI-native detection, behavioral analysis]</p>
  </aside>
</section>
```

---

### After [Company]

```html
<section class="after-[company]">
  <h2>After [Company]</h2>

  <p>[What changed—overview paragraph]</p>

  <div class="results-grid">
    <div class="business-results">
      <h3>Business Results</h3>
      <ul>
        <li>[Business outcome 1]</li>
        <li>[Business outcome 2]</li>
      </ul>
    </div>
    <div class="technical-results">
      <h3>Technical Results</h3>
      <ul>
        <li>[Technical outcome 1]</li>
        <li>[Technical outcome 2]</li>
      </ul>
    </div>
  </div>

  <blockquote class="hero-quote">
    <p>"[Strongest customer testimonial—2-3 sentences]"</p>
    <cite>
      <img src="[speaker-photo.jpg]" alt="[Name]">
      <span class="name">[Name]</span>
      <span class="title">[Title], [Company]</span>
    </cite>
  </blockquote>
</section>
```

---

### Key Results

```html
<section class="key-results">
  <h2>Key Results</h2>

  <table class="metrics-table">
    <thead>
      <tr>
        <th>Metric</th>
        <th>Before</th>
        <th>After</th>
        <th>Improvement</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Mean Time to Resolution</td>
        <td>4 hours</td>
        <td>45 minutes</td>
        <td class="highlight">81% reduction</td>
      </tr>
      <!-- Additional rows -->
    </tbody>
  </table>
</section>
```

---

### Call to Action

```html
<section class="cta">
  <h2>Sign Up for a Demo</h2>
  <p>[Customer] achieved [key result] with the company. See how AI-native threat detection can work for your team.</p>

  <div class="cta-buttons">
    <a href="https://[your-site]" class="btn-primary">Sign Up for a Demo</a>
  </div>
</section>
```

---

### Related Content (Footer)

```html
<section class="related">
  <h2>More Customer Stories</h2>

  <div class="case-study-cards">
    <a href="[related-case-study-1]">
      <span class="industry">[Industry]</span>
      <h3>[Headline]</h3>
    </a>
    <a href="[related-case-study-2]">
      <span class="industry">[Industry]</span>
      <h3>[Headline]</h3>
    </a>
  </div>
</section>
```

---

## Mobile Optimization Notes

- **Hero metrics**: Stack vertically, use large typography
- **Tables**: Convert to card layout on mobile
- **Blockquotes**: Full-width with left border accent
- **CTAs**: Sticky footer button on mobile

## Accessibility Checklist

- [ ] All images have alt text
- [ ] Quote citations properly marked up
- [ ] Heading hierarchy is logical (h1 > h2 > h3)
- [ ] Color contrast meets WCAG AA standards
- [ ] Links are descriptive (not "click here")

## Schema Markup (Optional)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Case study headline]",
  "author": {
    "@type": "Organization",
    "name": "[Company]"
  },
  "about": {
    "@type": "Organization",
    "name": "[Customer Name]"
  },
  "datePublished": "[YYYY-MM-DD]"
}
```
