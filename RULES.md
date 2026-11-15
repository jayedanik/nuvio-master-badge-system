# Nuvio Design System & Theme Engine Rules (v4.0.0-LOCKED)

> **Official Design Architecture & Automatic Theme Synchronization Standard**  
> Every badge, logo, preview, and theme in this repository adheres to these immutable rules.

---

## 1. Core Invariants (কখনোই ভাঙা যাবে না)

1. **Canvas Height Standard:**
   - Every badge in every theme has an exact height of **`96px`** (`CANVAS_H = 96`).
   - High-resolution rendering must use **4x supersampling** (`384px` canvas rendered and downscaled with `LANCZOS`).
2. **100% Alpha Transparency & Zero-Border Manifest:**
   - Zero solid black cards, zero artificial pill borders, and zero smoked capsules.
   - All assets are transparent WebP (`#00000000`).
   - Every manifest `.json` must set `"tagStyle": "none"`, `"tagColor": ""`, and `"borderColor": ""` to prevent Nuvio Desktop from drawing hardware outline boxes.
3. **18px Horizontal Safe Margin (Anti-Crop Standard):**
   - Every badge must maintain a minimum of **`18px`** transparent margin on left and right (`pad_left >= 18px`, `pad_right >= 18px`).
   - Prevents Nuvio Desktop's `RoundedCornerShape` clip from slicing outer letters or icons on player stream chips.
4. **Locked Masterpiece Showcases:**
   - `previews/theme-ecosystem.jpg` (2400x969px) is strictly locked to the 5-Tier Nothing Dot Matrix Architecture.
   - `previews/preview-washi-tape.jpg` (2400x1349px) is strictly locked to the Dark Emerald Frieren Showcase with dual 3D shadows and 60px elevated logos.
   - Verified via `SYSTEM_INTEGRITY.lock`.

---

## 2. Typography Standard by Theme (১৩টি থিমের ফন্ট রুলস)

| Theme ID | Theme Name | Primary Font | Secondary / Subtext Font | Visual Aesthetic |
|---|---|---|---|---|
| `pristine` | Pristine Master | `Arial Bold` / `Segoe UI Bold` | `Segoe UI` | Clean OLED Floating Vector Sans |
| `studio-markers` | StreamBridge Studio Markers Enhanced | `Bahnschrift` | `Bahnschrift` | Condensed Technical Studio Monitor Marker |
| `gmk-keycaps` | GMK Custom Keycaps | `Bahnschrift` | `Bahnschrift` | Double-shot PBT Cherry Profile DIN Standard |
| `rgb-keycaps` | Cyberpunk RGB Keycaps | `Bahnschrift` | `Bahnschrift` | Translucent Pudding Keycaps with Neon RGB Underglow |
| `cinema-ticket` | Golden Age Cinema Ticket | `Impact` | `Times Bold` | Vintage Perforated Admission Ticket Stub |
| `enamel-pins` | Cloisonné Enamel Pins | `Cinzel-Bold` | `Times Bold` | Jewelry Cast Brass Bezel with Roman Engraving |
| `vhs-tape` | Retro VHS Magnetic Tape | `Impact` | `Impact` | Aged Paper Cassette Label with Rainbow Stripes |
| `clapperboard` | Hollywood Clapperboard | `Impact` | `Bahnschrift` | Matte Slate Slate with Sound-Sync Chevrons |
| `audiophile-vfd` | Audiophile Vacuum Fluorescent | `Consolas Bold` | `Consolas Bold` | Cyan Phosphor Vacuum Tube Monospace |
| `neotokyo-tag` | NeoTokyo Cyberpunk Asset Tag | `Bahnschrift` | `Bahnschrift` | Weathered Industrial Machinery Tag Stencil |
| `criterion-leather` | Criterion Archival Leather | `CinzelDecorative-Bold` | `Times Bold` | Gilded Moroccan Leather with Debossed Gold Leaf |
| `liquid-glass` | Apple VisionOS Liquid Glass | `Outfit` | `Inter` | Pure Translucent Liquid Droplet with Caustic Rims |
| `washi-tape` | Artisan Japanese Washi Tape | `Cinzel-Bold` | `MS Gothic` | Handmade Mulberry Rolls with 3D Drop Shadows |

---

## 3. Universal Unicode Font Fallbacks (কোনো ল্যাঙ্গুয়েজ এরর নয়)

All text generators use the universal fallback hierarchy to prevent `OSError: cannot open resource` or glyph tofu boxes:
- **Japanese (Hiragana / Katakana):** `YuGothB.ttc` &rarr; `msgothic.ttc` &rarr; `msyh.ttc`
- **Chinese (CJK):** `msyh.ttc` &rarr; `simsun.ttc`
- **Korean (Hangul):** `malgun.ttf` &rarr; `malgunbd.ttf`
- **Indic & South Asian (Bengali, Hindi, Tamil, Telugu, Odia, Sinhala, etc.):** `Nirmala.ttc`
- **Southeast Asian (Thai, Lao, Khmer):** `LeelaUIb.ttf` &rarr; `LeelawUI.ttf` &rarr; `tahoma.ttf`
- **Myanmar (Burmese):** `mmrtext.ttf`
- **Caucasian (Georgian, Armenian):** `sylfaen.ttf`
- **Ethiopic / Amharic:** `ebrima.ttf` &rarr; `seguiemj.ttf`
- **Middle Eastern (Arabic, Persian, Urdu, Pashto):** `tahoma.ttf`
- **Hebrew:** `arialbd.ttf` &rarr; `segoeui.ttf`

---

## 4. How to Automatically Apply Rules

### Adding a New Badge or Logo
To add a new badge across **all 13 themes** automatically adhering to all typography and material rules:

```bash
# Brand or streaming logo:
python scripts/auto_apply_rules.py add-badge --id crunchyroll --src path/to/logo.png --category streaming

# Video tech or language badge:
python scripts/auto_apply_rules.py add-badge --id prores --main-text "PRORES" --sub-text "422 HQ" --category tech
```

This single command automatically:
1. Validates and cleans alpha transparency (strips black cards).
2. Generates the 96px base badge in `badges/`.
3. Renders across all 9 physical themes with authentic theme typography.
4. Generates the refractive capsule for Liquid Glass.
5. Generates the fibrous deckled roll with 3D elevation shadow for Washi Tape.
6. Synchronizes `badges.json` and all 13 theme `.json` files.

---

### Creating a New Theme
To create a new theme that automatically inherits all baseline badges:

```bash
python scripts/auto_apply_rules.py create-theme \
  --id cyber-matrix \
  --name "Cyber Matrix Terminal" \
  --primary-font "consolab.ttf" \
  --secondary-font "consolab.ttf" \
  --style "Green Phosphor CRT terminal screen with scanlines" \
  --accent "#22c55e"
```

---

## 5. System Integrity Verification

Run anytime to verify all 94 master artifacts remain 100% byte-for-byte untampered:

```bash
python scripts/verify_system_integrity.py
```
