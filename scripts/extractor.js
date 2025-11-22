#!/usr/bin/env node
// Consolidated extractor: single declaration of argv and a single extract implementation.

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const argv = require('minimist')(process.argv.slice(2));

const inputPath = argv.input || 'embed/channels.json';
const outputPath = argv.output || 'embed/channels.resolved.json';
const concurrency = Math.max(1, parseInt(argv.concurrency || argv.c || '4', 10));

const USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36';

// global error handlers -> write to debug log for CI inspection
process.on('unhandledRejection', (reason) => {
  try { fs.appendFileSync('debug/extractor.log', `[UNHANDLED REJECTION] ${new Date().toISOString()} ${reason && reason.stack ? reason.stack : reason}\n`); } catch (e) { }
  console.error('UnhandledRejection', reason);
});
process.on('uncaughtException', (err) => {
  try { fs.appendFileSync('debug/extractor.log', `[UNCAUGHT EXCEPTION] ${new Date().toISOString()} ${err && err.stack ? err.stack : err}\n`); } catch (e) { }
  console.error('UncaughtException', err && err.stack ? err.stack : err);
  process.exit(1);
});

// small helper to write to debug log in a consistent, synchronous way
function writeDebug(line) {
  try {
    fs.mkdirSync('debug', { recursive: true });
  } catch (e) { }
  try { fs.appendFileSync('debug/extractor.log', `${line}\n`); } catch (e) { console.error('Failed to write debug log', e && e.message ? e.message : e); }
}

// ensure we always write an exit footer so artifacts are easier to reason about
process.on('exit', (code) => {
  try { fs.appendFileSync('debug/extractor.log', `=== exit ${new Date().toISOString()} code=${code} ===\n`); } catch (e) { }
});

