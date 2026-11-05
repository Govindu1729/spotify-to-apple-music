#!/usr/bin/env python3
"""
Spotify to Apple Music Playlist Migration Tool

A free, no-API-key-required tool to migrate Spotify playlists to Apple Music.
Uses browser automation and public APIs to bypass Premium/Developer account requirements.

Author: Your Name
Date: 2026
"""

import sys
import time
from datetime import datetime

from scraper import scrape_spotify_playlist, match_spotify_to_apple
from browser import migrate_playlist_to_apple
import config


def save_failed_tracks(failed_tracks, filename=config.FAILED_TRACKS_FILE):
    """
    Save failed tracks to a text file for manual review.
    
    Args:
        failed_tracks: List of failed track dictionaries
        filename: Output filename
    """
    if not failed_tracks:
        return
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Failed to add {len(failed_tracks)} tracks\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        
        for track in failed_tracks:
            f.write(f"• {track['title']} - {track['artist']}\n")
    
    print(f"\n💾 Saved failed tracks to: {filename}")


def save_success_log(success_tracks, filename=config.SUCCESS_LOG_FILE):
    """
    Save successful migrations to a log file.
    
    Args:
        success_tracks: List of successfully added track dictionaries
        filename: Output filename
    """
    if not success_tracks:
        return
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Successfully added {len(success_tracks)} tracks\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        
        for track in success_tracks:
            f.write(f"✅ {track['title']} - {track['artist']}\n")
            f.write(f"   Apple Music: {track.get('apple_url', 'N/A')}\n\n")
    
    print(f"💾 Saved success log to: {filename}")


def main():
    """
    Main entry point for the migration tool.
    """
    print("="*70)
    print("🎵 Spotify to Apple Music Migration Tool")
    print("="*70)
    print("\nThis tool will:")
    print("  1. Scrape your Spotify playlist (no API key required)")
    print("  2. Match tracks to Apple Music catalog (no dev account required)")
    print("  3. Add matched tracks to your Apple Music library (browser automation)")
    print("\n" + "="*70)
    
    # Get playlist URL from user
    playlist_url = input("\n📋 Enter Spotify playlist URL: ").strip()
    
    if not playlist_url:
        print("❌ Error: No URL provided")
        sys.exit(1)
    
    if "spotify.com/playlist" not in playlist_url:
        print("❌ Error: Invalid Spotify playlist URL")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("⏱️  Estimated time: ~{} minutes".format(
        len(range(1)) // 60  # Will be updated
    ))
    print("="*70)
    
    # Step 1: Scrape Spotify playlist
    try:
        spotify_tracks = scrape_spotify_playlist(playlist_url)
    except Exception as e:
        print(f"\n❌ Error scraping Spotify: {e}")
        sys.exit(1)
    
    if not spotify_tracks:
        print("\n❌ No tracks found in playlist")
        sys.exit(1)
    
    # Update time estimate
    estimated_minutes = (len(spotify_tracks) * (config.DELAY_BETWEEN_REQUESTS + 1)) // 60
    print(f"\n⏱️  Estimated time: ~{estimated_minutes} minutes for matching")
    
    # Step 2: Match tracks to Apple Music
    matched_tracks, unmatched_tracks = match_spotify_to_apple(spotify_tracks)
    
    if not matched_tracks:
        print("\n❌ No tracks could be matched to Apple Music")
        save_failed_tracks(unmatched_tracks)
        sys.exit(1)
    
    # Step 3: Migrate to Apple Music
    print("\n" + "="*70)
    print(f"🎯 Ready to add {len(matched_tracks)} tracks to Apple Music")
    print("="*70)
    
    confirm = input("\n⚠️  This will open a browser window. Continue? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("\n👋 Migration cancelled")
        save_failed_tracks(unmatched_tracks)
        sys.exit(0)
    
    try:
        results = migrate_playlist_to_apple(matched_tracks)
        
        # Save results
        save_failed_tracks(results["failed"] + unmatched_tracks)
        save_success_log(results["success"])
        
        # Print summary
        print("\n" + "="*70)
        print("📊 MIGRATION SUMMARY")
        print("="*70)
        print(f"✅ Successfully added: {len(results['success'])} tracks")
        print(f"❌ Failed to add: {len(results['failed'])} tracks")
        print(f"⚠️  Not found in Apple Music: {len(unmatched_tracks)} tracks")
        print("="*70)
        print("\n🎉 Migration complete!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Migration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
