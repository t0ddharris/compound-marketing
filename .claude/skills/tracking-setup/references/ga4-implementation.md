# GA4 Implementation Reference

Detailed implementation guide for Google Analytics 4.

## Configuration

### Data Streams

- One stream per platform (web, iOS, Android)
- Enable enhanced measurement for automatic tracking
- Configure data retention (2 months default, 14 months max)
- Enable Google Signals (for cross-device, if consented)

### Enhanced Measurement Events (Automatic)

| Event | Description | Configuration |
|-------|-------------|---------------|
| page_view | Page loads | Automatic |
| scroll | 90% scroll depth | Toggle on/off |
| outbound_click | Click to external domain | Automatic |
| site_search | Search query used | Configure parameter |
| video_engagement | YouTube video plays | Toggle on/off |
| file_download | PDF, docs, etc. | Configurable extensions |

### Recommended Events

Use Google's predefined events when possible for enhanced reporting:

**All properties:**
- login, sign_up
- share
- search

**E-commerce:**
- view_item, view_item_list
- add_to_cart, remove_from_cart
- begin_checkout
- add_payment_info
- purchase, refund

**Games:**
- level_up, unlock_achievement
- post_score, spend_virtual_currency

Reference: https://support.google.com/analytics/answer/9267735

---

## Custom Events

### gtag.js Implementation

```javascript
// Basic event
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});

// Event with value
gtag('event', 'purchase', {
  'transaction_id': 'T12345',
  'value': 99.99,
  'currency': 'USD',
  'items': [{
    'item_id': 'SKU123',
    'item_name': 'Product Name',
    'price': 99.99
  }]
});

// User properties
gtag('set', 'user_properties', {
  'user_type': 'premium',
  'plan_name': 'pro'
});

// User ID (for logged-in users)
gtag('config', 'GA_MEASUREMENT_ID', {
  'user_id': 'USER_ID'
});
```

### Google Tag Manager (dataLayer)

```javascript
// Custom event
dataLayer.push({
  'event': 'signup_completed',
  'method': 'email',
  'plan': 'free'
});

// Set user properties
dataLayer.push({
  'user_id': '12345',
  'user_type': 'premium'
});

// E-commerce purchase
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 99.99,
    'currency': 'USD',
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99,
      'quantity': 1
    }]
  }
});

// Clear ecommerce before sending (best practice)
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'view_item',
  'ecommerce': {
    // ...
  }
});
```

---

## Conversions Setup

### Creating Conversions

1. **Collect the event** - Ensure event is firing in GA4
2. **Mark as conversion** - Admin > Events > Mark as conversion
3. **Set counting method**:
   - Once per session (leads, signups)
   - Every event (purchases)
4. **Import to Google Ads** - For conversion-optimized bidding

### Conversion Values

```javascript
// Event with conversion value
gtag('event', 'purchase', {
  'value': 99.99,
  'currency': 'USD'
});
```

Or set default value in GA4 Admin when marking conversion.

---

## Custom Dimensions and Metrics

### When to Use

**Custom dimensions:**
- Properties you want to segment/filter by
- User attributes (plan type, industry)
- Content attributes (author, category)

**Custom metrics:**
- Numeric values to aggregate
- Scores, counts, durations

### Setup Steps

1. Admin > Data display > Custom definitions
2. Create dimension or metric
3. Choose scope:
   - **Event**: Per event (content_type)
   - **User**: Per user (account_type)
   - **Item**: Per product (product_category)
4. Enter parameter name (must match event parameter)

### Examples

| Dimension | Scope | Parameter | Description |
|-----------|-------|-----------|-------------|
| User Type | User | user_type | Free, trial, paid |
| Content Author | Event | author | Blog post author |
| Product Category | Item | item_category | E-commerce category |

---

## Audiences

### Creating Audiences

Admin > Data display > Audiences

**Use cases:**
- Remarketing audiences (export to Ads)
- Segment analysis
- Trigger-based events

### Audience Examples

**High-intent visitors:**
- Viewed pricing page
- Did not convert
- In last 7 days

**Engaged users:**
- 3+ sessions
- Or 5+ minutes total engagement

