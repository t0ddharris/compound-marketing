# X (Twitter) Analytics Setup

Your account needs X Premium+ (or equivalent API access) to use these analytics features.

## 1. Get API Access

1. Go to the [X Developer Portal](https://developer.x.com/en/portal/dashboard)
2. Sign in with the [your-x-handle] account (or an account with developer access)
3. If you don't have a project yet, create one:
   - **Project name:** [Your Brand] Analytics
   - **Use case:** Analytics / Reporting
4. Create an **App** inside the project

## 2. Generate a Bearer Token

1. In your App settings, go to **Keys and tokens**
2. Under **Bearer Token**, click **Generate**
3. Copy the token

The Bearer Token provides app-level read access, which is sufficient for pulling tweet metrics and profile stats for [your-x-handle].

## 3. Add to .env

```bash
X_BEARER_TOKEN=your_bearer_token_here
X_USERNAME=[your-x-handle]
```

## API Tier

With Premium+, you should have access to the **Pro** tier or equivalent, which includes:
- Tweet lookup with `public_metrics` (impressions, likes, retweets, replies, quotes, bookmarks)
- User timeline with up to 100 tweets per request
- Higher rate limits than Basic

## Rate Limits

Pro tier rate limits (per 15-minute window):
- Tweet lookup: 900 requests
- User tweet timeline: 1,500 requests
- User lookup: 900 requests

These are more than enough for analytics pulls.

## Token Renewal

Bearer tokens do not expire unless regenerated. If you regenerate it in the Developer Portal, update `.env` with the new token.
