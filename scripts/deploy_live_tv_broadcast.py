import os, sys, json, re, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "live-tv-broadcast")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

font_imp = ImageFont.truetype("impact.ttf", int(56 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(42 * SCALE))

GOLD = (250, 204, 21, 255)
AMBER = (245, 158, 11, 255)
CYAN = (56, 189, 248, 255)
GREEN = (34, 197, 94, 255)
RED = (239, 68, 68, 255)
PURPLE = (192, 132, 252, 255)
WHITE = (255, 255, 255, 255)
MUTED = (200, 210, 225, 255)

# Curated Live TV & Sports text badges (Pure Chroma Broadcast Type - Zero Background)
TEXT_SPECS = {
    # Live & Feeds
    "247": ("24/7", GREEN),
    "ppv": ("PPV", GOLD),
    "hd-feed": ("HD-FEED", WHITE),
    "live-hd": ("LIVE HD", WHITE),
    "sd-feed": ("SD-FEED", MUTED),
    "live-sd": ("LIVE SD", MUTED),
    "raw": ("RAW", RED),
    "live-raw": ("RAW", RED),
    "live-hfr": ("LIVE HFR", CYAN),
    "backup": ("BACKUP", AMBER),
    "live-backup": ("BACKUP", AMBER),
    "catchup": ("CATCHUP", CYAN),
    "region-in": ("IN FEED", AMBER),
    "region-uk": ("UK FEED", CYAN),
    "region-us": ("US FEED", CYAN),
    # Resolutions
    "8k": ("8K", GOLD),
    "4k": ("4K", GOLD),
    "1440p": ("1440P", WHITE),
    "1080p": ("1080P", WHITE),
    "720p": ("720P", WHITE),
    "576p": ("576P", MUTED),
    "480p": ("480P", MUTED),
    "lowres": ("LOWRES", MUTED),
    # Framerates (Sports critical)
    "120fps": ("120FPS", CYAN),
    "60fps": ("60FPS", CYAN),
    "50fps": ("50FPS", CYAN),
    "hfr": ("HFR", CYAN),
    # HDR / Broadcast Dynamic Range
    "hlg": ("HLG", AMBER),
    "hdr10plus": ("HDR10+", AMBER),
    "hdr10": ("HDR10", AMBER),
    "hdr": ("HDR", AMBER),
    "dolby-vision": ("VISION", AMBER),
    "sdr": ("SDR", MUTED),
    # Stream Codecs
    "hevc": ("HEVC", WHITE),
    "avc": ("H.264", WHITE),
    "av1": ("AV1", GREEN),
    "vp9": ("VP9", WHITE),
    # Audio & Channels
    "atmos": ("ATMOS", CYAN),
    "ddp": ("DD+", CYAN),
    "dd": ("DD", CYAN),
    "aac": ("AAC", WHITE),
    "mp3": ("MP3", WHITE),
    "opus": ("OPUS", WHITE),
    "7.1": ("7.1", CYAN),
    "5.1": ("5.1", CYAN),
    "2.0": ("2.0", CYAN),
    "1.0": ("1.0", MUTED),
    # Stream Protocol / Source
    "hls": ("HLS", GREEN),
    "mpegts": ("MPEG-TS", WHITE),
    "ts": ("TS", WHITE),
    "mp4": ("MP4", WHITE),
    "hdtv": ("HDTV", WHITE),
    "direct": ("DIRECT", GREEN),
    # Language Tags
    "dual": ("DUAL", AMBER),
    "multi": ("MULTI", AMBER),
    "original": ("ORIG", WHITE),
    "dubbed": ("DUBBED", WHITE),
}

LANG_FLAGS = {
    "bengali": ("bd", "BENGALI"),
    "bangladesh-flag": ("bd", "BANGLADESH"),
    "hindi": ("in", "HINDI"),
    "india-flag": ("in", "INDIA"),
    "urdu": ("pk", "URDU"),
    "english": ("gb", "ENGLISH"),
    "english-flag": ("gb", "ENGLISH"),
    "uk": ("gb", "UK"),
    "us": ("us", "USA"),
    "usa-flag": ("us", "USA"),
    "spanish": ("es", "SPANISH"),
    "arabic": ("sa", "ARABIC"),
    "saudi-arabia-flag": ("sa", "ARABIC"),
    "french": ("fr", "FRENCH"),
    "german": ("de", "GERMAN"),
    "portuguese": ("pt", "PORTUGUESE"),
    "italian": ("it", "ITALIAN"),
    "russian": ("ru", "RUSSIAN"),
    "japanese": ("jp", "JAPANESE"),
    "korean": ("kr", "KOREAN"),
    "turkish": ("tr", "TURKISH"),
}

TV_NETWORK_IDS = {
    "bbc", "cbs", "itv", "amc", "fx", "syfy", "natgeo", "thecw",
    "jiohotstar", "sonyliv", "peacock", "toffee", "rabbithole", "bongo",
    "prime", "appletv", "dazn", "espn", "fancode", "tsports"
}

def add_crisp_shadow(canvas, blur_r=2.0, offset_y=2.0):
    a = canvas.split()[3]
    sh_mask = a.filter(ImageFilter.GaussianBlur(blur_r * SCALE))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 240), (0, 0), sh_mask)
    out = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, int(offset_y * SCALE)))
    out.alpha_composite(canvas)
    return out

