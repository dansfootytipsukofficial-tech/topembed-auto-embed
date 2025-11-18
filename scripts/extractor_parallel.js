#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const argv = require('minimist')(process.argv.slice(2));

const inputPath = argv.input || 'embed/channels.json';
const outputPath = argv.output || 'embed/channels.resolved.json';
const concurrency = Math.max(1, parseInt(argv.concurrency || argv.c || 4, 10));
console.log('Using concurrency =', concurrency);

async function extract() {
  if (!fs.existsSync(inputPath)) {
    console.error('Input channels file not found:', inputPath);
    process.exit(1);
  }
  const raw = fs.readFileSync(inputPath, 'utf8');
  let channels;
  try {
    const j = JSON.parse(raw);
    channels = j.channels || j;
  } catch (e) {
    console.error('Failed to parse input JSON', e.message);
    process.exit(1);
  }

  const browser = await puppeteer.launch({args: ['--no-sandbox','--disable-setuid-sandbox']});
  const results = [];

  async function processChannel(ch) {
    const url = typeof ch === 'string' ? ch : ch.url || ch.page || ch.link || ch.channel || ch;
    console.log('Processing', url);
    const page = await browser.newPage();
    const found = new Set();
    try {
      page.on('requestfinished', (req) => {
        try {
          const rurl = req.url();
          if (/\.m3u8(\?|$)/i.test(rurl) || /\.mp4(\?|$)/i.test(rurl)) {
            found.add(rurl);
          }
        } catch (e) {}
      });

      page.on('response', (res) => {
        try {
          const ct = res.headers()['content-type'] || '';
          const rurl = res.url();
          if (/mpegurl|application\/vnd\.apple\.mpegurl|vnd\.apple\.mpegurl/i.test(ct)) {
            found.add(rurl);
          }
        } catch (e) {}
      });

      await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36');
      try {
        await page.goto(url, {waitUntil: 'networkidle2', timeout: 30000});
        await page.waitForTimeout(3000);
      } catch (e) {
        console.warn('Page load failed for', url, e.message);
      }

      try {
        const pageText = await page.content();
        const m3u8match = pageText.match(/https?:\/\/[^"'<>\s]+\.m3u8/gi) || pageText.match(/https?:\/\/[^"'<>\s]+(\/playlist|\/manifest)[^"'<>\s]*/gi);
        if (m3u8match) m3u8match.forEach(u => found.add(u));
      } catch (e) {}

      const foundArr = Array.from(found);
      console.log(' Found', foundArr.length, 'streams for', url);
      return {page: url, streams: foundArr};
    } finally {
      try { await page.close(); } catch(e){}
    }
  }

  const queue = channels.slice();
  const workers = new Array(concurrency).fill(0).map(async () => {
    while (queue.length) {
      const ch = queue.shift();
      if (!ch) break;
      const res = await processChannel(ch);
      results.push(res);
    }
  });

  try {
    await Promise.all(workers);
  } finally {
    try { await browser.close(); } catch(e){}
  }

  const out = {generated_at: new Date().toISOString(), channels: results};
  fs.mkdirSync(path.dirname(outputPath), {recursive: true});
  fs.writeFileSync(outputPath, JSON.stringify(out, null, 2));
  console.log('Wrote', outputPath);
}

extract().catch(err => {
  console.error(err);
  process.exit(1);
});
