import os, subprocess, base64
import numpy as np
from PIL import Image

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
PREVIEWS_DIR = os.path.join(REPO_ROOT, "previews")
SCRIPT_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
BRAIN_DIR = r"C:\Users\yourt\.gemini\antigravity\brain\fb22a0fc-6924-43f9-ab27-8d6db9906f8f"

# 1. Fonts
with open(os.path.join(SCRIPT_DIR, "Ndot55-Regular.otf"), "rb") as f:
    b64_ndot = base64.b64encode(f.read()).decode("utf-8")

FONTS_DIR = r"C:\Users\yourt\.gemini\antigravity\brain\e3a87934-5f4d-4111-a44e-2f095bc5cbab\scratch\caveman\extension\fonts"
with open(os.path.join(FONTS_DIR, "geist-sans.woff2"), "rb") as f:
    b64_geist_sans = base64.b64encode(f.read()).decode("utf-8")
with open(os.path.join(FONTS_DIR, "geist-mono.woff2"), "rb") as f:
    b64_geist_mono = base64.b64encode(f.read()).decode("utf-8")

# 2. Glass texture for standard themes
GLASS_PATH = os.path.join(BRAIN_DIR, ".user_uploaded", "media_1794657324184_293a4cf2.jpg")
with open(GLASS_PATH, "rb") as f:
    b64_glass = base64.b64encode(f.read()).decode("utf-8")

# 3. Exact clean aurora background for Theme 12
CLEAN_BG_PATH = os.path.join(BRAIN_DIR, "exact_user_clean_bg.jpg")
with open(CLEAN_BG_PATH, "rb") as f:
    b64_aurora_bg = base64.b64encode(f.read()).decode("utf-8")

def make_cinema_bg():
    H, W = 1188, 2400
    y_coords, x_coords = np.meshgrid(np.arange(H), np.arange(W), indexing='ij')
    tx = x_coords / float(W)
    ty = y_coords / float(H)
    mask_text = np.clip((tx - 0.17) / 0.12, 0.0, 1.0)
    top_text = np.clip((ty - 0.13) / 0.08, 0.0, 1.0)
    text_prot = (0.16 + 0.84 * mask_text) * (0.35 + 0.65 * top_text)
    
    img = np.zeros((H, W, 3), dtype=np.float32)
    img[:, :, 0] = 6    # B
    img[:, :, 1] = 8    # G
    img[:, :, 2] = 16   # R
    
    orbs = [
        (1450, 580, 420, 1.0),
        (1950, 480, 360, 0.9),
        (1150, 680, 280, 0.75),
        (1700, 780, 320, 0.85),
        (2200, 720, 260, 0.7),
        (1300, 340, 220, 0.6),
        (1850, 260, 240, 0.65),
        (950, 520, 200, 0.5)
    ]
    for ox, oy, r, intensity in orbs:
        dist_sq = ((x_coords - ox)/float(r))**2 + ((y_coords - oy)/float(r))**2
        glow = np.exp(-dist_sq) * 220.0 * intensity
        img[:, :, 2] += glow * 1.0 * text_prot
        img[:, :, 1] += glow * 0.62 * text_prot
        img[:, :, 0] += glow * 0.12 * text_prot
        
    return np.clip(img, 0, 255).astype(np.uint8)

cin_bg_arr = make_cinema_bg()
im_cin = Image.fromarray(cin_bg_arr)
tmp_cin_p = os.path.join(SCRIPT_DIR, "tmp_cin_bg_master.jpg")
im_cin.save(tmp_cin_p, quality=96)
with open(tmp_cin_p, "rb") as f:
    b64_cinema_bg = base64.b64encode(f.read()).decode("utf-8")
if os.path.exists(tmp_cin_p): os.remove(tmp_cin_p)

GOOGLE_FONTS_LINK = "https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Chakra+Petch:wght@700&family=Cinzel+Decorative:wght@700&family=Cinzel:wght@700;800&family=Orbitron:wght@800;900&family=Oxanium:wght@800&family=Playfair+Display:wght@800;900&family=Righteous&family=Space+Grotesk:wght@700&family=Teko:wght@700&family=Inter:wght@800;900&display=swap"

