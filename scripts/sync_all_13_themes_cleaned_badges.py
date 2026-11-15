import os, sys, shutil
from PIL import Image
import numpy as np

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEMES_DIR = os.path.join(REPO_ROOT, "themes")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
BRAIN_SCRATCH = r"C:\Users\yourt\.gemini\antigravity\brain\fb22a0fc-6924-43f9-ab27-8d6db9906f8f\scratch"

sys.path.append(SCRATCH_DIR)
sys.path.append(BRAIN_SCRATCH)

import build_all_bespoke_themed_badges_v5 as b5
import generate_all_liquid_glass_theme as gl
import generate_all_washi_tape_theme as gw

THEME_RENDERERS_9 = {
    "gmk-keycaps": b5.render_gmk_keycaps,
    "rgb-keycaps": b5.render_rgb_keycaps,
    "cinema-ticket": b5.render_cinema_ticket,
    "enamel-pins": b5.render_enamel_pins,
    "vhs-tape": b5.render_vhs_tape,
    "clapperboard": b5.render_clapperboard,
    "audiophile-vfd": b5.render_audiophile_vfd,
    "neotokyo-tag": b5.render_neotokyo_tag,
    "criterion-leather": b5.render_criterion_leather,
}

CLEANED_BADGE_NAMES = [
    # 4 Brand Logos
    "alldebrid", "wetv", "sonyliv", "sonypictures",
    # 86 Smoked Pill Badges
    "120fps", "247", "3d-fsbs", "3d-hsbs", "3d-mvc", "3d-ou",
    "50fps", "6.1", "60fps", "6_1", "altt", "anaglyph",
    "avi", "backup", "banglaflix", "batch", "bigfile", "bw",
    "catchup", "chaupal", "cinematic", "dts-es", "dts-hd-hra",
    "dvd-remux", "fake-hdr", "full-disc", "fulldisc", "hardsub",
    "hd-feed", "hdrip", "hfr", "hls", "hungama", "hybrid",
    "internal", "itunes", "klikk", "kurdish", "latino-flag",
    "limited", "line-audio", "live-backup", "live-hd", "live-hfr",
    "live-raw", "live-sd", "lowres", "lpcm", "m2ts",
    "manoramamax", "mp3", "mpeg2", "mpegts", "msubs",
    "mxplayer", "open-matte", "original", "planetmarathi", "ppv",
    "proper", "rabbithole", "raw", "region-in", "region-uk",
    "region-us", "repack", "sample", "sd-feed", "sdh",
    "season-pack", "seasonpack", "shemaroome", "sonypicturescore",
    "special", "telecine", "ts", "tvrip", "ullu", "uncensored",
    "upscaled", "usenet", "vc1", "version", "vostfr", "web",
    "welsh-flag"
]

def sync_studio_markers():
    print("--- 1. Syncing to studio-markers ---")
    sm_dir = os.path.join(THEMES_DIR, "studio-markers", "badges")
    os.makedirs(sm_dir, exist_ok=True)
    count = 0
    for name in CLEANED_BADGE_NAMES:
        src = os.path.join(BADGES_DIR, f"{name}.webp")
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(sm_dir, f"{name}.webp"))
            count += 1
    print(f"Synced {count} badges to studio-markers.")

def sync_nine_bespoke_themes():
    print("--- 2. Rendering 9 Bespoke Physical Themes ---")
    for theme_id, renderer in THEME_RENDERERS_9.items():
        theme_badges_dir = os.path.join(THEMES_DIR, theme_id, "badges")
        os.makedirs(theme_badges_dir, exist_ok=True)
        count = 0
        for name in CLEANED_BADGE_NAMES:
            src = os.path.join(BADGES_DIR, f"{name}.webp")
            if not os.path.exists(src):
                continue
            raw_img = Image.open(src).convert("RGBA")
            bbox = raw_img.getbbox()
            if not bbox:
                continue
            glyph = raw_img.crop(bbox)
            
            try:
                themed_badge = renderer(True, glyph, None, None, badge_id=name)
            except TypeError:
                themed_badge = renderer(True, glyph, None, None)
                
            out_p = os.path.join(theme_badges_dir, f"{name}.webp")
            themed_badge.save(out_p, "WEBP", quality=95, method=6)
            count += 1
        print(f"Rendered {count} badges for {theme_id}.")

def sync_liquid_glass():
    print("--- 3. Rendering VisionOS Liquid Glass Theme ---")
    count = 0
    for name in CLEANED_BADGE_NAMES:
        ok = gl.generate_single_badge(name)
        if ok:
            count += 1
    print(f"Rendered {count} badges for liquid-glass.")

def sync_washi_tape():
    print("--- 4. Rendering Artisan Washi Tape Theme ---")
    count = 0
    for name in CLEANED_BADGE_NAMES:
        ok = gw.build_washi_badge_for_name(name)
        if ok:
            count += 1
    print(f"Rendered {count} badges for washi-tape.")

def main():
    print("=== SYNCHRONIZING ALL 90 CLEANED BADGES ACROSS ALL 13 THEMES ===")
    sync_studio_markers()
    sync_nine_bespoke_themes()
    sync_liquid_glass()
    sync_washi_tape()
    print("\n[SUCCESS] Universal Synchronization Complete across all 13 themes!")

if __name__ == "__main__":
    main()
