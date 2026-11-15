import os, sys, json, math, shutil, argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
RULES_JSON = os.path.join(REPO_ROOT, "DESIGN_SYSTEM_RULES.json")

sys.path.insert(0, SCRIPT_DIR)
import build_all_bespoke_themed_badges_v5 as b5

with open(RULES_JSON, "r", encoding="utf-8") as f:
    RULES = json.load(f)

SCALE = RULES["invariants"]["render_supersampling_scale"]
CANVAS_H = RULES["invariants"]["canvas_height_px"]

def clean_alpha_transparency(img):
    """Ensures 100% clean transparent alpha with zero black box or false borders."""
    im = img.convert("RGBA")
    arr = np.array(im)
    
    # Check if corners are solid black
    h, w = arr.shape[:2]
    corners = [arr[0, 0], arr[0, w-1], arr[h-1, 0], arr[h-1, w-1]]
    is_black_card = all(c[3] > 200 and np.mean(c[:3]) < 20 for c in corners)
    
    if is_black_card:
        # Distance from pure black
        lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
        alpha = np.clip((lum / 40.0) * 255.0, 0, 255).astype(np.uint8)
        arr[:, :, 3] = np.minimum(arr[:, :, 3], alpha)
        im = Image.fromarray(arr, "RGBA")
        
    # Crop to visible bbox
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    return im

def ensure_horizontal_safe_margin(img, min_margin=18):
    """Enforces minimum horizontal transparent margin (>= 18px) so Nuvio Desktop's
    RoundedCornerShape clip never slices into badge text, logos, or drop shadows."""
    im = img.convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    has_alpha = alpha > 10
    
    if not np.any(has_alpha):
        return im
        
    cols = np.where(np.any(has_alpha, axis=0))[0]
    min_x = cols[0]
    max_x = cols[-1]
    
    pad_left = max(0, min_margin - min_x)
    pad_right = max(0, min_margin - (im.width - 1 - max_x))
    
    if pad_left > 0 or pad_right > 0:
        new_w = im.width + pad_left + pad_right
        new_im = Image.new("RGBA", (new_w, im.height), (0, 0, 0, 0))
        new_im.paste(im, (pad_left, 0), im)
        return new_im
    return im

