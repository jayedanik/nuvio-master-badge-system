import os, sys, math, random, shutil, hashlib, subprocess, base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "washi-tape")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
PREVIEWS_DIR = os.path.join(REPO_ROOT, "previews")
LOCK_FILE = os.path.join(REPO_ROOT, "SYSTEM_INTEGRITY.lock")
BRAIN_DIR = r"C:\Users\yourt\.gemini\antigravity\brain\fb22a0fc-6924-43f9-ab27-8d6db9906f8f"
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

sys.path.append(SCRATCH_DIR)
import build_full_multitype_dark_washi_theme as bfm
rolls = bfm.get_tuned_box_rolls()
roll_keys = list(rolls.keys())

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

BRAND_GLOW_COLORS = {
    "netflix": (229, 9, 20),
    "prime": (0, 168, 225),
    "primevideo": (0, 168, 225),
    "disney": (30, 110, 255),
    "disneyplus": (30, 110, 255),
    "jiohotstar": (20, 80, 240),
    "crunchyroll": (244, 117, 33),
    "hoichoi": (229, 9, 20),
    "chorki": (255, 190, 24),
    "peacock": (0, 164, 228),
    "hulu": (28, 231, 131),
    "appletv": (245, 245, 250),
    "apple": (245, 245, 250),
    "max": (0, 43, 231),
    "hbomax": (0, 43, 231),
    "shudder": (220, 38, 38),
    "mubi": (0, 200, 240),
    "warnerbros": (0, 77, 179),
    "universal": (59, 130, 246),
    "mgm": (218, 165, 32),
    "sonypictures": (230, 235, 245),
    "a24": (255, 255, 255),
    "ghibli": (56, 189, 248),
    "redchillies": (239, 68, 68),
    "paramount": (0, 100, 255),
    "paramount_studio": (0, 100, 255),
    "toho": (239, 68, 68),
    "lionsgate": (217, 119, 6),
    "bbc": (239, 68, 68),
    "amc": (217, 119, 6),
    "amcplus": (217, 119, 6),
    "dolby-vision": (245, 180, 50),
    "dolby-atmos": (255, 220, 100),
    "realdebrid": (245, 158, 11),
    "alldebrid": (16, 185, 129),
    "premiumize": (59, 130, 246),
    "torbox": (168, 85, 247),
    "debridlink": (14, 165, 233),
    "1337x": (220, 38, 38),
    "torrentgalaxy": (147, 51, 234),
    "yts": (22, 163, 74),
    "eztv": (37, 99, 235),
    "rarbg": (30, 64, 175),
    "bongo": (239, 68, 68),
    "toffee": (234, 179, 8)
}

TECH_GLOW_COLORS = {
    "4k": (255, 215, 80),
    "remux": (255, 220, 120),
    "dolby-atmos": (255, 220, 100),
    "imax": (0, 170, 230),
    "dtsx": (249, 115, 22),
    "cached": (210, 140, 50),
    "live": (239, 68, 68),
    "1080p": (220, 235, 255),
    "web-dl": (220, 235, 255),
    "bluray": (0, 168, 225),
    "hdr10plus": (245, 158, 11),
    "hdr10": (245, 158, 11),
    "hlg": (234, 179, 8),
    "truehd": (180, 225, 255),
    "ddp": (180, 225, 255),
    "7.1": (180, 225, 255),
    "5.1": (180, 225, 255),
    "av1": (16, 185, 129),
    "dual": (217, 119, 6),
    "extended": (217, 119, 6),
    "3d": (168, 85, 247),
    "bangladesh-flag": (16, 185, 129),
    "india-flag": (249, 115, 22),
    "usa-flag": (59, 130, 246),
    "uk": (37, 99, 235),
    "japan-flag": (239, 68, 68),
    "korean": (59, 130, 246),
    "france": (37, 99, 235),
    "germany": (245, 158, 11),
    "nepali-flag": (220, 38, 38),
    "saudi-arabia-flag": (16, 185, 129),
    "spain": (239, 68, 68),
    "italy": (16, 185, 129),
    "brazil": (234, 179, 8),
    "russia": (59, 130, 246)
}

