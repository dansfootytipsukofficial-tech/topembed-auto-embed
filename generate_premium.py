#!/usr/bin/env python3
"""Generate a premium streaming platform UI from topembed API.

This enhanced version includes:
- Modern, professional UI design
- Search and filter functionality
- Category organization
- Responsive grid layout
- Dark theme optimized for streaming
- Favorites/recently watched (localStorage)
- Better player controls
- Live status indicators

Usage: python generate_premium.py --output out --limit 200
"""
import argparse
import json
import os
import re
from urllib.parse import unquote
from collections import defaultdict

import requests

API_URL = "https://topembed.pw/api.php?format=json"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>StreamHub - Live Sports, Movies & TV</title>
<style>
:root {
  --primary: #e50914;
  --primary-dark: #b20710;
  --bg-dark: #0a0a0a;
  --bg-card: #1a1a1a;
  --bg-hover: #2a2a2a;
  --text: #ffffff;
  --text-muted: #999999;
  --border: #333333;
  --accent: #0a84ff;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--bg-dark);
  color: var(--text);
  line-height: 1.6;
}

/* Header */
.header {
  background: linear-gradient(to bottom, rgba(10,10,10,0.95), rgba(10,10,10,0.9));
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 1px solid var(--border);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.logo {
  font-size: 1.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary) 0%, #ff6b6b 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

.search-bar {
  flex: 1;
  max-width: 500px;
  position: relative;
}

.search-bar input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 0.95rem;
  transition: all 0.3s;
}

.search-bar input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(229, 9, 20, 0.1);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}

.header-stats {
  display: flex;
  gap: 1.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-number {
  color: var(--primary);
  font-weight: 700;
  font-size: 1.1rem;
}

/* Filters */
.filters {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem 2rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.filter-btn {
  padding: 0.6rem 1.2rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  font-weight: 500;
}

.filter-btn:hover {
  background: var(--bg-hover);
  border-color: var(--primary);
}

.filter-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

/* Player Section */
.player-section {
  position: sticky;
  top: 72px;
  background: #000;
  z-index: 999;
  border-bottom: 2px solid var(--primary);
}

.player-container {
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
}

.player-wrapper {
  position: relative;
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
  background: #000;
}

.player-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.player-info {
  padding: 1rem 2rem;
  background: linear-gradient(to bottom, rgba(0,0,0,0.9), rgba(0,0,0,0.7));
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.now-playing {
  font-size: 1.2rem;
  font-weight: 600;
}

.player-controls {
  display: flex;
  gap: 1rem;
}

.control-btn {
  padding: 0.5rem 1rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s;
}

.control-btn:hover {
  background: var(--primary);
  border-color: var(--primary);
}

.player-placeholder {
  padding: 3rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
}

.player-placeholder h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text-muted);
}

/* Content Grid */
.content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.category-section {
  margin-bottom: 3rem;
}

.category-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  padding-left: 0.5rem;
  border-left: 4px solid var(--primary);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.channel-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
  position: relative;
}

.channel-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(229, 9, 20, 0.3);
  border-color: var(--primary);
}

.channel-card-header {
  padding: 1rem;
  background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-hover) 100%);
  border-bottom: 1px solid var(--border);
}

.channel-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.channel-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: var(--text-muted);
}

.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  animation: pulse 2s infinite;
  margin-right: 0.5rem;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.channel-card-body {
  padding: 1rem;
}

.channel-actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: scale(1.02);
}

.btn-secondary {
  background: var(--bg-hover);
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background: var(--border);
}

.favorite-btn {
  width: 40px;
  height: 40px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  background: var(--bg-hover);
  border: 1px solid var(--border);
}

.favorite-btn.active {
  color: var(--primary);
}

/* Empty States */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-muted);
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

/* Footer */
.footer {
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  padding: 2rem;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-top: 4rem;
}

/* Responsive */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-bar {
    max-width: 100%;
  }
  
  .filters {
    padding: 1rem;
  }
  
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
  }
  
  .content {
    padding: 1rem;
  }
}

