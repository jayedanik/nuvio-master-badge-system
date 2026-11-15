#!/usr/bin/env python3
"""
Nuvio Master Badge System — Universal Synchronization Engine
------------------------------------------------------------
Automatically synchronizes:
1. `badges.json` (source of truth: filter count, language count, groups, services)
2. `badges/` directory (WebP asset count, disk footprint)
3. `themes/` directory (Auto-generates themed variants for any new/unthemed badges)
4. `previews/nuvio-hero.svg` (Badge count, language count, theme count, version pill)
5. `previews/theme-ecosystem.jpg` (High-end 2400x1200 master showcase for ALL theme universes)
6. `previews/preview-studio-markers.jpg` (StreamBridge Studio Markers Enhanced showcase)
7. `README.md` (Shield badges, descriptions, in-app stats, cache-busters)
8. GitHub Repository About / Description (via gh CLI if available)
9. Git tags, backup branch, ZIP archive, and GitHub Release with detailed changelog (when --release is passed)

Usage:
  python scripts/sync_repo_master.py                # Syncs themes, SVG, ecosystem, README, and repo metadata
  python scripts/sync_repo_master.py --release      # Syncs everything + creates tag, release & backups
  python scripts/sync_repo_master.py --version v3.5.0 --release
"""

import os
import sys
import re
import json
import hashlib
import zipfile
import subprocess
import argparse
import base64
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PREVIEWS_DIR = os.path.join(REPO_ROOT, "previews")
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEMES_DIR = os.path.join(REPO_ROOT, "themes")
BADGES_JSON = os.path.join(REPO_ROOT, "badges.json")
HERO_SVG = os.path.join(PREVIEWS_DIR, "nuvio-hero.svg")
README_MD = os.path.join(REPO_ROOT, "README.md")
VERSION_FILE = os.path.join(REPO_ROOT, "VERSION")
BACKUP_DIR = r"C:\Users\yourt\.gemini\antigravity\backups"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Fonts discovery
FONTS_DIR = os.path.join(REPO_ROOT, ".fonts")
FALLBACK_FONTS_DIR = r"C:\Users\yourt\.gemini\antigravity\brain\e3a87934-5f4d-4111-a44e-2f095bc5cbab\scratch\caveman\extension\fonts"

def load_fonts_base64():
    f_sans = os.path.join(FONTS_DIR, "geist-sans.woff2")
    f_mono = os.path.join(FONTS_DIR, "geist-mono.woff2")
    if not os.path.exists(f_sans) or not os.path.exists(f_mono):
        f_sans = os.path.join(FALLBACK_FONTS_DIR, "geist-sans.woff2")
        f_mono = os.path.join(FALLBACK_FONTS_DIR, "geist-mono.woff2")
    
    b64_sans, b64_mono = "", ""
    if os.path.exists(f_sans):
        with open(f_sans, "rb") as f:
            b64_sans = base64.b64encode(f.read()).decode("utf-8")
    if os.path.exists(f_mono):
        with open(f_mono, "rb") as f:
            b64_mono = base64.b64encode(f.read()).decode("utf-8")
    return b64_sans, b64_mono

# Import theme rendering engine
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
if SCRATCH_DIR not in sys.path:
    sys.path.append(SCRATCH_DIR)

try:
    import build_all_bespoke_themed_badges_v5 as theme_engine
except ImportError:
    theme_engine = None

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
if theme_engine:
    theme_engine.RGB_KEYCAP_COLORS.update(CUSTOM_RGB_COLORS)