def make_washi_tape(w_px, h_px, roll_tex, seed=42):
    sw, sh = w_px * SCALE, h_px * SCALE
    pad_y = 10 * SCALE
    y_t = pad_y
    y_b = sh - pad_y
    rnd = random.Random(seed)
    num_steps = 32
    left_pts = []
    base_l = 10 * SCALE
    for i in range(num_steps + 1):
        y = y_t + (y_b - y_t) * (i / float(num_steps))
        jitter = (rnd.random() - 0.5) * 3.2 * SCALE + math.sin(i * 0.5) * 1.8 * SCALE
        left_pts.append((base_l + jitter, y))
    right_pts = []
    base_r = sw - 10 * SCALE
    for i in range(num_steps, -1, -1):
        y = y_t + (y_b - y_t) * (i / float(num_steps))
        jitter = (rnd.random() - 0.5) * 3.2 * SCALE + math.sin(i * 0.6 + 1.2) * 1.8 * SCALE
        right_pts.append((base_r + jitter, y))
    poly = left_pts + right_pts
    mask = Image.new("L", (sw, sh), 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.0 * SCALE))
    
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
    
    shadow_mask = mask.filter(ImageFilter.GaussianBlur(2.0 * SCALE))
    shadow = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 190), (0, 0), shadow_mask)
    comp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    comp.paste(shadow, (0, int(2.5 * SCALE)), shadow)
    comp.paste(tape, (0, 0), tape)
    return comp.resize((w_px, h_px), Image.Resampling.LANCZOS)

def get_glow_color(name, im):
    if name in BRAND_GLOW_COLORS:
        return BRAND_GLOW_COLORS[name]
    if name in TECH_GLOW_COLORS:
        return TECH_GLOW_COLORS[name]
    arr = np.array(im)
    vis = arr[:, :, 3] > 40
    if np.sum(vis) < 10:
        return (255, 235, 175)
    rgb = arr[vis, :3]
    std_c = np.std(rgb, axis=1)
    lum = 0.299 * rgb[:, 0] + 0.587 * rgb[:, 1] + 0.114 * rgb[:, 2]
    if np.mean(std_c) < 18 and np.mean(lum) > 180:
        return (255, 235, 175)
    median_c = np.median(rgb, axis=0)
    r, g, b = int(median_c[0]), int(median_c[1]), int(median_c[2])
    return (max(r, 45), max(g, 45), max(b, 45))

def render_max_cover_badge(name):
    # Rule 1: live.webp is NEVER wrapped in a badge or tape!
    if name == "live":
        src_live = os.path.join(BADGES_DIR, "live.webp")
        dst_live = os.path.join(THEME_BADGES_DIR, "live.webp")
        shutil.copyfile(src_live, dst_live)
        return name, True

    src_p = os.path.join(BADGES_DIR, f"{name}.webp")
    if not os.path.exists(src_p):
        return name, False

    orig = Image.open(src_p).convert("RGBA")
    bbox = orig.getbbox()
    glyph = orig.crop(bbox) if bbox else orig

    # Approved Prototype 2: target_h = 72, safe width max 220
    target_h = 72
    sc = min(target_h / float(glyph.height), 220.0 / float(glyph.width))
    gw_w = max(1, int(round(glyph.width * sc)))
    gw_h = max(1, int(round(glyph.height * sc)))
    glyph_sc = glyph.resize((gw_w, gw_h), Image.Resampling.LANCZOS)

    # Tight wrap around glyph with 18px deckled edge safety margin
    tw = max(gw_w + 36, 110)

    # Deterministic roll texture
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(name))
    roll_key = roll_keys[seed % len(roll_keys)]
    roll_tex = rolls[roll_key]["tex"]

    tape = make_washi_tape(tw, NATIVE_H, roll_tex, seed=seed)
    badge = Image.new("RGBA", (tw, NATIVE_H), (0, 0, 0, 0))
    badge.alpha_composite(tape)

    gx = (tw - gw_w) // 2
    gy = (NATIVE_H - gw_h) // 2
    g_alpha = glyph_sc.split()[3]

    # Chromatic glow + 3D elevation + occlusion shadows
    glow_rgb = get_glow_color(name, glyph_sc)
    outer_mask = g_alpha.filter(ImageFilter.GaussianBlur(3.5))
    outer_glow = Image.new("RGBA", (gw_w, gw_h), (0, 0, 0, 0))
    outer_glow.paste((glow_rgb[0], glow_rgb[1], glow_rgb[2], 210), (0, 0), outer_mask)
    badge.alpha_composite(outer_glow, (gx, gy))

    deep_mask = g_alpha.filter(ImageFilter.GaussianBlur(3.0))
    deep_sh = Image.new("RGBA", (gw_w, gw_h), (0, 0, 0, 0))
    deep_sh.paste((0, 0, 0, 220), (0, 0), deep_mask)
    badge.alpha_composite(deep_sh, (gx, gy + 3))

    occ_mask = g_alpha.filter(ImageFilter.GaussianBlur(1.2))
    occ_sh = Image.new("RGBA", (gw_w, gw_h), (0, 0, 0, 0))
    occ_sh.paste((0, 0, 0, 240), (0, 0), occ_mask)
    badge.alpha_composite(occ_sh, (gx, gy + 1))

    badge.alpha_composite(glyph_sc, (gx, gy))

    out_p = os.path.join(THEME_BADGES_DIR, f"{name}.webp")
    badge.save(out_p, "WEBP", quality=95, method=6)
    return name, True

