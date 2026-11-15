import os, sys, random, shutil, hashlib
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "washi-tape")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
sys.path.append(SCRATCH_DIR)
import build_full_multitype_dark_washi_theme as bfm

rolls = bfm.get_tuned_box_rolls()
roll_keys = list(rolls.keys())

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

def make_obsidian_washi_card(w_px, h_px, roll_tex, seed=42, radius_px=26):
    sw, sh = w_px * SCALE, h_px * SCALE
    m_x = 2 * SCALE
    m_y = 3 * SCALE
    rad = radius_px * SCALE
    
    # 1. Main outer card mask
    mask = Image.new("L", (sw, sh), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([m_x, m_y, sw - m_x - 1, sh - m_y - 1], radius=rad, fill=255)
    
    # 2. Tile washi texture inside mask
    r_w, r_h = roll_tex.size
    t_ratio = float(sh) / float(r_h)
    scaled_r_w = max(1, int(round(r_w * t_ratio)))
    tex_scaled = roll_tex.resize((scaled_r_w, sh), Image.Resampling.LANCZOS)
    tiled = Image.new("RGBA", (sw, sh))
    x_offset = int((seed * 37) % scaled_r_w)
    curr_x = -x_offset
    while curr_x < sw:
        tiled.paste(tex_scaled, (curr_x, 0))
        curr_x += scaled_r_w
        
    card = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    card.paste(tiled, (0, 0), mask)
    
    # 3. Obsidian top specular sheen (gradient on top 45% of card)
    sheen = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(sheen)
    for y in range(m_y, m_y + int(sh * 0.45)):
        alpha_val = int(35 * (1.0 - (y - m_y) / (sh * 0.45)))
        sdraw.line([(m_x, y), (sw - m_x - 1, y)], fill=(255, 255, 255, alpha_val))
    sheen_arr = np.array(sheen)
    mask_arr = np.array(mask) / 255.0
    sheen_arr[..., 3] = (sheen_arr[..., 3] * mask_arr).astype(np.uint8)
    sheen = Image.fromarray(sheen_arr, "RGBA")
    card.alpha_composite(sheen)
    
    # 4. Obsidian 1.5px border highlight
    b_mask = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(b_mask)
    b_width = int(1.5 * SCALE)
    bdraw.rounded_rectangle([m_x, m_y, sw - m_x - 1, sh - m_y - 1], radius=rad, outline=(255, 255, 255, 80), width=b_width)
    card.alpha_composite(b_mask)
    
    # 5. Obsidian soft drop shadow
    shadow_mask = mask.filter(ImageFilter.GaussianBlur(1.8 * SCALE))
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 180), (0, 0), shadow_mask)
    
    comp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    comp.paste(shadow, (0, int(2.0 * SCALE)), shadow)
    comp.paste(card, (0, 0), card)
    return comp.resize((w_px, h_px), Image.Resampling.LANCZOS)

def process_badge(filename):
    name = filename[:-5]
    if name == "live":
        src_live = os.path.join(BADGES_DIR, "live.webp")
        dst_live = os.path.join(THEME_BADGES_DIR, "live.webp")
        shutil.copyfile(src_live, dst_live)
        return name, True

    src_p = os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return name, False

    orig = Image.open(src_p).convert("RGBA")
    bbox = orig.getbbox()
    glyph = orig.crop(bbox) if bbox else orig

    # Crisp compact sizing
    target_h = 60
    sc = min(target_h / float(glyph.height), 180.0 / float(glyph.width))
    gw_w = max(1, int(round(glyph.width * sc)))
    gw_h = max(1, int(round(glyph.height * sc)))
    glyph_sc = glyph.resize((gw_w, gw_h), Image.Resampling.LANCZOS)

    tw = max(gw_w + 38, 115)
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(name))
    roll_key = roll_keys[seed % len(roll_keys)]
    roll_tex = rolls[roll_key]["tex"]

    card = make_obsidian_washi_card(tw, NATIVE_H, roll_tex, seed=seed, radius_px=26)

    gx = (tw - gw_w) // 2
    gy = (NATIVE_H - gw_h) // 2
    g_alpha = glyph_sc.split()[3]

    deep_mask = g_alpha.filter(ImageFilter.GaussianBlur(1.8))
    deep_sh = Image.new("RGBA", (gw_w, gw_h), (0, 0, 0, 0))
    deep_sh.paste((0, 0, 0, 220), (0, 0), deep_mask)
    card.alpha_composite(deep_sh, (gx, gy + 2))
    card.alpha_composite(glyph_sc, (gx, gy))

    out_p = os.path.join(THEME_BADGES_DIR, filename)
    card.save(out_p, "WEBP", quality=95, method=6)
    return name, True

def main():
    print("==================================================")
    print("DEPLOYING AUTHENTIC OBSIDIAN-SHAPED WASHI TAPE THEME")
    print("==================================================")
    files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(process_badge, files))
    print(f"Rendered {len(results)} badges with exact Obsidian card shape & washi texture.")
    
    # Verify live.webp
    dst_live = os.path.join(THEME_BADGES_DIR, "live.webp")
    h = hashlib.sha256(open(dst_live, "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, "CRITICAL: washi live.webp hash mismatch!"
    print("[SUCCESS] live.webp 100% verified untouched.")

if __name__ == "__main__":
    main()