KNOWN_THEMES = [
    ("01", "pristine", "Pristine Master", "Floating OLED Typography", "#38bdf8", "badges"),
    ("02", "studio-markers", "StreamBridge Enhanced", "Frameless Studio Markers", "#f59e0b", "themes/studio-markers/badges"),
    ("03", "gmk-keycaps", "GMK Custom Keycaps", "Double-Shot PBT Dish", "#a78bfa", "themes/gmk-keycaps/badges"),
    ("04", "rgb-keycaps", "Neon RGB Pudding", "Chroma Cyan Underglow", "#00f2fe", "themes/rgb-keycaps/badges"),
    ("05", "cinema-ticket", "Cinema Ticket", "24K Gold Pinstripe Stub", "#f59e0b", "themes/cinema-ticket/badges"),
    ("06", "enamel-pins", "Cloisonné Enamel", "Cast Jewelry Brass Rim", "#eab308", "themes/enamel-pins/badges"),
    ("07", "vhs-tape", "Retro VHS Tape", "1980s Analog Paper Label", "#fb7185", "themes/vhs-tape/badges"),
    ("08", "clapperboard", "Cinema Clapperboard", "Hollywood Slate Chevrons", "#f43f5e", "themes/clapperboard/badges"),
    ("09", "audiophile-vfd", "Audiophile VFD", "Cyan Phosphor Tube", "#2dd4bf", "themes/audiophile-vfd/badges"),
    ("10", "neotokyo-tag", "Neo-Tokyo Tag", "Shibuya Hazard Techwear", "#ec4899", "themes/neotokyo-tag/badges"),
    ("11", "criterion-leather", "Criterion Leather", "Debossed Archival Gold", "#d97706", "themes/criterion-leather/badges")
]

def run_cmd(cmd, cwd=REPO_ROOT, check=True):
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"Command failed: {cmd}\nstderr: {res.stderr}")
    return res.stdout.strip(), res.returncode

def get_latest_version(override=None):
    if override:
        return override.strip()
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            v = f.read().strip()
            if v:
                return v
    stdout, rc = run_cmd("git describe --tags --abbrev=0", check=False)
    if rc == 0 and stdout:
        return stdout.splitlines()[-1].strip()
    return "v3.5.0"

def get_file_md5(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def auto_theme_missing_or_unthemed_badges():
    """
    Checks all badges in badges/ and ensures every physical theme has an
    authentic themed physical badge rather than a raw un-styled copy.
    """
    if not theme_engine:
        print("Note: theme_engine not available, skipping auto-theming step.")
        return

    print("Checking for unthemed or missing badges across all physical themes...")
    pristine_files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]
    pristine_hashes = {}
    for f in pristine_files:
        pristine_hashes[f] = get_file_md5(os.path.join(BADGES_DIR, f))

    theme_dirs = [d for d in os.listdir(THEMES_DIR) if os.path.isdir(os.path.join(THEMES_DIR, d))]
    
    priority_theming = [
        "realdebrid", "torbox", "alldebrid", "premiumize", "debridlink",
        "1337x", "rarbg", "piratebay", "thepiratebay", "tpb", "yts", "yify",
        "eztv", "torrentgalaxy", "tgx", "rutracker", "nyaa"
    ]

    themed_count = 0
    for b_id in priority_theming:
        f_name = f"{b_id}.webp"
        p_path = os.path.join(BADGES_DIR, f_name)
        if not os.path.exists(p_path):
            continue

        raw_img = Image.open(p_path).convert("RGBA")
        bbox = raw_img.getbbox()
        if not bbox:
            continue
        logo_img = raw_img.crop(bbox)

        for theme_id in theme_dirs:
            if theme_id not in theme_engine.THEME_RENDERERS:
                continue
            out_file = os.path.join(THEMES_DIR, theme_id, "badges", f_name)
            needs_theming = False
            if not os.path.exists(out_file):
                needs_theming = True
            else:
                if get_file_md5(out_file) == pristine_hashes[f_name]:
                    needs_theming = True

            if needs_theming:
                renderer = theme_engine.THEME_RENDERERS[theme_id]
                try:
                    themed_badge = renderer(True, logo_img, None, None, badge_id=b_id)
                except TypeError:
                    themed_badge = renderer(True, logo_img, None, None)
                os.makedirs(os.path.dirname(out_file), exist_ok=True)
                themed_badge.save(out_file, "WEBP", quality=95)
                themed_count += 1

    if themed_count > 0:
        print(f"Auto-themed {themed_count} badge files across themes.")
    else:
        print("All priority badges are already 100% styled into their themes.")

