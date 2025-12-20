Troubleshooting the generated TopEmbed site

This guide covers common issues when setting up and using automated sports streams with Weebly and GitHub Pages.

## Table of Contents
- [Setup Issues](#setup-issues)
- [Player and Stream Issues](#player-and-stream-issues)
- [Weebly Embedding Issues](#weebly-embedding-issues)
- [GitHub Actions Workflow Issues](#github-actions-workflow-issues)
- [General Debugging Tips](#general-debugging-tips)

---

## Setup Issues

### GitHub Actions Not Running

**Symptoms:** No workflows appear in the Actions tab, or workflows don't run on schedule.

**Solutions:**
1. Ensure GitHub Actions are enabled:
   - Go to repository Settings > Actions > General
   - Enable "Allow all actions and reusable workflows"
2. For scheduled workflows, note that GitHub may delay execution during high-load periods
3. Manually trigger a workflow:
   - Go to Actions tab
   - Select "Generate TopEmbed static site"
   - Click "Run workflow"

### GitHub Pages Not Working

**Symptoms:** Visiting the GitHub Pages URL shows a 404 error or doesn't load.

**Solutions:**
1. Verify GitHub Pages is enabled:
   - Go to Settings > Pages
   - Source should be set to "gh-pages" branch
   - The URL should be displayed at the top
2. Wait 5-10 minutes after enabling Pages or pushing changes
3. Check if gh-pages branch exists:
   - Click "branches" on main repo page
   - If gh-pages doesn't exist, run the "Generate TopEmbed static site" workflow manually
4. For private repositories:
   - GitHub Pages requires GitHub Pro or above
   - Consider making the repository public

### Workflow Fails During Run

**Symptoms:** Red X mark on workflow runs in Actions tab.

**Solutions:**
1. Click on the failed workflow run to see details
2. Expand the failed step to read error messages
3. Common issues:
   - **API timeout:** TopEmbed API may be down or slow; wait and re-run
   - **Puppeteer installation fails:** Workflow will retry; usually resolves on next run
   - **Permission denied on push:** Ensure repository settings allow Actions to write

---

## Player and Stream Issues

### Player shows "No channel loaded" or iframe is blank

**Causes:**
- No channel has been clicked yet (expected behavior)
- The clicked channel failed to load

**Solutions:**
1. Try clicking different channel tiles
2. Click the "Open" link on a card to test the channel URL directly in a new tab
3. If the direct link fails, that specific channel is not available
4. Wait for the next daily update when channels refresh

### Iframe shows "Refused to Connect" or "X-Frame-Options" error

**Causes:**
- Some TopEmbed channels block iframe embedding using X-Frame-Options or CSP headers
- This is a security measure from the source

**Solutions:**
1. This affects specific channels, not all channels
2. Use the "Open" link to view blocked channels in a new tab instead
3. No reliable workaround exists (proxying raises legal issues)
4. Focus on channels that work in iframes

### Streams Play But No Audio/Video

**Causes:**
- Browser autoplay policies block media with sound
- Stream hasn't loaded yet
- Stream URL is invalid or expired

**Solutions:**
1. Click inside the iframe to give it focus, then play
2. Enable autoplay in browser settings for your domain
3. Check browser console (F12) for specific errors
4. Try a different channel to verify it's channel-specific

### CORS / Mixed Content Errors

**Symptoms:** Console shows CORS errors or mixed content warnings.

**Causes:**
- Your GitHub Pages site is HTTPS but some stream URLs use HTTP
- Browser blocks insecure content on secure pages

**Solutions:**
1. Ensure your GitHub Pages site uses HTTPS (should be automatic)
2. Unfortunately, you cannot force HTTP streams to HTTPS
3. Channels with HTTPS URLs will work; HTTP-only channels may not
4. This is a browser security limitation, not a bug

### Channels Work Intermittently

**Causes:**
- Third-party stream sources go online/offline
- TopEmbed rotates or removes channels
- Geographic restrictions or rate limiting

**Solutions:**
1. This is expected behavior with third-party sources
2. The daily update will refresh the channel list
3. More channels = higher chance of finding working ones
4. Consider increasing the `--limit` parameter in generate.py to fetch more channels

---

## Weebly Embedding Issues

### Embed Code Element Not Available

**Symptoms:** Can't find "Embed Code" element in Weebly editor.

**Solutions:**
1. Embed Code is available in most Weebly plans
2. Look in the "Basic" elements section in the editor sidebar
3. For older Weebly editors, look for "Custom HTML" or "Code Block"
4. If not available, upgrade your Weebly plan or contact Weebly support

### Iframe Not Displaying on Weebly Page

**Symptoms:** Empty space or nothing shows where the iframe should be.

**Solutions:**
1. Ensure you clicked "Update" after pasting the embed code
2. Check that your GitHub Pages URL is correct
3. Right-click the empty space and "Inspect Element" (F12) to see if iframe loaded
4. View page source (Ctrl+U) to verify iframe code was included
5. Try viewing in an incognito/private window to rule out cache issues

### Iframe Shows But Content Not Loading

**Symptoms:** Gray box or loading spinner, but content never appears.

**Solutions:**
1. Test the GitHub Pages URL directly in a new browser tab
2. If URL works directly but not in iframe, check browser console for errors
3. Verify the `/embed/` path is correct in the iframe src
4. Try increasing iframe height to 1000px or more
5. Clear browser cache and reload

### Iframe Too Small or Poorly Sized

**Symptoms:** Scrollbars inside iframe, or content cut off.

**Solutions:**
1. Increase height in iframe code: `height="1200"` or higher
2. For responsive sizing, use percentage: `height: 80vh;` in style attribute
3. Consider full-page iframe for dedicated stream pages

---

## GitHub Actions Workflow Issues

### Workflow Runs But Produces Empty Channel List

**Symptoms:** Generated page has no channels or very few channels.

**Solutions:**
1. Check workflow logs:
   - Actions tab > Select the workflow run
   - Expand "Run generator" step
   - Look for "Fetching API..." and "Building HTML with X channels"
2. If API fetch failed:
   - TopEmbed API may be temporarily down
   - Check https://topembed.pw/api.php?format=json in a browser
   - Wait a few hours and let the next scheduled run try again
3. If extractor fails:
   - Check "Run extractor" step logs
   - Puppeteer issues may require workflow retry
   - Download extractor-debug artifact for detailed logs

### Cannot Download Workflow Artifacts

**Symptoms:** "extractor-debug" artifact not available.

**Solutions:**
1. Artifacts only exist for ~90 days by default
2. Only available if workflow completed (even with errors)
3. Must be logged in to GitHub to download artifacts
4. Check if the workflow step that uploads artifacts ran

### Workflow Runs But GitHub Pages Not Updating

**Symptoms:** Workflow succeeds but site content is stale.

**Solutions:**
1. Check if "Prepare gh-pages branch" step succeeded
2. Verify push to gh-pages was successful
3. Wait 5-10 minutes for GitHub Pages to rebuild
4. Hard refresh browser (Ctrl+Shift+R) to clear cache
5. Check gh-pages branch directly to see if files updated

### Node Modules or Debug Files Committed

**Symptoms:** Repository has large node_modules directory or debug logs in commits.

**Solutions:**
1. These should be gitignored (see .gitignore)
2. If accidentally committed:
   ```bash
   git rm -r --cached node_modules debug
   git commit -m "Remove ignored files"
   git push
   ```
3. Verify .gitignore includes `node_modules/` and `debug/`

---

## General Debugging Tips

### Browser Console (F12)

Open your browser's developer console to see:
- Network requests (see which streams load/fail)
- Console errors (CORS, CSP, JavaScript errors)
- Security warnings (mixed content, blocked resources)

**How to use:**
1. Press F12 (or right-click > Inspect)
2. Go to Console tab for error messages
3. Go to Network tab to see stream URL requests
4. Filter by "m3u8" or "mp4" to see media requests

### Check Generated Files

The workflow outputs these files you can inspect:

1. **channels.json** - Raw list of channel URLs fetched
   - Location: `/out/channels.json` in gh-pages branch
   - Check if URLs look valid
   - Verify the list isn't empty

2. **index.html** - The generated player page
   - Location: `/embed/index.html` in gh-pages branch
   - View source to verify structure
   - Check that channels were rendered

3. **extractor.log** - Detailed extractor debug info
   - Download from workflow artifacts
   - Shows which channels were processed
   - Contains error details for failed channels

### Test Locally

You can run the generator locally for faster iteration:

```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Generate from existing channels
python generate.py --input-channels embed/channels.json --output test-out --limit 20

# Or fetch from API
python generate.py --output test-out --limit 20

# Open in browser
open test-out/index.html  # or start a local server
```

### Verify Channel URLs Manually

Test individual channel URLs:
1. Copy a channel URL from channels.json
2. Paste in browser address bar
3. See if it loads/plays in the browser directly
4. If it doesn't work directly, it won't work in the iframe

### Check Repository Settings

Verify these settings are correct:
1. **Actions**: Enabled, all actions allowed
2. **Pages**: Source set to gh-pages branch
3. **Visibility**: Public (or Private with GitHub Pro for Pages)

---

## Still Having Issues?

If you've tried the above and still have problems:

1. **Check existing GitHub Issues** in this repository for similar problems
2. **Open a new Issue** with:
   - Detailed description of the problem
   - What you've tried
   - Screenshots of errors
   - Link to your repository (if public)
   - Workflow run logs or console errors
3. **Review the documentation** again:
   - [WEEBLY-SETUP.md](WEEBLY-SETUP.md) - Full setup guide
   - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
   - [README.md](README.md) - Technical overview

---

## Legal and Compliance Issues

### AdSense Policy Concerns

**Issue:** Worried about AdSense compliance with third-party streams.

**Best Practice:**
- Keep the `/embed/` page ad-free (no AdSense code)
- Show ads on landing pages (like `landing_page.html`)
- Separate content: ads on entry pages, streams on dedicated pages
- Verify streams are legal in your jurisdiction

### Copyright Concerns

**Issue:** Uncertain about streaming rights.

**Recommendation:**
- TopEmbed aggregates third-party streams (may include copyrighted content)
- **You are responsible** for ensuring you have rights to display content
- Check local laws regarding streaming and embedding
- Consider consulting a lawyer if hosting commercially

---

## Need More Help?

- 📧 Contact: Create an issue on GitHub
- 📚 Docs: [WEEBLY-SETUP.md](WEEBLY-SETUP.md), [QUICKSTART.md](QUICKSTART.md)
- 🔍 Search: Check closed issues for solutions

