# LinkedIn Analytics Setup

## 1. Create a LinkedIn Developer App

1. Go to [LinkedIn Developer Portal](https://developer.linkedin.com/apps)
2. Click **Create App**
3. Fill in:
   - **App name:** [Your Brand] Analytics
   - **LinkedIn Page:** Select your company page
   - **App logo:** Upload your company logo
4. Submit and note your **Client ID** and **Client Secret**

## 2. Request API Access

In your app settings, go to the **Products** tab and request access to:
- **Share on LinkedIn** (gives `w_member_social`)
- **Community Management API** (gives `r_organization_social`, `w_organization_social`)

The Community Management API is what provides organization-level analytics. Approval may take a few days.

## 3. Required Permissions (Scopes)

- `r_organization_social` — Read organization posts and share statistics
- `r_organization_admin` — Read organization page data and follower stats

## 4. Get an Access Token

### Option A: Quick token via OAuth Playground

1. In the Developer Portal, go to **Auth** tab
2. Set **Redirect URL** to `https://localhost:3000/callback`
3. Build the authorization URL:
   ```
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https://localhost:3000/callback&scope=r_organization_social%20r_organization_admin
   ```
4. Open in browser, authorize, grab the `code` from the redirect URL
5. Exchange for token:
   ```bash
   curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
     -d "grant_type=authorization_code" \
     -d "code=YOUR_CODE" \
     -d "redirect_uri=https://localhost:3000/callback" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET"
   ```
6. Copy the `access_token` from the response

### Option B: Use the LinkedIn Token Generator (simpler)

Some developer apps have a **Token Generator** under the Auth tab that lets you generate a token with selected scopes directly.

## 5. Find Your Organization ID

1. Go to your [LinkedIn Company Page]([your-linkedin-company-url]) as an admin
2. The org ID is in the URL path, or you can find it via the API:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://api.linkedin.com/v2/organizationAcls?q=roleAssignee&role=ADMINISTRATOR&projection=(elements*(organization~(id,localizedName)))"
   ```
3. The `id` field is your organization ID (a number like `12345678`)

## 6. Add to .env

```bash
LINKEDIN_ACCESS_TOKEN=your_access_token_here
LINKEDIN_ORG_ID=your_org_id_here
```

## Token Renewal

LinkedIn access tokens expire after **60 days**. When yours expires:
1. Re-run the OAuth flow above
2. Update `LINKEDIN_ACCESS_TOKEN` in `.env`

A refresh token flow can automate this, but for monthly analytics checks the manual renewal is fine.
