"""
Configuration settings for Spotify to Apple Music migration
"""

# Spotify settings
SPOTIFY_EMBED_BASE_URL = "https://open.spotify.com/embed/playlist"

# iTunes Search API (no authentication required)
ITUNES_SEARCH_API = "https://itunes.apple.com/search"

# Apple Music settings
APPLE_MUSIC_URL = "https://music.apple.com"
APPLE_MUSIC_LOGIN_URL = "https://music.apple.com/account/login"

# Browser settings
HEADLESS_MODE = False  # Set to True to run browser in background
SLOW_MO_MS = 100  # Slow down browser actions for debugging (ms)

# Rate limiting (to avoid getting blocked)
DELAY_BETWEEN_REQUESTS = 2  # seconds
DELAY_BETWEEN_ADDS = 3  # seconds

# Output files
FAILED_TRACKS_FILE = "failed_tracks.txt"
SUCCESS_LOG_FILE = "success_log.txt"

# User agent for requests
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
