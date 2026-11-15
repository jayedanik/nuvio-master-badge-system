import os, sys

REPO_ROOT = r"C:\Users\yourt\.gemini\antigravity\scratch\nuvio-badges-original"
sys.path.append(os.path.join(REPO_ROOT, "scripts"))
from render_nothing_masterpiece import render_html_preview, THEME_CONFIGS

def main():
    print("==================================================================")
    print("UPDATING ALL 13 GITHUB THEME PREVIEW BANNERS (KEEPING EXACT DESIGNS)")
    print("==================================================================")
    
    for cfg in THEME_CONFIGS:
        tid = cfg["id"]
        print(f"--> Rendering razor-sharp preview for {tid}...")
        render_html_preview(cfg)
        
    print("[SUCCESS] All 13 preview banners updated with latest badges.")

if __name__ == "__main__":
    main()
