import os, subprocess, base64
from PIL import Image

REPO_ROOT = "C:/Users/yourt/.gemini/antigravity/scratch/nuvio-badges-original"
PREVIEWS_DIR = os.path.join(REPO_ROOT, "previews")
SCRIPT_DIR = "C:/Users/yourt/.gemini/antigravity/scratch"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BRAIN_DIR = r"C:\Users\yourt\.gemini\antigravity\brain\fb22a0fc-6924-43f9-ab27-8d6db9906f8f"

# Fonts
with open(os.path.join(SCRIPT_DIR, "Ndot55-Regular.otf"), "rb") as f:
    b64_ndot = base64.b64encode(f.read()).decode("utf-8")

FONTS_DIR = r"C:\Users\yourt\.gemini\antigravity\brain\e3a87934-5f4d-4111-a44e-2f095bc5cbab\scratch\caveman\extension\fonts"
with open(os.path.join(FONTS_DIR, "geist-sans.woff2"), "rb") as f:
    b64_geist_sans = base64.b64encode(f.read()).decode("utf-8")
with open(os.path.join(FONTS_DIR, "geist-mono.woff2"), "rb") as f:
    b64_geist_mono = base64.b64encode(f.read()).decode("utf-8")

# Glass texture
GLASS_PATH = r"C:\Users\yourt\.gemini\antigravity\brain\fb22a0fc-6924-43f9-ab27-8d6db9906f8f\.user_uploaded\media_1794657324184_293a4cf2.jpg"
with open(GLASS_PATH, "rb") as f:
    b64_glass = base64.b64encode(f.read()).decode("utf-8")

THEMES = [
    ("pristine", "Pristine", "#38bdf8",
     "Ultra-clean floating OLED typography with official Dolby and HDR branding"),
    ("studio-markers", "Studio Markers", "#f59e0b",
     "Frameless ultra-legible studio monitor typography with vivid chromatic accents"),
    ("gmk-keycaps", "GMK Keycaps", "#a78bfa",
     "Double-shot mechanical keycaps with scooped spherical dish & textured matte borders"),
    ("rgb-keycaps", "RGB Keycaps", "#00f2fe",
     "Dual-layer translucent pudding keycaps with dynamic cybernetic gradient underglow"),
    ("cinema-ticket", "Cinema Ticket", "#f59e0b",
     "Authentic perforated cinema admission stubs with 24K gold foil trim & serial stamp"),
    ("enamel-pins", "Enamel Pins", "#fbbf24",
     "Jewelry-grade metal lapel badges with 24K gold brass framing & polished mineral enamel"),
    ("vhs-tape", "VHS Tape", "#ef4444",
     "Authentic 1980s analog magnetic cassette labels with vintage tracking stripes & barcode"),
    ("clapperboard", "Clapperboard", "#e2e8f0",
     "Matte wooden movie production slates with bold diagonal acrylic chevrons"),
    ("audiophile-vfd", "Audiophile VFD", "#22d3ee",
     "Vintage Japanese vacuum fluorescent display tube glass with glowing cyan phosphor"),
    ("neotokyo-tag", "Neo-Tokyo Tag", "#f43f5e",
     "Distressed industrial cyberpunk inspection tags with hazard stripes & serial stamps"),
    ("criterion-leather", "Criterion Leather", "#d97706",
     "Handcrafted archival leather book spine binding with deep gold leaf hot-stamping"),
    ("liquid-glass", "VisionOS Liquid Glass", "#38bdf8",
     "WWDC25 droplet optics with 3D convex liquid meniscus curvature, caustic refraction & smoked translucent core"),
]

