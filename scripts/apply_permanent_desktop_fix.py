import os, json, glob
from PIL import Image
import numpy as np

REPO_ROOT = r'C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original'
TARGET_SAFE_MARGIN = 18

print('=== STEP 1: Updating all JSON manifests for zero black box/border ===')

manifest_files = glob.glob(os.path.join(REPO_ROOT, '*.json')) + glob.glob(os.path.join(REPO_ROOT, 'themes', '*', '*.json'))
# Exclude design rules
manifest_files = [f for f in manifest_files if not f.endswith('DESIGN_SYSTEM_RULES.json') and not f.endswith('package.json')]

updated_manifests = 0
for mpath in manifest_files:
    try:
        with open(mpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        changed = False
        if 'filters' in data:
            for filt in data['filters']:
                if filt.get('tagStyle') != 'none' or filt.get('borderColor') != '' or filt.get('tagColor') != '':
                    filt['tagStyle'] = 'none'
                    filt['tagColor'] = ''
                    filt['borderColor'] = ''
                    changed = True
        
        if changed:
            with open(mpath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            updated_manifests += 1
            print(f'  Updated manifest: {os.path.relpath(mpath, REPO_ROOT)}')
    except Exception as e:
        print(f'  Error updating {mpath}: {e}')

print(f'Total manifests updated: {updated_manifests}')

print('\n=== STEP 2: Applying 18px horizontal safe padding to all badges across all themes ===')

# Directories to scan
badge_dirs = [os.path.join(REPO_ROOT, 'badges')]
for tdir in os.listdir(os.path.join(REPO_ROOT, 'themes')):
    p = os.path.join(REPO_ROOT, 'themes', tdir, 'badges')
    if os.path.isdir(p):
        badge_dirs.append(p)

total_processed = 0
total_padded = 0

for bdir in badge_dirs:
    rel_dir = os.path.relpath(bdir, REPO_ROOT)
    dir_padded = 0
    dir_total = 0
    for fname in os.listdir(bdir):
        if not fname.endswith('.webp'):
            continue
        
        fpath = os.path.join(bdir, fname)
        try:
            im = Image.open(fpath)
            arr = np.array(im)
            if arr.ndim != 3 or arr.shape[2] != 4:
                continue
            
            alpha = arr[:, :, 3]
            nz = np.argwhere(alpha > 10)
            if len(nz) == 0:
                continue
            
            ymin, xmin = nz.min(axis=0)
            ymax, xmax = nz.max(axis=0)
            lm = xmin
            rm = im.width - 1 - xmax
            
            pad_l = max(0, TARGET_SAFE_MARGIN - lm)
            pad_r = max(0, TARGET_SAFE_MARGIN - rm)
            
            dir_total += 1
            total_processed += 1
            
            if pad_l > 0 or pad_r > 0:
                new_w = im.width + pad_l + pad_r
                new_im = Image.new('RGBA', (new_w, im.height), (0, 0, 0, 0))
                new_im.paste(im, (pad_l, 0))
                new_im.save(fpath, format='WEBP', quality=95, method=4)
                dir_padded += 1
                total_padded += 1
        except Exception as e:
            print(f'Error processing {fpath}: {e}')
    
    print(f'  {rel_dir}: padded {dir_padded}/{dir_total} badges to >= {TARGET_SAFE_MARGIN}px safe margin')

print(f'\nTotal badges evaluated: {total_processed}, Total padded: {total_padded}')
