import os, sys, shutil, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = r'C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original'
BADGES_DIR = os.path.join(REPO_ROOT, 'badges')
THEME_DIR = os.path.join(REPO_ROOT, 'themes', 'neotokyo-tag')
THEME_BADGES_DIR = os.path.join(THEME_DIR, 'badges')
THEME_SHARP_DIR = os.path.join(THEME_DIR, 'sharp')
SCRATCH_DIR = r'C:\Users\yourt\.gemini\antigravity\scratch'
OTT_DIR = os.path.join(SCRATCH_DIR, 'clean_ott_assets')
FLAG_DIR = os.path.join(SCRATCH_DIR, 'official_flags_png')
LIVE_HASH_ORIG = '0c347dc4bb347d1046caa3149acaf628cf53fd7ffadb39f2c6b48501a6ae42ca'

SCALE = 4
NATIVE_H = 96
TOTAL_H = NATIVE_H * SCALE
pad_y = 6 * SCALE
h = TOTAL_H - pad_y * 2
pad_left = 18 * SCALE
pad_right = 14 * SCALE
hazard_pink = (255, 45, 85, 255)

font_micro = ImageFont.truetype('bahnschrift.ttf', 8 * SCALE)
font_bold = ImageFont.truetype('arialbd.ttf', int(48 * SCALE))
font_lang = ImageFont.truetype('arialbd.ttf', int(40 * SCALE))

CLEAN_TEXTS = {
    '4k': ('4K', (255, 255, 255, 255)),
    '8k': ('8K', (255, 255, 255, 255)),
    '1080p': ('1080P', (255, 255, 255, 255)),
    '720p': ('720P', (255, 255, 255, 255)),
    '480p': ('480P', (255, 255, 255, 255)),
    '1440p': ('1440P', (255, 255, 255, 255)),
    '576p': ('576P', (255, 255, 255, 255)),
    '3d': ('3D', (255, 255, 255, 255)),
    'hevc': ('HEVC', (255, 255, 255, 255)),
    'av1': ('AV1', (255, 255, 255, 255)),
    'x264': ('x264', (255, 255, 255, 255)),
    'x265': ('x265', (255, 255, 255, 255)),
    'h264': ('H.264', (255, 255, 255, 255)),
    'h265': ('H.265', (255, 255, 255, 255)),
    'vp9': ('VP9', (255, 255, 255, 255)),
    'vc1': ('VC-1', (255, 255, 255, 255)),
    'vvc': ('VVC', (255, 255, 255, 255)),
    '10-bit': ('10-BIT', (255, 255, 255, 255)),
    '10bit': ('10-BIT', (255, 255, 255, 255)),
    '8-bit': ('8-BIT', (255, 255, 255, 255)),
    '8bit': ('8-BIT', (255, 255, 255, 255)),
    '12-bit': ('12-BIT', (255, 255, 255, 255)),
    '12bit': ('12-BIT', (255, 255, 255, 255)),
    '5.1': ('5.1', (255, 255, 255, 255)),
    '5_1': ('5.1', (255, 255, 255, 255)),
    '7.1': ('7.1', (255, 255, 255, 255)),
    '7_1': ('7.1', (255, 255, 255, 255)),
    '2.0': ('2.0', (255, 255, 255, 255)),
    '2_0': ('2.0', (255, 255, 255, 255)),
    '1.0': ('1.0', (255, 255, 255, 255)),
    '1_0': ('1.0', (255, 255, 255, 255)),
    '6.1': ('6.1', (255, 255, 255, 255)),
    '6_1': ('6.1', (255, 255, 255, 255)),
    'atmos': ('ATMOS', (255, 255, 255, 255)),
    'dolby-atmos': ('ATMOS', (255, 255, 255, 255)),
    'truehd': ('TRUEHD', (255, 255, 255, 255)),
    'dts': ('DTS', (255, 255, 255, 255)),
    'dts-hd': ('DTS-HD', (255, 255, 255, 255)),
    'dtsx': ('DTS:X', (255, 255, 255, 255)),
    'dts-x': ('DTS:X', (255, 255, 255, 255)),
    'flac': ('FLAC', (255, 255, 255, 255)),
    'aac': ('AAC', (255, 255, 255, 255)),
    'ac3': ('AC3', (255, 255, 255, 255)),
    'eac3': ('EAC3', (255, 255, 255, 255)),
    'mp3': ('MP3', (255, 255, 255, 255)),
    'opus': ('OPUS', (255, 255, 255, 255)),
    'web-dl': ('WEB-DL', (255, 255, 255, 255)),
    'webdl': ('WEB-DL', (255, 255, 255, 255)),
    'webrip': ('WEBRIP', (255, 255, 255, 255)),
    'bluray': ('BLURAY', (255, 255, 255, 255)),
    'remux': ('REMUX', (255, 255, 255, 255)),
    'hdtv': ('HDTV', (255, 255, 255, 255)),
    'dvd': ('DVD', (255, 255, 255, 255)),
    'cached': ('CACHED', (255, 204, 0, 255)),
    'uncached': ('UNCACHED', (160, 160, 170, 255)),
    'mkv': ('MKV', (255, 255, 255, 255)),
    'mp4': ('MP4', (255, 255, 255, 255)),
    'avi': ('AVI', (255, 255, 255, 255)),
    'ts': ('TS', (255, 255, 255, 255)),
    'm2ts': ('M2TS', (255, 255, 255, 255)),
    'hdr': ('HDR', (255, 255, 255, 255)),
    'hdr10': ('HDR10', (255, 255, 255, 255)),
    'hdr10plus': ('HDR10+', (255, 255, 255, 255)),
    'dv': ('VISION', (210, 180, 140, 255)),
    'dolby-vision': ('VISION', (210, 180, 140, 255)),
    'dv-only': ('DV ONLY', (210, 180, 140, 255)),
    'imax': ('IMAX', (0, 170, 230, 255)),
    '60fps': ('60 FPS', (255, 255, 255, 255)),
    '120fps': ('120 FPS', (255, 255, 255, 255)),
    '50fps': ('50 FPS', (255, 255, 255, 255)),
    '24fps': ('24 FPS', (255, 255, 255, 255)),
    'extended': ('EXTENDED', (255, 255, 255, 255)),
    'unrated': ('UNRATED', (255, 255, 255, 255)),
    'remastered': ('REMASTERED', (255, 255, 255, 255)),
    'directors-cut': ('DIRECTOR CUT', (255, 255, 255, 255)),
}

