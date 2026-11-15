
OTT_BOOSTS = {
    "disney": 1.55,
    "disneyplus": 1.55,
    "appletv": 1.35,
    "apple": 1.35,
    "max": 1.30,
    "hbomax": 1.30,
    "sonyliv": 1.40,
    "zee5": 1.35,
    "sunnxt": 1.40,
    "aha": 1.30,
    "toffee": 1.10,
    "hoichoi": 1.30,
    "alldebrid": 1.45,
    "torbox": 1.30,
    "mubi": 1.20,
    "criterion": 1.18,
    "jiocinema": 1.20,
    "binge": 1.15,
    "bioscope": 1.15,
}

def get_ott_min_w(badge_id, scale):
    if badge_id in ("disney", "disneyplus"):
        return int(245 * scale)
    elif badge_id == "alldebrid":
        return int(275 * scale)
    elif badge_id == "torbox":
        return int(250 * scale)
    elif badge_id in ("realdebrid", "real-debrid"):
        return int(330 * scale)
    elif badge_id in ("1337x", "yts"):
        return int(200 * scale)
    elif badge_id == "hoichoi":
        return int(230 * scale)
    elif badge_id in ("appletv", "apple"):
        return int(215 * scale)
    elif badge_id in ("max", "hbomax"):
        return int(210 * scale)
    elif badge_id in ("sonyliv", "zee5", "sunnxt"):
        return int(205 * scale)
    elif badge_id in ("aha", "mubi", "criterion", "addatimes"):
        return int(210 * scale)
    elif badge_id == "live":
        return int(260 * scale)
    return int(235 * scale)
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DIR = "C:/Users/yourt/.gemini/antigravity/scratch"
OTT_DIR = os.path.join(SCRATCH_DIR, "clean_ott_assets")
FLAG_DIR = os.path.join(SCRATCH_DIR, "official_flags_png")

SCALE = 4
CANVAS_H = 96
TOTAL_H = CANVAS_H * SCALE

# Typography
font_main = ImageFont.truetype("arialbd.ttf", 34 * SCALE)
font_vfd = ImageFont.truetype("consolab.ttf", 34 * SCALE)
font_vfd_sub = ImageFont.truetype("consolab.ttf", 22 * SCALE)
font_cinema = ImageFont.truetype("impact.ttf", 38 * SCALE)
font_cinema_sub = ImageFont.truetype("arialbd.ttf", 22 * SCALE)
font_bahn_main = ImageFont.truetype("bahnschrift.ttf", 34 * SCALE)
font_bahn_sub = ImageFont.truetype("bahnschrift.ttf", 22 * SCALE)
font_bahn_micro = ImageFont.truetype("bahnschrift.ttf", 9 * SCALE)
font_leather_main = ImageFont.truetype("timesbd.ttf", 36 * SCALE)
font_leather_sub = ImageFont.truetype("timesbd.ttf", 22 * SCALE)

cinzel_path = os.path.join(REPO_ROOT, ".fonts", "Cinzel-Bold.ttf")
if not os.path.exists(cinzel_path):
    cinzel_path = os.path.join(SCRIPT_DIR, "Cinzel-Bold.ttf")
try:
    font_enamel_main = ImageFont.truetype(cinzel_path, 34 * SCALE)
    font_enamel_sub = ImageFont.truetype(cinzel_path, 22 * SCALE)
except Exception:
    font_enamel_main = font_leather_main
    font_enamel_sub = font_leather_sub

cinzel_dec_path = os.path.join(REPO_ROOT, ".fonts", "CinzelDecorative-Bold.ttf")
if not os.path.exists(cinzel_dec_path):
    cinzel_dec_path = os.path.join(SCRIPT_DIR, "CinzelDecorative-Bold.ttf")
try:
    font_criterion_main = ImageFont.truetype(cinzel_dec_path, 34 * SCALE)
except Exception:
    font_criterion_main = font_leather_main

def get_font_for_text(text, size, default_font="arialbd.ttf"):
    if not text:
        try:
            return ImageFont.truetype(default_font, int(size))
        except Exception:
            return ImageFont.truetype("arialbd.ttf", int(size))
    for ch in text:
        cp = ord(ch)
        # Japanese (Hiragana, Katakana) - fallback order: Yu Gothic Bold, MS Gothic, MS YaHei
        if 0x3040 <= cp <= 0x30FF:
            for fn in ["YuGothB.ttc", "msgothic.ttc", "msyh.ttc"]:
                try:
                    return ImageFont.truetype(fn, int(size))
                except Exception:
                    continue
        # Chinese (CJK Unified Ideographs)
        elif 0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF:
            for fn in ["msyh.ttc", "simsun.ttc"]:
                try:
                    return ImageFont.truetype(fn, int(size))
                except Exception:
                    continue
        # Korean (Hangul)
        elif 0xAC00 <= cp <= 0xD7AF or 0x1100 <= cp <= 0x11FF:
            for fn in ["malgun.ttf", "malgunbd.ttf"]:
                try:
                    return ImageFont.truetype(fn, int(size))
                except Exception:
                    continue
        # Indic, Sinhala & Odia (Bengali, Hindi, Marathi, Nepali, Tamil, Telugu, Kannada, Malayalam, Gujarati, Punjabi, Odia, Sinhala)
        elif (0x0900 <= cp <= 0x0DFF or 0x0A00 <= cp <= 0x0A7F or 0x0A80 <= cp <= 0x0AFF):
            try:
                return ImageFont.truetype("Nirmala.ttc", int(size))
            except Exception:
                pass
        # Thai, Lao, Khmer
        elif (0x0E00 <= cp <= 0x0E7F or 0x0E80 <= cp <= 0x0EFF or 0x1780 <= cp <= 0x17FF):
            for fn in ["LeelaUIb.ttf", "LeelawUI.ttf", "tahoma.ttf"]:
                try:
                    return ImageFont.truetype(fn, int(size))
                except Exception:
                    continue
        # Myanmar / Burmese
        elif 0x1000 <= cp <= 0x109F:
            try:
                return ImageFont.truetype("mmrtext.ttf", int(size))
            except Exception:
                pass
        # Georgian
        elif 0x10A0 <= cp <= 0x10FF or 0x2D00 <= cp <= 0x2D2F:
            try:
                return ImageFont.truetype("sylfaen.ttf", int(size))
            except Exception:
                pass
        # Armenian
        elif 0x0530 <= cp <= 0x058F:
            try:
                return ImageFont.truetype("sylfaen.ttf", int(size))
            except Exception:
                pass
        # Ethiopic / Amharic
        elif 0x1200 <= cp <= 0x137F:
            for fn in ["ebrima.ttf", "seguiemj.ttf"]:
                try:
                    return ImageFont.truetype(fn, int(size))
                except Exception:
                    continue
        # Arabic, Persian, Urdu, Pashto
        elif 0x0600 <= cp <= 0x06FF or 0x0750 <= cp <= 0x077F:
            try:
                return ImageFont.truetype("tahoma.ttf", int(size))
            except Exception:
                pass
        # Hebrew
        elif 0x0590 <= cp <= 0x05FF:
            try:
                return ImageFont.truetype("arialbd.ttf", int(size))
            except Exception:
                pass
    try:
        return ImageFont.truetype(default_font, int(size))
    except Exception:
        return ImageFont.truetype("arialbd.ttf", int(size))

OTT_SPECS = [
    ("netflix", "netflix.png"),
    ("jiohotstar", "jiohotstar.png"),
    ("prime", "prime.png"),
    ("primevideo", "prime.png"),
    ("disney", "disney.png"),
    ("disneyplus", "disney.png"),
    ("appletv", "appletv.png"),
    ("max", "max.png"),
    ("hbomax", "max.png"),
    ("hoichoi", "hoichoi.png"),
    ("chorki", "chorki.png"),
    ("toffee", "toffee.png"),
    ("binge", "binge.png"),
    ("bioscope", "bioscope.png"),
    ("bongo", "bongo.png"),
    ("zee5", "zee5.png"),
    ("sonyliv", "sonyliv.png"),
    ("paramount", "paramount.png"),
    ("hulu", "hulu.png"),
    ("peacock", "peacock.png"),
    ("crunchyroll", "crunchyroll.png"),
    ("aha", "aha.png"),
    ("sunnxt", "sunnxt.png"),
    ("addatimes", "addatimes.png"),
    ("jiocinema", "jiocinema.png"),
    ("mubi", "mubi.png"),
    ("criterion", "criterion.png"),
    ("a24", "a24.png"),
    ("alldebrid", "alldebrid.png"),
    ("torbox", "torbox.png"),
    ("realdebrid", "realdebrid.png"),
    ("real-debrid", "realdebrid.png"),
    ("1337x", "1337x.png"),
    ("yts", "yts.png"),
]

