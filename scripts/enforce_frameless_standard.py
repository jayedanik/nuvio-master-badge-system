#!/usr/bin/env python3
"""
StreamBridge Frameless Standard Enforcer & Guardrail Watchdog
============================================================
Enforces 100% borderless, transparent rendering across all themes and badges.
Standard:
  - tagStyle: "filled"
  - tagColor: "#00000000" (transparent)
  - borderColor: "#00000000" (transparent)
  - textColor: "#FFFFFF"
  - group.borderColor: "#00000000"
  - Locked previews: previews/preview-washi-tape.jpg, previews/theme-ecosystem.jpg
"""

import os, sys, json, glob, argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCKED_PREVIEWS = [
    os.path.join(REPO_ROOT, "previews", "preview-washi-tape.jpg"),
    os.path.join(REPO_ROOT, "previews", "theme-ecosystem.jpg")
]

def find_all_theme_jsons():
    files = glob.glob(os.path.join(REPO_ROOT, "*.json"))
    files += glob.glob(os.path.join(REPO_ROOT, "themes", "*", "*.json"))
    # Filter out system config files
    ignored = {"DESIGN_SYSTEM_RULES.json", "package.json", "package-lock.json", "tsconfig.json"}
    return [f for f in sorted(files) if os.path.basename(f) not in ignored]

def audit_and_enforce(fix=True):
    json_files = find_all_theme_jsons()
    total_filters = 0
    total_fixed_filters = 0
    total_files_fixed = 0
    violations = []

    print(f"[AUDIT] Scanning {len(json_files)} theme manifest JSONs...")
    
    for fpath in json_files:
        rel_path = os.path.relpath(fpath, REPO_ROOT)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            violations.append(f"{rel_path}: JSON decode error: {e}")
            continue

        changed = False
        filters = data.get("filters", [])
        groups = data.get("groups", [])
        
        file_fixed_count = 0
        for filt in filters:
            total_filters += 1
            needs_fix = (
                filt.get("tagStyle") != "filled" or
                filt.get("tagColor") != "#00000000" or
                filt.get("borderColor") != "#00000000" or
                filt.get("textColor") != "#FFFFFF"
            )
            if needs_fix:
                if fix:
                    filt["tagStyle"] = "filled"
                    filt["tagColor"] = "#00000000"
                    filt["borderColor"] = "#00000000"
                    filt["textColor"] = "#FFFFFF"
                    changed = True
                    file_fixed_count += 1
                else:
                    violations.append(f"{rel_path}: filter '{filt.get('id', 'unknown')}' does not follow frameless standard")

        # Also verify groups have transparent border
        for grp in groups:
            if grp.get("borderColor") != "#00000000":
                if fix:
                    grp["borderColor"] = "#00000000"
                    changed = True
                else:
                    violations.append(f"{rel_path}: group '{grp.get('id')}' borderColor is not #00000000")

        if changed and fix:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            total_files_fixed += 1
            total_fixed_filters += file_fixed_count
            print(f"  [FIXED] {rel_path} ({file_fixed_count} filters updated to frameless)")

    # Verify locked previews exist
    for p in LOCKED_PREVIEWS:
        if not os.path.exists(p):
            violations.append(f"CRITICAL: Locked preview missing: {os.path.relpath(p, REPO_ROOT)}")

    print(f"\n[SUMMARY] Evaluated {total_filters} filters across {len(json_files)} manifests.")
    if fix:
        print(f"[RESULT] Successfully enforced frameless standard. Files modified: {total_files_fixed}, Filters fixed: {total_fixed_filters}.")
        return 0
    else:
        if violations:
            print(f"[FAIL] Detected {len(violations)} frameless standard violations:")
            for v in violations[:20]:
                print(f"  - {v}")
            return 1
        else:
            print("[PASS] 100% of theme manifests comply with StreamBridge Frameless Standard!")
            return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enforce StreamBridge Frameless Standard")
    parser.add_argument("--check", action="store_true", help="Audit only without making changes")
    args = parser.parse_args()
    
    code = audit_and_enforce(fix=not args.check)
    sys.exit(code)
