import os, sys, json, re, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "manga-halftone")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

font_bold = ImageFont.truetype("impact.ttf", int(50 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(42 * SCALE))

ACCENT_GOLD = (250, 204, 21, 255)
ACCENT_AMBER = (245, 158, 11, 255)
ACCENT_CYAN = (56, 189, 248, 255)
ACCENT_PINK = (255, 46, 99, 255)
ACCENT_PURPLE = (168, 85, 247, 255)
ACCENT_GREEN = (34, 197, 94, 255)
ACCENT_RED = (229, 9, 20, 255)

CLEAN_TEXTS = {
    "4k": ("4K", ACCENT_GOLD, ACCENT_GOLD),
    "8k": ("8K", ACCENT_GOLD, ACCENT_GOLD),
    "1080p": ("1080P", (255, 255, 255, 255), ACCENT_CYAN),
    "720p": ("720P", (255, 255, 255, 255), ACCENT_CYAN),
    "480p": ("480P", (220, 225, 235, 255), ACCENT_CYAN),
    "1440p": ("1440P", (255, 255, 255, 255), ACCENT_CYAN),
    "576p": ("576P", (220, 225, 235, 255), ACCENT_CYAN),
    "3d": ("3D", (255, 255, 255, 255), ACCENT_PURPLE),
    "hevc": ("HEVC", (255, 255, 255, 255), ACCENT_PINK),
    "av1": ("AV1", (255, 255, 255, 255), ACCENT_GREEN),
    "x264": ("x264", (255, 255, 255, 255), ACCENT_PINK),
    "x265": ("x265", (255, 255, 255, 255), ACCENT_PINK),
    "h264": ("H.264", (255, 255, 255, 255), ACCENT_PINK),
    "h265": ("H.265", (255, 255, 255, 255), ACCENT_PINK),
    "vp9": ("VP9", (255, 255, 255, 255), ACCENT_PINK),
    "vc1": ("VC-1", (255, 255, 255, 255), ACCENT_PINK),
    "vvc": ("VVC", (255, 255, 255, 255), ACCENT_PINK),
    "10-bit": ("10-BIT", (255, 255, 255, 255), ACCENT_PURPLE),
    "10bit": ("10-BIT", (255, 255, 255, 255), ACCENT_PURPLE),
    "8-bit": ("8-BIT", (255, 255, 255, 255), ACCENT_PURPLE),
    "8bit": ("8-BIT", (255, 255, 255, 255), ACCENT_PURPLE),
    "12-bit": ("12-BIT", (255, 255, 255, 255), ACCENT_PURPLE),
    "12bit": ("12-BIT", (255, 255, 255, 255), ACCENT_PURPLE),
    "5.1": ("5.1", ACCENT_CYAN, ACCENT_CYAN),
    "5_1": ("5.1", ACCENT_CYAN, ACCENT_CYAN),
    "7.1": ("7.1", ACCENT_CYAN, ACCENT_CYAN),
    "7_1": ("7.1", ACCENT_CYAN, ACCENT_CYAN),
    "2.0": ("2.0", ACCENT_CYAN, ACCENT_CYAN),
    "2_0": ("2.0", ACCENT_CYAN, ACCENT_CYAN),
    "1.0": ("1.0", ACCENT_CYAN, ACCENT_CYAN),
    "1_0": ("1.0", ACCENT_CYAN, ACCENT_CYAN),
    "6.1": ("6.1", ACCENT_CYAN, ACCENT_CYAN),
    "6_1": ("6.1", ACCENT_CYAN, ACCENT_CYAN),
    "atmos": ("ATMOS", ACCENT_CYAN, ACCENT_CYAN),
    "dolby-atmos": ("ATMOS", ACCENT_CYAN, ACCENT_CYAN),
    "truehd": ("TRUEHD", ACCENT_CYAN, ACCENT_CYAN),
    "dts": ("DTS", ACCENT_CYAN, ACCENT_CYAN),
    "dts-hd": ("DTS-HD", ACCENT_CYAN, ACCENT_CYAN),
    "dtsx": ("DTS:X", ACCENT_AMBER, ACCENT_AMBER),
    "dts-x": ("DTS:X", ACCENT_AMBER, ACCENT_AMBER),
    "flac": ("FLAC", ACCENT_CYAN, ACCENT_CYAN),
    "aac": ("AAC", (255, 255, 255, 255), ACCENT_CYAN),
    "ac3": ("AC3", (255, 255, 255, 255), ACCENT_CYAN),
    "eac3": ("EAC3", (255, 255, 255, 255), ACCENT_CYAN),
    "ddp": ("DD+", ACCENT_CYAN, ACCENT_CYAN),
    "mp3": ("MP3", (255, 255, 255, 255), ACCENT_CYAN),
    "opus": ("OPUS", (255, 255, 255, 255), ACCENT_CYAN),
    "web-dl": ("WEB-DL", (255, 255, 255, 255), ACCENT_GREEN),
    "webdl": ("WEB-DL", (255, 255, 255, 255), ACCENT_GREEN),
    "webrip": ("WEBRIP", (255, 255, 255, 255), ACCENT_GREEN),
    "bluray": ("BLURAY", ACCENT_CYAN, ACCENT_CYAN),
    "blu-ray": ("BLURAY", ACCENT_CYAN, ACCENT_CYAN),
    "remux": ("REMUX", ACCENT_GOLD, ACCENT_GOLD),
    "hdtv": ("HDTV", (255, 255, 255, 255), ACCENT_GREEN),
    "dvd": ("DVD", (255, 255, 255, 255), ACCENT_GREEN),
    "cached": ("CACHED", ACCENT_GOLD, ACCENT_GOLD),
    "uncached": ("UNCACHED", (165, 170, 185, 255), (120, 125, 140, 255)),
    "mkv": ("MKV", (255, 255, 255, 255), ACCENT_PINK),
    "mp4": ("MP4", (255, 255, 255, 255), ACCENT_PINK),
    "avi": ("AVI", (255, 255, 255, 255), ACCENT_PINK),
    "ts": ("TS", (255, 255, 255, 255), ACCENT_PINK),
    "m2ts": ("M2TS", (255, 255, 255, 255), ACCENT_PINK),
    "hdr": ("HDR", ACCENT_AMBER, ACCENT_AMBER),
    "hdr10": ("HDR10", ACCENT_AMBER, ACCENT_AMBER),
    "hdr10plus": ("HDR10+", ACCENT_AMBER, ACCENT_AMBER),
    "hlg": ("HLG", ACCENT_AMBER, ACCENT_AMBER),
    "dv": ("VISION", ACCENT_AMBER, ACCENT_AMBER),
    "dolby-vision": ("VISION", ACCENT_AMBER, ACCENT_AMBER),
    "dv-only": ("DV ONLY", ACCENT_AMBER, ACCENT_AMBER),
    "imax": ("IMAX", ACCENT_CYAN, ACCENT_CYAN),
    "60fps": ("60 FPS", (255, 255, 255, 255), ACCENT_PURPLE),
    "120fps": ("120 FPS", (255, 255, 255, 255), ACCENT_PURPLE),
    "50fps": ("50 FPS", (255, 255, 255, 255), ACCENT_PURPLE),
    "24fps": ("24 FPS", (255, 255, 255, 255), ACCENT_PURPLE),
    "dual": ("DUAL", (255, 255, 255, 255), ACCENT_AMBER),
    "extended": ("EXTENDED", (255, 255, 255, 255), ACCENT_AMBER),
    "unrated": ("UNRATED", (255, 255, 255, 255), ACCENT_PINK),
    "remastered": ("REMASTERED", (255, 255, 255, 255), ACCENT_GOLD),
    "directors-cut": ("DIR CUT", (255, 255, 255, 255), ACCENT_GOLD),
}

def load_lang_flags():
    mapping = {
        "english-flag": ("gb", "ENGLISH"),
        "bangladesh-flag": ("bd", "BANGLADESH"),
        "india-flag": ("in", "INDIA"),
        "usa-flag": ("us", "USA"),
        "japan-flag": ("jp", "JAPAN"),
        "japan": ("jp", "JAPAN"),
        "korea-flag": ("kr", "KOREA"),
        "korea": ("kr", "KOREA"),
        "france": ("fr", "FRANCE"),
        "germany": ("de", "GERMANY"),
        "spain": ("es", "SPAIN"),
        "italy": ("it", "ITALY"),
        "russia": ("ru", "RUSSIA"),
        "brazil": ("br", "BRAZIL"),
        "nepal": ("np", "NEPAL"),
        "nepali-flag": ("np", "NEPALI"),
        "saudi-arabia-flag": ("sa", "ARABIC"),
        "saudi-arabia": ("sa", "ARABIC"),
    }
    b5_path = os.path.join(REPO_ROOT, "scripts", "build_all_bespoke_themed_badges_v5.py")
    if os.path.exists(b5_path):
        with open(b5_path, "r", encoding="utf-8") as f:
            code = f.read()
        m = re.search(r"LANG_SPECS\s*=\s*\[(.*?)\]", code, re.DOTALL)
        if m:
            for item in re.findall(r'\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)', m.group(1)):
                b_name, cc, m_text, _ = item
                mapping[b_name] = (cc, m_text)
    return mapping

LANG_FLAGS = load_lang_flags()

def make_manga_panel(w_px, h_px, accent=ACCENT_PINK):
    m_x = 6 * SCALE
    m_y = 6 * SCALE
    rad = 4 * SCALE
    canvas = Image.new("RGBA", (w_px, h_px), (0, 0, 0, 0))

    # Hard Manga Offset Ink Shadow
    sh = Image.new("RGBA", (w_px, h_px), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        [m_x + 3 * SCALE, m_y + 3 * SCALE, w_px - m_x + 1 * SCALE, h_px - m_y + 1 * SCALE],
        radius=rad,
        fill=(0, 0, 0, 235),
    )
    canvas.alpha_composite(sh)

    # Panel Base
    mask = Image.new("L", (w_px, h_px), 0)
    ImageDraw.Draw(mask).rounded_rectangle([m_x, m_y, w_px - m_x - 1, h_px - m_y - 1], radius=rad, fill=255)
    panel = Image.new("RGBA", (w_px, h_px), (18, 20, 28, 255))

    # Vectorized Ben-Day Halftone Dot Pattern
    yy, xx = np.mgrid[0:h_px, 0:w_px]
    step = int(7 * SCALE)
    dx = (xx % step) - step / 2.0
    dy = (yy % step) - step / 2.0
    dist = np.sqrt(dx * dx + dy * dy)
    intensity = np.clip((xx / float(w_px) * 0.6 + yy / float(h_px) * 0.4) - 0.15, 0.0, 1.0)
    dots = dist < ((1.6 * SCALE) * intensity)

    p_arr = np.array(panel)
    p_arr[dots, 0] = np.minimum(255, p_arr[dots, 0] + 22)
    p_arr[dots, 1] = np.minimum(255, p_arr[dots, 1] + 24)
    p_arr[dots, 2] = np.minimum(255, p_arr[dots, 2] + 34)
    canvas.paste(Image.fromarray(p_arr, "RGBA"), (0, 0), mask)

    # Left Manga Accent Bar + Crisp White Ink Frame
    fdraw = ImageDraw.Draw(canvas)
    fdraw.rectangle([m_x + 2 * SCALE, m_y + 2 * SCALE, m_x + 6 * SCALE, h_px - m_y - 2 * SCALE], fill=accent)
    fdraw.rounded_rectangle([m_x, m_y, w_px - m_x - 1, h_px - m_y - 1], radius=rad, outline=(245, 247, 255, 220), width=int(2.0 * SCALE))
    return canvas

def render_text_manga(text, color=(255, 255, 255, 255), accent=ACCENT_PINK):
    dummy = Image.new("RGBA", (1, 1))
    bb = ImageDraw.Draw(dummy).textbbox((0, 0), text, font=font_bold)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    card_w = max(tw + 36 * SCALE, 95 * SCALE)
    card = make_manga_panel(card_w, TOTAL_H, accent=accent)
    draw = ImageDraw.Draw(card)
    tx = (card_w - tw) // 2 - bb[0] + 2 * SCALE
    ty = (TOTAL_H - th) // 2 - bb[1]
    draw.text((tx + 2 * SCALE, ty + 2 * SCALE), text, font=font_bold, fill=(0, 0, 0, 240))
    draw.text((tx, ty), text, font=font_bold, fill=color)
    return card.resize((card_w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def render_flag_manga(cc, lang_text):
    flag_p = os.path.join(FLAG_DIR, f"{cc}.png")
    if not os.path.exists(flag_p):
        return None
    flag = Image.open(flag_p).convert("RGBA")
    fh = int(42 * SCALE)
    fw = int(flag.width * (fh / float(flag.height)))
    flag_sc = flag.resize((fw, fh), Image.Resampling.LANCZOS)

    fmask = Image.new("L", (fw, fh), 0)
    ImageDraw.Draw(fmask).rounded_rectangle([0, 0, fw - 1, fh - 1], radius=int(4 * SCALE), fill=255)
    flag_r = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    flag_r.paste(flag_sc, (0, 0), fmask)

    dummy = Image.new("RGBA", (1, 1))
    bb = ImageDraw.Draw(dummy).textbbox((0, 0), lang_text, font=font_sub)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]

    gap = int(10 * SCALE)
    cw = min(fw + gap + tw, int(190 * SCALE))
    card_w = max(fw + gap + tw + 36 * SCALE, 115 * SCALE)
    card = make_manga_panel(card_w, TOTAL_H, accent=ACCENT_CYAN)

    cx = (card_w - (fw + gap + tw)) // 2 + 2 * SCALE
    fy = (TOTAL_H - fh) // 2
    card.alpha_composite(flag_r, (cx, fy))

    draw = ImageDraw.Draw(card)
    tx = cx + fw + gap - bb[0]
    ty = (TOTAL_H - th) // 2 - bb[1]
    draw.text((tx + 2 * SCALE, ty + 2 * SCALE), lang_text, font=font_sub, fill=(0, 0, 0, 240))
    draw.text((tx, ty), lang_text, font=font_sub, fill=(255, 255, 255, 255))
    return card.resize((card_w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def render_logo_manga(img_p, accent=ACCENT_PINK):
    im = Image.open(img_p).convert("RGBA")
    bbox = im.getbbox()
    glyph = im.crop(bbox) if bbox else im

    target_h = int(54 * SCALE)
    max_w = int(185 * SCALE)
    sc = min(target_h / float(glyph.height), max_w / float(glyph.width))
    gw, gh = max(1, int(round(glyph.width * sc))), max(1, int(round(glyph.height * sc)))
    glyph_sc = glyph.resize((gw, gh), Image.Resampling.LANCZOS)

    card_w = max(gw + 36 * SCALE, 100 * SCALE)
    card = make_manga_panel(card_w, TOTAL_H, accent=accent)

    gx = (card_w - gw) // 2 + 2 * SCALE
    gy = (TOTAL_H - gh) // 2

    arr = np.array(glyph_sc)
    vis = arr[:, :, 3] > 50
    if np.any(vis):
        lum = np.mean(0.299 * arr[vis, 0] + 0.587 * arr[vis, 1] + 0.114 * arr[vis, 2])
        if lum < 60:
            ga = glyph_sc.split()[3]
            halo = ga.filter(ImageFilter.MaxFilter(5))
            white_bg = Image.new("RGBA", (gw, gh), (255, 255, 255, 230))
            card.paste(white_bg, (gx, gy), halo)

    ga = glyph_sc.split()[3]
    sh = Image.new("RGBA", (gw, gh), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 220), (0, 0), ga)
    card.alpha_composite(sh, (gx + 2 * SCALE, gy + 2 * SCALE))
    card.alpha_composite(glyph_sc, (gx, gy))
    return card.resize((card_w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def process_badge(filename):
    name = filename[:-5]
    if name == "live":
        src_live = os.path.join(BADGES_DIR, "live.webp")
        dst_live = os.path.join(THEME_BADGES_DIR, "live.webp")
        shutil.copyfile(src_live, dst_live)
        return name, True

    if name in CLEAN_TEXTS:
        txt, col, acc = CLEAN_TEXTS[name]
        badge = render_text_manga(txt, col, acc)
    elif name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        badge = render_flag_manga(cc, lang)
        if badge is None:
            badge = render_logo_manga(os.path.join(BADGES_DIR, filename), ACCENT_CYAN)
    else:
        ott_p = os.path.join(OTT_DIR, f"{name}.png")
        if os.path.exists(ott_p):
            acc = ACCENT_RED if "netflix" in name else ACCENT_PINK
            badge = render_logo_manga(ott_p, acc)
        else:
            src_p = os.path.join(BADGES_DIR, filename)
            if os.path.exists(src_p):
                badge = render_logo_manga(src_p, ACCENT_PINK)
            else:
                return name, False

    out_p = os.path.join(THEME_BADGES_DIR, filename)
    badge.save(out_p, "WEBP", quality=95, method=6)
    return name, True

def generate_manifests():
    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("filters", []):
        if "imageURL" in item:
            item["imageURL"] = item["imageURL"].replace("/main/badges/", "/main/themes/manga-halftone/badges/")
    for p in [os.path.join(REPO_ROOT, "manga-halftone.json"), os.path.join(THEME_DIR, "manga-halftone.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    print("Generated manga-halftone.json manifests.")

def main():
    os.makedirs(THEME_BADGES_DIR, exist_ok=True)
    files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]
    print(f"Deploying Manga Halftone theme across {len(files)} badges...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(process_badge, files))
    print(f"Rendered {len(results)} Manga Halftone badges.")

    dst_live = os.path.join(THEME_BADGES_DIR, "live.webp")
    h = hashlib.sha256(open(dst_live, "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, f"LIVE HASH MISMATCH: {h}"
    print("[SUCCESS] live.webp 100% verified untouched.")
    generate_manifests()

if __name__ == "__main__":
    main()