/* Loading Spinner */
.spinner {
  border: 3px solid var(--border);
  border-top: 3px solid var(--primary);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 2rem auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
</head>
<body>

<!-- Header -->
<header class="header">
  <div class="header-content">
    <div class="logo">🎬 StreamHub</div>
    <div class="search-bar">
      <span class="search-icon">🔍</span>
      <input type="text" id="searchInput" placeholder="Search channels, sports, movies...">
    </div>
    <div class="header-stats">
      <div class="stat">
        <span class="stat-number" id="channelCount">0</span>
        <span>Channels</span>
      </div>
      <div class="stat">
        <span class="stat-number" id="liveCount">0</span>
        <span>🔴 Live</span>
      </div>
    </div>
  </div>
</header>

<!-- Filters -->
<div class="filters">
  <button class="filter-btn active" data-filter="all">All Channels</button>
  <button class="filter-btn" data-filter="sports">⚽ Sports</button>
  <button class="filter-btn" data-filter="movies">🎬 Movies</button>
  <button class="filter-btn" data-filter="tv">📺 TV Shows</button>
  <button class="filter-btn" data-filter="news">📰 News</button>
  <button class="filter-btn" data-filter="favorites">⭐ Favorites</button>
  <button class="filter-btn" data-filter="recent">🕐 Recently Watched</button>
</div>

<!-- Player Section -->
<div class="player-section" id="playerSection" style="display:none;">
  <div class="player-container">
    <div class="player-wrapper" id="playerWrapper">
      <div class="player-placeholder">
        <h3>Select a channel to start streaming</h3>
        <p>Click any channel card below to watch</p>
      </div>
    </div>
    <div class="player-info" id="playerInfo" style="display:none;">
      <div class="now-playing" id="nowPlaying">Now Playing: Channel Name</div>
      <div class="player-controls">
        <button class="control-btn" onclick="closePlayer()">✕ Close</button>
        <button class="control-btn" onclick="toggleFavorite()">⭐ Favorite</button>
      </div>
    </div>
  </div>
</div>

<!-- Content Grid -->
<div class="content">
  <div id="contentContainer"></div>
  
  <div id="emptyState" class="empty-state" style="display:none;">
    <h3>No channels found</h3>
    <p>Try adjusting your search or filter</p>
  </div>
</div>

<!-- Footer -->
<footer class="footer">
  <p>StreamHub - Automated Streaming Platform</p>
  <p style="margin-top:0.5rem;font-size:0.75rem;">Content provided by third-party sources. Ensure you have appropriate rights to view.</p>
</footer>

<script>
// Channel data
const CHANNELS = {{ CHANNELS_JSON }};

// State
let currentChannel = null;
let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
let recentlyWatched = JSON.parse(localStorage.getItem('recentlyWatched') || '[]');
let currentFilter = 'all';
let searchQuery = '';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  updateStats();
  renderChannels();
  setupEventListeners();
});

function setupEventListeners() {
  // Search
  document.getElementById('searchInput').addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase();
    renderChannels();
  });
  
  // Filters
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      currentFilter = e.target.dataset.filter;
      renderChannels();
    });
  });
}

function categorizeChannel(label) {
  const lower = label.toLowerCase();
  
  // Sports
  if (/(espn|sport|football|soccer|nfl|nba|mlb|nhl|cricket|tennis|f1|racing|fox sports|sky sports|bt sport|bein)/i.test(label)) {
    return 'sports';
  }
  
  // News
  if (/(news|cnn|bbc|fox news|msnbc|sky news|al jazeera)/i.test(label)) {
    return 'news';
  }
  
  // Movies
  if (/(hbo|cinema|movie|film|showtime|starz)/i.test(label)) {
    return 'movies';
  }
  
  // TV
  return 'tv';
}