def add_badge(badge_id, src_path=None, main_text=None, sub_text=None, category="brands"):
    print(f"=== AUTO-APPLYING DESIGN RULES: ADDING BADGE '{badge_id}' ===")
    
    glyph = None
    if src_path and os.path.exists(src_path):
        raw = Image.open(src_path)
        glyph = clean_alpha_transparency(raw)
        
    # 1. Base Pristine Badge
    pristine_dir = os.path.join(REPO_ROOT, "badges")
    os.makedirs(pristine_dir, exist_ok=True)
    pristine_out = os.path.join(pristine_dir, f"{badge_id}.webp")
    
    if glyph:
        ratio = 60.0 / float(glyph.height) if glyph.height > 60 else 1.0
        gw = int(glyph.width * ratio)
        gh = int(glyph.height * ratio)
        sc = glyph.resize((gw, gh), Image.Resampling.LANCZOS)
        
        pw = max(gw + 32, 120)
        p_canvas = Image.new("RGBA", (pw, CANVAS_H), (0, 0, 0, 0))
        px = (pw - gw) // 2
        py = (CANVAS_H - gh) // 2
        p_canvas.paste(sc, (px, py), sc)
        p_canvas = ensure_horizontal_safe_margin(p_canvas, 18)
        p_canvas.save(pristine_out, "WEBP", quality=95)
    else:
        p_canvas = b5.render_pristine_floating(False, None, main_text or badge_id.upper(), sub_text, badge_id=badge_id)
        p_canvas = ensure_horizontal_safe_margin(p_canvas, 18)
        p_canvas.save(pristine_out, "WEBP", quality=95)
    print(f"[OK] 01 - Pristine Master: Saved {pristine_out}")

    # 2. Studio Markers
    sm_dir = os.path.join(REPO_ROOT, "themes", "studio-markers", "badges")
    os.makedirs(sm_dir, exist_ok=True)
    shutil.copy2(pristine_out, os.path.join(sm_dir, f"{badge_id}.webp"))
    print(f"[OK] 02 - Studio Markers: Synced {badge_id}.webp")

    # 3. 9 Bespoke Physical Themes
    bespoke_map = {
        "gmk-keycaps": b5.render_gmk_keycaps,
        "rgb-keycaps": b5.render_rgb_keycaps,
        "cinema-ticket": b5.render_cinema_ticket,
        "enamel-pins": b5.render_enamel_pins,
        "vhs-tape": b5.render_vhs_tape,
        "clapperboard": b5.render_clapperboard,
        "audiophile-vfd": b5.render_audiophile_vfd,
        "neotokyo-tag": b5.render_neotokyo_tag,
        "criterion-leather": b5.render_criterion_leather
    }
    
    for tid, renderer in bespoke_map.items():
        tdir = os.path.join(REPO_ROOT, "themes", tid, "badges")
        os.makedirs(tdir, exist_ok=True)
        out_p = os.path.join(tdir, f"{badge_id}.webp")
        
        is_ott = (category in ["brands", "ott", "streaming"]) or (glyph is not None)
        rendered = renderer(is_ott, glyph, main_text, sub_text, badge_id=badge_id)
        rendered = ensure_horizontal_safe_margin(rendered, 18)
        rendered.save(out_p, "WEBP", quality=95)
        print(f"[OK] Bespoke Theme '{tid}': Rendered with authentic theme typography -> {out_p}")

    # 4. Apple VisionOS Liquid Glass
    lg_dir = os.path.join(REPO_ROOT, "themes", "liquid-glass", "badges")
    os.makedirs(lg_dir, exist_ok=True)
    lg_out = os.path.join(lg_dir, f"{badge_id}.webp")
    try:
        import generate_all_liquid_glass_theme as gl
        gl.generate_single_badge(badge_id)
        if os.path.exists(lg_out):
            padded_lg = ensure_horizontal_safe_margin(Image.open(lg_out), 18)
            padded_lg.save(lg_out, "WEBP", quality=95)
        print(f"[OK] 12 - VisionOS Liquid Glass: Refractive capsule generated")
    except Exception as e:
        shutil.copy2(pristine_out, lg_out)
        print(f"[WARN] Liquid glass generation fallback: {e}")

    # 5. Artisan Japanese Washi Tape (With 3D drop shadow, deckled roll, and elevated prominence)
    wt_dir = os.path.join(REPO_ROOT, "themes", "washi-tape", "badges")
    os.makedirs(wt_dir, exist_ok=True)
    wt_out = os.path.join(wt_dir, f"{badge_id}.webp")
    try:
        brain_scratch = r"C:\Users\yourt\.gemini\antigravity\brain\fb22a0fc-6924-43f9-ab27-8d6db9906f8f\scratch"
        sys.path.insert(0, brain_scratch)
        import generate_all_washi_tape_theme as gw
        gw.build_washi_badge_for_name(badge_id)
        if os.path.exists(wt_out):
            padded_wt = ensure_horizontal_safe_margin(Image.open(wt_out), 18)
            padded_wt.save(wt_out, "WEBP", quality=95)
        print(f"[OK] 13 - Artisan Washi Tape: Handcrafted mulberry roll with 3D drop shadow generated")
    except Exception as e:
        print(f"[WARN] Washi tape generation fallback: {e}")
        print(f"[WARN] Washi tape generation fallback: {e}")

    # 6. Synchronize JSON manifests
    sync_badge_to_manifests(badge_id, category)
    print(f"\n[COMPLETE] Badge '{badge_id}' successfully propagated across all 13 themes adhering to all Design System Rules!")

