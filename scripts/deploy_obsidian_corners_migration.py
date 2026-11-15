import os, sys, subprocess, io, hashlib, shutil
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEMES_DIR = os.path.join(REPO_ROOT, "themes")
PREVIEWS_DIR = os.path.join(REPO_ROOT, "previews")
ECO_HASH_ORIG = "edbe9ec3468f2eb0bc69322d7361c5cd41a0eaf115afcb3b2da402136aa60c30"
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
sys.path.append(SCRATCH_DIR)
import build_full_multitype_dark_washi_theme as bfm
rolls = bfm.get_tuned_box_rolls()
roll_keys = list(rolls.keys())

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

def get_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def apply_obsidian_corners(im, radius=26):
    im = im.convert("RGBA")
    w, h = im.size
    scale = 4
    mask = Image.new("L", (w * scale, h * scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, w * scale - 1, h * scale - 1], radius=radius * scale, fill=255)
    mask = mask.resize((w, h), Image.Resampling.LANCZOS)
    
    orig_a = im.split()[3]
    a1 = np.array(mask, dtype=np.float32) / 255.0
    a2 = np.array(orig_a, dtype=np.float32) / 255.0
    fa = (a1 * a2 * 255.0).astype(np.uint8)
    final_a = Image.fromarray(fa, "L")
    
    r, g, b, _ = im.split()
    return Image.merge("RGBA", (r, g, b, final_a))

def make_washi_tape_obsidian(w_px, h_px, roll_tex, seed=42, radius_px=26):
    sw, sh = w_px * SCALE, h_px * SCALE
    m_x = 2 * SCALE
    m_y = 3 * SCALE
    rad = radius_px * SCALE
    
    mask = Image.new("L", (sw, sh), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([m_x, m_y, sw - m_x - 1, sh - m_y - 1], radius=rad, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.8 * SCALE))
    
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
        
    tape = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    tape.paste(tiled, (0, 0), mask)
    
    shadow_mask = mask.filter(ImageFilter.GaussianBlur(1.8 * SCALE))
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 180), (0, 0), shadow_mask)
    
    comp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    comp.paste(shadow, (0, int(2.0 * SCALE)), shadow)
    comp.paste(tape, (0, 0), tape)
    return comp.resize((w_px, h_px), Image.Resampling.LANCZOS)

def process_washi_badge(filename):
    name = filename[:-5]
    if name == "live":
        src_live = os.path.join(BADGES_DIR, "live.webp")
        dst_live = os.path.join(THEMES_DIR, "washi-tape", "badges", "live.webp")
        shutil.copyfile(src_live, dst_live)
        return name, True

    src_p = os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return name, False

    orig = Image.open(src_p).convert("RGBA")
    bbox = orig.getbbox()
    glyph = orig.crop(bbox) if bbox else orig

    tgt_h = 66
    sc = min(tgt_h / float(glyph.height), 200.0 / float(glyph.width))
    gw_w = max(1, int(round(glyph.width * sc)))
    gw_h = max(1, int(round(glyph.height * sc)))
    glyph_sc = glyph.resize((gw_w, gw_h), Image.Resampling.LANCZOS)

    tw = max(gw_w + 34, 105)
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(name))
    roll_key = roll_keys[seed % len(roll_keys)]
    roll_tex = rolls[roll_key]["tex"]

    tape = make_washi_tape_obsidian(tw, NATIVE_H, roll_tex, seed=seed, radius_px=26)
    badge = Image.new("RGBA", (tw, NATIVE_H), (0, 0, 0, 0))
    badge.alpha_composite(tape)

    gx = (tw - gw_w) // 2
    gy = (NATIVE_H - gw_h) // 2
    g_alpha = glyph_sc.split()[3]

    deep_mask = g_alpha.filter(ImageFilter.GaussianBlur(2.0))
    deep_sh = Image.new("RGBA", (gw_w, gw_h), (0, 0, 0, 0))
    deep_sh.paste((0, 0, 0, 220), (0, 0), deep_mask)
    badge.alpha_composite(deep_sh, (gx, gy + 2))
    badge.alpha_composite(glyph_sc, (gx, gy))

    out_p = os.path.join(THEMES_DIR, "washi-tape", "badges", filename)
    badge.save(out_p, "WEBP", quality=95, method=6)
    return name, True

