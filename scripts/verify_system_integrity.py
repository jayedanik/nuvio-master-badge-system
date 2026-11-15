import hashlib, os, sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK_FILE = os.path.join(REPO_ROOT, "SYSTEM_INTEGRITY.lock")

def get_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def verify():
    if not os.path.exists(LOCK_FILE):
        print(f"[FAIL] Missing lock file: {LOCK_FILE}")
        sys.exit(1)
        
    failures = []
    checked = 0
    with open(LOCK_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("  ", 1)
            if len(parts) != 2:
                continue
            expected_hash, rel_path = parts
            full_path = os.path.join(REPO_ROOT, rel_path)
            if not os.path.exists(full_path):
                failures.append(f"MISSING: {rel_path}")
                continue
            actual_hash = get_hash(full_path)
            if actual_hash != expected_hash:
                failures.append(f"MODIFIED: {rel_path} (expected {expected_hash[:10]}..., got {actual_hash[:10]}...)")
            checked += 1

    if failures:
        print(f"[FAIL] System integrity verification failed! {len(failures)} violations detected:")
        for fail in failures:
            print(f"  - {fail}")
        sys.exit(1)
    else:
        print(f"[SUCCESS] System Integrity 100% Verified! All {checked} locked artifacts match their immutable SHA-256 signatures.")
        sys.exit(0)

if __name__ == "__main__":
    verify()
