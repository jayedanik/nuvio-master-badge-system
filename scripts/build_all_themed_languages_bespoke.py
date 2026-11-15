import os, sys
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
THEMES_DIR = os.path.join(REPO_ROOT, "themes")
FLAG_DIR = r"C:\Users\yourt\.gemini\antigravity\scratch\official_flags_png"

sys.path.insert(0, SCRIPT_DIR)
import build_all_bespoke_themed_badges_v5 as b5

THEME_RENDERERS = {
    "gmk-keycaps": b5.render_gmk_keycaps,
    "rgb-keycaps": b5.render_rgb_keycaps,
    "cinema-ticket": b5.render_cinema_ticket,
    "enamel-pins": b5.render_enamel_pins,
    "vhs-tape": b5.render_vhs_tape,
    "clapperboard": b5.render_clapperboard,
    "audiophile-vfd": b5.render_audiophile_vfd,
    "neotokyo-tag": b5.render_neotokyo_tag,
    "criterion-leather": b5.render_criterion_leather,
}

# Country Badges: (output_filename, flag_code, eng_text, code)
COUNTRY_BADGES = [
    ("canada.webp", "ca", "CANADA", "CA"),
    ("australia.webp", "au", "AUSTRALIA", "AU"),
    ("argentina.webp", "ar", "ARGENTINA", "AR"),
    ("brazil.webp", "br", "BRAZIL", "PT-BR"),
    ("pakistan.webp", "pk", "PAKISTAN", "PK"),
    ("egypt.webp", "eg", "EGYPT", "EG"),
    ("switzerland.webp", "ch", "SWITZERLAND", "CH"),
    ("belgium.webp", "be", "BELGIUM", "BE"),
    ("austria.webp", "at", "AUSTRIA", "AT"),
    ("uk.webp", "gb", "UNITED KINGDOM", "UK"),
    ("southafrica.webp", "za", "SOUTH AFRICA", "ZA"),
    ("nigeria.webp", "ng", "NIGERIA", "NG"),
    ("singapore.webp", "sg", "SINGAPORE", "SG"),
    ("colombia.webp", "co", "COLOMBIA", "CO"),
    ("chile.webp", "cl", "CHILE", "CL"),
    ("morocco.webp", "ma", "MOROCCO", "MA"),
    ("scotland.webp", "gb-sct", "SCOTLAND", "SCT"),
    ("newzealand.webp", "nz", "NEW ZEALAND", "NZ"),
    ("mexico.webp", "mx", "MEXICO", "MX"),
    ("hongkong.webp", "hk", "HONG KONG", "HK"),
    ("taiwan.webp", "tw", "TAIWAN", "TW"),
    ("portugal.webp", "pt", "PORTUGUL", "PT"),
]