function filterChannels() {
  let filtered = CHANNELS;
  
  // Apply category filter
  if (currentFilter === 'favorites') {
    filtered = CHANNELS.filter(ch => favorites.includes(ch.url));
  } else if (currentFilter === 'recent') {
    filtered = CHANNELS.filter(ch => recentlyWatched.includes(ch.url));
  } else if (currentFilter !== 'all') {
    filtered = CHANNELS.filter(ch => categorizeChannel(ch.label) === currentFilter);
  }
  
  // Apply search
  if (searchQuery) {
    filtered = filtered.filter(ch => 
      ch.label.toLowerCase().includes(searchQuery)
    );
  }
  
  return filtered;
}

function renderChannels() {
  const container = document.getElementById('contentContainer');
  const emptyState = document.getElementById('emptyState');
  const filtered = filterChannels();
  
  if (filtered.length === 0) {
    container.innerHTML = '';
    emptyState.style.display = 'block';
    return;
  }
  
  emptyState.style.display = 'none';
  
  // Group by category
  const grouped = {};
  filtered.forEach(ch => {
    const cat = categorizeChannel(ch.label);
    if (!grouped[cat]) grouped[cat] = [];
    grouped[cat].push(ch);
  });
  
  const categoryNames = {
    sports: '⚽ Sports Channels',
    movies: '🎬 Movies & Entertainment',
    tv: '📺 TV Channels',
    news: '📰 News Channels'
  };
  
  let html = '';
  
  // If filtered by category or search, don't group
  if (currentFilter !== 'all' || searchQuery) {
    html += '<div class="category-section"><div class="grid">';
    filtered.forEach(ch => {
      html += renderChannelCard(ch);
    });
    html += '</div></div>';
  } else {
    // Group by category
    Object.keys(grouped).forEach(cat => {
      html += `
        <div class="category-section">
          <h2 class="category-title">${categoryNames[cat] || cat}</h2>
          <div class="grid">
            ${grouped[cat].map(ch => renderChannelCard(ch)).join('')}
          </div>
        </div>
      `;
    });
  }
  
  container.innerHTML = html;
}

function renderChannelCard(channel) {
  const isFavorite = favorites.includes(channel.url);
  const category = categorizeChannel(channel.label);
  
  return `
    <div class="channel-card" data-url="${channel.url}">
      <div class="channel-card-header">
        <div class="channel-title">${channel.label}</div>
        <div class="channel-meta">
          <span><span class="status-indicator"></span>Live</span>
          <span>${category.toUpperCase()}</span>
        </div>
      </div>
      <div class="channel-card-body">
        <div class="channel-actions">
          <button class="btn btn-primary" onclick="playChannel('${channel.url.replace(/'/g, "\\'")}', '${channel.label.replace(/'/g, "\\'")}')">
            ▶ Watch Now
          </button>
          <button class="favorite-btn ${isFavorite ? 'active' : ''}" onclick="toggleChannelFavorite('${channel.url.replace(/'/g, "\\'")}', event)">
            ${isFavorite ? '⭐' : '☆'}
          </button>
        </div>
      </div>
    </div>
  `;
}

function playChannel(url, label) {
  currentChannel = { url, label };
  
  // Add to recently watched
  if (!recentlyWatched.includes(url)) {
    recentlyWatched.unshift(url);
    if (recentlyWatched.length > 20) recentlyWatched.pop();
    localStorage.setItem('recentlyWatched', JSON.stringify(recentlyWatched));
  }
  
  // Show player section
  const playerSection = document.getElementById('playerSection');
  const playerWrapper = document.getElementById('playerWrapper');
  const playerInfo = document.getElementById('playerInfo');
  const nowPlaying = document.getElementById('nowPlaying');
  
  playerSection.style.display = 'block';
  playerInfo.style.display = 'flex';
  nowPlaying.textContent = `Now Playing: ${label}`;
  
  // Create iframe
  playerWrapper.innerHTML = `
    <iframe 
      src="${url}" 
      allowfullscreen 
      allow="autoplay; fullscreen; picture-in-picture"
      loading="eager">
    </iframe>
  `;
  
  // Scroll to player
  playerSection.scrollIntoView({ behavior: 'smooth' });
}

