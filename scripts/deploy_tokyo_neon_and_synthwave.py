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

font_impact = ImageFont.truetype("impact.ttf", int(50 * SCALE))
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

def neon_color_for(name):
    if name in ("4k", "8k", "dv", "dolby-vision", "dv-only", "hdr10plus", "imax", "cached"):
        return (255, 56, 165, 235)   # Tokyo neon magenta-pink
    if name in ("remux", "atmos", "dolby-atmos", "truehd", "dtsx", "dts-x", "120fps", "60fps", "av1"):
        return (0, 235, 255, 235)    # Electric cyan plasma
    if name in ("hdr", "hdr10", "hlg", "extended", "unrated", "remastered"):
        return (255, 196, 48, 235)   # Warm amber neon
    return (56, 189, 248, 235)       # Crisp ice-cyan

def render_tokyo_neon_badge(name, filename):
    glow_col = neon_color_for(name)
    if name in CLEAN_TEXTS:
        txt = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_impact)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 44 * SCALE, 108 * SCALE)
        tx, ty = (w - tw) // 2 - bb[0], (TOTAL_H - th) // 2 - bb[1]
        glow = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).text((tx, ty), txt, font=font_impact, fill=glow_col, stroke_width=int(4.2 * SCALE), stroke_fill=glow_col)
        glow = glow.filter(ImageFilter.GaussianBlur(6.5 * SCALE))
        c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
        c = Image.alpha_composite(c, glow)
        ImageDraw.Draw(c).text((tx, ty), txt, font=font_impact, fill=(248, 252, 255, 255), stroke_width=int(1.2 * SCALE), stroke_fill=glow_col)
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 10 * SCALE + tw
            w = max(cw + 44 * SCALE, 120 * SCALE)
            c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, (TOTAL_H - fl.height) // 2))
            tx, ty = cx_f + fl.width + 10 * SCALE - bb[0], (TOTAL_H - th) // 2 - bb[1]
            glow = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
            ImageDraw.Draw(glow).text((tx, ty), lang, font=font_sub, fill=glow_col, stroke_width=int(3.6 * SCALE), stroke_fill=glow_col)
            glow = glow.filter(ImageFilter.GaussianBlur(5.5 * SCALE))
            c = Image.alpha_composite(c, glow)
            ImageDraw.Draw(c).text((tx, ty), lang, font=font_sub, fill=(248, 252, 255, 255), stroke_width=int(1.0 * SCALE), stroke_fill=glow_col)
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    im = Image.open(src_p).convert("RGBA")
    bb = im.getbbox()
    g = im.crop(bb) if bb else im
    sc = min((48 * SCALE) / float(g.height), (156 * SCALE) / float(g.width))
    gw, gh = max(1, int(round(g.width * sc))), max(1, int(round(g.height * sc)))
    gs = g.resize((gw, gh), Image.Resampling.LANCZOS)
    w = max(gw + 36 * SCALE, 108 * SCALE)
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    gx, gy = (w - gw) // 2, (TOTAL_H - gh) // 2
    ga = gs.split()[3]
    halo = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    halo.paste(Image.new("RGBA", (gw, gh), (0, 235, 255, 130)), (gx, gy), ga.filter(ImageFilter.MaxFilter(5)))
    halo = halo.filter(ImageFilter.GaussianBlur(4.5 * SCALE))
    c = Image.alpha_composite(c, halo)
    c.alpha_composite(gs, (gx, gy))
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

SYNTH_ROWS = None
def get_synth_rows():
    global SYNTH_ROWS
    if SYNTH_ROWS is not None:
        return SYNTH_ROWS
    m_y = 8 * SCALE
    rows = np.zeros((TOTAL_H, 1, 4), dtype=np.uint8)
    for y in range(TOTAL_H):
        ty = np.clip((y - m_y) / float(TOTAL_H - 2 * m_y), 0.0, 1.0)
        if ty < 0.56:
            u = ty / 0.56
            r, g, b = int(14 + u * 64), int(8 + u * 12), int(42 + u * 78)
        else:
            u = (ty - 0.56) / 0.44
            r, g, b = int(28 - u * 14), int(10), int(48 - u * 22)
        rows[y, 0, 0], rows[y, 0, 1], rows[y, 0, 2], rows[y, 0, 3] = r, g, b, 255
    SYNTH_ROWS = rows
    return rows