# Language Badges: (output_filenames, flag_code, eng_text, native_text)
LANGUAGE_BADGES = [
    (["nepali.webp", "nepali-flag.webp"], "np", "NEPALI", "नेपाली"),
    (["sinhala.webp", "sinhala-flag.webp"], "lk", "SINHALA", "සිංහල"),
    (["cantonese.webp", "cantonese-flag.webp"], "hk", "CANTONESE", "粵語"),
    (["bhojpuri.webp", "bhojpuri-flag.webp"], "in", "BHOJPURI", "भोजपुरी"),
    (["odia.webp", "odia-flag.webp"], "in", "ODIA", "ଓଡ଼ିଆ"),
    (["assamese.webp", "assamese-flag.webp"], "in", "ASSAMESE", "অসমীয়া"),
    (["portuguese.webp", "portuguese-flag.webp"], "pt", "PORTUGUESE", "Português"),
    (["brazilian.webp", "brazilian-flag.webp"], "br", "BRAZILIAN", "PT-BR"),
    (["burmese.webp", "burmese-flag.webp"], "mm", "BURMESE", "မြန်မာ"),
    (["ukrainian.webp", "ukrainian-flag.webp"], "ua", "UKRAINIAN", "Українська"),
    (["polish.webp", "polish-flag.webp"], "pl", "POLISH", "Polski"),
    (["czech.webp", "czech-flag.webp"], "cz", "CZECH", "Čeština"),
    (["slovak.webp", "slovak-flag.webp"], "sk", "SLOVAK", "Slovenčina"),
    (["hungarian.webp", "hungarian-flag.webp"], "hu", "HUNGARIAN", "Magyar"),
    (["romanian.webp", "romanian-flag.webp"], "ro", "ROMANIAN", "Română"),
    (["bulgarian.webp", "bulgarian-flag.webp"], "bg", "BULGARIAN", "Български"),
    (["serbian.webp", "serbian-flag.webp"], "rs", "SERBIAN", "Српски"),
    (["croatian.webp", "croatian-flag.webp"], "hr", "CROATIAN", "Hrvatski"),
    (["slovenian.webp", "slovenian-flag.webp"], "si", "SLOVENIAN", "Slovenščina"),
    (["bosnian.webp", "bosnian-flag.webp"], "ba", "BOSNIAN", "Bosanski"),
    (["albanian.webp", "albanian-flag.webp"], "al", "ALBANIAN", "Shqip"),
    (["greek.webp", "greek-flag.webp"], "gr", "GREEK", "Ελληνικά"),
    (["dutch.webp", "dutch-flag.webp"], "nl", "DUTCH", "Nederlands"),
    (["swedish.webp", "swedish-flag.webp"], "se", "SWEDISH", "Svenska"),
    (["danish.webp", "danish-flag.webp"], "dk", "DANISH", "Dansk"),
    (["finnish.webp", "finnish-flag.webp"], "fi", "FINNISH", "Suomi"),
    (["estonian.webp", "estonian-flag.webp"], "ee", "ESTONIAN", "Eesti"),
    (["belarusian.webp", "belarusian-flag.webp"], "by", "BELARUSIAN", "Беларуская"),
    (["persian.webp", "persian-flag.webp"], "ir", "PERSIAN", "فارسی"),
    (["pashto.webp", "pashto-flag.webp"], "af", "PASHTO", "پښتو"),
    (["georgian.webp", "georgian-flag.webp"], "ge", "GEORGIAN", "ქართული"),
    (["armenian.webp", "armenian-flag.webp"], "am", "ARMENIAN", "Հայերեն"),
    (["azerbaijani.webp", "azerbaijani-flag.webp"], "az", "AZERBAIJANI", "Azərbaycan"),
    (["uzbek.webp", "uzbek-flag.webp"], "uz", "UZBEK", "Oʻzbekcha"),
    (["swahili.webp", "swahili-flag.webp"], "ke", "SWAHILI", "Kiswahili"),
    (["amharic.webp", "amharic-flag.webp"], "et", "AMHARIC", "አማርኛ"),
    (["afrikaans.webp", "afrikaans-flag.webp"], "za", "AFRIKAANS", "Afrikaans"),
    (["yoruba.webp", "yoruba-flag.webp"], "ng", "YORUBA", "Yorùbá"),
    (["zulu.webp", "zulu-flag.webp"], "za", "ZULU", "isiZulu"),
    (["bangladesh.webp", "bangladesh-flag.webp"], "bd", "BANGLADESH", "বাংলা"),
    (["bengali.webp", "bengali-flag2.webp"], "bd", "BENGALI", "বাংলা"),
    (["hindi.webp", "hindi-flag.webp"], "in", "HINDI", "हिन्दी"),
    (["tamil.webp", "tamil-flag.webp"], "in", "TAMIL", "தமிழ்"),
    (["telugu.webp", "telugu-flag.webp"], "in", "TELUGU", "తెలుగు"),
    (["malayalam.webp", "malayalam-flag.webp"], "in", "MALAYALAM", "മലയാളം"),
    (["kannada.webp", "kannada-flag.webp"], "in", "KANNADA", "ಕನ್ನಡ"),
    (["marathi.webp", "marathi-flag.webp"], "in", "MARATHI", "मराठी"),
    (["gujarati.webp", "gujarati-flag.webp"], "in", "GUJARATI", "ગુજરાતી"),
    (["punjabi.webp", "punjabi-flag.webp"], "in", "PUNJABI", "ਪੰਜਾਬੀ"),
    (["urdu.webp", "urdu-flag.webp"], "pk", "URDU", "اردو"),
    (["japanese.webp", "japanese-flag.webp"], "jp", "JAPANESE", "日本語"),
    (["korean.webp", "korean-flag.webp"], "kr", "KOREAN", "한국어"),
    (["chinese.webp", "chinese-flag.webp"], "cn", "CHINESE", "中文"),
    (["french.webp", "french-flag.webp"], "fr", "FRENCH", "Français"),
    (["german.webp", "german-flag.webp"], "de", "GERMAN", "Deutsch"),
    (["spanish.webp", "spanish-flag.webp"], "es", "SPANISH", "Español"),
    (["italian.webp", "italian-flag.webp"], "it", "ITALIAN", "Italiano"),
    (["russian.webp", "russian-flag.webp"], "ru", "RUSSIAN", "Русский"),
    (["turkish.webp", "turkish-flag.webp"], "tr", "TURKISH", "Türkçe"),
    (["arabic.webp", "arabic-flag.webp"], "sa", "ARABIC", "العربية"),
    (["indonesian.webp", "indonesian-flag.webp"], "id", "INDONESIAN", "Bahasa"),
    (["malay.webp", "malay-flag.webp"], "my", "MALAY", "Melayu"),
    (["thai.webp", "thai-flag.webp"], "th", "THAI", "ไทย"),
    (["vietnamese.webp", "vietnamese-flag.webp"], "vn", "VIETNAMESE", "Tiếng Việt"),
    (["filipino.webp", "filipino-flag.webp"], "ph", "FILIPINO", "Tagalog"),
    (["khmer.webp", "khmer-flag.webp"], "kh", "KHMER", "ភាសាខ្មែរ"),
    (["lao.webp", "lao-flag.webp"], "la", "LAO", "ພາສາລາວ"),
    (["kazakh.webp", "kazakh-flag.webp"], "kz", "KAZAKH", "Қазақша"),
    (["mongolian.webp", "mongolian-flag.webp"], "mn", "MONGOLIAN", "Монгол"),
    (["icelandic.webp", "icelandic-flag.webp"], "is", "ICELANDIC", "Íslenska"),
    (["latvian.webp", "latvian-flag.webp"], "lv", "LATVIAN", "Latviešu"),
    (["lithuanian.webp", "lithuanian-flag.webp"], "lt", "LITHUANIAN", "Lietuvių"),
    (["macedonian.webp", "macedonian-flag.webp"], "mk", "MACEDONIAN", "Македонски"),
    (["norwegian.webp", "norwegian-flag.webp"], "no", "NORWEGIAN", "Norsk"),
    (["irish.webp", "irish-flag.webp"], "ie", "IRISH", "Gaeilge"),
    (["hebrew.webp", "hebrew-flag.webp"], "il", "HEBREW", "עברית"),
    (["catalan.webp", "catalan-flag.webp"], "es", "CATALAN", "Català"),
    (["basque.webp", "basque-flag.webp"], "es", "BASQUE", "Euskara"),
    (["galician.webp", "galician-flag.webp"], "es", "GALICIAN", "Galego"),
    (["hausa.webp", "hausa-flag.webp"], "ng", "HAUSA", "Hausa"),
]

