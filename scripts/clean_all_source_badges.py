import os
from PIL import Image
import numpy as np

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
BADGES_DIR = os.path.join(REPO_ROOT, "badges")
BRAIN_SCRATCH = r"C:\Users\yourt\.gemini\antigravity\brain\fb22a0fc-6924-43f9-ab27-8d6db9906f8f\scratch"

# 1. Four Master Brand Logos
BRAND_FIXES = {
    "alldebrid": {
        "src": os.path.join(BRAIN_SCRATCH, "clean_alldebrid.png"),
        "target_canvas": (265, 96)
    },
    "wetv": {
        "src": os.path.join(BRAIN_SCRATCH, "clean_wetv_full.png"),
        "target_canvas": (256, 96)
    },
    "sonyliv": {
        "src": os.path.join(BRAIN_SCRATCH, "extracted_sonyliv.png"),
        "target_canvas": (140, 96)
    },
    "sonypictures": {
        "src": os.path.join(BRAIN_SCRATCH, "clean_sonypictures.png"),
        "target_canvas": (199, 96)
    }
}

# 2. Eighty-Six Smoked Pill Badges
SMOKED_BADGES = [
    '120fps.webp', '247.webp', '3d-fsbs.webp', '3d-hsbs.webp', '3d-mvc.webp', '3d-ou.webp',
    '50fps.webp', '6.1.webp', '60fps.webp', '6_1.webp', 'altt.webp', 'anaglyph.webp',
    'avi.webp', 'backup.webp', 'banglaflix.webp', 'batch.webp', 'bigfile.webp', 'bw.webp',
    'catchup.webp', 'chaupal.webp', 'cinematic.webp', 'dts-es.webp', 'dts-hd-hra.webp',
    'dvd-remux.webp', 'fake-hdr.webp', 'full-disc.webp', 'fulldisc.webp', 'hardsub.webp',
    'hd-feed.webp', 'hdrip.webp', 'hfr.webp', 'hls.webp', 'hungama.webp', 'hybrid.webp',
    'internal.webp', 'itunes.webp', 'klikk.webp', 'kurdish.webp', 'latino-flag.webp',
    'limited.webp', 'line-audio.webp', 'live-backup.webp', 'live-hd.webp', 'live-hfr.webp',
    'live-raw.webp', 'live-sd.webp', 'lowres.webp', 'lpcm.webp', 'm2ts.webp',
    'manoramamax.webp', 'mp3.webp', 'mpeg2.webp', 'mpegts.webp', 'msubs.webp',
    'mxplayer.webp', 'open-matte.webp', 'original.webp', 'planetmarathi.webp', 'ppv.webp',
    'proper.webp', 'rabbithole.webp', 'raw.webp', 'region-in.webp', 'region-uk.webp',
    'region-us.webp', 'repack.webp', 'sample.webp', 'sd-feed.webp', 'sdh.webp',
    'season-pack.webp', 'seasonpack.webp', 'shemaroome.webp', 'sonypicturescore.webp',
    'special.webp', 'telecine.webp', 'ts.webp', 'tvrip.webp', 'ullu.webp', 'uncensored.webp',
    'upscaled.webp', 'usenet.webp', 'vc1.webp', 'version.webp', 'vostfr.webp', 'web.webp',
    'welsh-flag.webp'
]

def apply_brand_fixes():
    print("=== APPLYING 4 CLEAN BRAND LOGOS ===")
    for name, info in BRAND_FIXES.items():
        src_p = info["src"]
        if not os.path.exists(src_p):
            print(f"Error: {src_p} does not exist!")
            continue
        glyph = Image.open(src_p).convert("RGBA")
        gw, gh = glyph.size
        cw, ch = info["target_canvas"]
        
        # Scale if glyph height is too large for canvas
        if gh > (ch - 16):
            sc = (ch - 24) / float(gh)
            glyph = glyph.resize((int(gw * sc), int(gh * sc)), Image.Resampling.LANCZOS)
            gw, gh = glyph.size
            
        # Ensure canvas is at least wide enough for glyph + padding
        cw = max(cw, gw + 36)
        
        canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        cx = (cw - gw) // 2
        cy = (ch - gh) // 2
        canvas.paste(glyph, (cx, cy), glyph)
        
        out_p = os.path.join(BADGES_DIR, f"{name}.webp")
        canvas.save(out_p, "WEBP", quality=95, method=6)
        print(f"Saved clean brand badge: {name}.webp -> canvas {canvas.size}, glyph {glyph.size}")

def apply_smoked_fixes():
    print("\n=== CLEANING 86 SMOKED PILL BADGES ===")
    cleaned_count = 0
    for name in SMOKED_BADGES:
        p = os.path.join(BADGES_DIR, name)
        if not os.path.exists(p):
            print(f"Warning: {name} not found in badges dir")
            continue
            
        img = Image.open(p).convert("RGBA")
        arr = np.array(img)
        h, w = arr.shape[:2]
        
        # Crop inner area to completely bypass smoked capsule border
        crop_arr = arr[16:80, 18:w-18].copy()
        
        # Extract high opacity foreground typography / artwork
        fg_mask = (crop_arr[:, :, 3] > 100) & (np.maximum.reduce([crop_arr[:, :, 0], crop_arr[:, :, 1], crop_arr[:, :, 2]]) > 60)
        clean_arr = np.zeros_like(crop_arr)
        clean_arr[fg_mask] = crop_arr[fg_mask]
        
        clean_im = Image.fromarray(clean_arr, mode="RGBA")
        bbox = clean_im.getbbox()
        if not bbox:
            print(f"Error: Empty bbox for {name}")
            continue
            
        glyph = clean_im.crop(bbox)
        gw, gh = glyph.size
        
        # Standard native 96px canvas with 20px padding left & right
        cw = gw + 40
        ch = 96
        canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        canvas.paste(glyph, (20, (ch - gh) // 2), glyph)
        
        canvas.save(p, "WEBP", quality=95, method=6)
        cleaned_count += 1
        
    print(f"Successfully cleaned and saved {cleaned_count} smoked pill badges!")

if __name__ == "__main__":
    apply_brand_fixes()
    apply_smoked_fixes()
