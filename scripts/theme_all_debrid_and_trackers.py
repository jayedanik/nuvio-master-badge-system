#!/usr/bin/env python3
"""
Theme All Debrid Services & Torrent Trackers
--------------------------------------------
Transforms pristine flat vector debrid and torrent tracker logos into
authentic bespoke physical badges across all 9 physical themes:
1. GMK Custom Keycaps (Double-shot mechanical keycap chassis)
2. Neon RGB Pudding Keycaps (Translucent frosted pudding with dynamic RGB bloom)
3. Vintage Cinema Ticket (Perforated ticket stub with 24K gold foil trim)
4. Cloisonné Enamel Pins (Polished 24K gold brass with vitreous enamel shine)
5. Retro VHS Magnetic Tape (1980s analog cassette label with REC bar)
6. Director Cinema Clapperboard (Hollywood production slate stripes)
7. Audiophile Vacuum Fluorescent (VFD dark glass with CRT scanlines & phosphor glow)
8. Neo-Tokyo Cyberpunk Tag (Industrial telemetry & hazard accents)
9. Criterion Archival Leather (24K gold foil stamped archival leather)
"""

import os
import sys
from PIL import Image

sys.path.append(r"C:\Users\yourt\.gemini\antigravity\scratch")
import build_all_bespoke_themed_badges_v5 as engine

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
PRISTINE_DIR = os.path.join(REPO_ROOT, "badges")
THEMES_DIR = os.path.join(REPO_ROOT, "themes")

# Register custom RGB glow colors
CUSTOM_RGB_COLORS = {
    "realdebrid": (110, 190, 70),
    "torbox": (0, 210, 120),
    "alldebrid": (245, 166, 35),
    "premiumize": (0, 140, 220),
    "debridlink": (52, 152, 219),
    "1337x": (220, 50, 50),
    "rarbg": (60, 100, 210),
    "piratebay": (190, 140, 85),
    "thepiratebay": (190, 140, 85),
    "tpb": (190, 140, 85),
    "yts": (45, 180, 80),
    "yify": (45, 180, 80),
    "eztv": (60, 130, 220),
    "torrentgalaxy": (160, 80, 230),
    "tgx": (160, 80, 230),
    "rutracker": (50, 150, 220),
    "nyaa": (50, 140, 235),
}
engine.RGB_KEYCAP_COLORS.update(CUSTOM_RGB_COLORS)

TARGET_BADGES = [
    "realdebrid",
    "torbox",
    "alldebrid",
    "premiumize",
    "debridlink",
    "1337x",
    "rarbg",
    "piratebay",
    "thepiratebay",
    "tpb",
    "yts",
    "yify",
    "eztv",
    "torrentgalaxy",
    "tgx",
    "rutracker",
    "nyaa",
    "torrentio",
    "limetorrents",
    "torrentleech",
    "iptorrents",
    "kickasstorrents",
    "kat",
    "bitsearch",
    "torrentday",
    "fitgirl"
]

def theme_badge(badge_id):
    p_path = os.path.join(PRISTINE_DIR, f"{badge_id}.webp")
    if not os.path.exists(p_path):
        print(f"Skipping {badge_id}: pristine badge not found at {p_path}")
        return

    raw_img = Image.open(p_path).convert("RGBA")
    bbox = raw_img.getbbox()
    if not bbox:
        print(f"Skipping {badge_id}: empty image")
        return
    logo_img = raw_img.crop(bbox)

    print(f"\nProcessing {badge_id} (original content: {logo_img.size})...")

    for theme_id, renderer in engine.THEME_RENDERERS.items():
        if theme_id == "pristine":
            continue

        out_theme_dir = os.path.join(THEMES_DIR, theme_id, "badges")
        os.makedirs(out_theme_dir, exist_ok=True)
        out_file = os.path.join(out_theme_dir, f"{badge_id}.webp")

        try:
            themed_badge = renderer(True, logo_img, None, None, badge_id=badge_id)
        except TypeError:
            themed_badge = renderer(True, logo_img, None, None)

        themed_badge.save(out_file, "WEBP", quality=95)
        print(f"  [{theme_id}] saved {badge_id}.webp ({themed_badge.size})")

def main():
    print("=== THEMING DEBRID SERVICES & TORRENT TRACKERS ===")
    for b in TARGET_BADGES:
        theme_badge(b)
    print("\n[OK] All Debrid & Torrent Tracker badges themed across all 9 physical themes!")

if __name__ == "__main__":
    main()
