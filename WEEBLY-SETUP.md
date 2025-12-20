# Weebly Setup Guide — Automated Sports Streams

This guide shows you how to add automated, daily-updated sports streams to your Weebly website using this repository.

## Overview

This system automatically:
- Fetches live sports stream channels from TopEmbed API daily
- Extracts working stream URLs using Puppeteer
- Generates a clean, embeddable player page
- Updates automatically via GitHub Actions
- Serves the content from GitHub Pages (free hosting)

## Prerequisites

- A GitHub account (free)
- A Weebly website
- 10-15 minutes for initial setup

## Step 1: Fork or Use This Repository

### Option A: Use this repository directly (recommended for beginners)
1. If you're seeing this in the original repository, you can fork it by clicking "Fork" at the top right of the GitHub page
2. This creates your own copy that you control

### Option B: Create a new repository with these files
1. Create a new GitHub repository (public or private)
2. Copy all files from this repository into yours
3. Push the files to your new repository

## Step 2: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. If prompted, click "I understand my workflows, go ahead and enable them"
4. The workflows will run automatically:
   - Daily at 6:00 AM UTC (generates the embed page)
   - Daily at 2:00 AM UTC (extracts stream URLs)

## Step 3: Enable GitHub Pages

1. In your repository, go to **Settings** > **Pages**
2. Under "Source", select the **gh-pages** branch
3. Click **Save**
4. Wait a few minutes for the site to deploy
5. Your embed page will be available at: `https://[your-username].github.io/[repo-name]/embed/`

## Step 4: Embed in Your Weebly Site

### Method 1: Using Weebly's Embed Code Element (Recommended)

1. Log in to your Weebly site editor
2. Navigate to the page where you want to add streams
3. Drag an **Embed Code** element onto your page
4. Click **Edit Custom HTML**
5. Paste the following code:

```html
<div style="width:100%;max-width:1200px;margin:0 auto;">
  <iframe 
    src="https://[your-username].github.io/[repo-name]/embed/" 
    width="100%" 
    height="900" 
    style="border:0;display:block;"
    allowfullscreen>
  </iframe>
</div>
```

6. Replace `[your-username]` with your GitHub username
7. Replace `[repo-name]` with your repository name
8. Click **Update** and **Publish** your site

### Method 2: Full Page Embed

If you want to dedicate an entire page to streams:

1. Create a new page in Weebly
2. Add an **Embed Code** element
3. Use this code for a full-page experience:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body, html { margin:0; padding:0; height:100%; overflow:hidden; }
    iframe { width:100%; height:100vh; border:0; display:block; }
  </style>
</head>
<body>
  <iframe 
    src="https://[your-username].github.io/[repo-name]/embed/" 
    allowfullscreen>
  </iframe>
</body>
</html>
```

### Method 3: Link Button

Instead of embedding, you can add a button that opens streams in a new tab:

1. Add a **Button** element in Weebly
2. Set the button text to "Watch Live Streams" or similar
3. Set the link to: `https://[your-username].github.io/[repo-name]/embed/`
4. Choose "Open in new tab"

## Step 5: Test Your Integration

1. Visit your Weebly page
2. You should see a grid of sports channels
3. Click any channel tile to load the stream
4. The stream should play in the embedded player

## Customization Options

### Adjust Number of Channels

Edit `generate.py` line 162:
```python
p.add_argument('--limit', '-n', type=int, default=120, help='max channels to include')
```

Change `default=120` to your preferred number (e.g., `default=50` for fewer channels).

### Customize Appearance

The embedded page styles are in `generate.py` lines 24-34. You can modify:
- Colors (background, borders, buttons)
- Layout (card sizes, spacing)
- Fonts and text sizes

After making changes, commit and push to GitHub. The workflow will regenerate the page automatically.

### Change Update Schedule

Edit `.github/workflows/generate.yml` line 5:
```yaml
- cron: '0 6 * * *' # daily at 06:00 UTC
```

Use [crontab.guru](https://crontab.guru/) to create your preferred schedule.

## AdSense Compatibility

**Important**: The embedded streams page (`/embed/`) should be kept ad-free to comply with Google AdSense policies regarding third-party content.

### Recommended Setup:
1. Keep ads on your main Weebly pages
2. Keep the `/embed/` page ad-free
3. Use the `landing_page.html` as your main entry point with ads
4. Link from the landing page to the embed page

To use the landing page:
1. Your GitHub Pages will serve it at: `https://[your-username].github.io/[repo-name]/`
2. The landing page has AdSense placeholder code
3. Visitors click "Open Live Streams" to go to the ad-free player

## Troubleshooting

### Iframe Shows "Refused to Connect"
- Some browsers block iframes with third-party content
- Test in a different browser
- Check browser console for errors (F12 > Console tab)

### Streams Not Loading
- Wait 24 hours after setup for the first workflow run
- Check the "Actions" tab in GitHub to see if workflows are running
- Manually trigger a workflow by going to Actions > Generate TopEmbed static site > Run workflow

### Empty Channel List
- The TopEmbed API may be temporarily down
- Check `embed/channels.json` in your repository to see if channels were fetched
- The workflow logs will show any API errors

### GitHub Pages Not Working
- Ensure the repository is public (or you have GitHub Pro for private repos)
- Check Settings > Pages to confirm gh-pages branch is selected
- Wait 5-10 minutes after enabling Pages

## Support

See `TROUBLESHOOTING.md` for additional help with:
- CORS and mixed-content issues  
- CSP/X-Frame-Options blocks
- Debugging workflow failures

## Legal Notice

- TopEmbed channels may include copyrighted or paid streams
- Ensure you have rights to embed and display these streams
- This may affect AdSense compliance if ads are shown on pages with unauthorized content
- The repository maintainers are not responsible for content sourced from third-party APIs

## Next Steps

After setup, your streams will update automatically every day. No maintenance required!

Optional enhancements:
- Add custom branding to the generated page
- Create per-channel detail pages
- Add thumbnails for each channel
- Implement search/filter functionality