LANG_SPECS = [
    ("bangladesh", "bd", "BANGLADESH", "বাংলা"),
    ("bangladesh-flag", "bd", "BANGLADESH", "বাংলা"),
    ("bengali", "bd", "BENGALI", "বাংলা"),
    ("bengali-flag2", "bd", "BENGALI", "বাংলা"),
    ("hindi", "in", "HINDI", "हिन्दी"),
    ("hindi-flag", "in", "HINDI", "हिन्दी"),
    ("english", "gb", "ENGLISH", "English"),
    ("english-flag", "gb", "ENGLISH", "English"),
    ("uk", "gb", "ENGLISH", "UK"),
    ("us", "us", "ENGLISH", "USA"),
    ("japanese", "jp", "JAPANESE", "日本語"),
    ("japanese-flag", "jp", "JAPANESE", "日本語"),
    ("korean", "kr", "KOREAN", "한국어"),
    ("korean-flag", "kr", "KOREAN", "한국어"),
    ("chinese", "cn", "CHINESE", "中文"),
    ("chinese-flag", "cn", "CHINESE", "中文"),
    ("cantonese", "hk", "CANTONESE", "粵語"),
    ("spanish", "es", "SPANISH", "Español"),
    ("spanish-flag", "es", "SPANISH", "Español"),
    ("french", "fr", "FRENCH", "Français"),
    ("french-flag", "fr", "FRENCH", "Français"),
    ("german", "de", "GERMAN", "Deutsch"),
    ("german-flag", "de", "GERMAN", "Deutsch"),
    ("italian", "it", "ITALIAN", "Italiano"),
    ("russian", "ru", "RUSSIAN", "Русский"),
    ("portuguese", "pt", "PORTUGUESE", "Português"),
    ("arabic", "sa", "ARABIC", "العربية"),
    ("turkish", "tr", "TURKISH", "Türkçe"),
    ("thai", "th", "THAI", "ไทย"),
    ("thai-flag", "th", "THAI", "ไทย"),
    ("vietnamese", "vn", "VIETNAMESE", "Tiếng Việt"),
    ("vietnamese-flag", "vn", "VIETNAMESE", "Tiếng Việt"),
    ("indonesian", "id", "INDONESIAN", "Bahasa"),
    ("indonesian-flag", "id", "INDONESIAN", "Bahasa"),
    ("filipino", "ph", "FILIPINO", "Tagalog"),
    ("filipino-flag", "ph", "FILIPINO", "Tagalog"),
    ("tamil", "in", "TAMIL", "தமிழ்"),
    ("tamil-flag", "in", "TAMIL", "தமிழ்"),
    ("telugu", "in", "TELUGU", "తెలుగు"),
    ("telugu-flag", "in", "TELUGU", "తెలుగు"),
    ("malayalam", "in", "MALAYALAM", "മലയാളം"),
    ("malayalam-flag", "in", "MALAYALAM", "മലയാളം"),
    ("kannada", "in", "KANNADA", "ಕನ್ನಡ"),
    ("kannada-flag", "in", "KANNADA", "ಕನ್ನಡ"),
    ("marathi", "in", "MARATHI", "मराठी"),
    ("marathi-flag", "in", "MARATHI", "मराठी"),
    ("gujarati", "in", "GUJARATI", "ગુજરાતી"),
    ("gujarati-flag", "in", "GUJARATI", "ગુજરાતી"),
    ("punjabi", "in", "PUNJABI", "ਪੰਜਾਬੀ"),
    ("punjabi-flag", "in", "PUNJABI", "ਪੰਜਾਬੀ"),
    ("urdu", "pk", "URDU", "اردو"),
    ("urdu-flag", "pk", "URDU", "اردو"),
]

def make_dark_logo(im, badge_id=None):
    if badge_id in ('alldebrid', 'rutracker'):
        return im
    arr = np.array(im.convert('RGBA')).copy()
    alphas = arr[:, :, 3] > 40
    
    if badge_id in ('disney', 'disneyplus'):
        arr[alphas, 0] = 4
        arr[alphas, 1] = 21
        arr[alphas, 2] = 48
        return Image.fromarray(arr)
        
    if badge_id == 'hulu':
        arr[alphas, 0] = 15
        arr[alphas, 1] = 65
        arr[alphas, 2] = 30
        return Image.fromarray(arr)
        
    if badge_id in ('realdebrid', 'real-debrid'):
        arr[alphas, 0] = 22
        arr[alphas, 1] = 48
        arr[alphas, 2] = 32
        return Image.fromarray(arr)

    if badge_id == 'torbox':
        r = arr[:, :, 0].astype(float)
        g = arr[:, :, 1].astype(float)
        b = arr[:, :, 2].astype(float)
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        alpha_cols = alphas.sum(axis=0)
        gap_x = 0
        for x in range(30, min(90, arr.shape[1])):
            if alpha_cols[x] == 0:
                gap_x = x
                break
        if gap_x == 0:
            gap_x = int(arr.shape[1] * 0.28)
        icon_alphas = alphas.copy()
        icon_alphas[:, gap_x:] = False
        thunder_mask = icon_alphas & (lum > 180)
        arr[thunder_mask, 0] = 255
        arr[thunder_mask, 1] = 255
        arr[thunder_mask, 2] = 255
        text_alphas = alphas.copy()
        text_alphas[:, :gap_x] = False
        text_mask = text_alphas & (lum > 100)
        arr[text_mask, 0] = 20
        arr[text_mask, 1] = 22
        arr[text_mask, 2] = 28
        return Image.fromarray(arr)

    r = arr[:, :, 0].astype(float)
    g = arr[:, :, 1].astype(float)
    b = arr[:, :, 2].astype(float)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    
    light_mask = alphas & (lum > 110)
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    diff = max_c - min_c
    white_mask = alphas & (diff < 40) & (min_c > 120)
    
    arr[white_mask, 0] = 18
    arr[white_mask, 1] = 20
    arr[white_mask, 2] = 26
    
    colored_light = light_mask & (~white_mask)
    if colored_light.sum() > 0:
        factor = 85.0 / np.maximum(lum[colored_light], 1.0)
        arr[colored_light, 0] = np.clip(r[colored_light] * factor, 0, 255).astype(np.uint8)
        arr[colored_light, 1] = np.clip(g[colored_light] * factor, 0, 255).astype(np.uint8)
        arr[colored_light, 2] = np.clip(b[colored_light] * factor, 0, 255).astype(np.uint8)
        
    return Image.fromarray(arr)