def main():
    print("=== RENDERING 100% BESPOKE THEMED LANGUAGE & COUNTRY BADGES ===")
    
    # Preload flags into memory
    flags_cache = {}
    for fn in os.listdir(FLAG_DIR):
        if fn.endswith(".png"):
            code = os.path.splitext(fn)[0]
            try:
                flags_cache[code] = Image.open(os.path.join(FLAG_DIR, fn)).convert("RGBA")
            except Exception:
                pass
                
    for theme_id, renderer in THEME_RENDERERS.items():
        theme_dir = os.path.join(THEMES_DIR, theme_id, "badges")
        os.makedirs(theme_dir, exist_ok=True)
        print(f"\nProcessing {theme_id}...")
        count = 0
        
        # 1. Countries
        for out_fn, fcode, eng, code in COUNTRY_BADGES:
            flag_im = flags_cache.get(fcode)
            b = renderer(False, flag_im, eng, code, badge_id=fcode)
            out_p = os.path.join(theme_dir, out_fn)
            b.save(out_p, "WEBP", quality=95)
            count += 1
            
        # 2. Languages
        for out_fnames, fcode, eng, nat in LANGUAGE_BADGES:
            flag_im = flags_cache.get(fcode)
            b = renderer(False, flag_im, eng, nat, badge_id=fcode)
            for out_fn in out_fnames:
                out_p = os.path.join(theme_dir, out_fn)
                b.save(out_p, "WEBP", quality=95)
                count += 1
                
        print(f"  Rendered {count} bespoke themed country/language badges in {theme_id}!")

    print("\nALL 9 BESPOKE THEMES RECEIVED AUTHENTIC THEMED LANGUAGE BADGES!")

if __name__ == "__main__":
    main()
