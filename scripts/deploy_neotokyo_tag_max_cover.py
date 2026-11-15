import os, sys, math, random, shutil, hashlib, subprocess, base64
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "neotokyo-tag")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
PREVIEWS_DIR = os.path.join(REPO_ROOT, "previews")
LOCK_FILE = os.path.join(REPO_ROOT, "SYSTEM_INTEGRITY.lock")
BRAIN_DIR = r"C:\Users\yourt\.gemini\antigravity\brain\fb22a0fc-6924-43f9-ab27-8d6db9906f8f"
LOCAL_SCRATCH = os.path.join(BRAIN_DIR, "scratch")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE
pad_y = 6 * SCALE
h = TOTAL_H - pad_y * 2
pad_left = 18 * SCALE
pad_right = 14 * SCALE
hazard_pink = (255, 45, 85, 255)

font_micro = ImageFont.truetype("bahnschrift.ttf", 8 * SCALE)

ROOT_MAP = {
    "webdl": "web-dl.webp",
    "webrip": "webrip.webp",
    "dv-only": "dv-only.webp",
    "dts-x": "dtsx.webp",
    "dts-hd": "dts-hd.webp",
    "real-debrid": "realdebrid.webp",
    "bengali": "bangladesh-flag.webp",
    "hindi": "hindi-flag.webp",
    "english": "english-flag.webp",
    "japanese": "japanese-flag.webp",
    "korean": "korean-flag.webp",
    "chinese": "chinese-flag.webp",
    "spanish": "spanish-flag.webp",
    "german": "german-flag.webp",
}

def render_neotokyo_badge(name):
    # Rule: live is NEVER wrapped in a badge or tag container!
    if name == "live":
        src_live = os.path.join(BADGES_DIR, "live.webp")
        dst_live = os.path.join(THEME_BADGES_DIR, "live.webp")
        shutil.copyfile(src_live, dst_live)
        return name, True

    src_name = ROOT_MAP.get(name, f"{name}.webp")
    src_p = os.path.join(BADGES_DIR, src_name)
    if not os.path.exists(src_p):
        src_p = os.path.join(THEME_BADGES_DIR, f"{name}.webp")
    if not os.path.exists(src_p):
        return name, False

    orig = Image.open(src_p).convert("RGBA")
    bbox = orig.getbbox()
    glyph = orig.crop(bbox) if bbox else orig

    # Max full-cover ceiling: target_h = 66px (in native scale, or 66*SCALE in 4x)
    target_h_sc = int(66 * SCALE)
    max_w_sc = int(180 * SCALE)
    sc = min(target_h_sc / float(glyph.height), max_w_sc / float(glyph.width))
    gw = max(1, int(round(glyph.width * sc)))
    gh = max(1, int(round(glyph.height * sc)))
    glyph_sc = glyph.resize((gw, gh), Image.Resampling.LANCZOS)

    total_w = max(gw + pad_left + pad_right, int(105 * SCALE))

    canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # Techwear dark slate chassis with subtle tech outline
    draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(4.5*SCALE), fill=(14, 16, 22, 255), outline=(42, 48, 60, 255), width=int(1.5*SCALE))

    # Left hazard stripe
    draw.rectangle([4*SCALE, pad_y + int(2.5*SCALE), 4*SCALE + int(3.5*SCALE), pad_y + h - int(2.5*SCALE)], fill=hazard_pink)

    # Top micro header
    clean_id = name.replace("-flag", "").replace("_studio", "").upper()
    micro_hdr = f"SYS // TAG // {clean_id[:10]}"
    draw.text((12 * SCALE, pad_y + 3 * SCALE), micro_hdr, font=font_micro, fill=(130, 145, 170, 230))

    # Position glyph
    content_cy = pad_y + int(10 * SCALE) + (h - int(10 * SCALE)) // 2
    gx = pad_left + (total_w - pad_left - pad_right - gw) // 2
    gy = content_cy - gh // 2

    # Subtle cyberpunk glow + dark drop shadow
    g_alpha = glyph_sc.split()[3]
    glow_mask = g_alpha.filter(ImageFilter.GaussianBlur(2.5 * SCALE))
    glow = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
    glow.paste((hazard_pink[0], hazard_pink[1], hazard_pink[2], 120), (0, 0), glow_mask)
    canvas.alpha_composite(glow, (gx, gy))

    sh_mask = g_alpha.filter(ImageFilter.GaussianBlur(2.0 * SCALE))
    sh = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 220), (0, 0), sh_mask)
    canvas.alpha_composite(sh, (gx, gy + int(2.5 * SCALE)))

    canvas.alpha_composite(glyph_sc, (gx, gy))

    final_w = max(1, int(round(total_w / float(SCALE))))
    badge = canvas.resize((final_w, NATIVE_H), Image.Resampling.LANCZOS)
    out_p = os.path.join(THEME_BADGES_DIR, f"{name}.webp")
    badge.save(out_p, "WEBP", quality=95, method=6)
    return name, True

def main():
    print("==================================================")
    print("DEPLOYING MAXIMUM FULL-COVER (66px) NEO-TOKYO TAG THEME")
    print("==================================================")

    os.makedirs(THEME_BADGES_DIR, exist_ok=True)
    all_names = set([f[:-5] for f in os.listdir(BADGES_DIR) if f.endswith(".webp")])
    for f in os.listdir(THEME_BADGES_DIR):
        if f.endswith(".webp"):
            all_names.add(f[:-5])

    print(f"Total badges to render for neotokyo-tag: {len(all_names)}")

    success_count = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        for name, ok in executor.map(render_neotokyo_badge, list(all_names)):
            if ok:
                success_count += 1
                if success_count % 100 == 0:
                    print(f"Rendered {success_count}/{len(all_names)} badges...")

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
    print("[RULE ENFORCED] live.webp has ZERO tag chassis/pink bar. Untouched broadcast beacon deployed.")

    total_deployed = len([f for f in os.listdir(THEME_BADGES_DIR) if f.endswith(".webp")])
    print(f"Total deployed badges in themes/neotokyo-tag/badges: {total_deployed}")

    # Copy rendered master preview to previews/preview-neotokyo-tag.jpg
    src_preview = os.path.join(BRAIN_DIR, "preview_neotokyo_tag_max_full_cover.jpg")
    dst_preview = os.path.join(PREVIEWS_DIR, "preview-neotokyo-tag.jpg")
    if os.path.exists(src_preview):
        shutil.copyfile(src_preview, dst_preview)
        print("Updated previews/preview-neotokyo-tag.jpg with master full-cover preview.")

    # Update SYSTEM_INTEGRITY.lock for neotokyo-tag hashes
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
                if "neotokyo-tag" in rel_p:
                    full_p = os.path.join(REPO_ROOT, rel_p)
                    if os.path.exists(full_p):
                        new_h = get_hash(full_p)
                        lines.append(f"{new_h}  {rel_p}\n")
                        continue
            lines.append(line)

    with open(LOCK_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Updated SYSTEM_INTEGRITY.lock with new neotokyo-tag hashes.")

if __name__ == "__main__":
    main()