LANG_FLAGS = {
    'bangladesh-flag': ('bd', 'BENGALI'),
    'bangladesh': ('bd', 'BENGALI'),
    'bengali': ('bd', 'BENGALI'),
    'english-flag': ('gb', 'ENGLISH'),
    'english': ('gb', 'ENGLISH'),
    'uk': ('gb', 'ENGLISH'),
    'us': ('us', 'ENGLISH'),
    'usa': ('us', 'ENGLISH'),
    'usa-flag': ('us', 'ENGLISH'),
    'hindi-flag': ('in', 'HINDI'),
    'hindi': ('in', 'HINDI'),
    'india': ('in', 'HINDI'),
    'india-flag': ('in', 'HINDI'),
    'japanese-flag': ('jp', 'JAPANESE'),
    'japanese': ('jp', 'JAPANESE'),
    'japan': ('jp', 'JAPANESE'),
    'japan-flag': ('jp', 'JAPANESE'),
    'korean-flag': ('kr', 'KOREAN'),
    'korean': ('kr', 'KOREAN'),
    'chinese-flag': ('cn', 'CHINESE'),
    'chinese': ('cn', 'CHINESE'),
    'spanish-flag': ('es', 'SPANISH'),
    'spanish': ('es', 'SPANISH'),
    'spain': ('es', 'SPANISH'),
    'french-flag': ('fr', 'FRENCH'),
    'french': ('fr', 'FRENCH'),
    'france': ('fr', 'FRENCH'),
    'german-flag': ('de', 'GERMAN'),
    'german': ('de', 'GERMAN'),
    'germany': ('de', 'GERMAN'),
    'italian-flag': ('it', 'ITALIAN'),
    'italian': ('it', 'ITALIAN'),
    'italy': ('it', 'ITALIAN'),
    'russian-flag': ('ru', 'RUSSIAN'),
    'russian': ('ru', 'RUSSIAN'),
    'russia': ('ru', 'RUSSIAN'),
    'arabic-flag': ('sa', 'ARABIC'),
    'arabic': ('sa', 'ARABIC'),
    'saudi-arabia-flag': ('sa', 'ARABIC'),
    'turkish-flag': ('tr', 'TURKISH'),
    'turkish': ('tr', 'TURKISH'),
    'nepali-flag': ('np', 'NEPALI'),
    'nepali': ('np', 'NEPALI'),
}

