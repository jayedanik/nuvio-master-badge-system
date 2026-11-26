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

font_mono = ImageFont.truetype("consolab.ttf", int(42 * SCALE))
font_bold = ImageFont.truetype("segoeuib.ttf", int(44 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(38 * SCALE))

SN_WHITE = (255, 255, 255, 255)
SN_YELLOW = (254, 240, 138, 255)
SN_PEACH = (254, 215, 170, 255)
SN_SKY = (186, 230, 253, 255)
SN_LAVENDER = (233, 213, 255, 255)
SN_MINT = (167, 243, 208, 255)
SN_PINK = (251, 207, 232, 255)

CLEAN_TEXTS = {
    "4k": ("4K", SN_YELLOW), "8k": ("8K", SN_YELLOW),
    "1080p": ("1080P", SN_SKY), "720p": ("720P", SN_SKY),
    "480p": ("480P", SN_WHITE), "1440p": ("1440P", SN_SKY),
    "576p": ("576P", SN_WHITE), "lowres": ("LOWRES", SN_WHITE),
    "3d": ("3D", SN_PINK),
    "hevc": ("HEVC", SN_SKY), "av1": ("AV1", SN_MINT),
    "avc": ("H.264", SN_SKY), "x264": ("x264", SN_SKY),
    "x265": ("x265", SN_SKY), "h264": ("H.264", SN_SKY),
    "h265": ("H.265", SN_SKY), "vp9": ("VP9", SN_SKY),
    "vc1": ("VC-1", SN_SKY), "vvc": ("VVC", SN_SKY),
    "10-bit": ("10-BIT", SN_LAVENDER), "10bit": ("10-BIT", SN_LAVENDER),
    "8-bit": ("8-BIT", SN_LAVENDER), "8bit": ("8-BIT", SN_LAVENDER),
    "12-bit": ("12-BIT", SN_LAVENDER), "12bit": ("12-BIT", SN_LAVENDER),
    "5.1": ("5.1", SN_YELLOW), "5_1": ("5.1", SN_YELLOW),
    "7.1": ("7.1", SN_YELLOW), "7_1": ("7.1", SN_YELLOW),
    "2.0": ("2.0", SN_YELLOW), "2_0": ("2.0", SN_YELLOW),
    "1.0": ("1.0", SN_YELLOW), "1_0": ("1.0", SN_YELLOW),
    "6.1": ("6.1", SN_YELLOW), "6_1": ("6.1", SN_YELLOW),
    "atmos": ("ATMOS", SN_SKY), "dolby-atmos": ("ATMOS", SN_SKY),
    "truehd": ("TRUEHD", SN_SKY), "dts": ("DTS", SN_SKY),
    "dts-hd": ("DTS-HD", SN_SKY), "dtsx": ("DTS:X", SN_PEACH),
    "dts-x": ("DTS:X", SN_PEACH), "flac": ("FLAC", SN_SKY),
    "aac": ("AAC", SN_WHITE), "ac3": ("AC3", SN_WHITE),
    "eac3": ("EAC3", SN_WHITE), "ddp": ("DD+", SN_WHITE),
    "dd": ("DD", SN_WHITE), "mp3": ("MP3", SN_WHITE), "opus": ("OPUS", SN_WHITE),
    "web-dl": ("WEB-DL", SN_MINT), "webdl": ("WEB-DL", SN_MINT),
    "webrip": ("WEBRIP", SN_MINT), "bluray": ("BLURAY", SN_SKY),
    "blu-ray": ("BLURAY", SN_SKY), "remux": ("REMUX", SN_YELLOW),
    "hdtv": ("HDTV", SN_MINT), "dvd": ("DVD", SN_MINT),
    "cached": ("CACHED", SN_YELLOW), "uncached": ("UNCACHED", SN_WHITE),
    "mkv": ("MKV", SN_PINK), "mp4": ("MP4", SN_PINK), "avi": ("AVI", SN_PINK),
    "ts": ("TS", SN_PINK), "m2ts": ("M2TS", SN_PINK),
    "hdr": ("HDR", SN_PEACH), "hdr10": ("HDR10", SN_PEACH),
    "hdr10plus": ("HDR10+", SN_PEACH), "hlg": ("HLG", SN_PEACH),
    "dv": ("VISION", SN_PEACH), "dolby-vision": ("VISION", SN_PEACH),
    "dv-only": ("DV ONLY", SN_PEACH), "imax": ("IMAX", SN_SKY),
    "60fps": ("60FPS", SN_LAVENDER), "120fps": ("120FPS", SN_LAVENDER),
    "50fps": ("50FPS", SN_LAVENDER), "24fps": ("24FPS", SN_LAVENDER), "hfr": ("HFR", SN_LAVENDER),
    "dual": ("DUAL", SN_MINT), "multi": ("MULTI", SN_MINT),
    "extended": ("EXTENDED", SN_PEACH), "unrated": ("UNRATED", SN_PINK),
    "remastered": ("REMASTERED", SN_YELLOW), "directors-cut": ("DIR CUT", SN_YELLOW),
}

def load_lang_flags():
    mapping = {
        "english-flag": ("gb", "ENGLISH"), "bangladesh-flag": ("bd", "BANGLADESH"),
        "india-flag": ("in", "INDIA"), "usa-flag": ("us", "USA"),
        "japan-flag": ("jp", "JAPAN"), "japan": ("jp", "JAPAN"),
        "korea-flag": ("kr", "KOREA"), "korea": ("kr", "KOREA"),
        "france": ("fr", "FRANCE"), "germany": ("de", "GERMANY"),
        "spain": ("es", "SPANISH"), "italy": ("it", "ITALY"),
        "russia": ("ru", "RUSSIA"), "brazil": ("br", "BRAZIL"),
        "nepal": ("np", "NEPAL"), "nepali-flag": ("np", "NEPALI"),
        "saudi-arabia-flag": ("sa", "ARABIC"), "saudi-arabia": ("sa", "ARABIC"),
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
    arr = np.array(glyph_sc)
    vis = arr[:, :, 3] > 50
    if not np.any(vis):
        return glyph_sc
    rgb = arr[vis, :3].astype(np.float32)
    lum = np.mean(0.299 * rgb[:, 0] + 0.587 * rgb[:, 1] + 0.114 * rgb[:, 2])
    sat = np.mean(np.max(rgb, axis=1) - np.min(rgb, axis=1))
    if lum > 195 and sat < 35:
        arr_dark = arr.copy()
        arr_dark[:, :, 0] = 20
        arr_dark[:, :, 1] = 20
        arr_dark[:, :, 2] = 24
        return Image.fromarray(arr_dark, "RGBA")
    return glyph_sc

def make_flag_img(cc, fh_px=int(38 * SCALE)):
    flag_p = os.path.join(FLAG_DIR, f"{cc}.png")
    if not os.path.exists(flag_p):
        return None
    flag = Image.open(flag_p).convert("RGBA")
    fw = int(flag.width * (fh_px / float(flag.height)))
    sc = flag.resize((fw, fh_px), Image.Resampling.LANCZOS)
    mask = Image.new("L", (fw, fh_px), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw - 1, fh_px - 1], radius=int(3 * SCALE), fill=255)
    out = Image.new("RGBA", (fw, fh_px), (0, 0, 0, 0))
    out.paste(sc, (0, 0), mask)
    return out

def fit_glyph(img_p, th=int(44 * SCALE), mw=int(150 * SCALE)):
    im = Image.open(img_p).convert("RGBA")
    bb = im.getbbox()
    g = im.crop(bb) if bb else im
    sc = min(th / float(g.height), mw / float(g.width))
    return g.resize((max(1, int(round(g.width * sc))), max(1, int(round(g.height * sc)))), Image.Resampling.LANCZOS)

# ==============================================================================
# THEME 1: MATRIX TERMINAL >_ (matrix-terminal)
# ==============================================================================
def render_matrix_badge(name, filename):
    m_x, m_y = 4 * SCALE, 8 * SCALE
    green_txt = (74, 222, 128, 255)
    green_rim = (34, 197, 94, 220)
    bg_col = (6, 14, 8, 252)

    if name in CLEAN_TEXTS:
        txt, _ = CLEAN_TEXTS[name]
        disp = f">_{txt}"
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), disp, font=font_mono)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 36 * SCALE, 102 * SCALE)
        c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(c)
        dr.rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], fill=bg_col, outline=green_rim, width=int(1.6 * SCALE))
        dr.text(((w - tw) // 2 - bb[0], (TOTAL_H - th) // 2 - bb[1]), disp, font=font_mono, fill=green_txt)
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 8 * SCALE + tw
            w = max(cw + 36 * SCALE, 110 * SCALE)
            c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
            dr = ImageDraw.Draw(c)
            dr.rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], fill=bg_col, outline=green_rim, width=int(1.6 * SCALE))
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, (TOTAL_H - fl.height) // 2))
            dr.text((cx_f + fl.width + 8 * SCALE - bb[0], (TOTAL_H - th) // 2 - bb[1]), lang, font=font_sub, fill=green_txt)
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    gs = fit_glyph(src_p)
    w = max(gs.width + 36 * SCALE, 102 * SCALE)
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(c)
    dr.rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], fill=bg_col, outline=green_rim, width=int(1.6 * SCALE))
    gx, gy = (w - gs.width) // 2, (TOTAL_H - gs.height) // 2
    arr = np.array(gs)
    vis = arr[:, :, 3] > 50
    if np.any(vis):
        lum = np.mean(0.299 * arr[vis, 0] + 0.587 * arr[vis, 1] + 0.114 * arr[vis, 2])
        if lum < 65:
            ga = gs.split()[3]
            halo = ga.filter(ImageFilter.MaxFilter(5))
            c.paste(Image.new("RGBA", gs.size, (255, 255, 255, 230)), (gx, gy), halo)
    c.alpha_composite(gs, (gx, gy))
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