def make_synthwave_panel(w):
    m_x, m_y, rad = 4 * SCALE, 8 * SCALE, 8 * SCALE
    mask = Image.new("L", (w, TOTAL_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, fill=255)
    base = Image.fromarray(np.repeat(get_synth_rows(), w, axis=1), "RGBA")
    bd = ImageDraw.Draw(base)
    hy = int(TOTAL_H * 0.56)
    bd.line([(m_x, hy), (w - m_x, hy)], fill=(255, 62, 185, 225), width=int(2 * SCALE))
    for gx in range(m_x, w - m_x, 22 * SCALE):
        bd.line([(gx, hy), (gx + (gx - w // 2) * 0.4, TOTAL_H - m_y)], fill=(0, 235, 255, 95), width=SCALE)
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    c.paste(base, (0, 0), mask)
    ImageDraw.Draw(c).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, outline=(0, 235, 255, 225), width=int(1.8 * SCALE))
    return c

def render_synthwave_badge(name, filename):
    if name in CLEAN_TEXTS:
        txt = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_impact)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 48 * SCALE, 112 * SCALE)
        c = make_synthwave_panel(w)
        tx, ty = (w - tw) // 2 - bb[0], (TOTAL_H - th) // 2 - bb[1]
        fg = (255, 224, 92, 255) if name in ("4k", "8k", "dv", "dolby-vision", "hdr10plus", "imax") else (255, 255, 255, 255)
        ImageDraw.Draw(c).text((tx, ty), txt, font=font_impact, fill=fg, stroke_width=int(2.4 * SCALE), stroke_fill=(255, 42, 165, 235))
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 8 * SCALE + tw
            w = max(cw + 48 * SCALE, 118 * SCALE)
            c = make_synthwave_panel(w)
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, (TOTAL_H - fl.height) // 2))
            tx, ty = cx_f + fl.width + 8 * SCALE - bb[0], (TOTAL_H - th) // 2 - bb[1]
            ImageDraw.Draw(c).text((tx, ty), lang, font=font_sub, fill=(255, 255, 255, 255), stroke_width=int(2.2 * SCALE), stroke_fill=(255, 42, 165, 235))
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
    arr = np.array(gs)
    vis = arr[:, :, 3] > 50
    ga = gs.split()[3]
    w = max(gw + 48 * SCALE, 112 * SCALE)
    c = make_synthwave_panel(w)
    gx, gy = (w - gw) // 2, (TOTAL_H - gh) // 2
    if np.any(vis):
        lum = np.mean(0.299 * arr[vis, 0] + 0.587 * arr[vis, 1] + 0.114 * arr[vis, 2])
        if lum < 95:
            halo = ga.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.5 * SCALE))
            c.paste(Image.new("RGBA", (gw, gh), (220, 245, 255, 225)), (gx, gy), halo)
        else:
            halo = ga.filter(ImageFilter.MaxFilter(5))
            c.paste(Image.new("RGBA", (gw, gh), (14, 8, 32, 210)), (gx, gy), halo)
    c.alpha_composite(gs, (gx, gy))
    return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

def build_theme(theme_id, render_fn):
    t_dir = os.path.join(REPO_ROOT, "themes", theme_id)
    tb_dir = os.path.join(t_dir, "badges")
    os.makedirs(tb_dir, exist_ok=True)
    files = [f for f in os.listdir(BADGES_DIR) if f.endswith(".webp")]

    def _job(fn):
        name = fn[:-5]
        out_p = os.path.join(tb_dir, fn)
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

    h = hashlib.sha256(open(os.path.join(tb_dir, "live.webp"), "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, f"{theme_id} live.webp hash mismatch!"

    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("filters", []):
        if "imageURL" in item:
            item["imageURL"] = item["imageURL"].replace("/main/badges/", f"/main/themes/{theme_id}/badges/")
    for p in [os.path.join(REPO_ROOT, f"{theme_id}.json"), os.path.join(t_dir, f"{theme_id}.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    print(f"[SUCCESS] {theme_id}: rendered {sum(res)}/{len(files)} badges + manifests.")

if __name__ == "__main__":
    get_synth_rows()
    build_theme("tokyo-neon", render_tokyo_neon_badge)
    build_theme("synthwave-84", render_synthwave_badge)