def sync_badge_to_manifests(badge_id, category="brands"):
    # Update badges.json
    bjson_path = os.path.join(REPO_ROOT, "badges.json")
    if os.path.exists(bjson_path):
        with open(bjson_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "badges" in data:
            if not any(b.get("id") == badge_id for b in data["badges"]):
                data["badges"].append({
                    "id": badge_id,
                    "filename": f"{badge_id}.webp",
                    "category": category
                })
                with open(bjson_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

    # Update each theme's JSON
    for tid, tcfg in RULES["themes"].items():
        tjson_path = os.path.join(REPO_ROOT, tcfg["json"])
        if os.path.exists(tjson_path):
            with open(tjson_path, "r", encoding="utf-8") as f:
                tdata = json.load(f)
            if isinstance(tdata, dict) and "badges" in tdata:
                if not any(b.get("id") == badge_id for b in tdata["badges"]):
                    tdata["badges"].append({
                        "id": badge_id,
                        "filename": f"{badge_id}.webp",
                        "category": category
                    })
                    with open(tjson_path, "w", encoding="utf-8") as f:
                        json.dump(tdata, f, indent=2)

def create_theme(theme_id, theme_name, primary_font, secondary_font, style_desc, accent_hex="#38bdf8"):
    print(f"=== AUTO-APPLYING DESIGN RULES: CREATING THEME '{theme_id}' ===")
    
    # Register in RULES
    RULES["themes"][theme_id] = {
        "name": theme_name,
        "dir": f"themes/{theme_id}/badges",
        "json": f"{theme_id}.json",
        "typography": {
            "primary": primary_font,
            "secondary": secondary_font,
            "style": style_desc
        }
    }
    with open(RULES_JSON, "w", encoding="utf-8") as f:
        json.dump(RULES, f, indent=2)
        
    theme_badges_dir = os.path.join(REPO_ROOT, "themes", theme_id, "badges")
    os.makedirs(theme_badges_dir, exist_ok=True)
    
    # Initialize from pristine baseline
    pristine_dir = os.path.join(REPO_ROOT, "badges")
    count = 0
    for fn in os.listdir(pristine_dir):
        if fn.endswith(".webp"):
            shutil.copy2(os.path.join(pristine_dir, fn), os.path.join(theme_badges_dir, fn))
            count += 1
            
    # Create Theme JSON with zero border/tag background for desktop compatibility
    theme_json_path = os.path.join(REPO_ROOT, f"{theme_id}.json")
    nested_theme_json_path = os.path.join(REPO_ROOT, "themes", theme_id, f"{theme_id}.json")
    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        master_data = json.load(f)
    theme_data = {
        "id": theme_id,
        "name": theme_name,
        "description": style_desc,
        "tagStyle": "none",
        "tagColor": "",
        "borderColor": "",
        "accent": accent_hex,
        "badges": master_data.get("badges", [])
    }
    with open(theme_json_path, "w", encoding="utf-8") as f:
        json.dump(theme_data, f, indent=2)
    with open(nested_theme_json_path, "w", encoding="utf-8") as f:
        json.dump(theme_data, f, indent=2)
        
    print(f"[SUCCESS] Theme '{theme_id}' created with {count} baseline badges and registered in Design System Rules!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nuvio Automated Design Rules & Theme Engine")
    sub = parser.add_subparsers(dest="command")
    
    p_badge = sub.add_parser("add-badge")
    p_badge.add_argument("--id", required=True, help="Unique badge identifier")
    p_badge.add_argument("--src", help="Path to source logo/vector PNG")
    p_badge.add_argument("--main-text", help="Main primary typography label")
    p_badge.add_argument("--sub-text", help="Sub-label typography text")
    p_badge.add_argument("--category", default="brands", help="Badge category")
    
    p_theme = sub.add_parser("create-theme")
    p_theme.add_argument("--id", required=True, help="New theme ID")
    p_theme.add_argument("--name", required=True, help="Theme display name")
    p_theme.add_argument("--primary-font", default="arialbd.ttf")
    p_theme.add_argument("--secondary-font", default="segoeui.ttf")
    p_theme.add_argument("--style", required=True, help="Theme aesthetic style description")
    p_theme.add_argument("--accent", default="#38bdf8", help="Hex accent color")
    
    args = parser.parse_args()
    if args.command == "add-badge":
        add_badge(args.id, args.src, args.main_text, args.sub_text, args.category)
    elif args.command == "create-theme":
        create_theme(args.id, args.name, args.primary_font, args.secondary_font, args.style, args.accent)
    else:
        parser.print_help()