def main():
    print("==================================================")
    print("DEPLOYING MAXIMUM FULL-COVER (72px) WASHI TAPE THEME")
    print("==================================================")
    
    os.makedirs(THEME_BADGES_DIR, exist_ok=True)
    master_badges = [f[:-5] for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]
    print(f"Total master badges to process: {len(master_badges)}")

    success_count = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        for name, ok in executor.map(render_max_cover_badge, master_badges):
            if ok:
                success_count += 1
                if success_count % 100 == 0:
                    print(f"Processed {success_count}/{len(master_badges)} badges...")

    print(f"Successfully rendered {success_count} badges!")

    # Mirror essential aliases
    aliases = [
        ("bangladesh-flag", "bangladesh"),
        ("bangladesh-flag", "bengali"),
        ("hindi-flag", "india-flag"),
        ("hindi-flag", "india"),
        ("hindi-flag", "hindi"),
        ("english-flag", "usa-flag"),
        ("english-flag", "english"),
        ("english-flag", "usa"),
        ("japanese-flag", "japan-flag"),
        ("japanese-flag", "japanese"),
        ("japanese-flag", "japan"),
        ("korean-flag", "korean"),
        ("korean-flag", "korea-flag"),
        ("korean-flag", "korea"),
        ("french-flag", "france"),
        ("french-flag", "french"),
        ("german-flag", "germany"),
        ("german-flag", "german"),
        ("nepali-flag", "nepali"),
        ("nepali-flag", "nepal"),
        ("arabic-flag", "saudi-arabia-flag"),
        ("arabic-flag", "arabic"),
        ("spanish-flag", "spain"),
        ("spanish-flag", "spanish"),
        ("italian-flag", "italy"),
        ("italian-flag", "italian"),
        ("brazilian-flag", "brazil"),
        ("brazilian-flag", "portuguese"),
        ("russian-flag", "russia"),
        ("russian-flag", "russian"),
        ("prime", "primevideo"),
        ("max", "hbomax"),
        ("dtsx", "dts-x"),
        ("dtsx", "dts"),
        ("web-dl", "webdl"),
        ("bluray", "blu-ray"),
        ("paramount_studio", "paramount"),
    ]

    for src, dst in aliases:
        src_p = os.path.join(THEME_BADGES_DIR, f"{src}.webp")
        dst_p = os.path.join(THEME_BADGES_DIR, f"{dst}.webp")
        if os.path.exists(src_p):
            shutil.copyfile(src_p, dst_p)

    # CRITICAL: live.webp MUST BE UNTOUCHED RAW BROADCAST BEACON
    src_live = os.path.join(BADGES_DIR, "live.webp")
    dst_live = os.path.join(THEME_BADGES_DIR, "live.webp")
    shutil.copyfile(src_live, dst_live)
    print("[RULE ENFORCED] live.webp has ZERO badge/tape container. Untouched broadcast beacon deployed.")

    total_deployed = len([f for f in os.listdir(THEME_BADGES_DIR) if f.endswith(".webp")])
    print(f"Total deployed badges in themes/washi-tape/badges: {total_deployed}")

    # Copy rendered master preview to previews/preview-washi-tape.jpg
    src_preview = os.path.join(BRAIN_DIR, "preview_washi_tape_max_full_cover.jpg")
    dst_preview = os.path.join(PREVIEWS_DIR, "preview-washi-tape.jpg")
    if os.path.exists(src_preview):
        shutil.copyfile(src_preview, dst_preview)
        print("Updated previews/preview-washi-tape.jpg with master full-cover preview.")

    # Update SYSTEM_INTEGRITY.lock for washi-tape hashes
    def get_hash(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()

    lines = []
    with open(LOCK_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                lines.append(line)
                continue
            parts = line_str.split("  ", 1)
            if len(parts) == 2:
                _, rel_p = parts
                if "washi-tape" in rel_p:
                    full_p = os.path.join(REPO_ROOT, rel_p)
                    if os.path.exists(full_p):
                        new_h = get_hash(full_p)
                        lines.append(f"{new_h}  {rel_p}\n")
                        continue
            lines.append(line)

    with open(LOCK_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Updated SYSTEM_INTEGRITY.lock with new washi-tape hashes.")

if __name__ == "__main__":
    main()