def inspect_repository():
    with open(BADGES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    filters = data.get("filters", [])
    total_filters = len(filters)

    by_group = {}
    for f in filters:
        g = f.get("groupId", "unknown")
        by_group[g] = by_group.get(g, 0) + 1

    lang_count = by_group.get("language", 0)
    service_count = by_group.get("service", 0)
    group_count = len(data.get("groups", []))

    webp_files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]
    total_assets = len(webp_files)

    total_bytes = sum(os.path.getsize(os.path.join(BADGES_DIR, f)) for f in webp_files)
    size_mb = total_bytes / (1024 * 1024)

    theme_dirs = [d for d in os.listdir(THEMES_DIR) if os.path.isdir(os.path.join(THEMES_DIR, d))] if os.path.exists(THEMES_DIR) else []
    total_themes = len(theme_dirs) + 1

    return {
        "badge_count": total_filters,
        "asset_count": total_assets,
        "lang_count": lang_count,
        "service_count": service_count,
        "group_count": group_count,
        "theme_count": total_themes,
        "size_mb": round(size_mb, 2)
    }

def update_hero_svg(stats, version):
    if not os.path.exists(HERO_SVG):
        print(f"Warning: {HERO_SVG} not found!")
        return False

    with open(HERO_SVG, "r", encoding="utf-8") as f:
        svg = f.read()

    svg = re.sub(
        r'(<!-- Stat 1:.*-->\s*<g[^>]*>\s*<text[^>]*class="stat-val"[^>]*>)[^<]+(</text>)',
        rf'\g<1>{stats["badge_count"]}\g<2>',
        svg
    )

    svg = re.sub(
        r'(<!-- Stat 2:.*-->\s*<g[^>]*>\s*<text[^>]*class="stat-val"[^>]*>)[^<]+(</text>)',
        rf'\g<1>{stats["theme_count"]}\g<2>',
        svg
    )

    svg = re.sub(
        r'(<!-- Stat 3:.*-->\s*<g[^>]*>\s*<text[^>]*class="stat-val"[^>]*>)[^<]+(</text>)',
        rf'\g<1>{stats["lang_count"]}\g<2>',
        svg
    )
    svg = re.sub(
        r'<!-- Stat 3: \d+ Languages -->',
        f'<!-- Stat 3: {stats["lang_count"]} Languages -->',
        svg
    )

    svg = re.sub(
        r'(<!-- Version tag -->\s*<g[^>]*>[\s\S]*?<text[^>]*font-family="\'JetBrains Mono\', monospace"[^>]*>)[^<]+(</text>)',
        rf'\g<1>{version}\g<2>',
        svg
    )

    with open(HERO_SVG, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Updated {HERO_SVG} -> Badges: {stats['badge_count']}, Themes: {stats['theme_count']}, Languages: {stats['lang_count']}, Version: {version}")
    return True

def update_theme_ecosystem_preview(stats, version):
    """
    Renders authentic Nothing Dot Matrix 6-tier ecosystem showcase representing all 13 theme universes.
    """
    try:
        import render_nothing_masterpiece as rnm
        rnm.render_ecosystem()
        return True
    except Exception as e:
        print(f"Error rendering ecosystem via render_nothing_masterpiece: {e}")

    if not os.path.exists(EDGE_PATH):
        print("Note: Edge not found, skipping ecosystem render.")
        return False

    b64_sans, b64_mono = load_fonts_base64()
    
    existing_ids = {t[1] for t in KNOWN_THEMES}
    themes_list = list(KNOWN_THEMES)
    if os.path.exists(THEMES_DIR):
        theme_dirs = sorted([d for d in os.listdir(THEMES_DIR) if os.path.isdir(os.path.join(THEMES_DIR, d))])
        next_idx = len(themes_list) + 1
        for d in theme_dirs:
            if d not in existing_ids and d != "pristine":
                clean_name = d.replace("-", " ").title()
                themes_list.append((f"{next_idx:02d}", d, clean_name, "Master Stream Style", "#38bdf8", f"themes/{d}/badges"))
                next_idx += 1

    total_themes_count = len(themes_list)
    showcase_badges = ["4k.webp", "dolby-vision.webp", "netflix.webp"]

    cards_html = ""
    for num, tid, name, sub, accent, rel_dir in themes_list:
        badges_dir = os.path.join(REPO_ROOT, rel_dir)
        badges_html = ""
        for b in showcase_badges:
            b_p = os.path.join(badges_dir, b)
            if not os.path.exists(b_p):
                b_p = os.path.join(REPO_ROOT, "badges", b)
            if os.path.exists(b_p):
                b_url = b_p.replace("\\", "/")
                badges_html += f'<div class="badge-slot"><img src="file:///{b_url}" alt="{b}" /></div>\n'

        cards_html += f"""
        <div class="theme-card">
          <div class="card-header">
            <div class="card-tag" style="color: {accent};">
              {num}. {name}
            </div>
            <div class="card-sub">{sub}</div>
          </div>
          <div class="card-badges">
            {badges_html}
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @font-face {{
    font-family: 'Geist Sans';
    src: url('data:font/woff2;base64,{b64_sans}') format('woff2');
    font-weight: 100 900;
  }}
  @font-face {{
    font-family: 'Geist Mono';
    src: url('data:font/woff2;base64,{b64_mono}') format('woff2');
    font-weight: 100 900;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    overflow: hidden !important;
    scrollbar-width: none !important;
    background: #06080c;
  }}
  body {{
    font-family: 'Geist Sans', -apple-system, sans-serif;
    color: #ffffff;
    -webkit-font-smoothing: antialiased;
  }}
  .showcase-container {{
    width: 2400px;
    height: 1200px;
    padding: 38px 85px 28px 85px;
    background: radial-gradient(1300px 520px at 15% 0%, rgba(56, 189, 248, 0.12) 0%, transparent 60%),
                radial-gradient(1000px 450px at 85% 25%, rgba(168, 85, 247, 0.08) 0%, transparent 60%),
                linear-gradient(180deg, #0c1017 0%, #06080c 100%);
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding-bottom: 18px;
  }}
  .main-title {{
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1.2px;
    color: #ffffff;
    line-height: 1.05;
  }}
  .subtitle {{
    font-size: 16.5px;
    color: rgba(255, 255, 255, 0.50);
    font-weight: 400;
    letter-spacing: -0.1px;
    margin-top: 5px;
  }}
  .header-meta {{
    font-family: 'Geist Mono', monospace;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 2px;
    color: rgba(255, 255, 255, 0.38);
    text-transform: uppercase;
  }}
  .meta-sep {{
    margin: 0 12px;
    color: rgba(255, 255, 255, 0.15);
  }}
  .themes-grid {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 16px;
    margin-top: 12px;
    margin-bottom: 8px;
    height: 910px;
    align-content: space-between;
  }}
  .theme-card {{
    width: 356px;
    height: 440px;
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 14px 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .card-header {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 8px;
  }}
  .card-tag {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.4px;
  }}
  .card-sub {{
    font-size: 11.5px;
    color: rgba(255, 255, 255, 0.35);
    font-weight: 400;
  }}
  .card-badges {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
    gap: 8px;
    flex: 1;
    padding: 10px 0 4px 0;
  }}
  .badge-slot {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 72px;
  }}
  .badge-slot img {{
    height: 60px;
    width: auto;
    max-width: 90%;
    object-fit: contain;
    filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.5));
  }}
  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 12px;
    font-family: 'Geist Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    color: rgba(255, 255, 255, 0.25);
    text-transform: uppercase;
  }}
</style>
</head>
<body>
<div class="showcase-container">
  <div class="header">
    <div class="title-group">
      <h1 class="main-title">The {total_themes_count}-Theme Material Ecosystem</h1>
      <div class="subtitle">Every stream indicator engineered across {total_themes_count} bespoke physical material systems</div>
    </div>
    <div class="header-meta">
      <span>{total_themes_count} UNIVERSES</span>
      <span class="meta-sep">&bull;</span>
      <span>{stats['badge_count']} RULES</span>
      <span class="meta-sep">&bull;</span>
      <span>96PX NATIVE</span>
    </div>
  </div>

  <div class="themes-grid">
    {cards_html}
  </div>

  <div class="footer">
    <span>NUVIO MEDIA PLAYER // MASTER STREAM BADGE SYSTEM</span>
    <span>OFFICIAL THEME SHOWCASE // ULTRA-HD 2400&times;1200</span>
  </div>
</div>
</body>
</html>"""

    tmp_html = os.path.join(SCRATCH_DIR, "temp_ecosystem_sync.html")
    tmp_png = os.path.join(SCRATCH_DIR, "temp_ecosystem_sync.png")
    out_jpg = os.path.join(PREVIEWS_DIR, "theme-ecosystem.jpg")

    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)

    if not os.path.exists(EDGE_PATH):
        print("Note: Edge not found on this system, keeping existing theme ecosystem image.")
        return

    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        "--force-device-scale-factor=1",
        "--window-size=2400,1200",
        f"--screenshot={tmp_png}",
        f"file:///{tmp_html.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(tmp_png):
        im = Image.open(tmp_png).convert("RGB")
        if im.size != (2400, 1200):
            im = im.crop((0, 0, 2400, 1200))
        im.save(out_jpg, "JPEG", quality=95, optimize=True)
        print(f"Updated Theme Ecosystem Showcase: {out_jpg} ({total_themes_count} Themes)")
        os.remove(tmp_png)

    if os.path.exists(tmp_html):
        os.remove(tmp_html)

    return True