# ------------------------------------------------------------------------------
# 1. RETRO VHS MAGNETIC TAPE (Theme 6)
# ------------------------------------------------------------------------------
def render_vhs_tape(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    barcode_w = 20 * SCALE
    pad_l = barcode_w + 18 * SCALE
    pad_r = 18 * SCALE
    gap = 10 * SCALE

    pad_y = 6 * SCALE
    h = TOTAL_H - pad_y * 2
    sy = pad_y + h - int(10 * SCALE)
    stripe_h = 3.5 * SCALE
    content_cy = (pad_y + 4 * SCALE + sy) // 2

    if is_ott:
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(46 * SCALE * boost), int(52 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        logo_dark = make_dark_logo(element_img, badge_id) if element_img else None
        el_scaled = logo_dark.resize((target_w, target_h), Image.Resampling.LANCZOS) if logo_dark else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_l + target_w + pad_r)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Aged Matte Paper
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(6*SCALE), fill=(242, 238, 230, 255), outline=(195, 185, 170, 255), width=int(1.5*SCALE))

        # 80s Rainbow Stripe
        draw.rectangle([6*SCALE, sy, total_w - 6*SCALE, sy + stripe_h], fill=(225, 45, 35, 255))
        draw.rectangle([6*SCALE, sy + stripe_h, total_w - 6*SCALE, sy + stripe_h*2], fill=(245, 135, 25, 255))
        draw.rectangle([6*SCALE, sy + stripe_h*2, total_w - 6*SCALE, sy + stripe_h*3], fill=(245, 205, 35, 255))

        # Barcode on left
        bc_x = 9 * SCALE
        bc_y1 = pad_y + 8 * SCALE
        bc_y2 = sy - 4 * SCALE
        bar_patterns = [2, 1, 3, 1, 2, 4, 1, 3, 2, 1, 4]
        cur_bx = bc_x
        for bw in bar_patterns:
            draw.line([(cur_bx, bc_y1), (cur_bx, bc_y2)], fill=(25, 25, 30, 255), width=int(bw * 0.8 * SCALE))
            cur_bx += int((bw + 1.2) * 0.8 * SCALE)
            if cur_bx > pad_l - 6*SCALE:
                break

        logo_x = pad_l + (total_w - pad_l - pad_r - target_w) // 2
        if el_scaled:
            canvas.paste(el_scaled, (logo_x, content_cy - target_h // 2), el_scaled)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_cinema
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="impact.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(1.8 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = pad_l + content_w + pad_r

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(6*SCALE), fill=(242, 238, 230, 255), outline=(195, 185, 170, 255), width=int(1.5*SCALE))

        draw.rectangle([6*SCALE, sy, total_w - 6*SCALE, sy + stripe_h], fill=(225, 45, 35, 255))
        draw.rectangle([6*SCALE, sy + stripe_h, total_w - 6*SCALE, sy + stripe_h*2], fill=(245, 135, 25, 255))
        draw.rectangle([6*SCALE, sy + stripe_h*2, total_w - 6*SCALE, sy + stripe_h*3], fill=(245, 205, 35, 255))

        bc_x = 9 * SCALE
        bc_y1 = pad_y + 8 * SCALE
        bc_y2 = sy - 4 * SCALE
        bar_patterns = [2, 1, 3, 1, 2, 4, 1, 3, 2, 1, 4]
        cur_bx = bc_x
        for bw in bar_patterns:
            draw.line([(cur_bx, bc_y1), (cur_bx, bc_y2)], fill=(25, 25, 30, 255), width=int(bw * 0.8 * SCALE))
            cur_bx += int((bw + 1.2) * 0.8 * SCALE)
            if cur_bx > pad_l - 6*SCALE:
                break

        cur_x = pad_l
        if el_scaled:
            canvas.paste(el_scaled, (cur_x, content_cy - target_h // 2), el_scaled)
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, content_cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=(20, 22, 28, 255))
            cur_x += w_m + gap

        draw.line([(cur_x, content_cy - 12*SCALE), (cur_x, content_cy + 12*SCALE)], fill=(180, 170, 155, 255), width=div_w)
        cur_x += div_w + gap

        if sub_text:
            draw.text((cur_x, content_cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=(225, 45, 35, 255))

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

# ------------------------------------------------------------------------------
# 2. VINTAGE CINEMA TICKET (Theme 4)
# ------------------------------------------------------------------------------
def render_cinema_ticket(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    pad_y = 6 * SCALE
    h = TOTAL_H - pad_y * 2
    pad_h = 24 * SCALE
    gap = 10 * SCALE
    chamfer = 10 * SCALE

    gold_1 = (215, 175, 60, 255)
    gold_2 = (255, 230, 140, 255)

    if is_ott:
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(48 * SCALE * boost), int(54 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_h * 2 + target_w)

        poly_pts = [
            (4*SCALE + chamfer, pad_y),
            (total_w - 4*SCALE - chamfer, pad_y),
            (total_w - 4*SCALE, pad_y + chamfer),
            (total_w - 4*SCALE, pad_y + h - chamfer),
            (total_w - 4*SCALE - chamfer, pad_y + h),
            (4*SCALE + chamfer, pad_y + h),
            (4*SCALE, pad_y + h - chamfer),
            (4*SCALE, pad_y + chamfer)
        ]

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Shadow & Velvet black body
        draw.polygon([(x, y + 4*SCALE) for x, y in poly_pts], fill=(0, 0, 0, 150))
        draw.polygon(poly_pts, fill=(12, 13, 16, 255))

        # Punch notches on sides
        notch_r = 7 * SCALE
        notch_cy = pad_y + h // 2
        draw.ellipse([4*SCALE - notch_r, notch_cy - notch_r, 4*SCALE + notch_r, notch_cy + notch_r], fill=(0, 0, 0, 0))
        draw.ellipse([total_w - 4*SCALE - notch_r, notch_cy - notch_r, total_w - 4*SCALE + notch_r, notch_cy + notch_r], fill=(0, 0, 0, 0))

        # 24K Double Gold Pinstripes
        draw.polygon(poly_pts, outline=gold_1, width=int(2*SCALE))

        inset = 4.5 * SCALE
        poly_inner = [
            (4*SCALE + chamfer + inset*0.5, pad_y + inset),
            (total_w - 4*SCALE - chamfer - inset*0.5, pad_y + inset),
            (total_w - 4*SCALE - inset, pad_y + chamfer + inset*0.5),
            (total_w - 4*SCALE - inset, pad_y + h - chamfer - inset*0.5),
            (total_w - 4*SCALE - chamfer - inset*0.5, pad_y + h - inset),
            (4*SCALE + chamfer + inset*0.5, pad_y + h - inset),
            (4*SCALE + inset, pad_y + h - chamfer - inset*0.5),
            (4*SCALE + inset, pad_y + chamfer + inset*0.5)
        ]
        draw.polygon(poly_inner, outline=gold_2, width=int(1.2*SCALE))

        logo_x = (total_w - target_w) // 2
        cy = pad_y + h // 2
        if el_scaled:
            canvas.paste(el_scaled, (logo_x, cy - target_h // 2), el_scaled)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_cinema
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="timesbd.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(1.8 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = max(int(260 * SCALE) if badge_id == "live" else int(235 * SCALE), pad_h * 2 + content_w)

        poly_pts = [
            (4*SCALE + chamfer, pad_y),
            (total_w - 4*SCALE - chamfer, pad_y),
            (total_w - 4*SCALE, pad_y + chamfer),
            (total_w - 4*SCALE, pad_y + h - chamfer),
            (total_w - 4*SCALE - chamfer, pad_y + h),
            (4*SCALE + chamfer, pad_y + h),
            (4*SCALE, pad_y + h - chamfer),
            (4*SCALE, pad_y + chamfer)
        ]

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.polygon([(x, y + 4*SCALE) for x, y in poly_pts], fill=(0, 0, 0, 150))
        draw.polygon(poly_pts, fill=(12, 13, 16, 255))

        notch_r = 7 * SCALE
        notch_cy = pad_y + h // 2
        draw.ellipse([4*SCALE - notch_r, notch_cy - notch_r, 4*SCALE + notch_r, notch_cy + notch_r], fill=(0, 0, 0, 0))
        draw.ellipse([total_w - 4*SCALE - notch_r, notch_cy - notch_r, total_w - 4*SCALE + notch_r, notch_cy + notch_r], fill=(0, 0, 0, 0))

        draw.polygon(poly_pts, outline=gold_1, width=int(2*SCALE))

        inset = 4.5 * SCALE
        poly_inner = [
            (4*SCALE + chamfer + inset*0.5, pad_y + inset),
            (total_w - 4*SCALE - chamfer - inset*0.5, pad_y + inset),
            (total_w - 4*SCALE - inset, pad_y + chamfer + inset*0.5),
            (total_w - 4*SCALE - inset, pad_y + h - chamfer - inset*0.5),
            (total_w - 4*SCALE - chamfer - inset*0.5, pad_y + h - inset),
            (4*SCALE + chamfer + inset*0.5, pad_y + h - inset),
            (4*SCALE + inset, pad_y + h - chamfer - inset*0.5),
            (4*SCALE + inset, pad_y + chamfer + inset*0.5)
        ]
        draw.polygon(poly_inner, outline=gold_2, width=int(1.2*SCALE))

        cy = pad_y + h // 2
        cur_x = (total_w - content_w) // 2

        if el_scaled:
            canvas.paste(el_scaled, (cur_x, cy - target_h // 2), el_scaled)
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=(255, 255, 255, 255))
            cur_x += w_m + gap

        draw.line([(cur_x, cy - 12*SCALE), (cur_x, cy + 12*SCALE)], fill=(160, 135, 60, 255), width=div_w)
        cur_x += div_w + gap

        if sub_text:
            draw.text((cur_x, cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=gold_2)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

# ------------------------------------------------------------------------------
# 3. GMK CUSTOM KEYCAPS (Theme 2)
# ------------------------------------------------------------------------------
def render_gmk_keycaps(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    pad_h = 24 * SCALE
    gap = 10 * SCALE

    th = {
        "skirt": (14, 16, 22, 255), "front": (26, 30, 40, 255),
        "top": (51, 60, 78, 255), "dish": (42, 46, 63, 255),
        "legend": (255, 255, 255, 255), "sub": (185, 200, 225, 255),
        "border": (80, 95, 125, 255)
    }

    top_y1 = 3 * SCALE
    top_y2 = TOTAL_H - 16 * SCALE
    dish_y1 = top_y1 + 3 * SCALE
    dish_y2 = top_y2 - 3 * SCALE
    dish_cy = (dish_y1 + dish_y2) // 2

    if is_ott:
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(46 * SCALE * boost), int(52 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_h * 2 + target_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Floor drop shadow
        draw.rounded_rectangle([4*SCALE, 12*SCALE, total_w - 4*SCALE, TOTAL_H - 1*SCALE], radius=int(14*SCALE), fill=(0, 0, 0, 140))
        # Skirt & Front Wall
        draw.rounded_rectangle([3*SCALE, 6*SCALE, total_w - 3*SCALE, TOTAL_H - 4*SCALE], radius=int(13*SCALE), fill=th["skirt"])
        draw.rounded_rectangle([3*SCALE, 4*SCALE, total_w - 3*SCALE, TOTAL_H - 8*SCALE], radius=int(12*SCALE), fill=th["front"])
        # Angled Top Surface
        draw.rounded_rectangle([4*SCALE, top_y1, total_w - 4*SCALE, top_y2], radius=int(11*SCALE), fill=th["top"], outline=th["border"], width=int(1.5*SCALE))
        # Concave Scoop Dish
        dish_x1 = 7 * SCALE
        dish_x2 = total_w - 7 * SCALE
        draw.rounded_rectangle([dish_x1, dish_y1, dish_x2, dish_y2], radius=int(9*SCALE), fill=th["dish"])

        logo_x = (total_w - target_w) // 2
        if el_scaled:
            canvas.paste(el_scaled, (logo_x, dish_cy - target_h // 2), el_scaled)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_bahn_main
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="bahnschrift.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(2 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = max(int(260 * SCALE) if badge_id == "live" else int(235 * SCALE), pad_h * 2 + content_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.rounded_rectangle([4*SCALE, 12*SCALE, total_w - 4*SCALE, TOTAL_H - 1*SCALE], radius=int(14*SCALE), fill=(0, 0, 0, 140))
        draw.rounded_rectangle([3*SCALE, 6*SCALE, total_w - 3*SCALE, TOTAL_H - 4*SCALE], radius=int(13*SCALE), fill=th["skirt"])
        draw.rounded_rectangle([3*SCALE, 4*SCALE, total_w - 3*SCALE, TOTAL_H - 8*SCALE], radius=int(12*SCALE), fill=th["front"])
        draw.rounded_rectangle([4*SCALE, top_y1, total_w - 4*SCALE, top_y2], radius=int(11*SCALE), fill=th["top"], outline=th["border"], width=int(1.5*SCALE))

        dish_x1 = 7 * SCALE
        dish_x2 = total_w - 7 * SCALE
        draw.rounded_rectangle([dish_x1, dish_y1, dish_x2, dish_y2], radius=int(9*SCALE), fill=th["dish"])

        cur_x = (total_w - content_w) // 2

        if el_scaled:
            canvas.paste(el_scaled, (cur_x, dish_cy - target_h // 2), el_scaled)
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, dish_cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=th["legend"])
            cur_x += w_m + gap

        draw.line([(cur_x, dish_cy - 12*SCALE), (cur_x, dish_cy + 12*SCALE)], fill=(120, 135, 160, 180), width=div_w)
        cur_x += div_w + gap

        if sub_text:
            draw.text((cur_x, dish_cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=th["sub"])

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

RGB_KEYCAP_COLORS = {
    "torrentio": (0, 220, 255),
    "limetorrents": (75, 220, 60),
    "torrentleech": (0, 210, 255),
    "iptorrents": (30, 140, 255),
    "kickasstorrents": (235, 175, 45),
    "kat": (235, 175, 45),
    "bitsearch": (0, 220, 210),
    "torrentday": (0, 180, 255),
    "fitgirl": (255, 45, 130),

    "netflix": (229, 9, 20),
    "jiohotstar": (255, 204, 0),
    "prime": (0, 168, 225),
    "primevideo": (0, 168, 225),
    "disney": (0, 230, 255),
    "disneyplus": (0, 230, 255),
    "appletv": (240, 245, 255),
    "hbomax": (168, 85, 247),
    "max": (168, 85, 247),
    "hoichoi": (229, 9, 20),
    "chorki": (255, 19, 86),
    "toffee": (249, 115, 22),
    "binge": (229, 9, 20),
    "peacock": (16, 185, 129),
    "paramount": (56, 189, 248),
    "hulu": (34, 197, 94),
    "crunchyroll": (249, 115, 22),
    "aha": (249, 115, 22),
    "sunnxt": (255, 204, 0),
    "zee5": (168, 85, 247),
    "sonyliv": (56, 189, 248),
    "jiocinema": (229, 9, 20),
    "bangladesh": (16, 185, 129),
    "bangladesh-flag": (16, 185, 129),
    "bengali": (16, 185, 129),
    "bengali-flag2": (16, 185, 129),
    "hindi": (245, 158, 11),
    "hindi-flag": (245, 158, 11),
    "english": (59, 130, 246),
    "english-flag": (59, 130, 246),
    "japanese": (239, 68, 68),
    "japanese-flag": (239, 68, 68),
    "korean": (99, 102, 241),
    "korean-flag": (99, 102, 241),
    "chinese": (239, 68, 68),
    "chinese-flag": (239, 68, 68),
    "spanish": (245, 158, 11),
    "spanish-flag": (245, 158, 11),
    "german": (234, 179, 8),
    "german-flag": (234, 179, 8),
    "french": (59, 130, 246),
    "french-flag": (59, 130, 246),
    "italian": (34, 197, 94),
    "russian": (59, 130, 246),
    "turkish": (239, 68, 68),
    "arabic": (16, 185, 129),
    "thai": (59, 130, 246),
    "thai-flag": (59, 130, 246),
    "vietnamese": (239, 68, 68),
    "vietnamese-flag": (239, 68, 68),
    "indonesian": (239, 68, 68),
    "indonesian-flag": (239, 68, 68),
    "portuguese": (34, 197, 94),
    "punjabi": (245, 158, 11),
    "punjabi-flag": (245, 158, 11),
    "marathi": (245, 158, 11),
    "marathi-flag": (245, 158, 11),
    "telugu": (245, 158, 11),
    "telugu-flag": (245, 158, 11),
    "tamil": (245, 158, 11),
    "tamil-flag": (245, 158, 11),
    "kannada": (245, 158, 11),
    "kannada-flag": (245, 158, 11),
    "malayalam": (245, 158, 11),
    "malayalam-flag": (245, 158, 11),
    "gujarati": (245, 158, 11),
    "gujarati-flag": (245, 158, 11),
    "urdu": (16, 185, 129),
    "urdu-flag": (16, 185, 129),
}

# ------------------------------------------------------------------------------
# 4. NEON RGB PUDDING KEYCAPS (Theme 3 - Authentic Chroma Underglow & MX Stem)
# ------------------------------------------------------------------------------
def render_rgb_keycaps(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    rgb_col = RGB_KEYCAP_COLORS.get(badge_id, (0, 242, 254))

    pad_l = 42 * SCALE
    pad_r = 24 * SCALE
    gap = 10 * SCALE

    if is_ott:
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(48 * SCALE * boost), int(54 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None
        min_w = max(196 * SCALE, get_ott_min_w(badge_id, SCALE))
        content_w = target_w
        total_w = max(min_w, pad_l + content_w + pad_r)
    else:
        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        f_m = font_bahn_main
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="bahnschrift.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(2.0 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = pad_l + content_w + pad_r

    canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)

    # 1. Radiant Ambient Floor RGB Glow (Rich Gaussian Blur matching Rows 1-4)
    glow_canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_canvas)
    g_draw.rounded_rectangle([4*SCALE, 10*SCALE, total_w - 4*SCALE, TOTAL_H - 1*SCALE], radius=int(14*SCALE), fill=rgb_col + (190,))
    canvas.alpha_composite(glow_canvas.filter(ImageFilter.GaussianBlur(radius=int(6*SCALE))))

    # 2. Translucent Milky White Pudding Skirt (Diffusing underglow matching Rows 1-4)
    draw.rounded_rectangle([3*SCALE, 6*SCALE, total_w - 3*SCALE, TOTAL_H - 4*SCALE], radius=int(13*SCALE), fill=(240, 245, 255, 195), outline=rgb_col + (255,), width=int(1.8*SCALE))

    # 3. 3D Keycap Front Wall & Top Surface Face (giving identical 3D volume as Rows 1-4)
    top_y1 = 3 * SCALE
    top_y2 = TOTAL_H - 18 * SCALE
    draw.rounded_rectangle([3*SCALE, 4*SCALE, total_w - 3*SCALE, TOTAL_H - 8*SCALE], radius=int(12*SCALE), fill=(22, 25, 32, 255))
    draw.rounded_rectangle([4*SCALE, top_y1, total_w - 4*SCALE, top_y2], radius=int(10*SCALE), fill=(16, 18, 24, 255), outline=(55, 62, 78, 255), width=int(1.5*SCALE))

    # 4. Concave Spherical Scoop Dish with Specular Highlight (matching Rows 1-4)
    dish_x1 = 7 * SCALE
    dish_y1 = top_y1 + 3 * SCALE
    dish_x2 = total_w - 7 * SCALE
    dish_y2 = top_y2 - 3 * SCALE
    draw.rounded_rectangle([dish_x1, dish_y1, dish_x2, dish_y2], radius=int(8*SCALE), fill=(28, 32, 42, 255))
    draw.arc([dish_x1 + 4*SCALE, dish_y1 + 1*SCALE, dish_x2 - 4*SCALE, dish_y1 + 12*SCALE], 0, 180, fill=(255, 255, 255, 80), width=int(1.5*SCALE))

    # 5. Illuminated Cherry MX Switch Stem with Glowing LED Diode (matching Rows 1-4)
    stem_cx = 18 * SCALE
    stem_cy = (dish_y1 + dish_y2) // 2
    draw.ellipse([stem_cx - 10*SCALE, stem_cy - 10*SCALE, stem_cx + 10*SCALE, stem_cy + 10*SCALE], fill=(10, 12, 16, 255), outline=rgb_col + (255,), width=int(1.5*SCALE))
    draw.ellipse([stem_cx - 3*SCALE, stem_cy - 3*SCALE, stem_cx + 3*SCALE, stem_cy + 3*SCALE], fill=rgb_col + (255,))
    arm = 6 * SCALE
    thk = 2.2 * SCALE
    draw.rectangle([stem_cx - thk, stem_cy - arm, stem_cx + thk, stem_cy + arm], fill=(255, 255, 255, 255))
    draw.rectangle([stem_cx - arm, stem_cy - thk, stem_cx + arm, stem_cy + thk], fill=(255, 255, 255, 255))

    cy = (dish_y1 + dish_y2) // 2

    if is_ott:
        logo_x = pad_l + (total_w - pad_l - pad_r - target_w) // 2
        if el_scaled:
            arr_el = np.array(el_scaled).astype(float)
            m_alpha = arr_el[:, :, 3] > 30
            if m_alpha.sum() > 0:
                mean_lum = arr_el[m_alpha, :3].mean()
                if mean_lum < 60:
                    mult = 160.0 / max(mean_lum, 1.0)
                    arr_el[m_alpha, :3] = np.clip(arr_el[m_alpha, :3] * mult, 0, 255)
                    el_scaled = Image.fromarray(arr_el.astype(np.uint8))
            canvas.paste(el_scaled, (logo_x, cy - target_h // 2), el_scaled)
    else:
        x_curr = pad_l
        if el_scaled:
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            canvas.paste(flag_c, (x_curr, cy - target_h // 2), flag_c)
            x_curr += target_w + gap

        if main_text:
            draw.text((x_curr, cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=(255, 255, 255, 255))
            x_curr += w_m + gap

        draw.line([(x_curr, cy - 12*SCALE), (x_curr, cy + 12*SCALE)], fill=rgb_col + (255,), width=div_w)
        x_curr += div_w + gap

        if sub_text:
            draw.text((x_curr, cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=(255, 255, 255, 220))

    final_w = max(1, int(round(total_w / SCALE)))
    return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

# ------------------------------------------------------------------------------
# 5. DIRECTOR CINEMA CLAPPERBOARD (Theme 7)
# ------------------------------------------------------------------------------
def render_clapperboard(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    pad_h = 24 * SCALE
    gap = 10 * SCALE

    pad_y = 6 * SCALE
    h = TOTAL_H - pad_y * 2
    stick_h = int(16 * SCALE)
    slate_y1 = pad_y + stick_h
    slate_y2 = pad_y + h
    slate_cy = (slate_y1 + slate_y2) // 2

    if is_ott:
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(48 * SCALE * boost), int(54 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_h * 2 + target_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Slate Body with drop shadow
        draw.rounded_rectangle([4*SCALE, pad_y + 4*SCALE, total_w - 4*SCALE, pad_y + h + 4*SCALE], radius=int(6*SCALE), fill=(0, 0, 0, 150))
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(6*SCALE), fill=(20, 22, 26, 255), outline=(55, 60, 72, 255), width=int(1.5*SCALE))

        # Clapper Stick (Top 16*SCALE) with diagonal stripes slanting "\"
        stick_mask = Image.new("L", (total_w, TOTAL_H), 0)
        m_draw = ImageDraw.Draw(stick_mask)
        m_draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(6*SCALE), fill=255)
        m_draw.rectangle([0, pad_y + stick_h, total_w, TOTAL_H], fill=0)

        stick_img = Image.new("RGBA", (total_w, TOTAL_H), (20, 22, 26, 255))
        s_draw = ImageDraw.Draw(stick_img)
        stripe_w = int(10 * SCALE)
        for sx in range(int(-20*SCALE), int(total_w + 30*SCALE), stripe_w * 2):
            s_draw.polygon([
                (sx, pad_y + stick_h), (sx + stripe_w, pad_y + stick_h),
                (sx + stripe_w + stick_h, pad_y), (sx + stick_h, pad_y)
            ], fill=(240, 240, 245, 255))
        canvas.paste(stick_img, (0, 0), stick_mask)

        # Stick separator line
        draw.line([(4*SCALE, pad_y + stick_h), (total_w - 4*SCALE, pad_y + stick_h)], fill=(40, 44, 52, 255), width=int(2*SCALE))

        logo_x = (total_w - target_w) // 2
        if el_scaled:
            canvas.paste(el_scaled, (logo_x, slate_cy - target_h // 2), el_scaled)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_cinema
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="bahnschrift.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(1.8 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = max(int(260 * SCALE) if badge_id == "live" else int(235 * SCALE), pad_h * 2 + content_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.rounded_rectangle([4*SCALE, pad_y + 4*SCALE, total_w - 4*SCALE, pad_y + h + 4*SCALE], radius=int(6*SCALE), fill=(0, 0, 0, 150))
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(6*SCALE), fill=(20, 22, 26, 255), outline=(55, 60, 72, 255), width=int(1.5*SCALE))

        stick_mask = Image.new("L", (total_w, TOTAL_H), 0)
        m_draw = ImageDraw.Draw(stick_mask)
        m_draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(6*SCALE), fill=255)
        m_draw.rectangle([0, pad_y + stick_h, total_w, TOTAL_H], fill=0)

        stick_img = Image.new("RGBA", (total_w, TOTAL_H), (20, 22, 26, 255))
        s_draw = ImageDraw.Draw(stick_img)
        stripe_w = int(10 * SCALE)
        for sx in range(int(-20*SCALE), int(total_w + 30*SCALE), stripe_w * 2):
            s_draw.polygon([
                (sx, pad_y + stick_h), (sx + stripe_w, pad_y + stick_h),
                (sx + stripe_w + stick_h, pad_y), (sx + stick_h, pad_y)
            ], fill=(240, 240, 245, 255))
        canvas.paste(stick_img, (0, 0), stick_mask)

        draw.line([(4*SCALE, pad_y + stick_h), (total_w - 4*SCALE, pad_y + stick_h)], fill=(40, 44, 52, 255), width=int(2*SCALE))

        cur_x = (total_w - content_w) // 2

        if el_scaled:
            canvas.paste(el_scaled, (cur_x, slate_cy - target_h // 2), el_scaled)
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, slate_cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=(255, 255, 255, 255))
            cur_x += w_m + gap

        draw.line([(cur_x, slate_cy - 12*SCALE), (cur_x, slate_cy + 12*SCALE)], fill=(70, 80, 95, 255), width=div_w)
        cur_x += div_w + gap

        if sub_text:
            draw.text((cur_x, slate_cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=(200, 210, 225, 255))

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

# ------------------------------------------------------------------------------
# 6. CLOISONNÉ ENAMEL PINS (Theme 5)
# ------------------------------------------------------------------------------
ENAMEL_OTT_COLORS = {
    'netflix': (52, 12, 16, 255),
    'prime': (12, 28, 56, 255),
    'primevideo': (12, 28, 56, 255),
    'disney': (8, 24, 62, 255),
    'disneyplus': (8, 24, 62, 255),
    'appletv': (22, 24, 30, 255),
    'apple': (22, 24, 30, 255),
    'max': (42, 16, 68, 255),
    'hbomax': (42, 16, 68, 255),
    'hbo': (42, 16, 68, 255),
    'hoichoi': (54, 10, 14, 255),
    'chorki': (54, 12, 38, 255),
    'jiohotstar': (10, 22, 48, 255),
    'hotstar': (10, 22, 48, 255),
    'hulu': (12, 48, 24, 255),
    'paramount': (10, 30, 68, 255),
    'peacock': (22, 25, 32, 255),
    'crunchyroll': (58, 24, 10, 255),
    'sonyliv': (26, 20, 48, 255),
    'zee5': (44, 16, 52, 255),
    'bongo': (52, 12, 22, 255),
    'toffee': (54, 24, 12, 255),
    'binge': (48, 14, 28, 255),
    'bioscope': (18, 30, 50, 255),
    'aha': (54, 24, 10, 255),
    'sunnxt': (56, 30, 10, 255),
    'addatimes': (50, 12, 18, 255),
    'jiocinema': (52, 12, 36, 255),
    'mubi': (24, 24, 28, 255),
    'criterion': (36, 28, 14, 255),
    'a24': (20, 20, 24, 255),
    'alldebrid': (88, 64, 12, 255),
    'realdebrid': (18, 22, 28, 255),
    'real-debrid': (18, 22, 28, 255),
    'torbox': (14, 48, 28, 255),
    'torrentio': (12, 34, 60, 255),
    'limetorrents': (14, 48, 24, 255),
    'torrentleech': (16, 28, 54, 255),
    'iptorrents': (14, 30, 64, 255),
    'kickasstorrents': (56, 30, 12, 255),
    'kat': (56, 30, 12, 255),
    'bitsearch': (12, 42, 44, 255),
    'torrentday': (16, 32, 64, 255),
    'fitgirl': (58, 14, 36, 255),
    '1337x': (52, 14, 16, 255),
    'yts': (16, 44, 24, 255),
}

ENAMEL_LANG_COLORS = {
    'bd': (12, 44, 24, 255),
    'in': (48, 24, 10, 255),
    'gb': (16, 26, 56, 255),
    'us': (16, 26, 56, 255),
    'jp': (48, 14, 20, 255),
    'kr': (18, 28, 60, 255),
    'cn': (54, 12, 16, 255),
    'es': (50, 18, 14, 255),
    'fr': (14, 26, 58, 255),
    'de': (36, 28, 16, 255),
    'it': (14, 42, 22, 255),
    'ru': (16, 28, 56, 255),
    'sa': (12, 44, 24, 255),
    'tr': (50, 14, 18, 255),
    'br': (12, 44, 24, 255),
    'pt': (12, 44, 24, 255),
}

def render_enamel_pins(is_ott, element_img, main_text, sub_text, badge_id=None, cc=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    pad_y = 6 * SCALE
    h = TOTAL_H - pad_y * 2
    pad_h = 24 * SCALE
    gap = 10 * SCALE
    rad = int(14 * SCALE)

    gold_base = (205, 155, 40, 255)
    gold_highlight = (255, 230, 140, 255)

    if is_ott:
        bed_color = ENAMEL_OTT_COLORS.get(badge_id, (18, 26, 44, 255))
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(48 * SCALE * boost), int(54 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_h * 2 + target_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Drop shadow
        draw.rounded_rectangle([4*SCALE, pad_y + 4*SCALE, total_w - 4*SCALE, pad_y + h + 4*SCALE], radius=rad, fill=(0, 0, 0, 140))

        # Cast Brass Rim
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=rad, fill=gold_base)
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=rad, outline=gold_highlight, width=int(1.8*SCALE))

        # Recessed Glossy Enamel Bed (100% solid jewel tone)
        inset = int(3.5 * SCALE)
        draw.rounded_rectangle([4*SCALE + inset, pad_y + inset, total_w - 4*SCALE - inset, pad_y + h - inset], radius=rad - int(2*SCALE), fill=bed_color)

        # Specular glint (smooth alpha composite - NEVER overwrites bed)
        glint_img = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glint_img)
        g_draw.polygon([
            (4*SCALE + 15*SCALE, pad_y + inset),
            (4*SCALE + 42*SCALE, pad_y + inset),
            (4*SCALE + 22*SCALE, pad_y + h - inset),
            (4*SCALE - 5*SCALE, pad_y + h - inset)
        ], fill=(255, 255, 255, 40))
        canvas = Image.alpha_composite(canvas, glint_img)

        logo_x = (total_w - target_w) // 2
        cy = pad_y + h // 2
        if el_scaled:
            canvas.alpha_composite(el_scaled, (logo_x, cy - target_h // 2))

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        if cc is None and badge_id:
            for b_n, c_code, _, _ in LANG_SPECS:
                if b_n == badge_id:
                    cc = c_code
                    break
        bed_color = ENAMEL_LANG_COLORS.get(cc, (18, 26, 44, 255))

        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_enamel_main
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="timesbd.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(1.8 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = max(int(260 * SCALE) if badge_id == "live" else int(235 * SCALE), pad_h * 2 + content_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Drop shadow
        draw.rounded_rectangle([4*SCALE, pad_y + 4*SCALE, total_w - 4*SCALE, pad_y + h + 4*SCALE], radius=rad, fill=(0, 0, 0, 140))

        # Cast Brass Rim
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=rad, fill=gold_base)
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=rad, outline=gold_highlight, width=int(1.8*SCALE))

        # Recessed Glossy Enamel Bed (100% solid jewel tone)
        inset = int(3.5 * SCALE)
        draw.rounded_rectangle([4*SCALE + inset, pad_y + inset, total_w - 4*SCALE - inset, pad_y + h - inset], radius=rad - int(2*SCALE), fill=bed_color)

        # Specular glint
        glint_img = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glint_img)
        g_draw.polygon([
            (4*SCALE + 15*SCALE, pad_y + inset),
            (4*SCALE + 42*SCALE, pad_y + inset),
            (4*SCALE + 22*SCALE, pad_y + h - inset),
            (4*SCALE - 5*SCALE, pad_y + h - inset)
        ], fill=(255, 255, 255, 40))
        canvas = Image.alpha_composite(canvas, glint_img)

        # Re-create draw for active composite canvas
        draw = ImageDraw.Draw(canvas)

        cy = pad_y + h // 2
        cur_x = (total_w - content_w) // 2

        if el_scaled:
            canvas.alpha_composite(el_scaled, (cur_x, cy - target_h // 2))
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=(255, 255, 255, 255))
            cur_x += w_m + gap

        draw.line([(cur_x, cy - 12*SCALE), (cur_x, cy + 12*SCALE)], fill=(180, 140, 40, 255), width=div_w)
        cur_x += div_w + gap

        if sub_text:
            draw.text((cur_x, cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=(255, 225, 120, 255))

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

# ------------------------------------------------------------------------------
# 7. AUDIOPHILE VACUUM FLUORESCENT (Theme 8)
# ------------------------------------------------------------------------------
def render_audiophile_vfd(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    pad_y = 6 * SCALE
    h = TOTAL_H - pad_y * 2
    pad_h = 24 * SCALE
    gap = 10 * SCALE

    cyan_phosphor = (0, 240, 255, 255)

    if is_ott:
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(48 * SCALE * boost), int(54 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_h * 2 + target_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Chassis
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(6*SCALE), fill=(18, 20, 24, 255), outline=(50, 54, 62, 255), width=int(1.5*SCALE))

        # Smoked Glass Window
        win_inset = int(4 * SCALE)
        draw.rounded_rectangle([4*SCALE + win_inset, pad_y + win_inset, total_w - 4*SCALE - win_inset, pad_y + h - win_inset], radius=int(4*SCALE), fill=(6, 22, 28, 255), outline=(35, 60, 72, 255), width=int(1.2*SCALE))

        # Scanlines
        for ly in range(pad_y + win_inset + 2*SCALE, pad_y + h - win_inset, int(2.5*SCALE)):
            draw.line([(4*SCALE + win_inset, ly), (total_w - 4*SCALE - win_inset, ly)], fill=(12, 38, 48, 160), width=int(1*SCALE))

        logo_x = (total_w - target_w) // 2
        cy = pad_y + h // 2
        if el_scaled:
            canvas.paste(el_scaled, (logo_x, cy - target_h // 2), el_scaled)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_vfd
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="consolab.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        dot_str = "•"
        bb_d = d.textbbox((0, 0), dot_str, font=f_m)
        w_d = bb_d[2] - bb_d[0]
        h_d = bb_d[3] - bb_d[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        content_w = target_w + gap + w_m + gap + w_d + gap + w_s
        total_w = max(int(260 * SCALE) if badge_id == "live" else int(235 * SCALE), pad_h * 2 + content_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(6*SCALE), fill=(18, 20, 24, 255), outline=(50, 54, 62, 255), width=int(1.5*SCALE))

        win_inset = int(4 * SCALE)
        draw.rounded_rectangle([4*SCALE + win_inset, pad_y + win_inset, total_w - 4*SCALE - win_inset, pad_y + h - win_inset], radius=int(4*SCALE), fill=(6, 22, 28, 255), outline=(35, 60, 72, 255), width=int(1.2*SCALE))

        for ly in range(pad_y + win_inset + 2*SCALE, pad_y + h - win_inset, int(2.5*SCALE)):
            draw.line([(4*SCALE + win_inset, ly), (total_w - 4*SCALE - win_inset, ly)], fill=(12, 38, 48, 160), width=int(1*SCALE))

        cy = pad_y + h // 2
        cur_x = (total_w - content_w) // 2

        if el_scaled:
            canvas.paste(el_scaled, (cur_x, cy - target_h // 2), el_scaled)
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=cyan_phosphor)
            cur_x += w_m + gap

        draw.text((cur_x, cy - bb_d[1] - h_d // 2), dot_str, font=f_m, fill=cyan_phosphor)
        cur_x += w_d + gap

        if sub_text:
            draw.text((cur_x, cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=cyan_phosphor)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

# ------------------------------------------------------------------------------
# 8. NEO-TOKYO CYBERPUNK TAG (Theme 9)
# ------------------------------------------------------------------------------
def render_neotokyo_tag(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    pad_y = 6 * SCALE
    h = TOTAL_H - pad_y * 2
    pad_h = 24 * SCALE
    gap = 10 * SCALE

    hazard_pink = (255, 45, 85, 255)
    micro_header = "SYS // STREAM // RAW" if is_ott else f"SYS // LANG // {main_text}"

    bb_hdr = d.textbbox((0, 0), micro_header, font=font_bahn_micro)
    h_hdr = bb_hdr[3] - bb_hdr[1]
    header_space = h_hdr + 4 * SCALE
    content_cy = pad_y + header_space + (h - header_space) // 2

    if is_ott:
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(48 * SCALE * boost), int(54 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_h * 2 + target_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # Techwear dark slate chassis
        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(4*SCALE), fill=(14, 16, 20, 255), outline=(42, 46, 56, 255), width=int(1.5*SCALE))

        # Vertical Left Hazard Bar
        draw.rectangle([4*SCALE, pad_y + 2*SCALE, 4*SCALE + int(3.5*SCALE), pad_y + h - 2*SCALE], fill=hazard_pink)

        # Top micro header
        draw.text((12 * SCALE, pad_y + 4 * SCALE), micro_header, font=font_bahn_micro, fill=(120, 130, 150, 255))

        logo_x = (total_w - target_w) // 2
        if el_scaled:
            canvas.paste(el_scaled, (logo_x, content_cy - target_h // 2), el_scaled)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_bahn_main
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="bahnschrift.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(2 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = max(int(260 * SCALE) if badge_id == "live" else int(235 * SCALE), pad_h * 2 + content_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        draw.rounded_rectangle([4*SCALE, pad_y, total_w - 4*SCALE, pad_y + h], radius=int(4*SCALE), fill=(14, 16, 20, 255), outline=(42, 46, 56, 255), width=int(1.5*SCALE))

        draw.rectangle([4*SCALE, pad_y + 2*SCALE, 4*SCALE + int(3.5*SCALE), pad_y + h - 2*SCALE], fill=hazard_pink)

        draw.text((12 * SCALE, pad_y + 4 * SCALE), micro_header, font=font_bahn_micro, fill=(120, 130, 150, 255))

        cur_x = (total_w - content_w) // 2

        if el_scaled:
            canvas.paste(el_scaled, (cur_x, content_cy - target_h // 2), el_scaled)
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, content_cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=(255, 255, 255, 255))
            cur_x += w_m + gap

        draw.line([(cur_x, content_cy - 12*SCALE), (cur_x, content_cy + 12*SCALE)], fill=hazard_pink, width=div_w)
        cur_x += div_w + gap

        if sub_text:
            draw.text((cur_x, content_cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=(200, 210, 225, 255))

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

# ------------------------------------------------------------------------------
# 9. CRITERION ARCHIVAL LEATHER (Theme 10 - 100% Match to 4k.webp & realdebrid.webp)
# ------------------------------------------------------------------------------
def render_criterion_leather(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    pad_h = 24 * SCALE
    gap = 12 * SCALE

    gold_outline = (212, 175, 55, 240)
    gold_rivet = (255, 223, 110, 255)

    if is_ott:
        boost = OTT_BOOSTS.get(badge_id, 1.0) if "badge_id" in locals() and badge_id else 1.0
        target_h = min(int(46 * SCALE * boost), int(52 * SCALE))
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_h * 2 + target_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # 1. Deep Archival Leather Fill (identical bounds to 4k.webp)
        draw.rounded_rectangle(
            [4 * SCALE, 6 * SCALE, total_w - 4 * SCALE, 90 * SCALE],
            radius=int(6 * SCALE),
            fill=(16, 18, 19, 255)
        )

        # 2. Single 24K Gold Pinstripe Border (identical to 4k.webp)
        draw.rounded_rectangle(
            [7 * SCALE, 9 * SCALE, total_w - 8 * SCALE, 86 * SCALE],
            radius=int(5 * SCALE),
            outline=gold_outline,
            width=int(1.8 * SCALE)
        )

        # 3. Four Corner Gold Diamond Rivets (detached inside corners)
        d_rad = 3.0 * SCALE
        corners = [
            (12.5 * SCALE, 13.5 * SCALE),
            (total_w - 12.5 * SCALE, 13.5 * SCALE),
            (total_w - 12.5 * SCALE, 81.5 * SCALE),
            (12.5 * SCALE, 81.5 * SCALE)
        ]
        for cx, cy_pt in corners:
            draw.polygon([
                (cx, cy_pt - d_rad), (cx + d_rad, cy_pt),
                (cx, cy_pt + d_rad), (cx - d_rad, cy_pt)
            ], fill=gold_rivet)

        # 4. Center Logo
        logo_x = (total_w - target_w) // 2
        cy = 48 * SCALE
        if el_scaled:
            arr_el = np.array(el_scaled).astype(float)
            m_alpha = arr_el[:, :, 3] > 30
            if m_alpha.sum() > 0:
                mean_lum = arr_el[m_alpha, :3].mean()
                if mean_lum < 60:
                    mult = 160.0 / max(mean_lum, 1.0)
                    arr_el[m_alpha, :3] = np.clip(arr_el[m_alpha, :3] * mult, 0, 255)
                    el_scaled = Image.fromarray(arr_el.astype(np.uint8))
            canvas.paste(el_scaled, (logo_x, cy - target_h // 2), el_scaled)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        target_h = 28 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_criterion_main
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="timesbd.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(1.8 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = max(int(260 * SCALE) if badge_id == "live" else int(235 * SCALE), pad_h * 2 + content_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # 1. Deep Archival Leather Fill
        draw.rounded_rectangle(
            [4 * SCALE, 6 * SCALE, total_w - 4 * SCALE, 90 * SCALE],
            radius=int(6 * SCALE),
            fill=(16, 18, 19, 255)
        )

        # 2. Single 24K Gold Pinstripe Border (identical to 4k.webp)
        draw.rounded_rectangle(
            [7 * SCALE, 9 * SCALE, total_w - 8 * SCALE, 86 * SCALE],
            radius=int(5 * SCALE),
            outline=gold_outline,
            width=int(1.8 * SCALE)
        )

        # 3. Four Corner Gold Diamond Rivets (detached inside corners)
        d_rad = 3.0 * SCALE
        corners = [
            (12.5 * SCALE, 13.5 * SCALE),
            (total_w - 12.5 * SCALE, 13.5 * SCALE),
            (total_w - 12.5 * SCALE, 81.5 * SCALE),
            (12.5 * SCALE, 81.5 * SCALE)
        ]
        for cx, cy_pt in corners:
            draw.polygon([
                (cx, cy_pt - d_rad), (cx + d_rad, cy_pt),
                (cx, cy_pt + d_rad), (cx - d_rad, cy_pt)
            ], fill=gold_rivet)

        cy = 48 * SCALE
        cur_x = (total_w - content_w) // 2

        if el_scaled:
            canvas.paste(el_scaled, (cur_x, cy - target_h // 2), el_scaled)
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=(245, 215, 110, 255))
            cur_x += w_m + gap

        draw.line([(cur_x, cy - 12*SCALE), (cur_x, cy + 12*SCALE)], fill=(180, 150, 70, 255), width=div_w)
        cur_x += div_w + gap

        if sub_text:
            draw.text((cur_x, cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=(225, 195, 95, 255))

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

# ------------------------------------------------------------------------------
# 10. PRISTINE MASTER (Theme 1 - Pure Floating)
# ------------------------------------------------------------------------------
def render_pristine_floating(is_ott, element_img, main_text, sub_text, badge_id=None):
    dummy = Image.new("RGBA", (1, 1))
    d = ImageDraw.Draw(dummy)

    pad_h = 20 * SCALE
    gap = 10 * SCALE

    if is_ott:
        target_h = 60 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS) if element_img else None

        min_w = get_ott_min_w(badge_id, SCALE)
        total_w = max(min_w, pad_h * 2 + target_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        cy = TOTAL_H // 2
        logo_x = (total_w - target_w) // 2
        if el_scaled:
            canvas.paste(el_scaled, (logo_x, cy - target_h // 2), el_scaled)

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)
    else:
        target_h = 32 * SCALE
        target_w = int(element_img.width * (target_h / element_img.height)) if element_img else 0
        if element_img:
            el_scaled = element_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, target_w, target_h], radius=int(3*SCALE), fill=255)
            flag_c = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
            flag_c.paste(el_scaled, (0, 0), mask)
            el_scaled = flag_c
        else:
            el_scaled = None

        f_m = font_main
        f_s = get_font_for_text(sub_text, 22 * SCALE, default_font="arialbd.ttf")

        bb_m = d.textbbox((0, 0), main_text, font=f_m) if main_text else (0, 0, 0, 0)
        w_m = bb_m[2] - bb_m[0]
        h_m = bb_m[3] - bb_m[1]

        bb_s = d.textbbox((0, 0), sub_text, font=f_s) if sub_text else (0, 0, 0, 0)
        w_s = bb_s[2] - bb_s[0]
        h_s = bb_s[3] - bb_s[1]

        div_w = int(1.5 * SCALE)
        content_w = target_w + gap + w_m + gap + div_w + gap + w_s
        total_w = max(int(260 * SCALE) if badge_id == "live" else int(235 * SCALE), pad_h * 2 + content_w)

        canvas = Image.new("RGBA", (total_w, TOTAL_H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        cy = TOTAL_H // 2
        cur_x = pad_h

        if el_scaled:
            canvas.paste(el_scaled, (cur_x, cy - target_h // 2), el_scaled)
            cur_x += target_w + gap

        if main_text:
            draw.text((cur_x, cy - bb_m[1] - h_m // 2), main_text, font=f_m, fill=(255, 255, 255, 255))
            cur_x += w_m + gap

        draw.line([(cur_x, cy - 14*SCALE), (cur_x, cy + 14*SCALE)], fill=(150, 160, 175, 180), width=div_w)
        cur_x += div_w + gap

        if sub_text:
            draw.text((cur_x, cy - bb_s[1] - h_s // 2), sub_text, font=f_s, fill=(200, 210, 225, 255))

        final_w = max(1, int(round(total_w / SCALE)))
        return canvas.resize((final_w, CANVAS_H), Image.Resampling.LANCZOS)

THEME_RENDERERS = {
    "vhs-tape": render_vhs_tape,
    "cinema-ticket": render_cinema_ticket,
    "gmk-keycaps": render_gmk_keycaps,
    "rgb-keycaps": render_rgb_keycaps,
    "clapperboard": render_clapperboard,
    "enamel-pins": render_enamel_pins,
    "audiophile-vfd": render_audiophile_vfd,
    "neotokyo-tag": render_neotokyo_tag,
    "criterion-leather": render_criterion_leather,
    "pristine": render_pristine_floating,
}

def main():
    print("=== BUILDING BESPOKE THEMED BADGES V5 (ULTRA-BALANCED PROPORTIONS & MATERIALS) ===")

    ott_images = {}
    for b_name, img_file in OTT_SPECS:
        img_p = os.path.join(OTT_DIR, img_file)
        if os.path.exists(img_p):
            ott_images[b_name] = Image.open(img_p).convert("RGBA")
        else:
            print(f"Warning: OTT asset missing {img_p}")

    flag_images = {}
    for b_name, cc, m_text, s_text in LANG_SPECS:
        flag_p = os.path.join(FLAG_DIR, f"{cc}.png")
        if os.path.exists(flag_p) and cc not in flag_images:
            flag_images[cc] = Image.open(flag_p).convert("RGBA")

    if len(sys.argv) > 1:
        all_themes = [t for t in sys.argv[1:] if t in THEME_RENDERERS]
    else:
        all_themes = list(THEME_RENDERERS.keys())
    for theme_id in all_themes:
        renderer = THEME_RENDERERS[theme_id]
        if theme_id == "pristine":
            out_dir = os.path.join(REPO_ROOT, "badges")
        else:
            out_dir = os.path.join(REPO_ROOT, "themes", theme_id, "badges")
        os.makedirs(out_dir, exist_ok=True)

        print(f"Rendering theme: {theme_id} -> {out_dir}")

        for b_name, img_file in OTT_SPECS:
            if b_name in ott_images:
                try:
                    badge = renderer(True, ott_images[b_name], None, None, badge_id=b_name)
                except TypeError:
                    badge = renderer(True, ott_images[b_name], None, None)
                badge.save(os.path.join(out_dir, f"{b_name}.webp"), "WEBP", quality=95)

        for b_name, cc, m_text, s_text in LANG_SPECS:
            flag_img = flag_images.get(cc)
            if flag_img:
                try:
                    badge = renderer(False, flag_img, m_text, s_text, badge_id=b_name, cc=cc)
                except TypeError:
                    try:
                        badge = renderer(False, flag_img, m_text, s_text, badge_id=b_name)
                    except TypeError:
                        badge = renderer(False, flag_img, m_text, s_text)
                badge.save(os.path.join(out_dir, f"{b_name}.webp"), "WEBP", quality=95)

    print("\nSUCCESS: All OTT and Language badges rendered with 100% canonical physical harmonization!")

if __name__ == "__main__":
    main()
