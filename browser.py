import re
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Delay between tracks to prevent Apple's rate limiting (seconds)
DELAY_BETWEEN_TRACKS = 2

def verify_login(page):
    """Checks if the user is logged in by looking for a user profile avatar or specific nav links."""
    try:
        # Look for the search bar which is present for logged-in users
        page.locator('input[type="search"], [aria-label="Search"]').first.wait_for(state="visible", timeout=10000)
        return True
    except Exception:
        return False

def click_add_button(page):
    """Attempts to click the Add to Library button using multiple fallback selectors."""
    # 1. Try standard "Add to Library" aria-labels and classes
    add_selectors = [
        'button[aria-label="Add to Library"]',
        'button[aria-label="Add"]',
        'button[aria-label*="Add"]',
        'button.add-to-library',
        'button[data-testid="add-button"]',
        'button[aria-label*="Plus"]',
        'button:has(svg[aria-label*="Plus"])'
    ]
    
    for sel in add_selectors:
        try:
            btn = page.locator(sel).first
            # Use a very short timeout just to check if it's already there
            if btn.is_visible(timeout=1000):
                btn.click()
                return True
        except Exception:
            continue

    # 2. Try the "More" (...) menu (sometimes the Add button is hidden here)
    try:
        more_selectors = [
            'button[aria-label*="More"]',
            'button[aria-label*="Actions"]',
            'button.more-button',
            'button[aria-label="More Options"]'
        ]
        for sel in more_selectors:
            more_btn = page.locator(sel).first
            if more_btn.is_visible(timeout=1000):
                more_btn.click()
                page.wait_for_timeout(500) # Wait for dropdown menu to render
                
                # Look for "Add to Library" in the dropdown/menu
                menu_selectors = [
                    'button:has-text("Add to Library")',
                    'button:has-text("Add to playlist")',
                    'button:has-text("Add")',
                    '[role="menuitem"]:has-text("Add")'
                ]
                for m_sel in menu_selectors:
                    menu_item = page.locator(m_sel).first
                    if menu_item.is_visible(timeout=1000):
                        menu_item.click()
                        return True
                break # Clicked more button but couldn't find add item, stop trying more buttons
    except Exception:
        pass

    return False

def migrate_playlist_to_apple(tracks):
    """
    Automates adding tracks into Apple Music via Playwright.
    """
    print("\n🚀 Starting migration of tracks to Apple Music...")
    
    with sync_playwright() as p:
        # Launch in headed mode so the user can log in and see the magic happen
        # slow_mo makes it easier to watch and sometimes prevents bot detection
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # 1. Navigate to Apple Music
        print("\n🌐 Opening Apple Music web player...")
        try:
            # domcontentloaded is much safer than networkidle for Apple's heavy web app
            page.goto("https://music.apple.com/us/listen-now", wait_until="domcontentloaded", timeout=20000)
        except PlaywrightTimeoutError:
            print("⚠️  Initial page load timed out, but we'll continue. Please ensure you are logged in.")

        # 2. Wait for user login
        print("\n" + "="*60)
        print("🔐 PLEASE LOG IN TO APPLE MUSIC")
        print("="*60)
        print("1. Sign in with your Apple ID in the browser window")
        print("2. Make sure you have an active Apple Music subscription")
        print("3. Once logged in and you see the main dashboard, return here")
        print("="*60)
        input("\n⏎  Press ENTER once you are logged in and ready to continue...")

        print("✅ Verifying login status...")
        if not verify_login(page):
            print("⚠️  Could not verify login status. The script might fail on adding tracks.")

        success_count = 0
        failed_tracks = []

        # 3. Process each track
        for i, track in enumerate(tracks):
            title = track.get('title', '')
            artist = track.get('artist', '')
            url = track.get('apple_music_url', '')
            
            print(f"\n[{i+1}/{len(tracks)}] Adding: {title} - {artist}")

            if not url:
                print("  ❌ No Apple Music URL found for this track.")
                failed_tracks.append(f"{title} - {artist} (No URL)")
                continue

            try:
                # Navigate to the track URL
                # Use domcontentloaded + a manual wait for React hydration
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(2000) # Wait 2s for JS to render the track UI
                
                # Try to click the Add button
                if click_add_button(page):
                    print("  ✅ Added to library!")
                    success_count += 1
                    page.wait_for_timeout(1500) # Wait for UI to update before next track
                else:
                    print("  ⚠️  Could not find 'Add' button. Might already be in library or UI changed.")
                    failed_tracks.append(f"{title} - {artist} (Button not found)")

            except PlaywrightTimeoutError as e:
                print(f"  ❌ Timeout error: {str(e).splitlines()[0]}")
                failed_tracks.append(f"{title} - {artist} (Timeout)")
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                failed_tracks.append(f"{title} - {artist} (Error)")

            # Delay to avoid rate limiting
            time.sleep(DELAY_BETWEEN_TRACKS)

        print("\n" + "="*60)
        print("🎉 Migration Complete!")
        print(f"✅ Successfully added: {success_count} tracks")
        print(f"❌ Failed/Skipped: {len(failed_tracks)} tracks")
        
        if failed_tracks:
            print("\nFailed/Skipped tracks:")
            for t in failed_tracks[:5]: # Show first 5
                print(f"  - {t}")
            if len(failed_tracks) > 5:
                print(f"  ... and {len(failed_tracks) - 5} more")

        print("\n⏳ Keeping browser open for 10 seconds so you can review...")
        time.sleep(10)
        browser.close()

    return success_count, failed_tracks