def make_text_glyph(text, color=(255, 255, 255, 255)):
    dummy = Image.new('RGBA', (1, 1))
    d = ImageDraw.Draw(dummy)
    bb = d.textbbox((0, 0), text, font=font_bold)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    im = Image.new('RGBA', (tw + 10, th + 10), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((5 - bb[0], 5 - bb[1]), text, font=font_bold, fill=color)
    return im

def make_flag_glyph(cc, text):
    flag_p = os.path.join(FLAG_DIR, f'{cc}.png')
    if not os.path.exists(flag_p):
        return None
    flag = Image.open(flag_p).convert('RGBA')
    fh = int(44 * SCALE)
    fw = int(flag.width * (fh / float(flag.height)))
    flag_sc = flag.resize((fw, fh), Image.Resampling.LANCZOS)
    
    fmask = Image.new('L', (fw, fh), 0)
    ImageDraw.Draw(fmask).rounded_rectangle([0, 0, fw-1, fh-1], radius=int(5*SCALE), fill=255)
    flag_rounded = Image.new('RGBA', (fw, fh), (0, 0, 0, 0))
    flag_rounded.paste(flag_sc, (0, 0), fmask)
    
    dummy = Image.new('RGBA', (1, 1))
    d = ImageDraw.Draw(dummy)
    bb = d.textbbox((0, 0), text, font=font_lang)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    
    gap = int(10 * SCALE)
    total_w = fw + gap + tw
    im = Image.new('RGBA', (total_w, max(fh, th)), (0, 0, 0, 0))
    im.alpha_composite(flag_rounded, (0, (im.height - fh) // 2))
    ImageDraw.Draw(im).text((fw + gap - bb[0], (im.height - th) // 2 - bb[1]), text, font=font_lang, fill=(255, 255, 255, 255))
    return im

def render_neotokyo(name, glyph_im, max_w_native=220):
    bbox = glyph_im.getbbox()
    glyph = glyph_im.crop(bbox) if bbox else glyph_im
    
    target_h_sc = int(54 * SCALE)
    max_w_sc = int((max_w_native - 32) * SCALE)
    sc = min(target_h_sc / float(glyph.height), max_w_sc / float(glyph.width))
    gw = max(1, int(round(glyph.width * sc)))
    gh = max(1, int(round(glyph.height * sc)))
    glyph_sc = glyph.resize((gw, gh), Image.Resampling.LANCZOS)
    
    total_w = max(gw + pad_left + pad_right, int(95 * SCALE))
    
    canvas = Image.new('RGBA', (total_w, TOTAL_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Obsidian curved corners (r = 22px in SCALE=4)
    card_r = int(5.5 * SCALE)
    draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=card_r, fill=(14, 16, 22, 255), outline=(42, 48, 60, 255), width=int(1.5*SCALE))
    
    # Left hazard stripe
    draw.rectangle([4*SCALE, pad_y + int(2.5*SCALE), 4*SCALE + int(3.5*SCALE), pad_y + h - int(2.5*SCALE)], fill=hazard_pink)
    
    # Top micro header
    clean_id = name.replace('-flag', '').replace('_studio', '').upper()
    micro_hdr = f'SYS // TAG // {clean_id[:10]}'
    draw.text((12 * SCALE, pad_y + 3 * SCALE), micro_hdr, font=font_micro, fill=(130, 145, 170, 230))
    
    content_cy = pad_y + int(10 * SCALE) + (h - int(10 * SCALE)) // 2
    gx = pad_left + (total_w - pad_left - pad_right - gw) // 2
    gy = content_cy - gh // 2
    
    g_alpha = glyph_sc.split()[3]
    glow_mask = g_alpha.filter(ImageFilter.GaussianBlur(2.2 * SCALE))
    glow = Image.new('RGBA', (gw, gh), (0, 0, 0, 0))
    glow.paste((hazard_pink[0], hazard_pink[1], hazard_pink[2], 100), (0, 0), glow_mask)
    canvas.alpha_composite(glow, (gx, gy))
    
    sh_mask = g_alpha.filter(ImageFilter.GaussianBlur(1.8 * SCALE))
    sh = Image.new('RGBA', (gw, gh), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 220), (0, 0), sh_mask)
    canvas.alpha_composite(sh, (gx, gy + int(2.0 * SCALE)))
    canvas.alpha_composite(glyph_sc, (gx, gy))
    
    final_w = max(1, int(round(total_w / float(SCALE))))
    return canvas.resize((final_w, NATIVE_H), Image.Resampling.LANCZOS)

def process_badge(filename):
    name = filename[:-5]
    if name == 'live':
        src_live = os.path.join(BADGES_DIR, 'live.webp')
        shutil.copyfile(src_live, os.path.join(THEME_BADGES_DIR, 'live.webp'))
        shutil.copyfile(src_live, os.path.join(THEME_SHARP_DIR, 'live.webp'))
        return name, True

    # 1. Clean technical text badge
    if name in CLEAN_TEXTS:
        txt, col = CLEAN_TEXTS[name]
        glyph = make_text_glyph(txt, col)
        badge = render_neotokyo(name, glyph)
    # 2. Clean flag badge
    elif name in LANG_FLAGS:
        cc, lang = LANG_FLAGS[name]
        glyph = make_flag_glyph(cc, lang)
        if glyph:
            badge = render_neotokyo(name, glyph, max_w_native=200)
        else:
            src_p = os.path.join(BADGES_DIR, filename)
            badge = render_neotokyo(name, Image.open(src_p), max_w_native=200)
    # 3. Clean OTT brand logo
    else:
        ott_p = os.path.join(OTT_DIR, f'{name}.png')
        if os.path.exists(ott_p):
            badge = render_neotokyo(name, Image.open(ott_p))
        else:
            src_p = os.path.join(BADGES_DIR, filename)
            if not os.path.exists(src_p):
                src_p = os.path.join(THEME_BADGES_DIR, filename)
            if os.path.exists(src_p):
                badge = render_neotokyo(name, Image.open(src_p))
            else:
                return name, False

    out1 = os.path.join(THEME_BADGES_DIR, filename)
    out2 = os.path.join(THEME_SHARP_DIR, filename)
    badge.save(out1, 'WEBP', quality=95, method=6)
    badge.save(out2, 'WEBP', quality=95, method=6)
    return name, True

def main():
    print('Deploying Authentic Neo-Tokyo Tag System across all badges...')
    os.makedirs(THEME_BADGES_DIR, exist_ok=True)
    os.makedirs(THEME_SHARP_DIR, exist_ok=True)
    
    files = [f for f in os.listdir(THEME_BADGES_DIR) if f.endswith('.webp')]
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(process_badge, files))
        
    print(f'Processed {len(results)} authentic Neo-Tokyo Tag badges!')
    
    # Check live.webp hash
    live_p = os.path.join(THEME_BADGES_DIR, 'live.webp')
    h = hashlib.sha256(open(live_p, 'rb').read()).hexdigest()
    assert h == LIVE_HASH_ORIG, f'LIVE HASH MISMATCH: {h}'
    print('[SUCCESS] live.webp 100% verified!')

if __name__ == '__main__':
    main()