TIERS = [
    ("HERO", "Best quality. Gold & master marks, max 2-3 per stream",
     ["4k", "remux", "dolby-vision", "dolby-atmos", "imax", "dtsx", "cached", "live"]),
    ("CORE", "The facts people pick a stream by",
     ["1080p", "web-dl", "bluray", "hdr10plus", "hdr10", "hlg", "truehd", "ddp", "7.1", "5.1", "av1", "dual", "extended", "3d"]),
    ("STREAMING", "Official global & regional platform sources",
     ["netflix", "jiohotstar", "shudder", "prime", "disney", "appletv", "max", "hulu", "peacock", "crunchyroll", "hoichoi", "chorki", "mubi"]),
    ("STUDIOS", "Theatrical cinema & television production houses",
     ["warnerbros", "universal", "mgm", "sonypictures", "a24", "ghibli", "redchillies", "paramount_studio", "toho", "lionsgate", "bbc", "amc"]),
    ("LANGUAGES", "Sovereign territory flags & multi-language audio tracks",
     ["bangladesh-flag", "india-flag", "usa-flag", "uk", "japan-flag", "korean", "france", "germany", "nepali-flag", "saudi-arabia-flag", "spain", "italy", "brazil", "russia"])
]

def render_theme_preview(theme_id, title_name, accent_hex, desc):
    badge_dir = os.path.join(REPO_ROOT, "themes", theme_id, "badges") if theme_id != "pristine" else os.path.join(REPO_ROOT, "badges")
    
    tiers_html = ""
    for tier_name, tier_sub, badges in TIERS:
        badges_html = ""
        for b_name in badges:
            b_path = os.path.join(badge_dir, f"{b_name}.webp")
            if not os.path.exists(b_path):
                b_path = os.path.join(REPO_ROOT, "badges", f"{b_name}.webp")
            if os.path.exists(b_path):
                with open(b_path, "rb") as bf:
                    b64_img = base64.b64encode(bf.read()).decode("utf-8")
                badges_html += f'<div class="badge-item"><img src="data:image/webp;base64,{b64_img}" alt="{b_name}" /></div>\n'

        tiers_html += f"""
        <div class="tier-row">
          <div class="tier-meta">
            <div class="tier-title">{tier_name}</div>
            <div class="tier-desc">{tier_sub}</div>
          </div>
          <div class="tier-badges">
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
    font-family: 'NDot55';
    src: url('data:font/otf;base64,{b64_ndot}') format('opentype');
  }}
  @font-face {{
    font-family: 'Geist Sans';
    src: url('data:font/woff2;base64,{b64_geist_sans}') format('woff2');
    font-weight: 100 900;
  }}
  @font-face {{
    font-family: 'Geist Mono';
    src: url('data:font/woff2;base64,{b64_geist_mono}') format('woff2');
    font-weight: 100 900;
  }}
  
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    margin: 0;
    padding: 0;
    background: transparent !important;
    width: 2400px;
  }}
  
  body {{
    font-family: 'Geist Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #ffffff;
    -webkit-font-smoothing: antialiased;
  }}
  
  .canvas {{
    width: 2400px;
    padding: 72px 96px 56px 96px;
    position: relative;
    background: 
      radial-gradient(1400px 600px at 15% 0%, {accent_hex}16 0%, transparent 65%),
      radial-gradient(1000px 500px at 85% 10%, rgba(255, 255, 255, 0.03) 0%, transparent 55%),
      linear-gradient(180deg, rgba(8, 10, 16, 0.86) 0%, rgba(5, 6, 10, 0.91) 100%),
      url('data:image/jpeg;base64,{b64_glass}') center / cover no-repeat,
      #08090d;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
  }}
  
  .header {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding-bottom: 40px;
  }}
  
  .title {{
    display: flex;
    align-items: center;
    gap: 18px;
    line-height: 1.1;
  }}
  
  .brand-name {{
    font-family: 'NDot55', monospace;
    font-size: 48px;
    letter-spacing: 2.2px;
    color: #ffffff;
    text-transform: uppercase;
  }}
  
  .dot {{
    color: rgba(255, 255, 255, 0.25);
    font-size: 38px;
  }}
  
  .theme-name {{
    font-size: 48px;
    font-weight: 700;
    letter-spacing: -1px;
    color: {accent_hex};
  }}
  
  .header-desc {{
    font-size: 20px;
    color: rgba(255, 255, 255, 0.44);
    letter-spacing: -0.2px;
  }}
  
  .tiers-container {{
    display: flex;
    flex-direction: column;
  }}
  
  .tier-row {{
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 52px;
    align-items: center;
    padding: 26px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
  }}
  
  .tier-meta {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  
  .tier-title {{
    font-family: 'NDot55', monospace;
    font-size: 22px;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    color: #ffffff;
  }}
  
  .tier-desc {{
    font-size: 14.5px;
    line-height: 1.45;
    color: rgba(255, 255, 255, 0.38);
    letter-spacing: -0.1px;
  }}
  
  .tier-badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 16px 20px;
    align-items: center;
  }}
  
  .badge-item {{
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  
  .badge-item img {{
    height: 68px;
    width: auto;
    object-fit: contain;
    filter: drop-shadow(0 8px 18px rgba(0, 0, 0, 0.70));
  }}
  
  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 36px;
    font-family: 'Geist Mono', monospace;
    font-size: 13.5px;
    letter-spacing: 1.8px;
    color: rgba(255, 255, 255, 0.28);
    text-transform: uppercase;
  }}
</style>
</head>
<body>
  <div id="canvas" class="canvas">
    <div class="header">
      <div class="title">
        <span class="brand-name">NUVIO MASTER BADGES</span>
        <span class="dot">·</span>
        <span class="theme-name">{title_name}</span>
      </div>
      <div class="header-desc">{desc}. 512 badges in this style; a sample shown by tier.</div>
    </div>
    
    <div class="tiers-container">
      {tiers_html}
    </div>
    
    <div class="footer">
      <span>Official Dolby, IMAX, Studio & Streaming marks</span>
      <span>96px Native Master • Zero CPU Overhead • Hardware Accelerated</span>
    </div>
  </div>
</body>
</html>"""

    tmp_html = os.path.join(SCRIPT_DIR, f"temp_nothing_{theme_id}.html")
    tmp_png = os.path.join(SCRIPT_DIR, f"temp_nothing_{theme_id}.png")
    out_jpg = os.path.join(PREVIEWS_DIR, f"preview-{theme_id}.jpg")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)
        
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=2400,2500",
        "--default-background-color=00000000",
        f"--screenshot={tmp_png}",
        tmp_html
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(tmp_png):
        im = Image.open(tmp_png)
        bbox = im.getbbox()
        if bbox:
            im_cropped = im.crop((0, 0, 2400, bbox[3]))
            im_cropped.convert("RGB").save(out_jpg, quality=95)
            print(f"[OK] Rendered {theme_id:20} -> {out_jpg} (Height: {im_cropped.size[1]}px)")
        os.remove(tmp_png)
    if os.path.exists(tmp_html):
        os.remove(tmp_html)