async function processChannel(browser, ch) {
  const url = typeof ch === 'string' ? ch : ch.url || ch.page || ch.link || ch.channel || ch;
  const page = await browser.newPage();
  // set sensible timeouts for navigation and operations
  page.setDefaultNavigationTimeout(90000);
  page.setDefaultTimeout(90000);
  // forward page console messages to our stdout (and debug file)
  page.on('console', msg => {
    try {
      const text = msg.text ? msg.text() : String(msg);
      console.log('[page console]', text);
      try { fs.appendFileSync('debug/extractor.log', `[PAGE CONSOLE] ${new Date().toISOString()} ${text}\n`); } catch (e) { /* ignore */ }
    } catch (e) { }
  });
  const found = new Set();
  // collect async response parsing promises so we can await them before finishing
  const responseParsers = [];

  // capture requests and responses for media URLs
  page.on('requestfinished', (req) => {
    try {
      const rurl = req.url();
      if (/\.m3u8(\?|$)/i.test(rurl) || /\.mp4(\?|$)/i.test(rurl)) found.add(rurl);
    } catch (e) { /* ignore */ }
  });

  page.on('response', (res) => {
    try {
      const headers = res.headers ? res.headers() : {};
      const ct = (headers['content-type'] || headers['Content-Type'] || '');
      const rurl = res.url();
      // immediate matches
      if (/\.m3u8(\?|$)/i.test(rurl) || /mpegurl|application\/vnd\.apple\.mpegurl|vnd\.apple\.mpegurl/i.test(ct)) {
        found.add(rurl);
      }

      // if response looks textual or is small, try to read it and scan for playlists
      if (/text|json|xml|mpegurl|application\/vnd\.apple\.mpegurl/i.test(ct) || /\.m3u8(\?|$)/i.test(rurl)) {
        const p = res.text().then(txt => {
          try {
            const matches = (txt.match(/https?:\/\/[^"'<>\\s]+\.m3u8/gi) || txt.match(/https?:\/\/[^"'<>\\s]+(\/playlist|\/manifest)[^"'<>\\s]*/gi) || []);
            matches.forEach(u => found.add(u));
          } catch (e) { /* ignore parse */ }
        }).catch(() => {});
        responseParsers.push(p);
      }
    } catch (e) { /* ignore */ }
  });

    try {
      // best-effort: set UA, then load page and capture content
      try {
        await page.setUserAgent(USER_AGENT);
      } catch (e) {
        console.warn('Page setup failed for', url, e && e.message ? e.message : e);
        try { fs.appendFileSync('debug/extractor.log', `[PAGE SETUP ERROR] ${new Date().toISOString()} ${url} ${e && e.stack ? e.stack : e}\n`); } catch (ee) { }
      }

      try {
        // navigate and wait for a reasonably quiet network state
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 90000 });
        // allow additional time for JS-driven manifest assembly
        await page.waitForTimeout(8000);
        // sometimes pages keep sockets open; a short extra idle helps
        await page.waitForNetworkIdle({ idleTime: 2000, timeout: 5000 }).catch(() => {});
      } catch (e) {
        console.warn('Page load failed for', url, e && e.message ? e.message : e);
        try { fs.appendFileSync('debug/extractor.log', `[PAGE LOAD ERROR] ${new Date().toISOString()} ${url} ${e && e.stack ? e.stack : e}\n`); } catch (ee) { }
      }

      try {
        const pageText = await page.content();
        const m3u8match = (pageText.match(/https?:\/\/[^"'<\>\s]+\.m3u8/gi)
          || pageText.match(/https?:\/\/[^"'<\>\s]+(\/playlist|\/manifest)[^"'<\>\s]*/gi)
          || []);
        m3u8match.forEach(u => found.add(u));
      } catch (e) {
        // ignore content parse errors
      }

      // wait for any response parsing to finish (from response handlers)
      try { await Promise.all(responseParsers); } catch (e) { /* ignore */ }

      // last attempt: try to inspect common JS variables that players expose
      try {
        const extra = await page.evaluate(() => {
          try {
            // common Hls.js instance heuristics
            if (window.hls && window.hls.config) return window.hls.config && window.hls.url ? window.hls.url : null;
            // look for source tags
            const vid = document.querySelector('video');
            if (vid && vid.currentSrc) return vid.currentSrc;
          } catch (e) { }
          return null;
        });
        if (extra && typeof extra === 'string') found.add(extra);
      } catch (e) { }

      return { page: url, streams: Array.from(found) };
    } finally {
      try { await page.close(); } catch (e) { /* ignore */ }
    }
}

async function extract() {
  let channels = [];
  if (!fs.existsSync(inputPath)) {
    console.warn('Input channels file not found, continuing with empty channels list:', inputPath);
  } else {
    const raw = fs.readFileSync(inputPath, 'utf8');
    try {
      const j = JSON.parse(raw);
      channels = j.channels || j;
    } catch (e) {
      console.warn('Failed to parse input JSON, continuing with empty channels list', e && e.message ? e.message : e);
      channels = [];
    }
  }

  console.log('Channels to process:', Array.isArray(channels) ? channels.length : 0, 'concurrency =', concurrency);
  // ensure debug folder exists and write an initial run header
  writeDebug(`\n=== run at ${new Date().toISOString()} ===`);
  writeDebug(`Channels to process: ${Array.isArray(channels) ? channels.length : 0} concurrency=${concurrency}`);

  // Puppeteer launch with retries and CI-friendly flags
  async function launchBrowserWithRetries(retries = 3) {
    let lastErr = null;
    for (let i = 0; i < retries; i++) {
      try {
        const launchOpts = { args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'], timeout: 120000 };
        // allow overriding executable path via env (for CI that caches Chrome)
        if (process.env.PUPPETEER_EXECUTABLE_PATH) launchOpts.executablePath = process.env.PUPPETEER_EXECUTABLE_PATH;
        const b = await puppeteer.launch(launchOpts);
        try { fs.appendFileSync('debug/extractor.log', `[BROWSER] launched attempt=${i + 1}\n`); } catch (e) { }
        return b;
      } catch (err) {
        lastErr = err;
        console.warn('Puppeteer launch attempt', i + 1, 'failed:', err && err.message ? err.message : err);
        try { fs.appendFileSync('debug/extractor.log', `[BROWSER ERROR] attempt=${i + 1} ${err && err.stack ? err.stack : err}\n`); } catch (e) { }
        // small backoff
        await new Promise(r => setTimeout(r, 2000 * (i + 1)));
      }
    }
    throw lastErr;
  }

  const browser = await launchBrowserWithRetries(3);
  const results = [];

  try {
    const queue = channels.slice();
    const workers = new Array(concurrency).fill(0).map(async () => {
      while (true) {
        const ch = queue.shift();
        if (!ch) break;
        try {
          const res = await processChannel(browser, ch);
          console.log(' Found', res.streams.length, 'for', res.page);
          // Write per-channel findings to debug so artifacts contain progress
          writeDebug(`[CHANNEL] ${res.page} found=${res.streams.length}`);
          if (res.streams && res.streams.length) writeDebug(`[CHANNEL STREAMS] ${res.page} ${res.streams.join(' | ')}`);
          results.push(res);
        } catch (err) {
          console.warn('Channel error', err && err.message ? err.message : err);
          writeDebug(`[CHANNEL ERROR] ${(typeof ch === 'string' ? ch : ch.url || ch.page)} ${err && err.stack ? err.stack : err}`);
          results.push({ page: (typeof ch === 'string' ? ch : ch.url || ch.page), streams: [] });
        }
      }
    });

    await Promise.all(workers);
  } finally {
    try { await browser.close(); } catch (e) { /* ignore */ }
  }

  const out = { generated_at: new Date().toISOString(), channels: results };
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, JSON.stringify(out, null, 2));
  console.log('Wrote', outputPath);
  writeDebug(`Wrote ${outputPath} channels=${results.length}`);
}

extract().catch(err => {
  console.error(err && err.stack ? err.stack : err);
  process.exit(1);
});
