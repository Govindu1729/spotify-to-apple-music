"""
Scraper module for Spotify playlists and Apple Music catalog search.
No API keys or Premium accounts required!
"""

import re
import json
import time
import urllib.request
import urllib.parse
from typing import List, Dict, Optional

import config


def scrape_spotify_playlist(playlist_url: str) -> List[Dict[str, str]]:
    """
    Scrape a Spotify playlist using the public embed page.
    No Spotify API key or Premium account required.
    
    Args:
        playlist_url: Full Spotify playlist URL
        
    Returns:
        List of dictionaries with 'title' and 'artist' keys
    """
    # Extract playlist ID from URL
    match = re.search(r'spotify\.com/playlist/([a-zA-Z0-9]+)', playlist_url)
    if not match:
        raise ValueError(f"Invalid Spotify playlist URL: {playlist_url}")
    
    playlist_id = match.group(1)
    embed_url = f"{config.SPOTIFY_EMBED_BASE_URL}/{playlist_id}"
    
    print(f"🎵 Scraping Spotify playlist: {playlist_url}")
    
    # Fetch the embed page
    req = urllib.request.Request(embed_url, headers={"User-Agent": config.USER_AGENT})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8")
    except Exception as e:
        raise ConnectionError(f"Failed to fetch Spotify embed page: {e}")
    
    # Extract the hidden JSON data from __NEXT_DATA__ script tag
    json_match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">({.*?})</script>',
        html,
        re.DOTALL
    )
    
    if not json_match:
        raise ValueError("Could not find playlist data in Spotify embed page")
    
    try:
        data = json.loads(json_match.group(1))
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse Spotify playlist JSON: {e}")
    
    # Navigate to track list in the JSON structure
    track_list = (
        data.get("props", {})
        .get("pageProps", {})
        .get("state", {})
        .get("data", {})
        .get("entity", {})
        .get("trackList", [])
    )
    
    if not track_list:
        print("⚠️  No tracks found in playlist")
        return []
    
    # Extract track information
    tracks = []
    for t in track_list:
        title = t.get("title", "").strip()
        artist = t.get("subtitle", "").strip()
        
        if title and artist:
            tracks.append({"title": title, "artist": artist})
    
    print(f"✅ Found {len(tracks)} tracks in Spotify playlist")
    return tracks


def search_apple_music(artist: str, title: str) -> Optional[str]:
    """
    Search for a track in Apple Music using the public iTunes Search API.
    No Apple Developer account required.
    
    Args:
        artist: Artist name
        title: Track title
        
    Returns:
        Apple Music web URL for the track, or None if not found
    """
    query = urllib.parse.quote(f"{artist} {title}")
    url = f"{config.ITUNES_SEARCH_API}?term={query}&entity=song&limit=1"
    
    req = urllib.request.Request(url, headers={"User-Agent": config.USER_AGENT})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️  Error searching Apple Music for '{title}' by {artist}: {e}")
        return None
    
    if data.get("resultCount", 0) > 0:
        result = data["results"][0]
        track_url = result.get("trackViewUrl")
        
        if track_url:
            return track_url
    
    return None


def match_spotify_to_apple(tracks: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Match Spotify tracks to Apple Music catalog tracks.
    
    Args:
        tracks: List of Spotify track dictionaries
        
    Returns:
        List of matched tracks with Apple Music URLs
    """
    matched_tracks = []
    failed_tracks = []
    total = len(tracks)
    
    print(f"\n🔍 Matching {total} tracks to Apple Music...")
    
    for i, track in enumerate(tracks, 1):
        title = track["title"]
        artist = track["artist"]
        
        # Progress indicator
        if i % 10 == 0 or i == total:
            print(f"  Progress: {i}/{total}")
        
        # Search Apple Music
        apple_url = search_apple_music(artist, title)
        
        if apple_url:
            matched_tracks.append({
                "title": title,
                "artist": artist,
                "apple_url": apple_url
            })
        else:
            failed_tracks.append({
                "title": title,
                "artist": artist
            })
        
        # Rate limiting
        time.sleep(config.DELAY_BETWEEN_REQUESTS)
    
    print(f"\n✅ Successfully matched: {len(matched_tracks)} tracks")
    print(f"❌ Failed to match: {len(failed_tracks)} tracks")
    
    return matched_tracks, failed_tracks