def render_pure_chroma_text(text, color):
    dummy = Image.new("RGBA", (1, 1))
    bb = ImageDraw.Draw(dummy).textbbox((0, 0), text, font=font_imp)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    w = tw + 24 * SCALE
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(c)
    tx = (w - tw) // 2 - bb[0]
    ty = (TOTAL_H - th) // 2 - bb[1]
    dr.text((tx, ty), text, font=font_imp, fill=color, stroke_width=int(2.5 * SCALE), stroke_fill=(0, 0, 0, 245))
    c = add_crisp_shadow(c)
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def render_pure_chroma_flag(cc, lang_text):
    flag_p = os.path.join(FLAG_DIR, f"{cc}.png")
    if not os.path.exists(flag_p):
        return render_pure_chroma_text(lang_text, WHITE)
    flag = Image.open(flag_p).convert("RGBA")
    fh = int(44 * SCALE)
    fw = int(flag.width * (fh / float(flag.height)))
    sc = flag.resize((fw, fh), Image.Resampling.LANCZOS)
    fmask = Image.new("L", (fw, fh), 0)
    ImageDraw.Draw(fmask).rounded_rectangle([0, 0, fw - 1, fh - 1], radius=int(5 * SCALE), fill=255)
    flag_r = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    flag_r.paste(sc, (0, 0), fmask)

    dummy = Image.new("RGBA", (1, 1))
    bb = ImageDraw.Draw(dummy).textbbox((0, 0), lang_text, font=font_sub)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    gap = int(10 * SCALE)
    cw = fw + gap + tw
    w = cw + 22 * SCALE
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    cx = (w - cw) // 2
    c.alpha_composite(flag_r, (cx, (TOTAL_H - fh) // 2))
    dr = ImageDraw.Draw(c)
    tx = cx + fw + gap - bb[0]
    ty = (TOTAL_H - th) // 2 - bb[1]
    dr.text((tx, ty), lang_text, font=font_sub, fill=WHITE, stroke_width=int(2.2 * SCALE), stroke_fill=(0, 0, 0, 245))
    c = add_crisp_shadow(c)
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def render_pure_chroma_logo(img_p):
    im = Image.open(img_p).convert("RGBA")
    bbox = im.getbbox()
    glyph = im.crop(bbox) if bbox else im
    target_h = int(58 * SCALE)
    max_w = int(190 * SCALE)
    sc = min(target_h / float(glyph.height), max_w / float(glyph.width))
    gw, gh = max(1, int(round(glyph.width * sc))), max(1, int(round(glyph.height * sc)))
    glyph_sc = glyph.resize((gw, gh), Image.Resampling.LANCZOS)

    w = gw + 24 * SCALE
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    gx, gy = (w - gw) // 2, (TOTAL_H - gh) // 2

    arr = np.array(glyph_sc)
    vis = arr[:, :, 3] > 50
    if np.any(vis):
        lum = np.mean(0.299 * arr[vis, 0] + 0.587 * arr[vis, 1] + 0.114 * arr[vis, 2])
        if lum < 60:
            ga = glyph_sc.split()[3]
            halo = ga.filter(ImageFilter.MaxFilter(5))
            c.paste(Image.new("RGBA", (gw, gh), (255, 255, 255, 235)), (gx, gy), halo)

    c.alpha_composite(glyph_sc, (gx, gy))
    c = add_crisp_shadow(c)
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def main():
    os.makedirs(THEME_BADGES_DIR, exist_ok=True)
    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        master = json.load(f)

    allowed_ids = set(TEXT_SPECS.keys()) | set(LANG_FLAGS.keys()) | TV_NETWORK_IDS | {"live"}
    kept_filters = []
    kept_group_ids = set()

    for item in master.get("filters", []):
        bid = item.get("id")
        # Extract filename from imageURL
        url = item.get("imageURL", "")
        fname = os.path.basename(url)
        base = fname[:-5] if fname.endswith(".webp") else bid

        if bid in allowed_ids or base in allowed_ids:
            new_item = dict(item)
            new_item["imageURL"] = f"https://raw.githubusercontent.com/jayedanik/nuvio-master-badge-system/main/themes/live-tv-broadcast/badges/{fname}"
            kept_filters.append(new_item)
            kept_group_ids.add(item["groupId"])

    kept_groups = [g for g in master.get("groups", []) if g["id"] in kept_group_ids]
    out_manifest = {"groups": kept_groups, "filters": kept_filters}

    for p in [os.path.join(REPO_ROOT, "live-tv-broadcast.json"), os.path.join(THEME_DIR, "live-tv-broadcast.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(out_manifest, f, indent=2)

    # Render all required WebP files (both filter filenames and canonical keys)
    to_render = set(allowed_ids)
    for item in kept_filters:
        fname = os.path.basename(item["imageURL"])
        if fname.endswith(".webp"):
            to_render.add(fname[:-5])

    rendered = 0
    for name in sorted(to_render):
        out_p = os.path.join(THEME_BADGES_DIR, f"{name}.webp")
        if name == "live":
            shutil.copyfile(os.path.join(BADGES_DIR, "live.webp"), out_p)
        elif name in TEXT_SPECS:
            txt, col = TEXT_SPECS[name]
            render_pure_chroma_text(txt, col).save(out_p, "WEBP", quality=95, method=6)
        elif name in LANG_FLAGS:
            cc, lang = LANG_FLAGS[name]
            render_pure_chroma_flag(cc, lang).save(out_p, "WEBP", quality=95, method=6)
        else:
            ott_p = os.path.join(OTT_DIR, f"{name}.png")
            src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, f"{name}.webp")
            if os.path.exists(src_p):
                render_pure_chroma_logo(src_p).save(out_p, "WEBP", quality=95, method=6)
            else:
                continue
        rendered += 1

    h = hashlib.sha256(open(os.path.join(THEME_BADGES_DIR, "live.webp"), "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, "live.webp hash mismatch!"
    print(f"[SUCCESS] Rendered {rendered} Live TV & Sports badges + manifest ({len(kept_filters)} rules across {len(kept_groups)} groups). live.webp untouched.")

if __name__ == "__main__":
    main()