**Purchasers:**
- Purchase event
- For exclusion or lookalike

---

## Debugging

### DebugView

Enable with:
- URL parameter: `?debug_mode=true`
- Chrome extension: GA Debugger
- gtag: `'debug_mode': true` in config

View at: Reports > Configure > DebugView

### Real-Time Reports

Check events within 30 minutes:
Reports > Real-time

### Common Issues

**Events not appearing:**
- Check DebugView first
- Verify gtag/GTM firing
- Check filter exclusions

**Parameter values missing:**
- Custom dimension not created
- Parameter name mismatch
- Data still processing (24-48 hrs)

**Conversions not recording:**
- Event not marked as conversion
- Event name doesn't match
- Counting method (once vs. every)

---

## Data Quality

### Filters

Admin > Data streams > [Stream] > Configure tag settings > Define internal traffic

**Exclude:**
- Internal IP addresses
- Developer traffic
- Testing environments

### Cross-Domain Tracking

**STOP. Do the canonicalization precheck before configuring cross-domain.**

Before listing domains in GA4's "Configure your domains" setting, verify that each hostname in your list is actually *supposed* to be reachable. Common mistake: adding both `example.com` and `www.example.com` when only one should exist, because the other should 301-redirect to the canonical.

**The canonicalization precheck (run for each planned domain):**

```bash
curl -sI https://example.com/ | head -5
curl -sI https://www.example.com/ | head -5
```

Expected behavior: ONE of them returns `HTTP 200`, the other returns `HTTP 301` with a `location` header pointing to the canonical. If BOTH return `HTTP 200`, you have a canonicalization bug that must be fixed at the CDN/hosting layer (CloudFront Function, nginx, Vercel redirect, or `next.config.js`) BEFORE completing GA4 setup. Symptoms of not fixing it:

- GA4 splits traffic across two `hostName` values, fragmenting session and user counts
- SEO duplicate content — link equity dilutes across hostnames
- CookieYes / consent cookies set on one hostname don't apply to the other (different domains to the browser)
- HubSpot tracking cookies split the same way

**Only after confirming canonical redirects are in place, proceed:**

1. Admin > Data streams > [Stream] > Configure tag settings
2. Configure your domains
3. List all **distinct** domains that should share sessions (NOT apex + www variants — only the canonical one)

**Subdomain verification:** after configuring, verify each subdomain is actually firing the GTM container. Run:

```bash
curl -s https://subdomain.example.com/ | grep -o -E "GTM-[A-Z0-9]+|G-[A-Z0-9]+"
```

Each subdomain should return the SAME `GTM-XXXX` (or same `G-XXXX` measurement ID) as the main site. If a subdomain returns:

- **Nothing:** GTM is not installed there. Traffic is invisible to your main GA4 property. Fix by installing GTM on that subdomain (e.g., HubSpot Settings → Content → Pages → Domains → site header HTML; Docusaurus `themeConfig.gtag`; Mintlify `analytics` config).
- **A different measurement ID or container:** that subdomain has its own separate GA4 property. Either retire it and install the main container, or grant reporting access to both properties. Do NOT assume cross-domain tracking is working — it isn't.

Plan-vs-reality mismatch is common here. Check every subdomain before marking cross-domain setup complete.

---

### Consent Mode v2 — geo-target your denied defaults

**STOP. If using Consent Mode v2, default-deny globally is almost always wrong.**

Most sites that implement Consent Mode v2 do this by default:

```javascript
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'analytics_storage': 'denied',
  'wait_for_update': 500
});
```

This denies `analytics_storage` for **every visitor worldwide** until they explicitly accept cookies. Combined with typical 25–45% cookie-banner acceptance rates, this drops 55–75% of your traffic from GA4. GA4 will show roughly 25–40% of what cookieless tools like Plausible show for the same period.

This is stricter than the law requires. GDPR and similar opt-in laws only apply in regulated regions (EU/EEA under GDPR, UK under UK DPA, Switzerland under FADP). US, APAC, LATAM, and most of the rest of the world do NOT legally require pre-tracking consent. Denying analytics globally sacrifices the majority of your data for no legal benefit.

