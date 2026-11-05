# 📖 Usage Example

## Step-by-Step Example

### 1. Setup (First Time Only)

```bash
$ cd /Users/srimaan/Projects/spotify-to-apple-music
$ chmod +x setup.sh
$ ./setup.sh

🎵 Setting up Spotify to Apple Music Migration Tool...

✅ Python 3 found: Python 3.11.5
📦 Creating virtual environment...
✅ Virtual environment created
🔧 Activating virtual environment...
📥 Installing dependencies...
...
🌐 Installing Playwright browsers...
...
✅ Setup complete!
```

### 2. Run the Tool

```bash
$ source venv/bin/activate
(venv) $ python main.py
```

### 3. Interactive Session

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

⏱️  Estimated time: ~2 minutes

🔍 Matching 50 tracks to Apple Music...
  Progress: 10/50
  Progress: 20/50
  Progress: 30/50
  Progress: 40/50
  Progress: 50/50

✅ Successfully matched: 47 tracks
❌ Failed to match: 3 tracks

======================================================================
🎯 Ready to add 47 tracks to Apple Music
======================================================================

⚠️  This will open a browser window. Continue? (y/n): y

🚀 Starting migration of 47 tracks to Apple Music...

🌐 Opening Apple Music web player...

======================================================================
🔐 PLEASE LOG IN TO APPLE MUSIC
======================================================================
1. Sign in with your Apple ID in the browser window
2. Make sure you have an active Apple Music subscription
3. After logging in, return to this terminal
======================================================================

⏎  Press ENTER once you are logged in and ready to continue...

✅ Verifying login status...

[1/47] Adding: Blinding Lights - The Weeknd
  ✅ Successfully added to library

[2/47] Adding: Levitating - Dua Lipa
  ✅ Successfully added to library

[3/47] Adding: Save Your Tears - The Weeknd
  ✓  Already in library

[4/47] Adding: Good 4 U - Olivia Rodrigo
  ✅ Successfully added to library

[5/47] Adding: Stay - The Kid LAROI, Justin Bieber
  ⚠️  Could not find 'Add to Library' button

... (continues for all tracks) ...

======================================================================
📊 MIGRATION SUMMARY
======================================================================
✅ Successfully added: 43 tracks
❌ Failed to add: 2 tracks
⚠️  Not found in Apple Music: 3 tracks
======================================================================

🎉 Migration complete!

💾 Saved failed tracks to: failed_tracks.txt
💾 Saved success log to: success_log.txt
```

### 4. Review Results

**Check success_log.txt:**
```
Successfully added 43 tracks
Generated: 2026-11-05 14:32:15
============================================================

✅ Blinding Lights - The Weeknd
   Apple Music: https://music.apple.com/us/album/blinding-lights/1492518930?i=1492518933

✅ Levitating - Dua Lipa
   Apple Music: https://music.apple.com/us/album/levitating/1533967959?i=1533967960

... (43 tracks total) ...
```

**Check failed_tracks.txt:**
```
Failed to add 5 tracks
Generated: 2026-11-05 14:32:15
============================================================

• Stay - The Kid LAROI, Justin Bieber
• Peaches - Justin Bieber
• Montero - Lil Nas X
• Industry Baby - Lil Nas X, Jack Harlow
• Heat Waves - Glass Animals
```

### 5. Deactivate Virtual Environment

```bash
(venv) $ deactivate
$
```

## Testing with a Small Playlist

Create a test playlist with just 5-10 songs first:

1. In Spotify, create a new playlist called "Test Migration"
2. Add 5-10 of your favorite songs
3. Copy the playlist link
4. Run the tool with that URL

This helps you:
- Verify everything works
- Understand the process
- Identify any issues early
- Build confidence before migrating large playlists

## Running Overnight (Large Playlists)

For playlists with 100+ songs:

```bash
# Prevent your Mac from sleeping
caffeinate -i python main.py

# Or run with nohup (survives terminal closure)
nohup python main.py > migration.log 2>&1 &
```

## Batch Processing Multiple Playlists

Create a script to process multiple playlists:

```bash
#!/bin/bash
# migrate_all.sh

PLAYLISTS=(
  "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
  "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq8LiA"
  "https://open.spotify.com/playlist/37i9dQZF1DX1lVhptIYRda"
)

for url in "${PLAYLISTS[@]}"; do
  echo "Processing: $url"
  echo "$url" | python main.py
  echo "Waiting 60 seconds before next playlist..."
  sleep 60
done
```

## Common Workflow

```bash
# Daily workflow
cd /Users/srimaan/Projects/spotify-to-apple-music
source venv/bin/activate
python main.py
# (paste URL, follow prompts)
deactivate
```

---

**Happy migrating! 🎶**
