import os, sys, json, re, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
THEME_DIR = os.path.join(REPO_ROOT, "themes", "stained-glass")
THEME_BADGES_DIR = os.path.join(THEME_DIR, "badges")
SCRATCH_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")
LIVE_HASH_ORIG = "0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca"

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE

font_sans = ImageFont.truetype("segoeuib.ttf", int(42 * SCALE))
font_sub = ImageFont.truetype("arialbd.ttf", int(38 * SCALE))

JEWEL_RUBY = (139, 26, 42, 255)
JEWEL_AMBER = (145, 98, 16, 255)
JEWEL_ORANGE = (154, 62, 18, 255)
JEWEL_MAGENTA = (130, 28, 92, 255)
JEWEL_AMETHYST = (88, 42, 145, 255)
JEWEL_SAPPHIRE = (18, 88, 145, 255)
JEWEL_EMERALD = (16, 108, 72, 255)
JEWEL_SLATE = (34, 48, 74, 255)

CLEAN_TEXTS = {
    "4k": ("4K", JEWEL_AMBER), "8k": ("8K", JEWEL_AMBER),
    "1080p": ("1080P", JEWEL_SAPPHIRE), "720p": ("720P", JEWEL_SAPPHIRE),
    "480p": ("480P", JEWEL_SLATE), "1440p": ("1440P", JEWEL_SAPPHIRE),
    "576p": ("576P", JEWEL_SLATE), "lowres": ("LOWRES", JEWEL_SLATE),
    "3d": ("3D", JEWEL_AMETHYST),
    "hevc": ("HEVC", JEWEL_MAGENTA), "av1": ("AV1", JEWEL_EMERALD),
    "avc": ("H.264", JEWEL_MAGENTA), "x264": ("x264", JEWEL_MAGENTA),
    "x265": ("x265", JEWEL_MAGENTA), "h264": ("H.264", JEWEL_MAGENTA),
    "h265": ("H.265", JEWEL_MAGENTA), "vp9": ("VP9", JEWEL_MAGENTA),
    "vc1": ("VC-1", JEWEL_MAGENTA), "vvc": ("VVC", JEWEL_MAGENTA),
    "10-bit": ("10-BIT", JEWEL_AMETHYST), "10bit": ("10-BIT", JEWEL_AMETHYST),
    "8-bit": ("8-BIT", JEWEL_AMETHYST), "8bit": ("8-BIT", JEWEL_AMETHYST),
    "12-bit": ("12-BIT", JEWEL_AMETHYST), "12bit": ("12-BIT", JEWEL_AMETHYST),
    "5.1": ("5.1", JEWEL_SAPPHIRE), "5_1": ("5.1", JEWEL_SAPPHIRE),
    "7.1": ("7.1", JEWEL_SAPPHIRE), "7_1": ("7.1", JEWEL_SAPPHIRE),
    "2.0": ("2.0", JEWEL_SAPPHIRE), "2_0": ("2.0", JEWEL_SAPPHIRE),
    "1.0": ("1.0", JEWEL_SAPPHIRE), "1_0": ("1.0", JEWEL_SAPPHIRE),
    "6.1": ("6.1", JEWEL_SAPPHIRE), "6_1": ("6.1", JEWEL_SAPPHIRE),
    "atmos": ("ATMOS", JEWEL_SAPPHIRE), "dolby-atmos": ("ATMOS", JEWEL_SAPPHIRE),
    "truehd": ("TRUEHD", JEWEL_SAPPHIRE), "dts": ("DTS", JEWEL_SAPPHIRE),
    "dts-hd": ("DTS-HD", JEWEL_SAPPHIRE), "dtsx": ("DTS:X", JEWEL_ORANGE),
    "dts-x": ("DTS:X", JEWEL_ORANGE), "flac": ("FLAC", JEWEL_SAPPHIRE),
    "aac": ("AAC", JEWEL_SAPPHIRE), "ac3": ("AC3", JEWEL_SAPPHIRE),
    "eac3": ("EAC3", JEWEL_SAPPHIRE), "ddp": ("DD+", JEWEL_SAPPHIRE),
    "dd": ("DD", JEWEL_SAPPHIRE), "mp3": ("MP3", JEWEL_SAPPHIRE), "opus": ("OPUS", JEWEL_SAPPHIRE),
    "web-dl": ("WEB-DL", JEWEL_EMERALD), "webdl": ("WEB-DL", JEWEL_EMERALD),
    "webrip": ("WEBRIP", JEWEL_EMERALD), "bluray": ("BLURAY", JEWEL_SAPPHIRE),
    "blu-ray": ("BLURAY", JEWEL_SAPPHIRE), "remux": ("REMUX", JEWEL_AMBER),
    "hdtv": ("HDTV", JEWEL_EMERALD), "dvd": ("DVD", JEWEL_EMERALD),
    "cached": ("CACHED", JEWEL_AMBER), "uncached": ("UNCACHED", JEWEL_SLATE),
    "mkv": ("MKV", JEWEL_RUBY), "mp4": ("MP4", JEWEL_RUBY), "avi": ("AVI", JEWEL_RUBY),
    "ts": ("TS", JEWEL_RUBY), "m2ts": ("M2TS", JEWEL_RUBY),
    "hdr": ("HDR", JEWEL_ORANGE), "hdr10": ("HDR10", JEWEL_ORANGE),
    "hdr10plus": ("HDR10+", JEWEL_ORANGE), "hlg": ("HLG", JEWEL_ORANGE),
    "dv": ("VISION", JEWEL_ORANGE), "dolby-vision": ("VISION", JEWEL_ORANGE),
    "dv-only": ("DV ONLY", JEWEL_ORANGE), "imax": ("IMAX", JEWEL_SAPPHIRE),
    "60fps": ("60FPS", JEWEL_AMETHYST), "120fps": ("120FPS", JEWEL_AMETHYST),
    "50fps": ("50FPS", JEWEL_AMETHYST), "24fps": ("24FPS", JEWEL_AMETHYST), "hfr": ("HFR", JEWEL_AMETHYST),
    "dual": ("DUAL", JEWEL_ORANGE), "multi": ("MULTI", JEWEL_ORANGE),
    "extended": ("EXTENDED", JEWEL_ORANGE), "unrated": ("UNRATED", JEWEL_RUBY),
    "remastered": ("REMASTERED", JEWEL_AMBER), "directors-cut": ("DIR CUT", JEWEL_AMBER),
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

def make_stained_panel(w, jewel):
    m_x, m_y, rad = 4 * SCALE, 8 * SCALE, 12 * SCALE
    mask = Image.new("L", (w, TOTAL_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, fill=255)
    base = Image.new("RGBA", (w, TOTAL_H), jewel)
    bdr = ImageDraw.Draw(base)
    r1, g1, b1, _ = jewel
    shard1 = (max(0, r1 - 35), max(0, g1 - 35), max(0, b1 - 35), 255)
    shard2 = (min(255, r1 + 30), min(255, g1 + 30), min(255, b1 + 30), 255)
    bdr.polygon([(0, 0), (int(w * 0.38), 0), (int(w * 0.22), TOTAL_H), (0, TOTAL_H)], fill=shard1)
    bdr.polygon([(int(w * 0.68), 0), (w, 0), (w, TOTAL_H), (int(w * 0.82), TOTAL_H)], fill=shard2)
    bdr.line([(int(w * 0.38), 0), (int(w * 0.22), TOTAL_H)], fill=(12, 12, 14, 255), width=int(2.2 * SCALE))
    bdr.line([(int(w * 0.68), 0), (int(w * 0.82), TOTAL_H)], fill=(12, 12, 14, 255), width=int(2.2 * SCALE))
    c = Image.new("RGBA", (w, TOTAL_H), (0, 0, 0, 0))
    c.paste(base, (0, 0), mask)
    ImageDraw.Draw(c).rounded_rectangle([m_x, m_y, w - m_x - 1, TOTAL_H - m_y - 1], radius=rad, outline=(12, 12, 14, 255), width=int(2.5 * SCALE))
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

def render_stained_badge(name, filename):
    if name in CLEAN_TEXTS:
        txt, jewel = CLEAN_TEXTS[name]
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), txt, font=font_sans)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        w = max(tw + 40 * SCALE, 102 * SCALE)
        c = make_stained_panel(w, jewel)
        tx, ty = (w - tw) // 2 - bb[0], (TOTAL_H - th) // 2 - bb[1]
        ImageDraw.Draw(c).text((tx, ty), txt, font=font_sans, fill=(255, 255, 255, 255), stroke_width=int(1.8 * SCALE), stroke_fill=(0, 0, 0, 235))
        return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    if name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        fl = make_flag_img(cc)
        bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), lang, font=font_sub)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        if fl is not None:
            cw = fl.width + 8 * SCALE + tw
            w = max(cw + 40 * SCALE, 110 * SCALE)
            c = make_stained_panel(w, JEWEL_SAPPHIRE)
            cx_f = (w - cw) // 2
            c.alpha_composite(fl, (cx_f, (TOTAL_H - fl.height) // 2))
            tx, ty = cx_f + fl.width + 8 * SCALE - bb[0], (TOTAL_H - th) // 2 - bb[1]
            ImageDraw.Draw(c).text((tx, ty), lang, font=font_sub, fill=(255, 255, 255, 255), stroke_width=int(1.8 * SCALE), stroke_fill=(0, 0, 0, 235))
            return c.resize((w // SCALE, NATIVE_H), Image.Resampling.LANCZOS)

    ott_p = os.path.join(OTT_DIR, f"{name}.png")
    src_p = ott_p if os.path.exists(ott_p) else os.path.join(BADGES_DIR, filename)
    if not os.path.exists(src_p):
        return None
    im = Image.open(src_p).convert("RGBA")
    bb = im.getbbox()
    g = im.crop(bb) if bb else im
    sc = min((48 * SCALE) / float(g.height), (160 * SCALE) / float(g.width))
    gw, gh = max(1, int(round(g.width * sc))), max(1, int(round(g.height * sc)))
    gs = g.resize((gw, gh), Image.Resampling.LANCZOS)

    # Use deep slate-sapphire stained glass for brand logos so red/white/dark logos all pop cleanly
    jewel = JEWEL_SLATE
    w = max(gw + 40 * SCALE, 102 * SCALE)
    c = make_stained_panel(w, jewel)
    gx, gy = (w - gw) // 2, (TOTAL_H - gh) // 2

    arr = np.array(gs)
    vis = arr[:, :, 3] > 50
    if np.any(vis):
        lum = np.mean(0.299 * arr[vis, 0] + 0.587 * arr[vis, 1] + 0.114 * arr[vis, 2])
        if lum < 65:
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
        im = render_stained_badge(name, fn)
        if im is not None:
            im.save(out_p, "WEBP", quality=95, method=6)
            return True
        return False

    with ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(_job, files))

    h = hashlib.sha256(open(os.path.join(THEME_BADGES_DIR, "live.webp"), "rb").read()).hexdigest()
    assert h == LIVE_HASH_ORIG, "stained-glass live.webp hash mismatch!"

    with open(os.path.join(REPO_ROOT, "badges.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data.get("filters", []):
        if "imageURL" in item:
            item["imageURL"] = item["imageURL"].replace("/main/badges/", "/main/themes/stained-glass/badges/")
    for p in [os.path.join(REPO_ROOT, "stained-glass.json"), os.path.join(THEME_DIR, "stained-glass.json")]:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    print(f"[SUCCESS] stained-glass: rendered {sum(res)}/{len(files)} badges + manifests. live.webp verified.")

if __name__ == "__main__":
    main()
