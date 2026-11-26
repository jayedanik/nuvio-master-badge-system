import os, sys, json, re, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

font_bahn = ImageFont.truetype("bahnschrift.ttf", int(48 * SCALE))
font_imp = ImageFont.truetype("impact.ttf", int(48 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(40 * SCALE))

ACCENT_RED = (229, 9, 20, 255)
ACCENT_GOLD = (234, 179, 8, 255)
ACCENT_ORANGE = (249, 115, 22, 255)
ACCENT_PINK = (236, 72, 153, 255)
ACCENT_PURPLE = (168, 85, 247, 255)
ACCENT_BLUE = (14, 165, 233, 255)
ACCENT_GREEN = (16, 185, 129, 255)
ACCENT_ROSE = (244, 63, 94, 255)
ACCENT_INDIGO = (59, 130, 246, 255)

CLEAN_TEXTS = {
    "4k": ("4K", ACCENT_GOLD),
    "8k": ("8K", ACCENT_GOLD),
    "1080p": ("1080P", ACCENT_BLUE),
    "720p": ("720P", ACCENT_BLUE),
    "480p": ("480P", ACCENT_INDIGO),
    "1440p": ("1440P", ACCENT_BLUE),
    "576p": ("576P", ACCENT_INDIGO),
    "lowres": ("LOWRES", ACCENT_INDIGO),
    "3d": ("3D", ACCENT_PURPLE),
    "hevc": ("HEVC", ACCENT_PINK),
    "av1": ("AV1", ACCENT_GREEN),
    "avc": ("H.264", ACCENT_PINK),
    "x264": ("x264", ACCENT_PINK),
    "x265": ("x265", ACCENT_PINK),
    "h264": ("H.264", ACCENT_PINK),
    "h265": ("H.265", ACCENT_PINK),
    "vp9": ("VP9", ACCENT_PINK),
    "vc1": ("VC-1", ACCENT_PINK),
    "vvc": ("VVC", ACCENT_PINK),
    "10-bit": ("10-BIT", ACCENT_PURPLE),
    "10bit": ("10-BIT", ACCENT_PURPLE),
    "8-bit": ("8-BIT", ACCENT_PURPLE),
    "8bit": ("8-BIT", ACCENT_PURPLE),
    "12-bit": ("12-BIT", ACCENT_PURPLE),
    "12bit": ("12-BIT", ACCENT_PURPLE),
    "5.1": ("5.1", ACCENT_BLUE),
    "5_1": ("5.1", ACCENT_BLUE),
    "7.1": ("7.1", ACCENT_BLUE),
    "7_1": ("7.1", ACCENT_BLUE),
    "2.0": ("2.0", ACCENT_BLUE),
    "2_0": ("2.0", ACCENT_BLUE),
    "1.0": ("1.0", ACCENT_BLUE),
    "1_0": ("1.0", ACCENT_BLUE),
    "6.1": ("6.1", ACCENT_BLUE),
    "6_1": ("6.1", ACCENT_BLUE),
    "atmos": ("ATMOS", ACCENT_BLUE),
    "dolby-atmos": ("ATMOS", ACCENT_BLUE),
    "truehd": ("TRUEHD", ACCENT_BLUE),
    "dts": ("DTS", ACCENT_BLUE),
    "dts-hd": ("DTS-HD", ACCENT_BLUE),
    "dtsx": ("DTS:X", ACCENT_ORANGE),
    "dts-x": ("DTS:X", ACCENT_ORANGE),
    "flac": ("FLAC", ACCENT_BLUE),
    "aac": ("AAC", ACCENT_BLUE),
    "ac3": ("AC3", ACCENT_BLUE),
    "eac3": ("EAC3", ACCENT_BLUE),
    "ddp": ("DD+", ACCENT_BLUE),
    "dd": ("DD", ACCENT_BLUE),
    "mp3": ("MP3", ACCENT_BLUE),
    "opus": ("OPUS", ACCENT_BLUE),
    "web-dl": ("WEB-DL", ACCENT_GREEN),
    "webdl": ("WEB-DL", ACCENT_GREEN),
    "webrip": ("WEBRIP", ACCENT_GREEN),
    "bluray": ("BLURAY", ACCENT_BLUE),
    "blu-ray": ("BLURAY", ACCENT_BLUE),
    "remux": ("REMUX", ACCENT_GOLD),
    "hdtv": ("HDTV", ACCENT_GREEN),
    "dvd": ("DVD", ACCENT_GREEN),
    "cached": ("CACHED", ACCENT_GOLD),
    "uncached": ("UNCACHED", ACCENT_ROSE),
    "mkv": ("MKV", ACCENT_ROSE),
    "mp4": ("MP4", ACCENT_ROSE),
    "avi": ("AVI", ACCENT_ROSE),
    "ts": ("TS", ACCENT_ROSE),
    "m2ts": ("M2TS", ACCENT_ROSE),
    "hdr": ("HDR", ACCENT_ORANGE),
    "hdr10": ("HDR10", ACCENT_ORANGE),
    "hdr10plus": ("HDR10+", ACCENT_ORANGE),
    "hlg": ("HLG", ACCENT_ORANGE),
    "dv": ("VISION", ACCENT_ORANGE),
    "dolby-vision": ("VISION", ACCENT_ORANGE),
    "dv-only": ("DV ONLY", ACCENT_ORANGE),
    "imax": ("IMAX", ACCENT_BLUE),
    "60fps": ("60FPS", ACCENT_PURPLE),
    "120fps": ("120FPS", ACCENT_PURPLE),
    "50fps": ("50FPS", ACCENT_PURPLE),
    "24fps": ("24FPS", ACCENT_PURPLE),
    "hfr": ("HFR", ACCENT_PURPLE),
    "dual": ("DUAL", ACCENT_ORANGE),
    "multi": ("MULTI", ACCENT_ORANGE),
    "extended": ("EXTENDED", ACCENT_ORANGE),
    "unrated": ("UNRATED", ACCENT_ROSE),
    "remastered": ("REMASTERED", ACCENT_GOLD),
    "directors-cut": ("DIR CUT", ACCENT_GOLD),
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
        "spain": ("es", "SPANISH"),
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

def adapt_logo_for_light_surface(glyph_sc):
    """If a logo is mostly pure white/very bright, invert it to crisp dark ink (#121418) so it reads cleanly on cream & brushed chrome."""
    arr = np.array(glyph_sc)
    vis = arr[:, :, 3] > 50
    if not np.any(vis):
        return glyph_sc
    rgb = arr[vis, :3].astype(np.float32)
    lum = np.mean(0.299 * rgb[:, 0] + 0.587 * rgb[:, 1] + 0.114 * rgb[:, 2])
    sat = np.mean(np.max(rgb, axis=1) - np.min(rgb, axis=1))
    if lum > 200 and sat < 30:
        arr_dark = arr.copy()
        arr_dark[:, :, 0] = 18
        arr_dark[:, :, 1] = 20
        arr_dark[:, :, 2] = 24
        return Image.fromarray(arr_dark, "RGBA")
    return glyph_sc

def make_flag_img(cc, fh_px=int(40 * SCALE)):
    flag_p = os.path.join(FLAG_DIR, f"{cc}.png")
    if not os.path.exists(flag_p):
        return None
    flag = Image.open(flag_p).convert("RGBA")
    fw = int(flag.width * (fh_px / float(flag.height)))
    sc = flag.resize((fw, fh_px), Image.Resampling.LANCZOS)
    mask = Image.new("L", (fw, fh_px), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw - 1, fh_px - 1], radius=int(4 * SCALE), fill=255)
    out = Image.new("RGBA", (fw, fh_px), (0, 0, 0, 0))
    out.paste(sc, (0, 0), mask)
    return out

def fit_glyph(img_p, th=int(50 * SCALE), mw=int(165 * SCALE)):
    im = Image.open(img_p).convert("RGBA")
    bb = im.getbbox()
    g = im.crop(bb) if bb else im
    sc = min(th / float(g.height), mw / float(g.width))
    return g.resize((max(1, int(round(g.width * sc))), max(1, int(round(g.height * sc)))), Image.Resampling.LANCZOS)

# ==============================================================================
# THEME 1: SWISS BAUHAUS SPLIT-BLOCK (bauhaus-split)
# ==============================================================================
def render_bauhaus_badge(name, filename):
    left_w = int(20 * SCALE)
    m_x, m_y, rad = 4 * SCALE, 8 * SCALE, 10 * SCALE
    ink = (18, 20, 24, 255)
    cream = (242, 239, 232, 255)

    def build_panel(content_w, accent):
        right_w = max(content_w + 28 * SCALE, 72 * SCALE)
        w = left_w + right_w + 8 * SCALE
        c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
        mask = Image.new("L", (w, TOTAL_H), 0)
        ImageDraw.Draw(mask).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, fill=255)
        base = Image.new("RGBA", (w, TOTAL_H), cream)
        bd = ImageDraw.Draw(base)
        bd.rectangle([0, 0, m_x + left_w, TOTAL_H], fill=accent)
        dr = int(4.5 * SCALE)
        cx_dot, cy_dot = m_x + left_w // 2, TOTAL_H // 2
        bd.ellipse([cx_dot - dr, cy_dot - dr, cx_dot + dr, cy_dot + dr], fill=cream)
        c.paste(base, (0, 0), mask)
        return c, m_x + left_w, right_w, w

    if name in CLEAN_TEXTS:
        txt, acc = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_bahn)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        c, rx0, right_w, w = build_panel(tw, acc)
        tx = rx0 + (right_w - tw) // 2 - bb[0]
        ty = (TOTAL_H - th) // 2 - bb[1]
        ImageDraw.Draw(c).text((tx, ty), txt, font=font_bahn, fill=ink)
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 10 * SCALE + tw
            c, rx0, right_w, w = build_panel(cw, ACCENT_INDIGO)
            cx = rx0 + (right_w - cw) // 2
            c.alpha_composite(fl, (cx, (TOTAL_H - fl.height) // 2))
            tx = cx + fl.width + 10 * SCALE - bb[0]
            ty = (TOTAL_H - th) // 2 - bb[1]
            ImageDraw.Draw(c).text((tx, ty), lang, font=font_sub, fill=ink)
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    g = adapt_logo_for_light_surface(fit_glyph(src_p))
    acc = ACCENT_RED if "netflix" in name else ACCENT_INDIGO
    c, rx0, right_w, w = build_panel(g.width, acc)
    c.alpha_composite(g, (rx0 + (right_w - g.width) // 2, (TOTAL_H - g.height) // 2))
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

# ==============================================================================
# THEME 2: BRUSHED TITANIUM / CHROME PILL (titanium-chrome)
# ==============================================================================
CHROME_GRAD_CACHE = None
def get_chrome_row_colors():
    global CHROME_GRAD_CACHE
    if CHROME_GRAD_CACHE is not None:
        return CHROME_GRAD_CACHE
    rows = np.zeros((TOTAL_H, 1, 4), dtype=np.uint8)
    for y in range(TOTAL_H):
        t = y / float(TOTAL_H - 1)
        if t < 0.25:
            v = int(215 + 35 * (t / 0.25))
        elif t < 0.65:
            v = int(250 - 95 * ((t - 0.25) / 0.40))
        else:
            v = int(155 + 45 * ((t - 0.65) / 0.35))
        rows[y, 0, 0] = v
        rows[y, 0, 1] = min(255, v + 3)
        rows[y, 0, 2] = min(255, v + 8)
        rows[y, 0, 3] = 255
    CHROME_GRAD_CACHE = rows
    return rows

def render_chrome_badge(name, filename):
    m_x, m_y = 4 * SCALE, 8 * SCALE
    rad = (TOTAL_H - 2 * m_y) // 2
    ink = (18, 22, 28, 255)

    def build_pill(content_w):
        w = max(content_w + 44 * SCALE, 105 * SCALE)
        c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
        mask = Image.new("L", (w, TOTAL_H), 0)
        ImageDraw.Draw(mask).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, fill=255)
        garr = np.repeat(get_chrome_row_colors(), w, axis=1)
        c.paste(Image.fromarray(garr, "RGBA"), (0, 0), mask)
        ImageDraw.Draw(c).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, outline=(255, 255, 255, 210), width=int(1.6 * SCALE))
        return c, w

    if name in CLEAN_TEXTS:
        txt, _ = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_imp)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        c, w = build_pill(tw)
        tx = (w - tw) // 2 - bb[0]
        ty = (TOTAL_H - th) // 2 - bb[1]
        dr = ImageDraw.Draw(c)
        dr.text((tx, ty + int(1.2 * SCALE)), txt, font=font_imp, fill=(255, 255, 255, 170))
        dr.text((tx, ty), txt, font=font_imp, fill=ink)
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 10 * SCALE + tw
            c, w = build_pill(cw)
            cx = (w - cw) // 2
            c.alpha_composite(fl, (cx, (TOTAL_H - fl.height) // 2))
            tx = cx + fl.width + 10 * SCALE - bb[0]
            ty = (TOTAL_H - th) // 2 - bb[1]
            ImageDraw.Draw(c).text((tx, ty), lang, font=font_sub, fill=ink)
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    g = adapt_logo_for_light_surface(fit_glyph(src_p))
    c, w = build_pill(g.width)
    c.alpha_composite(g, ((w - g.width) // 2, (TOTAL_H - g.height) // 2))
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def deploy_theme(theme_id, render_fn):
    t_dir = os.path.join(REPO_ROOT, "themes", theme_id)
    b_dir = os.path.join(t_dir, "badges")
    os.makedirs(b_dir, exist_ok=True)
    files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]

    def _job(fn):
        name = fn[:-5]
        out_p = os.path.join(b_dir, fn)
        if name == "live":
            shutil.copyfile(os.path.join(BADGES_DIR, "live.webp"), out_p)
            return True
        im = render_fn(name, fn)
        if im is not None:
            im.save(out_p, "WEBP", quality=95, method=6)
            return True
        return False

    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(_job, files))

    h = hashlib.sha256(open(os.path.join(b_dir, "live.webp"), "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, f"{theme_id} live.webp hash mismatch!"

    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("filters", []):
        if "imageURL" in item:
            item["imageURL"] = item["imageURL"].replace("/main/badges/", f"/main/themes/{theme_id}/badges/")
    for p in [os.path.join(REPO_ROOT, f"{theme_id}.json"), os.path.join(t_dir, f"{theme_id}.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    print(f"[SUCCESS] {theme_id}: rendered {sum(res)}/{len(files)} badges + manifests. live.webp verified.")

def main():
    get_chrome_row_colors()
    deploy_theme("bauhaus-split", render_bauhaus_badge)
    deploy_theme("titanium-chrome", render_chrome_badge)

if __name__ == "__main__":
    main()
