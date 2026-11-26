import os, sys, json, re, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "comic-bubble")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

font_comic = ImageFont.truetype("comicbd.ttf", int(44 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(38 * SCALE))

CB_WHITE = (255, 255, 255, 255)
CB_YELLOW = (254, 240, 138, 255)
CB_PEACH = (254, 215, 170, 255)
CB_SKY = (186, 230, 253, 255)
CB_LAVENDER = (233, 213, 255, 255)
CB_MINT = (167, 243, 208, 255)
CB_PINK = (251, 207, 232, 255)

CLEAN_TEXTS = {
    "4k": ("4K", CB_YELLOW), "8k": ("8K", CB_YELLOW),
    "1080p": ("1080P", CB_SKY), "720p": ("720P", CB_SKY),
    "480p": ("480P", CB_WHITE), "1440p": ("1440P", CB_SKY),
    "576p": ("576P", CB_WHITE), "lowres": ("LOWRES", CB_WHITE),
    "3d": ("3D", CB_PINK),
    "hevc": ("HEVC", CB_SKY), "av1": ("AV1", CB_MINT),
    "avc": ("H.264", CB_SKY), "x264": ("x264", CB_SKY),
    "x265": ("x265", CB_SKY), "h264": ("H.264", CB_SKY),
    "h265": ("H.265", CB_SKY), "vp9": ("VP9", CB_SKY),
    "vc1": ("VC-1", CB_SKY), "vvc": ("VVC", CB_SKY),
    "10-bit": ("10-BIT", CB_LAVENDER), "10bit": ("10-BIT", CB_LAVENDER),
    "8-bit": ("8-BIT", CB_LAVENDER), "8bit": ("8-BIT", CB_LAVENDER),
    "12-bit": ("12-BIT", CB_LAVENDER), "12bit": ("12-BIT", CB_LAVENDER),
    "5.1": ("5.1", CB_WHITE), "5_1": ("5.1", CB_WHITE),
    "7.1": ("7.1", CB_WHITE), "7_1": ("7.1", CB_WHITE),
    "2.0": ("2.0", CB_WHITE), "2_0": ("2.0", CB_WHITE),
    "1.0": ("1.0", CB_WHITE), "1_0": ("1.0", CB_WHITE),
    "6.1": ("6.1", CB_WHITE), "6_1": ("6.1", CB_WHITE),
    "atmos": ("ATMOS", CB_SKY), "dolby-atmos": ("ATMOS", CB_SKY),
    "truehd": ("TRUEHD", CB_SKY), "dts": ("DTS", CB_SKY),
    "dts-hd": ("DTS-HD", CB_SKY), "dtsx": ("DTS:X", CB_PEACH),
    "dts-x": ("DTS:X", CB_PEACH), "flac": ("FLAC", CB_SKY),
    "aac": ("AAC", CB_WHITE), "ac3": ("AC3", CB_WHITE),
    "eac3": ("EAC3", CB_WHITE), "ddp": ("DD+", CB_WHITE),
    "dd": ("DD", CB_WHITE), "mp3": ("MP3", CB_WHITE), "opus": ("OPUS", CB_WHITE),
    "web-dl": ("WEB-DL", CB_MINT), "webdl": ("WEB-DL", CB_MINT),
    "webrip": ("WEBRIP", CB_MINT), "bluray": ("BLURAY", CB_SKY),
    "blu-ray": ("BLURAY", CB_SKY), "remux": ("REMUX", CB_YELLOW),
    "hdtv": ("HDTV", CB_MINT), "dvd": ("DVD", CB_MINT),
    "cached": ("CACHED", CB_YELLOW), "uncached": ("UNCACHED", CB_WHITE),
    "mkv": ("MKV", CB_PINK), "mp4": ("MP4", CB_PINK), "avi": ("AVI", CB_PINK),
    "ts": ("TS", CB_PINK), "m2ts": ("M2TS", CB_PINK),
    "hdr": ("HDR", CB_PEACH), "hdr10": ("HDR10", CB_PEACH),
    "hdr10plus": ("HDR10+", CB_PEACH), "hlg": ("HLG", CB_PEACH),
    "dv": ("VISION", CB_PEACH), "dolby-vision": ("VISION", CB_PEACH),
    "dv-only": ("DV ONLY", CB_PEACH), "imax": ("IMAX", CB_SKY),
    "60fps": ("60FPS", CB_LAVENDER), "120fps": ("120FPS", CB_LAVENDER),
    "50fps": ("50FPS", CB_LAVENDER), "24fps": ("24FPS", CB_LAVENDER), "hfr": ("HFR", CB_LAVENDER),
    "dual": ("DUAL", CB_MINT), "multi": ("MULTI", CB_MINT),
    "extended": ("EXTENDED", CB_PEACH), "unrated": ("UNRATED", CB_PINK),
    "remastered": ("REMASTERED", CB_YELLOW), "directors-cut": ("DIR CUT", CB_YELLOW),
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
        arr_dark[:, :, 0] = 12
        arr_dark[:, :, 1] = 12
        arr_dark[:, :, 2] = 14
        return Image.fromarray(arr_dark, "RGBA")
    return glyph_sc

def make_flag_img(cc, fh_px=int(36 * SCALE)):
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

def make_bubble(w, fill_col):
    m_x, m_y = 6 * SCALE, 6 * SCALE
    rad = (TOTAL_H - 2 * m_y - 8 * SCALE) // 2
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(c)
    dr.rounded_rectangle([m_x + 3 * SCALE, m_y + 3 * SCALE, w - m_x, TOTAL_H - m_y - 6 * SCALE], radius=rad, fill=(0, 0, 0, 255))
    dr.rounded_rectangle([m_x, m_y, w - m_x - 3 * SCALE, TOTAL_H - m_y - 9 * SCALE], radius=rad, fill=fill_col, outline=(0, 0, 0, 255), width=int(2.4 * SCALE))
    dr.polygon([(m_x + 16 * SCALE, TOTAL_H - m_y - 11 * SCALE), (m_x + 26 * SCALE, TOTAL_H - m_y - 11 * SCALE), (m_x + 12 * SCALE, TOTAL_H - m_y)], fill=fill_col, outline=(0, 0, 0, 255))
    cy_b = (m_y + TOTAL_H - m_y - 9 * SCALE) // 2
    return c, cy_b

def render_comic_badge(name, filename):
    ink = (12, 12, 14, 255)
    if name in CLEAN_TEXTS:
        txt, fill_col = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_comic)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 44 * SCALE, 104 * SCALE)
        c, cy_b = make_bubble(w, fill_col)
        ImageDraw.Draw(c).text(((w - tw) // 2 - bb[0], cy_b - th // 2 - bb[1]), txt, font=font_comic, fill=ink)
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 8 * SCALE + tw
            w = max(cw + 44 * SCALE, 112 * SCALE)
            c, cy_b = make_bubble(w, CB_WHITE)
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, cy_b - fl.height // 2))
            ImageDraw.Draw(c).text((cx_f + fl.width + 8 * SCALE - bb[0], cy_b - th // 2 - bb[1]), lang, font=font_sub, fill=ink)
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    im = Image.open(src_p).convert("RGBA")
    bb = im.getbbox()
    g = im.crop(bb) if bb else im
    sc = min((42 * SCALE) / float(g.height), (148 * SCALE) / float(g.width))
    gw, gh = max(1, int(round(g.width * sc))), max(1, int(round(g.height * sc)))
    gs = adapt_logo_for_light_surface(g.resize((gw, gh), Image.Resampling.LANCZOS))

    w = max(gw + 44 * SCALE, 104 * SCALE)
    c, cy_b = make_bubble(w, CB_WHITE)
    c.alpha_composite(gs, ((w - gw) // 2, cy_b - gh // 2))
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def main():
    os.makedirs(THEME_BADGES_DIR, exist_ok=True)
    files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]

    def _job(fn):
        name = fn[:-5]
        out_p = os.path.join(THEME_BADGES_DIR, fn)
        if name == "live":
            shutil.copyfile(os.path.join(BADGES_DIR, "live.webp"), out_p)
            return True
        im = render_comic_badge(name, fn)
        if im is not None:
            im.save(out_p, "WEBP", quality=95, method=6)
            return True
        return False

    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(_job, files))

    h = hashlib.sha256(open(os.path.join(THEME_BADGES_DIR, "live.webp"), "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, "comic-bubble live.webp hash mismatch!"

    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("filters", []):
        if "imageURL" in item:
            item["imageURL"] = item["imageURL"].replace("/main/badges/", "/main/themes/comic-bubble/badges/")
    for p in [os.path.join(REPO_ROOT, "comic-bubble.json"), os.path.join(THEME_DIR, "comic-bubble.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    print(f"[SUCCESS] comic-bubble: rendered {sum(res)}/{len(files)} badges + manifests. live.webp verified.")

if __name__ == "__main__":
    main()