THEME_CONFIGS = [
    {
        "id": "pristine",
        "name": "Pristine",
        "accent": "#38bdf8",
        "desc": "Ultra-clean floating OLED typography with official Dolby and HDR branding",
        "bg_type": "glass",
        "title_css": "font-family: 'Inter', sans-serif; font-weight: 900; background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 50%, #38bdf8 85%, #0284c7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.35));",
    },
    {
        "id": "studio-markers",
        "name": "Studio Markers",
        "accent": "#f59e0b",
        "desc": "Frameless ultra-legible studio monitor typography with vivid chromatic accents",
        "bg_type": "glass",
        "title_css": "font-family: 'Teko', sans-serif; font-weight: 700; font-size: 54px; letter-spacing: 2.5px; text-transform: uppercase; background: linear-gradient(135deg, #ffffff 15%, #fde047 50%, #eab308 80%, #ca8a04 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(250, 204, 21, 0.35));",
    },
    {
        "id": "gmk-keycaps",
        "name": "GMK Keycaps",
        "accent": "#a78bfa",
        "desc": "Double-shot mechanical keycaps with scooped spherical dish & textured matte borders",
        "bg_type": "glass",
        "title_css": "font-family: 'Space Grotesk', sans-serif; font-weight: 700; letter-spacing: -1px; background: linear-gradient(135deg, #ffffff 0%, #e9d5ff 35%, #c084fc 70%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(167, 139, 250, 0.4));",
    },
    {
        "id": "rgb-keycaps",
        "name": "RGB Keycaps",
        "accent": "#00f2fe",
        "desc": "Dual-layer translucent pudding keycaps with dynamic cybernetic gradient underglow",
        "bg_type": "glass",
        "title_css": "font-family: 'Chakra Petch', sans-serif; font-weight: 700; letter-spacing: 1px; background: linear-gradient(135deg, #00f2fe 0%, #4facfe 35%, #c084fc 70%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(0, 242, 254, 0.5));",
    },
    {
        "id": "cinema-ticket",
        "name": "Cinema Ticket",
        "accent": "#f59e0b",
        "desc": "Authentic perforated cinema admission stubs with 24K gold foil trim & serial stamp",
        "bg_type": "cinema_bokeh",
        "title_css": "font-family: 'Playfair Display', serif; font-weight: 900; background: linear-gradient(135deg, #fffbeb 0%, #fef08a 35%, #f59e0b 70%, #b45309 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(245, 158, 11, 0.4));",
    },
    {
        "id": "enamel-pins",
        "name": "Enamel Pins",
        "accent": "#fbbf24",
        "desc": "Jewelry-grade metal lapel badges with 24K gold brass framing & polished mineral enamel",
        "bg_type": "glass",
        "title_css": "font-family: 'Cinzel', serif; font-weight: 800; letter-spacing: 1.2px; background: linear-gradient(135deg, #ffffff 0%, #fef9c3 30%, #eab308 70%, #a16207 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(234, 179, 8, 0.4));",
    },
    {
        "id": "vhs-tape",
        "name": "VHS Tape",
        "accent": "#ef4444",
        "desc": "Authentic 1980s analog magnetic cassette labels with vintage tracking stripes & barcode",
        "bg_type": "glass",
        "title_css": "font-family: 'Righteous', cursive; background: linear-gradient(135deg, #fdf2f8 0%, #f472b6 35%, #ec4899 70%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(236, 72, 153, 0.45));",
    },
    {
        "id": "clapperboard",
        "name": "Clapperboard",
        "accent": "#e2e8f0",
        "desc": "Matte wooden movie production slates with bold diagonal acrylic chevrons",
        "bg_type": "glass",
        "title_css": "font-family: 'Bebas Neue', sans-serif; font-size: 54px; letter-spacing: 2px; background: linear-gradient(135deg, #ffffff 15%, #f1f5f9 50%, #cbd5e1 80%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(241, 245, 249, 0.4));",
    },
    {
        "id": "audiophile-vfd",
        "name": "Audiophile VFD",
        "accent": "#22d3ee",
        "desc": "Vintage Japanese vacuum fluorescent display tube glass with glowing cyan phosphor",
        "bg_type": "glass",
        "title_css": "font-family: 'Orbitron', sans-serif; font-weight: 900; letter-spacing: 2px; text-transform: uppercase; background: linear-gradient(135deg, #ecfdf5 0%, #a7f3d0 30%, #2dd4bf 70%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(45, 212, 191, 0.5));",
    },
    {
        "id": "neotokyo-tag",
        "name": "Neo-Tokyo Tag",
        "accent": "#f43f5e",
        "desc": "Distressed industrial cyberpunk inspection tags with hazard stripes & serial stamps",
        "bg_type": "glass",
        "title_css": "font-family: 'Oxanium', sans-serif; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; background: linear-gradient(135deg, #fff1f2 0%, #fb7185 30%, #ec4899 70%, #8b5cf6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(236, 72, 153, 0.45));",
    },
    {
        "id": "criterion-leather",
        "name": "Criterion Leather",
        "accent": "#d97706",
        "desc": "Handcrafted archival leather book spine binding with deep gold leaf hot-stamping",
        "bg_type": "glass",
        "title_css": "font-family: 'Cinzel Decorative', serif; font-weight: 700; letter-spacing: 1px; background: linear-gradient(135deg, #ffffff 0%, #fef08a 25%, #f59e0b 65%, #92400e 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(245, 158, 11, 0.4));",
    },
    {
        "id": "liquid-glass",
        "name": "VisionOS Pure Liquid Glass",
        "accent": "#38bdf8",
        "desc": "WWDC25 droplet optics with 3D convex liquid meniscus curvature, caustic refraction & smoked translucent core",
        "bg_type": "aurora",
        "title_css": "font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-weight: 800; letter-spacing: -0.5px; background: linear-gradient(90deg, #38bdf8 0%, #818cf8 28%, #c084fc 58%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.45));",
    },
    {
        "id": "washi-tape",
        "name": "Artisan Japanese Washi Tape",
        "accent": "#fb7185",
        "desc": "Handmade washi tape rolls with gold leaf hot-stamping, mulberry fiber texture & Japanese calligraphy",
        "bg_type": "glass",
        "title_css": "font-family: 'Cinzel', serif; font-weight: 800; letter-spacing: 1px; background: linear-gradient(135deg, #ffffff 10%, #ffe4e6 45%, #fb7185 75%, #e11d48 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(251, 113, 133, 0.45));",
    }
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

def render_html_preview(cfg):
    theme_id = cfg["id"]
    title_name = cfg["name"]
    accent_hex = cfg["accent"]
    desc = cfg["desc"]
    title_css = cfg["title_css"]
    bg_type = cfg.get("bg_type", "glass")

    if bg_type == "cinema_bokeh":
        bg_style = f"url('data:image/jpeg;base64,{b64_cinema_bg}') center / cover no-repeat, #08090d"
    elif bg_type == "aurora":
        bg_style = f"url('data:image/jpeg;base64,{b64_aurora_bg}') center / cover no-repeat, #08090d"
    else:
        bg_style = f"""
          radial-gradient(1400px 600px at 15% 0%, {accent_hex}18 0%, transparent 65%),
          radial-gradient(1000px 500px at 85% 10%, rgba(255, 255, 255, 0.03) 0%, transparent 55%),
          linear-gradient(180deg, rgba(8, 10, 16, 0.86) 0%, rgba(5, 6, 10, 0.91) 100%),
          url('data:image/jpeg;base64,{b64_glass}') center / cover no-repeat,
          #08090d
        """

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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{GOOGLE_FONTS_LINK}" rel="stylesheet">
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
    background: {bg_style};
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
    {title_css}
  }}
  
  .header-desc {{
    font-size: 20px;
    color: rgba(255, 255, 255, 0.55);
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
    border-top: 1px solid rgba(255, 255, 255, 0.10);
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
    color: rgba(255, 255, 255, 0.45);
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
    filter: drop-shadow(0 8px 18px rgba(0, 0, 0, 0.65));
  }}
  
  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 36px;
    font-family: 'Geist Mono', monospace;
    font-size: 13.5px;
    letter-spacing: 1.8px;
    color: rgba(255, 255, 255, 0.35);
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
        "--headless=new",
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
            im_cropped.convert("RGB").save(out_jpg, quality=96)
            print(f"[OK] Razor-sharp render: {theme_id:20} -> {out_jpg} (Height: {im_cropped.size[1]}px)")
        os.remove(tmp_png)
    if os.path.exists(tmp_html):
        os.remove(tmp_html)

def execute():
    print("=== RENDERING ALL 13 THEMES NATIVELY AT 2400px WITH BESPOKE TYPOGRAPHY & GRADIENTS ===")
    for cfg in THEME_CONFIGS:
        render_html_preview(cfg)
    print("=== ALL 13 THEMES RENDERED WITH RAZOR-SHARP PRECISION ===")

if __name__ == "__main__":
    execute()
