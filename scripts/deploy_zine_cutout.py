import os, sys, json, re, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "zine-cutout")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

font_imp = ImageFont.truetype("impact.ttf", int(48 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(38 * SCALE))

ZINE_WHITE = (255, 255, 255, 255)
ZINE_YELLOW = (250, 204, 21, 255)
ZINE_CYAN = (34, 211, 238, 255)
ZINE_MINT = (74, 222, 128, 255)
ZINE_PINK = (244, 114, 182, 255)
ZINE_PALETTE = [ZINE_WHITE, ZINE_YELLOW, ZINE_CYAN, ZINE_MINT, ZINE_PINK]

CLEAN_TEXTS = {
    "4k": ("4K", ZINE_YELLOW), "8k": ("8K", ZINE_YELLOW),
    "1080p": ("1080P", ZINE_WHITE), "720p": ("720P", ZINE_WHITE),
    "480p": ("480P", ZINE_WHITE), "1440p": ("1440P", ZINE_WHITE),
    "576p": ("576P", ZINE_WHITE), "lowres": ("LOWRES", ZINE_WHITE),
    "3d": ("3D", ZINE_PINK),
    "hevc": ("HEVC", ZINE_CYAN), "av1": ("AV1", ZINE_MINT),
    "avc": ("H.264", ZINE_CYAN), "x264": ("x264", ZINE_CYAN),
    "x265": ("x265", ZINE_CYAN), "h264": ("H.264", ZINE_CYAN),
    "h265": ("H.265", ZINE_CYAN), "vp9": ("VP9", ZINE_CYAN),
    "vc1": ("VC-1", ZINE_CYAN), "vvc": ("VVC", ZINE_CYAN),
    "10-bit": ("10-BIT", ZINE_WHITE), "10bit": ("10-BIT", ZINE_WHITE),
    "8-bit": ("8-BIT", ZINE_WHITE), "8bit": ("8-BIT", ZINE_WHITE),
    "12-bit": ("12-BIT", ZINE_WHITE), "12bit": ("12-BIT", ZINE_WHITE),
    "5.1": ("5.1", ZINE_WHITE), "5_1": ("5.1", ZINE_WHITE),
    "7.1": ("7.1", ZINE_WHITE), "7_1": ("7.1", ZINE_WHITE),
    "2.0": ("2.0", ZINE_WHITE), "2_0": ("2.0", ZINE_WHITE),
    "1.0": ("1.0", ZINE_WHITE), "1_0": ("1.0", ZINE_WHITE),
    "6.1": ("6.1", ZINE_WHITE), "6_1": ("6.1", ZINE_WHITE),
    "atmos": ("ATMOS", ZINE_YELLOW), "dolby-atmos": ("ATMOS", ZINE_YELLOW),
    "truehd": ("TRUEHD", ZINE_YELLOW), "dts": ("DTS", ZINE_YELLOW),
    "dts-hd": ("DTS-HD", ZINE_YELLOW), "dtsx": ("DTS:X", ZINE_YELLOW),
    "dts-x": ("DTS:X", ZINE_YELLOW), "flac": ("FLAC", ZINE_CYAN),
    "aac": ("AAC", ZINE_WHITE), "ac3": ("AC3", ZINE_WHITE),
    "eac3": ("EAC3", ZINE_WHITE), "ddp": ("DD+", ZINE_WHITE),
    "dd": ("DD", ZINE_WHITE), "mp3": ("MP3", ZINE_WHITE), "opus": ("OPUS", ZINE_WHITE),
    "web-dl": ("WEB-DL", ZINE_MINT), "webdl": ("WEB-DL", ZINE_MINT),
    "webrip": ("WEBRIP", ZINE_MINT), "bluray": ("BLURAY", ZINE_CYAN),
    "blu-ray": ("BLURAY", ZINE_CYAN), "remux": ("REMUX", ZINE_YELLOW),
    "hdtv": ("HDTV", ZINE_MINT), "dvd": ("DVD", ZINE_MINT),
    "cached": ("CACHED", ZINE_YELLOW), "uncached": ("UNCACHED", ZINE_WHITE),
    "mkv": ("MKV", ZINE_PINK), "mp4": ("MP4", ZINE_PINK), "avi": ("AVI", ZINE_PINK),
    "ts": ("TS", ZINE_PINK), "m2ts": ("M2TS", ZINE_PINK),
    "hdr": ("HDR", ZINE_YELLOW), "hdr10": ("HDR10", ZINE_YELLOW),
    "hdr10plus": ("HDR10+", ZINE_YELLOW), "hlg": ("HLG", ZINE_YELLOW),
    "dv": ("VISION", ZINE_WHITE), "dolby-vision": ("VISION", ZINE_WHITE),
    "dv-only": ("DV ONLY", ZINE_WHITE), "imax": ("IMAX", ZINE_CYAN),
    "60fps": ("60FPS", ZINE_CYAN), "120fps": ("120FPS", ZINE_CYAN),
    "50fps": ("50FPS", ZINE_CYAN), "24fps": ("24FPS", ZINE_CYAN), "hfr": ("HFR", ZINE_CYAN),
    "dual": ("DUAL", ZINE_MINT), "multi": ("MULTI", ZINE_MINT),
    "extended": ("EXTENDED", ZINE_PINK), "unrated": ("UNRATED", ZINE_PINK),
    "remastered": ("REMASTERED", ZINE_YELLOW), "directors-cut": ("DIR CUT", ZINE_YELLOW),
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

def make_flag_img(cc, fh_px=int(38 * SCALE)):
    flag_p = os.path.join(FLAG_DIR, f"{cc}.png")
    if not os.path.exists(flag_p):
        return None
    flag = Image.open(flag_p).convert("RGBA")
    fw = int(flag.width * (fh_px / float(flag.height)))
    sc = flag.resize((fw, fh_px), Image.Resampling.LANCZOS)
    mask = Image.new("L", (fw, fh_px), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, fw - 1, fh_px - 1], radius=int(2 * SCALE), fill=255)
    out = Image.new("RGBA", (fw, fh_px), (0, 0, 0, 0))
    out.paste(sc, (0, 0), mask)
    return out

def deterministic_tilt(name):
    seed = sum(ord(ch) * (i + 1) for i, ch in enumerate(name))
    return -1.6 if (seed % 2 == 0) else 1.6

def render_zine_badge(name, filename):
    tilt = deterministic_tilt(name)
    ink = (12, 12, 12, 255)
    m_x, m_y = 6 * SCALE, 10 * SCALE

    if name in CLEAN_TEXTS:
        txt, bg_col = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_imp)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 38 * SCALE, 102 * SCALE)
        c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
        dr = ImageDraw.Draw(c)
        dr.rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], fill=bg_col, outline=(0, 0, 0, 255), width=int(2.2 * SCALE))
        dr.text(((w - tw) // 2 - bb[0], (TOTAL_H - th) // 2 - bb[1]), txt, font=font_imp, fill=ink)
        rot = c.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=False)
        return rot.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 8 * SCALE + tw
            w = max(cw + 38 * SCALE, 110 * SCALE)
            c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
            dr = ImageDraw.Draw(c)
            dr.rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], fill=ZINE_WHITE, outline=(0, 0, 0, 255), width=int(2.2 * SCALE))
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, (TOTAL_H - fl.height) // 2))
            dr.text((cx_f + fl.width + 8 * SCALE - bb[0], (TOTAL_H - th) // 2 - bb[1]), lang, font=font_sub, fill=ink)
            rot = c.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=False)
            return rot.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    im = Image.open(src_p).convert("RGBA")
    bb = im.getbbox()
    g = im.crop(bb) if bb else im
    sc = min((44 * SCALE) / float(g.height), (150 * SCALE) / float(g.width))
    gw, gh = max(1, int(round(g.width * sc))), max(1, int(round(g.height * sc)))
    gs = adapt_logo_for_light_surface(g.resize((gw, gh), Image.Resampling.LANCZOS))

    w = max(gw + 38 * SCALE, 102 * SCALE)
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(c)
    dr.rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], fill=ZINE_WHITE, outline=(0, 0, 0, 255), width=int(2.2 * SCALE))
    c.alpha_composite(gs, ((w - gw) // 2, (TOTAL_H - gh) // 2))
    rot = c.rotate(tilt, resample=Image.Resampling.BICUBIC, expand=False)
    return rot.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def main():
    os.makedirs(THEME_BADGES_DIR, exist_ok=True)
    files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]

    def _job(fn):
        name = fn[:-5]
        out_p = os.path.join(THEME_BADGES_DIR, fn)
        if name == "live":
            shutil.copyfile(os.path.join(BADGES_DIR, "live.webp"), out_p)
            return True
        im = render_zine_badge(name, fn)
        if im is not None:
            im.save(out_p, "WEBP", quality=95, method=6)
            return True
        return False

    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(_job, files))

    h = hashlib.sha256(open(os.path.join(THEME_BADGES_DIR, "live.webp"), "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, "zine-cutout live.webp hash mismatch!"

    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("filters", []):
        if "imageURL" in item:
            item["imageURL"] = item["imageURL"].replace("/main/badges/", "/main/themes/zine-cutout/badges/")
    for p in [os.path.join(REPO_ROOT, "zine-cutout.json"), os.path.join(THEME_DIR, "zine-cutout.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    print(f"[SUCCESS] zine-cutout: rendered {sum(res)}/{len(files)} badges + manifests. live.webp verified.")

if __name__ == "__main__":
    main()