def process_neotokyo_tag():
    print("--> Processing Neo-Tokyo Tag from authentic commit 1b1b3b21...")
    out = subprocess.run(["git", "ls-tree", "-r", "--name-only", "1b1b3b21", "themes/neotokyo-tag/badges"],
                         cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    tree_files = [line.strip() for line in out.stdout.splitlines() if line.strip()]

    dst_badges = os.path.join(THEMES_DIR, "neotokyo-tag", "badges")
    dst_sharp = os.path.join(THEMES_DIR, "neotokyo-tag", "sharp")
    os.makedirs(dst_badges, exist_ok=True)
    os.makedirs(dst_sharp, exist_ok=True)

    src_live = os.path.join(BADGES_DIR, "live.webp")

    count = 0
    for tf in tree_files:
        fn = os.path.basename(tf)
        if fn == "live.webp":
            shutil.copyfile(src_live, os.path.join(dst_badges, "live.webp"))
            shutil.copyfile(src_live, os.path.join(dst_sharp, "live.webp"))
            continue

        proc = subprocess.run(["git", "show", f"1b1b3b21:{tf}"],
                              cwd=REPO_ROOT, capture_output=True, check=True)
        im = Image.open(io.BytesIO(proc.stdout)).convert("RGBA")
        
        # Save authentic sharp copy
        im.save(os.path.join(dst_sharp, fn), "WEBP", quality=95, method=6)
        
        # Apply Obsidian corners to badges copy
        obs = apply_obsidian_corners(im, radius=26)
        obs.save(os.path.join(dst_badges, fn), "WEBP", quality=95, method=6)
        count += 1

    # Mirror aliases
    aliases = {
        "usa.webp": "usa-flag.webp",
        "korea.webp": "korean-flag.webp",
        "russia.webp": "russian-flag.webp",
        "india.webp": "india-flag.webp",
        "germany.webp": "german-flag.webp",
        "france.webp": "french-flag.webp",
        "japan.webp": "japanese-flag.webp",
        "spain.webp": "spanish-flag.webp",
        "italy.webp": "italian-flag.webp",
        "nepal.webp": "nepali-flag.webp",
        "apple.webp": "appletv.webp",
        "blu-ray.webp": "bluray.webp",
        "korea-flag.webp": "korean-flag.webp",
        "japan-flag.webp": "japanese-flag.webp",
        "usa-flag.webp": "english-flag.webp" # fallback if needed
    }
    for alias, target in aliases.items():
        tp = os.path.join(dst_badges, target)
        if os.path.exists(tp):
            shutil.copyfile(tp, os.path.join(dst_badges, alias))
            shutil.copyfile(os.path.join(dst_sharp, target), os.path.join(dst_sharp, alias))

    print(f"    Neo-Tokyo Tag completed: {count} badges rendered with authentic layout & Obsidian corners.")

def process_theme_badges(theme_name):
    print(f"--> Processing {theme_name} with Obsidian corners (r=26px)...")
    bdir = os.path.join(THEMES_DIR, theme_name, "badges")
    if not os.path.exists(bdir):
        print(f"    Warning: {bdir} not found!")
        return

    src_live = os.path.join(BADGES_DIR, "live.webp")
    files = [f for f in os.listdir(bdir) if f.endswith(".webp")]
    count = 0
    for fn in files:
        fp = os.path.join(bdir, fn)
        if fn == "live.webp":
            shutil.copyfile(src_live, fp)
            continue
        im = Image.open(fp).convert("RGBA")
        obs = apply_obsidian_corners(im, radius=26)
        obs.save(fp, "WEBP", quality=95, method=6)
        count += 1
    print(f"    {theme_name} completed: {count} badges processed.")

def main():
    print("==================================================================")
    print("BATCH MIGRATION: 10 THEMES TO OBSIDIAN CARD CORNERS (r=26px)")
    print("EXEMPT THEMES: Pristine Master, Liquid Glass, Studio Markers")
    print("==================================================================")

    # 1. Pre-assertion
    p_eco = os.path.join(PREVIEWS_DIR, "theme-ecosystem.jpg")
    p_live = os.path.join(BADGES_DIR, "live.webp")
    assert get_hash(p_eco) == ECO_HASH_ORIG, "CRITICAL: theme-ecosystem.jpg baseline failed!"
    assert get_hash(p_live) == LIVE_HASH_ORIG, "CRITICAL: live.webp baseline failed!"

    # 2. Process Neo-Tokyo Tag from authentic commit 1b1b3b21
    process_neotokyo_tag()

    # 3. Process Washi Tape with Obsidian 4-Corner shape
    print("--> Processing Washi Tape with Obsidian 4 corners...")
    washi_files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(process_washi_badge, washi_files))
    print(f"    Washi Tape completed: {len(results)} badges rendered.")

    # 4. Process the remaining 8 themes
    themes_to_process = [
        "audiophile-vfd",
        "criterion-leather",
        "vhs-tape",
        "clapperboard",
        "cinema-ticket",
        "gmk-keycaps",
        "rgb-keycaps",
        "enamel-pins"
    ]
    for t in themes_to_process:
        process_theme_badges(t)

    # 5. Post-assertion: verify ALL live.webp across all themes
    print("--> Verifying integrity of live.webp across entire repository...")
    live_checks = [os.path.join(BADGES_DIR, "live.webp")]
    for t in os.listdir(THEMES_DIR):
        lp = os.path.join(THEMES_DIR, t, "badges", "live.webp")
        if os.path.exists(lp):
            live_checks.append(lp)
        sp = os.path.join(THEMES_DIR, t, "sharp", "live.webp")
        if os.path.exists(sp):
            live_checks.append(sp)

    for lp in live_checks:
        h = get_hash(lp)
        assert h == LIVE_HASH_ORIG, f"CRITICAL: live.webp altered at {lp}!"

    # 6. Post-assertion: verify theme-ecosystem.jpg untouched
    assert get_hash(p_eco) == ECO_HASH_ORIG, "CRITICAL: theme-ecosystem.jpg was altered!"
    print(f"[SUCCESS] All assertions passed! Verified {len(live_checks)} live.webp files & theme-ecosystem.jpg.")

if __name__ == "__main__":
    main()
