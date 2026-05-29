# YouTube Analytics Setup

## Converting to a Brand Channel

If your current YouTube channel is a personal channel and you want to convert it to a brand channel:

### Option A: Move to a Brand Account (preferred)

1. Sign in to YouTube at [youtube.com](https://www.youtube.com)
2. Go to **Settings** (gear icon) > **Account** > **Add or manage your channel(s)**
3. Click **Create a new channel** (this creates a Brand Account)
4. Name it "[Your Brand]" and configure it
5. To move existing content: Go to **Settings** > **Account** > **Move channel to a Brand Account**
6. Follow the prompts to transfer videos, subscribers, and playlists

### Option B: Create a Fresh Brand Channel

1. Go to [YouTube Channel Switcher](https://www.youtube.com/channel_switcher)
2. Click **Create a new channel**
3. Enter "[Your Brand]" as the channel name
4. This creates a Brand Account channel that multiple people can manage

### Brand Channel Benefits

- Multiple managers/owners without sharing passwords
- Separate from personal Google account
- Professional channel name (not tied to a person's name)
- Can be transferred to other team members

## API Setup

### 1. Enable YouTube APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create or select a project (e.g., "[Your Brand] Marketing")
3. Go to **APIs & Services** > **Library**
4. Enable both:
   - **YouTube Data API v3**
   - **YouTube Analytics API**

### 2. Create OAuth 2.0 Credentials

1. In the Cloud Console, go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. Application type: **Desktop app**
4. Name: "[Your Brand] Analytics CLI"
5. Download the JSON credentials file

### 3. Get an Access Token

The simplest way for CLI usage:

1. Go to [Google OAuth Playground](https://developers.google.com/oauthplayground/)
2. In the settings gear (top right), check **Use your own OAuth credentials**
3. Enter your Client ID and Client Secret
4. In Step 1, select scopes:
   - `https://www.googleapis.com/auth/yt-analytics.readonly`
   - `https://www.googleapis.com/auth/youtube.readonly`
5. Click **Authorize APIs** and sign in with the Google account that owns the channel
6. In Step 2, click **Exchange authorization code for tokens**
7. Copy the **Access Token**

### 4. Find Your Channel ID

1. Go to [YouTube Studio](https://studio.youtube.com)
2. Click your profile icon > **Settings** > **Channel** > **Advanced settings**
3. Your Channel ID starts with `UC` (e.g., `UCxxxxxxxxxxxxxxxxxxxxxx`)

Or via API:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://www.googleapis.com/youtube/v3/channels?part=id,snippet&mine=true"
```

### 5. Add to .env

```bash
YOUTUBE_ACCESS_TOKEN=your_access_token_here
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxxx
```

## Token Renewal

OAuth Playground tokens expire after **1 hour**. For regular use, you'll want to set up refresh token automation. For now, regenerate via the OAuth Playground when needed.

Future improvement: Add a `youtube-auth.ts` script that uses a stored refresh token to automatically get fresh access tokens.
