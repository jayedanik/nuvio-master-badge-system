import os, sys, json, re, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "holo-prism")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

font_bahn = ImageFont.truetype("bahnschrift.ttf", int(48 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(40 * SCALE))

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

def make_holo_panel(w):
    m_x, m_y, rad = 4 * SCALE, 8 * SCALE, 14 * SCALE
    outer_m = Image.new("L", (w, TOTAL_H), 0)
    ImageDraw.Draw(outer_m).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, fill=255)
    inner_m = Image.new("L", (w, TOTAL_H), 0)
    b_t = int(2.2 * SCALE)
    ImageDraw.Draw(inner_m).rounded_rectangle([m_x + b_t, m_y + b_t, w - m_x - 1 - b_t, TOTAL_H - m_y - 1 - b_t], radius=rad - b_t, fill=255)

    yy, xx = np.mgrid[0:TOTAL_H, 0:w]
    phase = (xx / float(w) * 0.75 + yy / float(TOTAL_H) * 0.35) * 6.28318
    r = (128 + 127 * np.sin(phase)).astype(np.uint8)
    g = (128 + 127 * np.sin(phase + 2.094)).astype(np.uint8)
    b = (128 + 127 * np.sin(phase + 4.188)).astype(np.uint8)
    holo_img = Image.fromarray(np.stack([r, g, b, np.full_like(r, 255)], axis=-1), "RGBA")

    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    c.paste(holo_img, (0, 0), outer_m)

    core_arr = np.zeros((TOTAL_H, w, 4), dtype=np.uint8)
    core_arr[:, :, 0] = (14 + (r * 0.08)).astype(np.uint8)
    core_arr[:, :, 1] = (16 + (g * 0.08)).astype(np.uint8)
    core_arr[:, :, 2] = (24 + (b * 0.09)).astype(np.uint8)
    core_arr[:, :, 3] = 248
    c.paste(Image.fromarray(core_arr, "RGBA"), (0, 0), inner_m)
    return c

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

def render_holo_badge(name, filename):
    if name in CLEAN_TEXTS:
        txt = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_bahn)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 40 * SCALE, 102 * SCALE)
        c = make_holo_panel(w)
        dr = ImageDraw.Draw(c)
        tx, ty = (w - tw) // 2 - bb[0], (TOTAL_H - th) // 2 - bb[1]
        dr.text((tx, ty + 2 * SCALE), txt, font=font_bahn, fill=(0, 0, 0, 220))
        dr.text((tx, ty), txt, font=font_bahn, fill=(255, 255, 255, 255))
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 10 * SCALE + tw
            w = max(cw + 40 * SCALE, 110 * SCALE)
            c = make_holo_panel(w)
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, (TOTAL_H - fl.height) // 2))
            tx, ty = cx_f + fl.width + 10 * SCALE - bb[0], (TOTAL_H - th) // 2 - bb[1]
            ImageDraw.Draw(c).text((tx, ty), lang, font=font_sub, fill=(255, 255, 255, 255))
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    im = Image.open(src_p).convert("RGBA")
    bb = im.getbbox()
    g = im.crop(bb) if bb else im
    sc = min((50 * SCALE) / float(g.height), (165 * SCALE) / float(g.width))
    gw, gh = max(1, int(round(g.width * sc))), max(1, int(round(g.height * sc)))
    gs = g.resize((gw, gh), Image.Resampling.LANCZOS)

    w = max(gw + 40 * SCALE, 102 * SCALE)
    c = make_holo_panel(w)
    gx, gy = (w - gw) // 2, (TOTAL_H - gh) // 2

    arr = np.array(gs)
    vis = arr[:, :, 3] > 50
    if np.any(vis):
        lum = np.mean(0.299 * arr[vis, 0] + 0.587 * arr[vis, 1] + 0.114 * arr[vis, 2])
        if lum < 60:
            ga = gs.split()[3]
            halo = ga.filter(ImageFilter.MaxFilter(5))
            c.paste(Image.new("RGBA", (gw, gh), (255, 255, 255, 230)), (gx, gy), halo)

    c.alpha_composite(gs, (gx, gy))
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
        im = render_holo_badge(name, fn)
        if im is not None:
            im.save(out_p, "WEBP", quality=95, method=6)
            return True
        return False

    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(_job, files))

    h = hashlib.sha256(open(os.path.join(THEME_BADGES_DIR, "live.webp"), "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, "holo-prism live.webp hash mismatch!"

    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("filters", []):
        if "imageURL" in item:
            item["imageURL"] = item["imageURL"].replace("/main/badges/", "/main/themes/holo-prism/badges/")
    for p in [os.path.join(REPO_ROOT, "holo-prism.json"), os.path.join(THEME_DIR, "holo-prism.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    print(f"[SUCCESS] holo-prism: rendered {sum(res)}/{len(files)} badges + manifests. live.webp verified.")

if __name__ == "__main__":
    main()