# ==============================================================================
# THEME 2: PEELED STICKY NOTE (sticky-note)
# ==============================================================================
def make_sticky_canvas(w, note_col):
    m_x, m_y = 4 * SCALE, 8 * SCALE
    fold = int(18 * SCALE)
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(c)
    poly = [(m_x, m_y), (w - m_x - 1, m_y), (w - m_x - 1, TOTAL_H - m_y - 1 - fold), (w - m_x - 1 - fold, TOTAL_H - m_y - 1), (m_x, TOTAL_H - m_y - 1)]
    dr.polygon(poly, fill=note_col)
    r1, g1, b1, _ = note_col
    flap = (max(0, r1 - 42), max(0, g1 - 42), max(0, b1 - 42), 255)
    dr.polygon([(w - m_x - 1 - fold, TOTAL_H - m_y - 1), (w - m_x - 1 - fold, TOTAL_H - m_y - 1 - fold), (w - m_x - 1, TOTAL_H - m_y - 1 - fold)], fill=flap)
    return c

def render_sticky_badge(name, filename):
    ink = (20, 20, 24, 255)
    if name in CLEAN_TEXTS:
        txt, note_col = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_bold)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 44 * SCALE, 106 * SCALE)
        c = make_sticky_canvas(w, note_col)
        ImageDraw.Draw(c).text(((w - tw) // 2 - bb[0], (TOTAL_H - th) // 2 - bb[1]), txt, font=font_bold, fill=ink)
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 8 * SCALE + tw
            w = max(cw + 44 * SCALE, 114 * SCALE)
            c = make_sticky_canvas(w, SN_WHITE)
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, (TOTAL_H - fl.height) // 2))
            ImageDraw.Draw(c).text((cx_f + fl.width + 8 * SCALE - bb[0], (TOTAL_H - th) // 2 - bb[1]), lang, font=font_sub, fill=ink)
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    gs = adapt_logo_for_light_surface(fit_glyph(src_p))
    w = max(gs.width + 44 * SCALE, 106 * SCALE)
    c = make_sticky_canvas(w, SN_WHITE)
    c.alpha_composite(gs, ((w - gs.width) // 2, (TOTAL_H - gs.height) // 2))
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
    deploy_theme("matrix-terminal", render_matrix_badge)
    deploy_theme("sticky-note", render_sticky_badge)

if __name__ == "__main__":
    main()
