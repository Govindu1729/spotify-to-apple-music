# 🚀 Quick Start Guide

## First Time Setup (One-Time)

```bash
# 1. Navigate to the project
cd /Users/srimaan/Projects/spotify-to-apple-music

# 2. Run the setup script (creates virtual environment and installs dependencies)
chmod +x setup.sh
./setup.sh
```

## Running the Tool (Every Time)

```bash
# 1. Navigate to the project
cd /Users/srimaan/Projects/spotify-to-apple-music

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Run the migration tool
python main.py

# 4. When done, deactivate
deactivate
```

## Example Session

```
======================================================================
🎵 Spotify to Apple Music Migration Tool
======================================================================

This tool will:
  1. Scrape your Spotify playlist (no API key required)
  2. Match tracks to Apple Music catalog (no dev account required)
  3. Add matched tracks to your Apple Music library (browser automation)

======================================================================

📋 Enter Spotify playlist URL: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M

🎵 Scraping Spotify playlist: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
✅ Found 50 tracks in Spotify playlist

🔍 Matching 50 tracks to Apple Music...
  Progress: 10/50
  Progress: 20/50
  Progress: 30/50
  Progress: 40/50
  Progress: 50/50

✅ Successfully matched: 47 tracks
❌ Failed to match: 3 tracks

🎯 Ready to add 47 tracks to Apple Music

⚠️  This will open a browser window. Continue? (y/n): y

🌐 Opening Apple Music web player...

======================================================================
🔐 PLEASE LOG IN TO APPLE MUSIC
======================================================================
1. Sign in with your Apple ID in the browser window
2. Make sure you have an active Apple Music subscription
3. After logging in, return to this terminal
======================================================================

⏎  Press ENTER once you are logged in and ready to continue...

[1/47] Adding: Blinding Lights - The Weeknd
  ✅ Successfully added to library

[2/47] Adding: Levitating - Dua Lipa
  ✅ Successfully added to library

... (continues for all tracks) ...

======================================================================
📊 MIGRATION SUMMARY
======================================================================
✅ Successfully added: 45 tracks
❌ Failed to add: 2 tracks
⚠️  Not found in Apple Music: 3 tracks
======================================================================

🎉 Migration complete!
```

## Getting Spotify Playlist URLs

### From Spotify Web Player
1. Go to open.spotify.com
2. Click on a playlist
3. Click the "..." (three dots) button
4. Click "Share"
5. Click "Copy Playlist Link"

### From Spotify Desktop App
1. Right-click on a playlist
2. Hover over "Share"
3. Click "Copy Playlist Link"

### From Spotify Mobile App
1. Tap on a playlist
2. Tap the "..." button
3. Tap "Share"
4. Tap "Copy Link"

## Common Issues

### "Command not found: python3"
- Install Python from python.org or use Homebrew: `brew install python3`

### "playwright: command not found"
- Make sure you activated the virtual environment: `source venv/bin/activate`

### "No module named 'playwright'"
- Reinstall: `pip install playwright && playwright install chromium`

### Browser won't open
- Check that Chrome/Chromium is installed
- Try running: `playwright install chromium`

## Tips for Large Playlists (100+ tracks)

1. **Run overnight**: These playlists can take 10-20 minutes
   ```bash
   python main.py  # Then leave it running
   ```

2. **Prevent sleep** (macOS):
   ```bash
   caffeinate -i python main.py
   ```

3. **Run in headless mode** (no browser window):
   - Edit `config.py` and set `HEADLESS_MODE = True`
   - You'll need to be already logged in to Apple Music

## Output Files

After each run, check these files:

- **`success_log.txt`**: List of all successfully added tracks with Apple Music URLs
- **`failed_tracks.txt`**: List of tracks that couldn't be added (for manual review)

## Uninstalling

```bash
# Remove the project folder
cd /Users/srimaan/Projects
rm -rf spotify-to-apple-music

# Remove Playwright browsers (optional, saves ~300MB)
rm -rf ~/Library/Caches/ms-playwright
```

---

**Happy migrating! 🎶**
