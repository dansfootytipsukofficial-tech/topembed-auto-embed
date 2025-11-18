Extractor and CI

This project includes a Puppeteer-based extractor that renders TopEmbed channel pages and captures final HLS stream URLs.

Run locally (macOS / zsh)

1) Install Node.js (Homebrew recommended):

   brew update
   brew install node

2) Install project deps and run dry run (5 pages):

   cd /Users/daniel/Downloads/topembed-auto-embed
   npm ci
   # dry-run: limit 5
   node scripts/extractor.js --input embed/channels.json --output embed/channels.resolved.json --concurrency 4 --limit 5

3) Full run:

   node scripts/extractor.js --input embed/channels.json --output embed/channels.resolved.json --concurrency 4

CI / GitHub Actions

A workflow is added at `.github/workflows/extractor.yml`. It runs on-demand (Actions → Run workflow) and nightly at 02:00 UTC.

If the extractor produces changes, the workflow opens a pull request `update/channels-resolved` with the updated `embed/channels.resolved.json` so you can review before merging.

Notes
- First run downloads Chromium (puppeteer) and may take a few minutes.
- If many channels fail to resolve, consider increasing timeouts or adding targeted token handling.
