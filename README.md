# 🎵 Spotify to Apple Music Migration Tool

A **completely free** playlist migration tool that moves your Spotify playlists to Apple Music without requiring:
- ❌ Spotify Premium account
- ❌ Spotify API keys
- ❌ Apple Developer account
- ❌ Any third-party services

## ✨ Features

- **Zero Cost**: Uses public APIs and browser automation instead of paid developer accounts
- **No API Keys Required**: Scrapes Spotify embed pages and uses iTunes Search API
- **Browser Automation**: Uses Playwright to automatically add tracks to your Apple Music library
- **Progress Tracking**: Real-time progress updates and detailed logs
- **Error Handling**: Graceful handling of missing tracks and rate limiting
- **Logging**: Saves success and failure reports for review

## 🚀 Quick Start

### Prerequisites

- macOS (tested on macOS Sonoma/Sequoia)
- Python 3.8 or higher
- Active Apple Music subscription
- Google Chrome or Chromium browser

### Installation

1. **Clone or download this repository**:
   ```bash
   cd /Users/srimaan/Projects/spotify-to-apple-music
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

### Usage

1. **Get your Spotify playlist URL**:
   - Open Spotify (web or desktop app)
   - Click the "..." menu on any playlist
   - Select "Share" → "Copy Playlist Link"

2. **Run the migration tool**:
   ```bash
   python main.py
   ```

3. **Follow the prompts**:
   - Paste your Spotify playlist URL
   - Wait for track matching (2-3 seconds per track)
   - Log in to Apple Music when the browser opens
   - Press Enter to start adding tracks

4. **Watch the magic happen** ✨
   - The browser will automatically navigate to each track
   - Click the "Add to Library" button
   - Continue until all tracks are processed

5. **Review the results**:
   - Check `success_log.txt` for successfully added tracks
   - Check `failed_tracks.txt` for tracks that couldn't be added

## 📁 Project Structure

```
spotify-to-apple-music/
├── main.py              # Main entry point
├── scraper.py           # Spotify scraping & iTunes API search
├── browser.py           # Playwright browser automation
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── success_log.txt      # Generated: successful migrations
└── failed_tracks.txt    # Generated: failed migrations
```

## 🔧 Configuration

Edit `config.py` to customize behavior:

```python
# Browser settings
HEADLESS_MODE = False        # Set to True to run browser in background
SLOW_MO_MS = 100            # Slow down browser actions (debugging)

# Rate limiting
DELAY_BETWEEN_REQUESTS = 2  # Seconds between iTunes API calls
DELAY_BETWEEN_ADDS = 3      # Seconds between adding tracks

# Output files
FAILED_TRACKS_FILE = "failed_tracks.txt"
SUCCESS_LOG_FILE = "success_log.txt"
```

## 🐛 Troubleshooting

### "Could not find 'Add to Library' button"

**Problem**: Apple Music changed their UI.

**Solution**: 
1. Open the track URL manually in your browser
2. Inspect the "Add" button to find the correct selector
3. Update the `add_track_to_library()` function in `browser.py`

### "Failed to fetch Spotify embed page"

**Problem**: Spotify may have changed their embed page structure.

**Solution**:
1. Visit the embed URL manually: `https://open.spotify.com/embed/playlist/{ID}`
2. Check if the `__NEXT_DATA__` script tag still exists
3. Update the JSON path in `scraper.py`

### Rate Limiting (403 Errors)

**Problem**: Too many requests to Apple Music or iTunes API.

**Solution**:
```python
# In config.py, increase delays:
DELAY_BETWEEN_REQUESTS = 5  # Increased from 2
DELAY_BETWEEN_ADDS = 10     # Increased from 3
```

### Browser Login Issues

**Problem**: Can't log in to Apple Music.

**Solution**:
1. Make sure you have an active Apple Music subscription
2. Try logging in manually first at music.apple.com
3. Use a different browser profile

## 🎯 How It Works

### 1. Spotify Scraping (No API Required)

Instead of using Spotify's Web API (which requires Premium and OAuth), we:
- Access the public Spotify embed page: `https://open.spotify.com/embed/playlist/{ID}`
- Extract the hidden `__NEXT_DATA__` JSON object
- Parse the track list directly from the page

### 2. Apple Music Search (No Developer Account)

Instead of using MusicKit (which requires a $99/year Apple Developer account), we:
- Use the public iTunes Search API: `https://itunes.apple.com/search`
- Search by artist + track name
- Get the Apple Music web URL for matched tracks

### 3. Library Addition (Browser Automation)

Instead of using Apple Music's API (which requires developer tokens), we:
- Launch a Chromium browser using Playwright
- Navigate to each track's Apple Music page
- Click the "Add to Library" button automatically
- Verify the track was added successfully

## ⚠️ Limitations

- **Match Accuracy**: Uses artist + title matching, not ISRC codes. May occasionally match wrong versions (remasters, live versions, etc.)
- **Speed**: Takes 2-3 seconds per track due to rate limiting
- **Manual Login**: Requires you to log in to Apple Music once per session
- **Browser Required**: Must keep the browser window open during migration

## 🔄 Alternative Methods

If this tool doesn't work for your use case, consider:

1. **SongShift** (iOS app) - Paid, but very reliable
2. **TuneMyMusic** (web) - Free tier with limitations
3. **Soundiiz** (web) - Paid service with extensive features
4. **Apple Shortcuts** - Native macOS automation (limited to local library)

## 🤝 Contributing

This is a personal project, but feel free to:
- Fork and modify for your needs
- Submit issues if you find bugs
- Share improvements to the browser selectors

## 📝 License

This project is released under the MIT License. Use at your own risk.

## 🙏 Credits

- **Playwright**: https://playwright.dev/
- **iTunes Search API**: https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/
- **Spotify Embed**: Public feature by Spotify

## 💡 Tips

1. **Test with a small playlist first** - Create a test playlist with 5-10 songs
2. **Run during off-peak hours** - Less likely to hit rate limits
3. **Keep your computer awake** - Use `caffeinate` on macOS to prevent sleep
4. **Backup your library** - Though unlikely, always have a backup plan

## 📊 Performance

- **Matching Speed**: ~2-3 seconds per track
- **Addition Speed**: ~3-5 seconds per track (includes browser navigation)
- **Success Rate**: ~85-95% (depending on catalog availability)
- **Large Playlists**: For 500+ tracks, consider running overnight

---

**Made with ❤️ for music lovers who want freedom from vendor lock-in**