**The correct pattern — geo-targeted denial with Advanced Consent Mode:**

```javascript
// Strict denial ONLY for regions that legally require consent
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'analytics_storage': 'denied',
  'wait_for_update': 500,
  'region': ['AT','BE','BG','HR','CY','CZ','DK','EE','FI','FR','DE','GR','HU','IS','IE','IT','LV','LI','LT','LU','MT','NL','NO','PL','PT','RO','SK','SI','ES','SE','GB','CH']
});

// Permissive default for rest of world: analytics granted, ads still denied
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'analytics_storage': 'granted'
});

// Advanced Consent Mode: cookieless pings + ad data redaction
// Enables behavioral modeling to recover denied-region traffic
gtag('set', 'url_passthrough', true);
gtag('set', 'ads_data_redaction', true);
```

**What each piece does:**

1. **Geo-targeted denial:** only visitors from the listed regions default to denied. Everywhere else, analytics is granted from page load — no banner friction, direct tracking. The region list covers EU27 + EEA (IS, LI, NO) + UK + Switzerland. Add CA provinces or BR if you're also targeting PIPEDA/LGPD-strict.

2. **Permissive default:** applies to all regions not matched by the first call. `ad_storage` and friends stay denied (ads consent is stricter and should still be opt-in globally for safety), but `analytics_storage` is granted so the GA4 tag fires on page load without waiting for consent.

3. **`url_passthrough: true`:** when consent is denied, GA4 passes through session identifiers in URL parameters instead of cookies. This keeps sessions consistent across navigation for denied visitors.

4. **`ads_data_redaction: true`:** when consent is denied, ad click identifiers are redacted before sending. Enables "cookieless pings" that Google uses for behavioral modeling to estimate missing traffic.

**Volume threshold for modeling:** Advanced Consent Mode's behavioral modeling requires the property to hit thresholds before GA4 will show modeled data:

- At least 1,000 events/day with `analytics_storage=denied` for 7+ consecutive days
- At least 1,000 daily users triggering the modeled event over the past 28 days

Below this volume, cookieless pings are still sent but modeling does not activate. The Reporting Identity setting (Admin > Property Settings > Reporting Identity) should be set to **Blended** to surface modeled data once it's available — but this is passive; it won't "break" anything below threshold, it will just show "Modeling is unavailable for this property."

**At low volume, the real lever is the geo-targeting change, not Advanced mode.** US-heavy or rest-of-world-heavy sites should see GA4 coverage jump to 70–90% of a cookieless baseline immediately after shipping the geo-targeted defaults, with modeling as future-proofing for when the site scales.

**Order of operations for Consent Mode setup:**

1. Before anything, verify CookieYes (or your CMP) is **also** configured with matching geo-targeting — the banner should only show for EU/UK/CH visitors, not globally. Otherwise US visitors see an unnecessary banner even though we're not blocking them. Check at `app.cookieyes.com` → site → Geo-Targeting.
2. Place the consent-defaults `<script>` with `beforeInteractive` strategy so it runs BEFORE GTM loads. In Next.js: use `<Script strategy="beforeInteractive">` in `app/layout.tsx`.
3. Inside GTM: confirm the GA4 tag has no manual "Additional consent checks" that would override the gtag defaults. The tag should rely on the gtag consent state, not enforce its own.
4. After deploy, verify in production devtools: `window.dataLayer` should contain the consent default calls with the `region` array, and the `url_passthrough` / `ads_data_redaction` sets.
5. Re-compare GA4 vs the cookieless baseline (Plausible, server logs) 2–3 days later. Coverage should have jumped.

### Session Settings

Admin > Data streams > [Stream] > Configure tag settings

- Session timeout (default 30 min)
- Engaged session duration (10 sec default)

---

## Integration with Google Ads

### Linking

1. Admin > Product links > Google Ads links
2. Enable auto-tagging in Google Ads
3. Import conversions in Google Ads

### Audience Export

Audiences created in GA4 can be used in Google Ads for:
- Remarketing campaigns
- Customer match
- Similar audiences