def update_readme(stats, version):
    if not os.path.exists(README_MD):
        print(f"Warning: {README_MD} not found!")
        return False

    with open(README_MD, "r", encoding="utf-8") as f:
        readme = f.read()

    # SVG hero banner cache buster
    readme = re.sub(
        r'<img src="previews/nuvio-hero\.svg[^"]*"',
        f'<img src="previews/nuvio-hero.svg?v={version}"',
        readme
    )

    # Ecosystem preview cache buster and alt text
    readme = re.sub(
        r'<img src="previews/theme-ecosystem\.jpg[^"]*"\s+alt="[^"]*"',
        f'<img src="previews/theme-ecosystem.jpg?v={version}" alt="{stats["theme_count"]} Masterpiece Theme Universes"',
        readme
    )
    readme = re.sub(
        r'Every stream in Nuvio can be experienced across \*\*\d+ radically distinct physical material universes\*\*',
        f'Every stream in Nuvio can be experienced across **{stats["theme_count"]} radically distinct physical material universes**',
        readme
    )

    # Shields.io badges
    readme = re.sub(
        r'https://img\.shields\.io/badge/Badges-\d+_[^"-]+-9b51e0',
        f'https://img.shields.io/badge/Badges-{stats["badge_count"]}_Stream_Rules-9b51e0',
        readme
    )
    readme = re.sub(
        r'https://img\.shields\.io/badge/Assets-\d+_[^"-]+-3b82f6',
        f'https://img.shields.io/badge/Assets-{stats["asset_count"]}_WebP_Files-3b82f6',
        readme
    )
    readme = re.sub(
        r'https://img\.shields\.io/badge/Themes-\d+_[^"-]+-f59e0b',
        f'https://img.shields.io/badge/Themes-{stats["theme_count"]}_Universes-f59e0b',
        readme
    )

    # Text descriptions
    readme = re.sub(
        r'(\d+)\s+curated stream badges\s+\((\d+)\s+master WebP assets[^)]*\)\s+across\s+(\d+\+?)\s+global and regional streaming platforms[\s\S]*?and\s+(\d+\+?)\s+sovereign world languages and territories',
        f'{stats["badge_count"]} curated stream badges ({stats["asset_count"]} master WebP assets with fallbacks & aliases) across {stats["service_count"]}+ global and regional streaming platforms, cinema studios, 4K/8K formats, spatial audio codecs, high-speed Debrid services, torrent indexers, and {stats["lang_count"]} sovereign world languages and territories',
        readme
    )

    readme = re.sub(
        r'Mapped across \d+ distinct groups, aligning 1:1 with Nuvio\'s in-app badge counter \(exactly \d+ enabled badges\)',
        f'Mapped across {stats["group_count"]} distinct groups, aligning 1:1 with Nuvio\'s in-app badge counter (exactly {stats["badge_count"]} enabled badges)',
        readme
    )
    readme = re.sub(
        r'guaranteeing fallback support with \d+ high-resolution WebP files and aliases',
        f'guaranteeing fallback support with {stats["asset_count"]} high-resolution WebP files and aliases',
        readme
    )

    # All theme preview cards cache buster
    readme = re.sub(
        r'(\<img src="previews/preview-[a-z0-9\-]+\.jpg)(\?[^"]*)?(")',
        rf'\g<1>?v={version}\g<3>',
        readme
    )

    with open(README_MD, "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"Updated {README_MD} -> Synchronized stats and cache-busters with version {version}")
    return True

def update_github_metadata(stats, version):
    desc = f"{stats['badge_count']} master stream badges ({stats['asset_count']} WebP assets & aliases) across {stats['theme_count']} theme universes for Nuvio media player. OTT platforms, cinema studios, 4K/8K, HDR/DV, spatial audio, Debrid, torrent trackers & {stats['lang_count']} sovereign languages. Native 96px, zero latency, OLED dark-mode."
    cmd = f'gh repo edit jayedanik/nuvio-master-badge-system --description "{desc}"'
    stdout, rc = run_cmd(cmd, check=False)
    if rc == 0:
        print("Updated GitHub repository description successfully.")
    else:
        print("Note: GitHub repo edit skipped or failed (gh cli auth check).")

def create_release_and_backups(stats, version, changelog=None):
    print(f"\n--- Creating Release and Multi-Layer Backups for {version} ---")

    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(version)

    run_cmd("git add -A")
    stdout, rc = run_cmd(f'git commit -m "chore(sync): automated repository synchronization for {version} [skip ci]"', check=False)
    if rc == 0:
        print(f"Committed sync changes to main: {stdout.splitlines()[0]}")
    run_cmd("git push origin main", check=False)

    run_cmd("git branch -f backup-stable-master HEAD")
    run_cmd("git push origin backup-stable-master --force", check=False)
    print("Updated backup-stable-master branch on origin.")

    tag_msg = f"Master Release {version}: {stats['badge_count']} rules, {stats['asset_count']} WebP assets, {stats['lang_count']} languages, {stats['theme_count']} themes"
    run_cmd(f'git tag -f -a {version} -m "{tag_msg}"')
    run_cmd(f"git push origin {version} --force", check=False)
    print(f"Pushed git tag {version}.")

    os.makedirs(BACKUP_DIR, exist_ok=True)
    zip_path = os.path.join(BACKUP_DIR, f"nuvio-master-badge-system-{version}.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(REPO_ROOT):
            if ".git" in root.split(os.sep):
                continue
            for file in files:
                full = os.path.join(root, file)
                rel = os.path.relpath(full, REPO_ROOT)
                zf.write(full, rel)
    print(f"Created local ZIP: {zip_path} ({os.path.getsize(zip_path):,} bytes)")

    bundle_path = os.path.join(BACKUP_DIR, f"nuvio-master-badge-system-{version}.bundle")
    run_cmd(f'git bundle create "{bundle_path}" --all')
    print(f"Created local Git Bundle: {bundle_path}")

    rel_title = f"{version} — Master Badge System ({stats['badge_count']} Rules, {stats['lang_count']} Languages)"
    
    # Detailed Release Notes
    if changelog:
        detailed_changes = changelog.strip()
    else:
        detailed_changes = """- **StreamBridge Studio Markers Enhanced:** Fixed mismatched 1440p resolution with official Gold 2K studio asset (`res-1440.png`); restored authentic `HLG` (lilac), `10-BIT` (slate-blue), `IMAX` (magenta), `IMAX Enhanced`, and `SDR` (metallic gradient); restored authentic `FLAC` and `AAC` audio soundwave badges.
- **Perceived Size Normalization (Optical Area Balancing):** Solved uneven OTT sizing across all badges. Scaled and boosted compact/tall logos (Disney+, Apple TV, HBO Max, SonyLIV, Zee5, Toffee) so every OTT logo has uniform visual presence without clipping.
- **StreamBridge Sovereign Languages Harmonization:** All 110 sovereign world languages & territory flags updated to StreamBridge's signature 3-letter capital typography (`BEN`, `BD`, `ENG`, `HIN`, `JPN`, etc.) in `#8299b7`.
- **Multi-Theme Previews & 11-Theme Ecosystem:** Regenerated all 11 preview cards and `theme-ecosystem.jpg` showcase (2400×1200) to reflect the newly balanced OTT dimensions and studio markers."""

    rel_notes_md = f"""# Nuvio Master Badge System {version}

### Release Summary
- **Badge Rules:** {stats['badge_count']} active stream rules
- **Master Assets:** {stats['asset_count']} high-resolution WebP files
- **Languages & Territories:** {stats['lang_count']} sovereign world languages & territory flags
- **Physical Themes:** {stats['theme_count']} theme universes
- **Total Footprint:** {stats['size_mb']} MB (OLED-optimized, zero-latency WebP)

### Key Changes & Improvements
{detailed_changes}

---
*Synchronized across GitHub repository, release archives, previews, and in-app manifest files.*
"""

    notes_tmp_file = os.path.join(SCRATCH_DIR, "release_notes_tmp.md")
    with open(notes_tmp_file, "w", encoding="utf-8") as f:
        f.write(rel_notes_md)

    gh_cmd = f'gh release create {version} "{zip_path}" --title "{rel_title}" --notes-file "{notes_tmp_file}" -R jayedanik/nuvio-master-badge-system'
    stdout, rc = run_cmd(gh_cmd, check=False)
    if rc != 0:
        run_cmd(f'gh release upload {version} "{zip_path}" --clobber -R jayedanik/nuvio-master-badge-system', check=False)
        run_cmd(f'gh release edit {version} --title "{rel_title}" --notes-file "{notes_tmp_file}" -R jayedanik/nuvio-master-badge-system', check=False)
        print(f"Updated existing GitHub Release {version} with detailed changelog.")
    else:
        print(f"Created new GitHub Release: {version} with detailed changelog.")

    if os.path.exists(notes_tmp_file):
        try: os.remove(notes_tmp_file)
        except: pass

def main():
    parser = argparse.ArgumentParser(description="Synchronize all badge repository stats, banner, readme, and releases.")
    parser.add_argument("--version", type=str, default=None, help="Target release version (e.g. v3.5.0)")
    parser.add_argument("--release", action="store_true", help="Perform full release: update tag, push, create zip & bundle, update GitHub Release")
    parser.add_argument("--notes", type=str, default=None, help="Detailed changelog for GitHub Release")
    args = parser.parse_args()

    version = get_latest_version(args.version)

    # 1. Automatically theme missing or copied badges across all physical themes!
    auto_theme_missing_or_unthemed_badges()

    # 2. Inspect repository
    stats = inspect_repository()

    print("=== NUVIO MASTER BADGE SYSTEM SYNCHRONIZATION ===")
    print(f"Version:      {version}")
    print(f"Badge Rules:  {stats['badge_count']}")
    print(f"WebP Assets:  {stats['asset_count']}")
    print(f"Languages:    {stats['lang_count']}")
    print(f"Platforms:    {stats['service_count']}")
    print(f"Themes:       {stats['theme_count']}")
    print(f"Asset Size:   {stats['size_mb']} MB")
    print("=================================================")

    # 3. Synchronize SVG, Theme Ecosystem, README, GitHub Metadata
    update_hero_svg(stats, version)
    update_theme_ecosystem_preview(stats, version)
    update_readme(stats, version)
    update_github_metadata(stats, version)

    # 4. Release & Backups
    if args.release:
        create_release_and_backups(stats, version, changelog=args.notes)

    print("\n[OK] Universal synchronization completed successfully!")

if __name__ == "__main__":
    main()