function closePlayer() {
  const playerSection = document.getElementById('playerSection');
  playerSection.style.display = 'none';
  currentChannel = null;
}

function toggleFavorite() {
  if (!currentChannel) return;
  toggleChannelFavorite(currentChannel.url);
}

function toggleChannelFavorite(url, event) {
  if (event) event.stopPropagation();
  
  const index = favorites.indexOf(url);
  if (index > -1) {
    favorites.splice(index, 1);
  } else {
    favorites.push(url);
  }
  localStorage.setItem('favorites', JSON.stringify(favorites));
  renderChannels();
}

function updateStats() {
  document.getElementById('channelCount').textContent = CHANNELS.length;
  document.getElementById('liveCount').textContent = CHANNELS.length;
}
</script>

</body>
</html>
"""


def safe_channel_label(url):
    """Extract a readable label from URL."""
    try:
        if url.startswith('https'):
            clean = url.replace('\\/', '/')
            label = clean.split('/')[-1]
            label = unquote(label)
            label = label.replace('+', ' ').replace('%20', ' ')
            return label
    except Exception:
        pass
    return url


def fetch_channels(limit=200):
    """Fetch channels from TopEmbed API."""
    print(f'Fetching channels from {API_URL}...')
    try:
        r = requests.get(API_URL, timeout=15)
        r.raise_for_status()
        data = r.json()
        channels = []
        seen = set()
        events = data.get('events', {})
        
        for day, items in events.items():
            for ev in items:
                for c in ev.get('channels', []) or []:
                    src = c.replace('\\/', '/')
                    if src not in seen:
                        seen.add(src)
                        label = safe_channel_label(src)
                        channels.append({'url': src, 'label': label})
                        if len(channels) >= limit:
                            return channels
        
        print(f'Fetched {len(channels)} channels')
        return channels
    except Exception as e:
        print(f'Error fetching channels: {e}')
        return []


def load_channels_from_file(path, limit=200):
    """Load channels from JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        
        if isinstance(data, dict) and 'channels' in data:
            urls = data['channels']
        elif isinstance(data, list):
            urls = data
        else:
            return []
        
        channels = []
        for url in urls[:limit]:
            if isinstance(url, str):
                label = safe_channel_label(url)
                channels.append({'url': url, 'label': label})
            elif isinstance(url, dict):
                channels.append(url)
        
        return channels
    except Exception as e:
        print(f'Error loading channels from file: {e}')
        return []


def build_html(channels, outpath):
    """Generate the premium HTML interface."""
    print(f'Building premium HTML with {len(channels)} channels...')
    
    # Prepare channel data for JavaScript
    channels_json = json.dumps(channels, indent=2)
    
    # Replace placeholder in template
    html = HTML_TEMPLATE.replace('{{ CHANNELS_JSON }}', channels_json)
    
    # Write files
    os.makedirs(outpath, exist_ok=True)
    
    # Write HTML
    html_path = os.path.join(outpath, 'index.html')
    with open(html_path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print(f'✓ Wrote {html_path}')
    
    # Write JSON
    json_path = os.path.join(outpath, 'channels.json')
    with open(json_path, 'w', encoding='utf-8') as fh:
        json.dump({'channels': [ch['url'] for ch in channels]}, fh, indent=2)
    print(f'✓ Wrote {json_path}')
    
    print(f'\n✨ Premium streaming platform generated successfully!')
    print(f'📂 Output directory: {outpath}')
    print(f'🎬 {len(channels)} channels available')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate premium streaming platform UI')
    parser.add_argument('--output', '-o', default='out', help='Output directory')
    parser.add_argument('--limit', '-n', type=int, default=200, help='Max channels to include')
    parser.add_argument('--input-channels', '-i', help='JSON file with channels list (overrides API fetch)')
    
    args = parser.parse_args()
    
    if args.input_channels:
        channels = load_channels_from_file(args.input_channels, limit=args.limit)
    else:
        channels = fetch_channels(limit=args.limit)
    
    if channels:
        build_html(channels, args.output)
    else:
        print('❌ No channels to process')
        exit(1)
