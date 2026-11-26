import os, sys, json, re, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "gta6-vice-sunset")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

font_gta = ImageFont.truetype("impact.ttf", int(52 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(38 * SCALE))

CLEAN_TEXTS = {
    "4k": "4K", "8k": "8K", "1080p": "1080P", "720p": "720P", "480p": "480P",
    "1440p": "1440P", "576p": "576P", "lowres": "LOWRES", "3d": "3D",
    "hevc": "HEVC", "av1": "AV1", "avc": "H.264", "x264": "x264", "x265": "x265",
    "h264": "H.264", "h265": "H.265", "vp9": "VP9", "vc1": "VC-1", "vvc": "VVC",
    "10-bit": "10-BIT", "10bit": "10-BIT", "8-bit": "8-BIT", "8bit": "8-BIT",
    "12-bit": "12-BIT", "12bit": "12-BIT",
    "5.1": "5.1", "5_1": "5.1", "7.1": "7.1", "7_1": "7.1", "2.0": "2.0",
    "2_0": "2.0", "1.0": "1.0", "1_0": "1.0", "6.1": "6.1", "6_1": "6.1",
    "atmos": "ATMOS", "dolby-atmos": "ATMOS", "truehd": "TRUEHD",
    "dts": "DTS", "dts-hd": "DTS-HD", "dtsx": "DTS:X", "dts-x": "DTS:X",
    "flac": "FLAC", "aac": "AAC", "ac3": "AC3", "eac3": "EAC3", "ddp": "DD+",
    "dd": "DD", "mp3": "MP3", "opus": "OPUS",
    "web-dl": "WEB-DL", "webdl": "WEB-DL", "webrip": "WEBRIP",
    "bluray": "BLURAY", "blu-ray": "BLURAY", "remux": "REMUX", "hdtv": "HDTV", "dvd": "DVD",
    "cached": "CACHED", "uncached": "UNCACHED",
    "mkv": "MKV", "mp4": "MP4", "avi": "AVI", "ts": "TS", "m2ts": "M2TS",
    "hdr": "HDR", "hdr10": "HDR10", "hdr10plus": "HDR10+", "hlg": "HLG",
    "dv": "VISION", "dolby-vision": "VISION", "dv-only": "DV ONLY", "imax": "IMAX",
    "60fps": "60FPS", "120fps": "120FPS", "50fps": "50FPS", "24fps": "24FPS", "hfr": "HFR",
    "dual": "DUAL", "multi": "MULTI", "extended": "EXTENDED", "unrated": "UNRATED",
    "remastered": "REMASTERED", "directors-cut": "DIR CUT",
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

SKY_ROWS = None
def get_sky_rows():
    global SKY_ROWS
    if SKY_ROWS is not None:
        return SKY_ROWS
    m_y = 8 * SCALE
    rows = np.zeros((TOTAL_H, 1, 4), dtype=np.uint8)
    for y in range(TOTAL_H):
        ty = np.clip((y - m_y) / float(TOTAL_H - 2 * m_y), 0.0, 1.0)
        if ty < 0.55:
            u = ty / 0.55
            r, g, b = int(28 * (1 - u) + 217 * u), int(16 * (1 - u) + 38 * u), int(62 * (1 - u) + 114 * u)
        else:
            u = (ty - 0.55) / 0.45
            r, g, b = int(217 * (1 - u) + 255 * u), int(38 * (1 - u) + 158 * u), int(114 * (1 - u) + 68 * u)
        rows[y, 0, 0], rows[y, 0, 1], rows[y, 0, 2], rows[y, 0, 3] = r, g, b, 255
    SKY_ROWS = rows
    return rows

def draw_palm_silhouette(draw, base_x, base_y, scale_p=1.0):
    s = scale_p * SCALE
    trunk = [(base_x, base_y), (base_x - 3 * s, base_y - 16 * s), (base_x - 1 * s, base_y - 32 * s)]
    draw.line(trunk, fill=(14, 8, 26, 220), width=max(1, int(3.2 * s)))
    tx, ty = trunk[-1]
    fronds = [
        [(tx, ty), (tx - 12 * s, ty - 6 * s), (tx - 18 * s, ty + 2 * s)],
        [(tx, ty), (tx - 10 * s, ty - 11 * s), (tx - 14 * s, ty - 8 * s)],
        [(tx, ty), (tx + 2 * s, ty - 12 * s), (tx + 8 * s, ty - 10 * s)],
        [(tx, ty), (tx + 12 * s, ty - 7 * s), (tx + 17 * s, ty + 1 * s)],
        [(tx, ty), (tx + 10 * s, ty - 1 * s), (tx + 14 * s, ty + 7 * s)],
    ]
    for fr in fronds:
        draw.polygon(fr, fill=(14, 8, 26, 220))

def make_vice_panel(w):
    m_x, m_y, rad = 4 * SCALE, 8 * SCALE, 8 * SCALE
    mask = Image.new("L", (w, TOTAL_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, fill=255)
    base = Image.fromarray(np.repeat(get_sky_rows(), w, axis=1), "RGBA")
    bdr = ImageDraw.Draw(base)
    sun_r = int(22 * SCALE)
    sx, sy = w - m_x - int(22 * SCALE), TOTAL_H - m_y - int(8 * SCALE)
    bdr.ellipse([sx - sun_r, sy - sun_r, sx + sun_r, sy + sun_r], fill=(255, 224, 130, 140))
    draw_palm_silhouette(bdr, w - m_x - int(14 * SCALE), TOTAL_H - m_y, scale_p=1.6)
    draw_palm_silhouette(bdr, m_x + int(14 * SCALE), TOTAL_H - m_y, scale_p=1.15)
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    c.paste(base, (0, 0), mask)
    ImageDraw.Draw(c).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, outline=(255, 190, 225, 210), width=int(1.6 * SCALE))
    return c

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

def render_gta6_badge(name, filename):
    if name in CLEAN_TEXTS:
        txt = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_gta)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 48 * SCALE, 112 * SCALE)
        c = make_vice_panel(w)
        tx, ty = (w - tw) // 2 - bb[0], (TOTAL_H - th) // 2 - bb[1]
        ImageDraw.Draw(c).text((tx, ty), txt, font=font_gta, fill=(255, 255, 255, 255), stroke_width=int(3.2 * SCALE), stroke_fill=(12, 6, 20, 250))
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 8 * SCALE + tw
            w = max(cw + 48 * SCALE, 118 * SCALE)
            c = make_vice_panel(w)
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, (TOTAL_H - fl.height) // 2))
            tx, ty = cx_f + fl.width + 8 * SCALE - bb[0], (TOTAL_H - th) // 2 - bb[1]
            ImageDraw.Draw(c).text((tx, ty), lang, font=font_sub, fill=(255, 255, 255, 255), stroke_width=int(2.8 * SCALE), stroke_fill=(12, 6, 20, 250))
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    im = Image.open(src_p).convert("RGBA")
    bb = im.getbbox()
    g = im.crop(bb) if bb else im
    sc = min((44 * SCALE) / float(g.height), (150 * SCALE) / float(g.width))
    gw, gh = max(1, int(round(g.width * sc))), max(1, int(round(g.height * sc)))
    gs = g.resize((gw, gh), Image.Resampling.LANCZOS)

    # Preserve original logo artwork & details; add adaptive contrast halo for Vice Sunset readability
    arr = np.array(gs)
    vis = arr[:, :, 3] > 50
    ga = gs.split()[3]
    w = max(gw + 48 * SCALE, 112 * SCALE)
    c = make_vice_panel(w)
    gx, gy = (w - gw) // 2, (TOTAL_H - gh) // 2
    if np.any(vis):
        lum = np.mean(0.299 * arr[vis, 0] + 0.587 * arr[vis, 1] + 0.114 * arr[vis, 2])
        if lum < 95:
            halo = ga.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.5 * SCALE))
            c.paste(Image.new("RGBA", (gw, gh), (255, 235, 245, 230)), (gx, gy), halo)
        else:
            halo = ga.filter(ImageFilter.MaxFilter(5))
            c.paste(Image.new("RGBA", (gw, gh), (12, 6, 20, 210)), (gx, gy), halo)
    c.alpha_composite(gs, (gx, gy))
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def main():
    get_sky_rows()
    os.makedirs(THEME_BADGES_DIR, exist_ok=True)
    files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]

    def _job(fn):
        name = fn[:-5]
        out_p = os.path.join(THEME_BADGES_DIR, fn)
        if name == "live":
            shutil.copyfile(os.path.join(BADGES_DIR, "live.webp"), out_p)
            return True
        im = render_gta6_badge(name, fn)
        if im is not None:
            im.save(out_p, "WEBP", quality=95, method=6)
            return True
        return False

    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(_job, files))

    h = hashlib.sha256(open(os.path.join(THEME_BADGES_DIR, "live.webp"), "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, "gta6-vice-sunset live.webp hash mismatch!"

    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("filters", []):
        if "imageURL" in item:
            item["imageURL"] = item["imageURL"].replace("/main/badges/", "/main/themes/gta6-vice-sunset/badges/")
    for p in [os.path.join(REPO_ROOT, "gta6-vice-sunset.json"), os.path.join(THEME_DIR, "gta6-vice-sunset.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    print(f"[SUCCESS] gta6-vice-sunset: rendered {sum(res)}/{len(files)} badges + manifests. live.webp verified.")

if __name__ == "__main__":
    main()