def render_ecosystem():
    ECOSYSTEM_TIERS = [
        ("OLED & MONITORS", "Pristine floating vectors & frameless studio monitor tags", [
            ("badges", "4k"),
            ("badges", "dolby-vision"),
            ("badges", "netflix"),
            ("themes/studio-markers/badges", "1080p"),
            ("themes/studio-markers/badges", "hdr10plus"),
            ("themes/studio-markers/badges", "warnerbros"),
            ("badges", "bangladesh-flag")
        ]),
        ("KEYBOARD KEYCAPS", "Double-shot PBT spherical dish & neon RGB translucent underglow", [
            ("themes/gmk-keycaps/badges", "4k"),
            ("themes/gmk-keycaps/badges", "dolby-atmos"),
            ("themes/gmk-keycaps/badges", "shudder"),
            ("themes/rgb-keycaps/badges", "remux"),
            ("themes/rgb-keycaps/badges", "imax"),
            ("themes/rgb-keycaps/badges", "disney"),
            ("themes/gmk-keycaps/badges", "japanese")
        ]),
        ("ANALOGUE CINEMA", "1980s perforated admission stubs & aged magnetic tape labels", [
            ("themes/cinema-ticket/badges", "4k"),
            ("themes/cinema-ticket/badges", "truehd"),
            ("themes/cinema-ticket/badges", "mgm"),
            ("themes/vhs-tape/badges", "1080p"),
            ("themes/vhs-tape/badges", "dtsx"),
            ("themes/vhs-tape/badges", "prime"),
            ("themes/vhs-tape/badges", "uk")
        ]),
        ("JEWELRY & SLATES", "Cast metal 24K brass enamel lapels & wooden director chevrons", [
            ("themes/enamel-pins/badges", "dolby-vision"),
            ("themes/enamel-pins/badges", "dolby-atmos"),
            ("themes/enamel-pins/badges", "sonypictures"),
            ("themes/clapperboard/badges", "4k"),
            ("themes/clapperboard/badges", "imax"),
            ("themes/clapperboard/badges", "a24"),
            ("themes/enamel-pins/badges", "korean")
        ]),
        ("VFD, TECH & LEATHER", "Cyan phosphor vacuum tubes, cyberpunk inspection tags & archival leather", [
            ("themes/audiophile-vfd/badges", "4k"),
            ("themes/audiophile-vfd/badges", "flac"),
            ("themes/neotokyo-tag/badges", "remux"),
            ("themes/neotokyo-tag/badges", "cached"),
            ("themes/criterion-leather/badges", "dolby-vision"),
            ("themes/criterion-leather/badges", "criterion"),
            ("themes/criterion-leather/badges", "nepali-flag")
        ])
    ]

    tiers_html = ""
    for tier_name, tier_sub, badges in ECOSYSTEM_TIERS:
        badges_html = ""
        for rel_dir, b_name in badges:
            b_path = os.path.join(REPO_ROOT, rel_dir, f"{b_name}.webp")
            if not os.path.exists(b_path):
                b_path = os.path.join(REPO_ROOT, "badges", f"{b_name}.webp")
            if os.path.exists(b_path):
                with open(b_path, "rb") as bf:
                    b64_img = base64.b64encode(bf.read()).decode("utf-8")
                badges_html += f'<div class="badge-item"><img src="data:image/webp;base64,{b64_img}" alt="{b_name}" /></div>\n'

        tiers_html += f"""
        <div class="tier-row">
          <div class="tier-meta">
            <div class="tier-title">{tier_name}</div>
            <div class="tier-desc">{tier_sub}</div>
          </div>
          <div class="tier-badges">
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
    font-family: 'NDot55';
    src: url('data:font/otf;base64,{b64_ndot}') format('opentype');
  }}
  @font-face {{
    font-family: 'Geist Sans';
    src: url('data:font/woff2;base64,{b64_geist_sans}') format('woff2');
    font-weight: 100 900;
  }}
  @font-face {{
    font-family: 'Geist Mono';
    src: url('data:font/woff2;base64,{b64_geist_mono}') format('woff2');
    font-weight: 100 900;
  }}
  
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    margin: 0;
    padding: 0;
    background: transparent !important;
    width: 2400px;
  }}
  
  body {{
    font-family: 'Geist Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    color: #ffffff;
    -webkit-font-smoothing: antialiased;
  }}
  
  .canvas {{
    width: 2400px;
    padding: 72px 96px 56px 96px;
    position: relative;
    background: 
      radial-gradient(1400px 600px at 15% 0%, rgba(56, 189, 248, 0.16) 0%, transparent 65%),
      radial-gradient(1000px 500px at 85% 10%, rgba(167, 139, 250, 0.08) 0%, transparent 55%),
      linear-gradient(180deg, rgba(8, 10, 16, 0.86) 0%, rgba(5, 6, 10, 0.91) 100%),
      url('data:image/jpeg;base64,{b64_glass}') center / cover no-repeat,
      #08090d;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
  }}
  
  .header {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding-bottom: 40px;
  }}
  
  .title {{
    display: flex;
    align-items: center;
    gap: 18px;
    line-height: 1.1;
  }}
  
  .brand-name {{
    font-family: 'NDot55', monospace;
    font-size: 48px;
    letter-spacing: 2.2px;
    color: #ffffff;
    text-transform: uppercase;
  }}
  
  .dot {{
    color: rgba(255, 255, 255, 0.25);
    font-size: 38px;
  }}
  
  .theme-name {{
    font-size: 48px;
    font-weight: 700;
    letter-spacing: -1px;
    color: #38bdf8;
  }}
  
  .header-desc {{
    font-size: 20px;
    color: rgba(255, 255, 255, 0.44);
    letter-spacing: -0.2px;
  }}
  
  .tiers-container {{
    display: flex;
    flex-direction: column;
  }}
  
  .tier-row {{
    display: grid;
    grid-template-columns: 320px 1fr;
    gap: 52px;
    align-items: center;
    padding: 26px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
  }}
  
  .tier-meta {{
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  
  .tier-title {{
    font-family: 'NDot55', monospace;
    font-size: 22px;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    color: #ffffff;
  }}
  
  .tier-desc {{
    font-size: 14.5px;
    line-height: 1.45;
    color: rgba(255, 255, 255, 0.38);
    letter-spacing: -0.1px;
  }}
  
  .tier-badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 16px 20px;
    align-items: center;
  }}
  
  .badge-item {{
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  
  .badge-item img {{
    height: 68px;
    width: auto;
    object-fit: contain;
    filter: drop-shadow(0 8px 18px rgba(0, 0, 0, 0.70));
  }}
  
  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 36px;
    font-family: 'Geist Mono', monospace;
    font-size: 13.5px;
    letter-spacing: 1.8px;
    color: rgba(255, 255, 255, 0.28);
    text-transform: uppercase;
  }}
</style>
</head>
<body>
  <div id="canvas" class="canvas">
    <div class="header">
      <div class="title">
        <span class="brand-name">NUVIO MASTER BADGES</span>
        <span class="dot">·</span>
        <span class="theme-name">Theme Architecture & Ecosystem</span>
      </div>
      <div class="header-desc">11 master physical material universes. Zero runtime CPU overhead; choose an aesthetic matching your theater setup.</div>
    </div>
    
    <div class="tiers-container">
      {tiers_html}
    </div>
    
    <div class="footer">
      <span>Official Dolby, IMAX, Studio & Streaming marks</span>
      <span>96px Native Master • Zero CPU Overhead • Hardware Accelerated</span>
    </div>
  </div>
</body>
</html>"""

    tmp_html = os.path.join(SCRIPT_DIR, "temp_nothing_ecosystem.html")
    tmp_png = os.path.join(SCRIPT_DIR, "temp_nothing_ecosystem.png")
    out_jpg = os.path.join(PREVIEWS_DIR, "theme-ecosystem.jpg")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)
        
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=2400,2500",
        "--default-background-color=00000000",
        f"--screenshot={tmp_png}",
        tmp_html
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(tmp_png):
        im = Image.open(tmp_png)
        bbox = im.getbbox()
        if bbox:
            im_cropped = im.crop((0, 0, 2400, bbox[3]))
            im_cropped.convert("RGB").save(out_jpg, quality=95)
            print(f"[OK] Rendered theme-ecosystem.jpg (Height: {im_cropped.size[1]}px)")
        os.remove(tmp_png)
    if os.path.exists(tmp_html):
        os.remove(tmp_html)

def main():
    print("=== RENDERING NOTHING DOT MATRIX BRANDED PREVIEWS FOR ALL 11 THEMES + ECOSYSTEM ===")
    render_ecosystem()
    for theme_id, title_name, accent_hex, desc in THEMES:
        render_theme_preview(theme_id, title_name, accent_hex, desc)
    print("=== ALL COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
