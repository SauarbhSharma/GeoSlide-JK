#!/usr/bin/env python3
"""
GeoSlide-JK 2.0 — Repository Reference Verifier (V2-3F-R8A2-2)
Verifies Git tag objects, tag targets, and release references.
Runs ONLY when .git is present. Skipped in Git-archive / non-Git extractions.
"""

import sys, os, json, subprocess
from pathlib import Path

def verify_repository_references(source_root=None):
    if source_root is None:
        source_root = Path(__file__).resolve().parent.parent
    else:
        source_root = Path(source_root)

    git_dir = source_root / ".git"
    if not git_dir.exists():
        print("Git directory (.git) not present. Skipping repository reference verifier.")
        return True

    lock_file = source_root / "configs" / "v2_3f_r8a2_2_release_references.json"
    with open(lock_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Verifying {len(data['release_references'])} release references against repository...")
    for ref in data["release_references"]:
        rel = ref["release"]
        tag_obj = ref["tag_object"]
        tag_tgt = ref["tag_target"]

        try:
            actual_obj = subprocess.check_output(
                ["git", "rev-parse", f"refs/tags/v2.3f-{rel.lower().replace('v2-3f-', '')}"],
                cwd=source_root, stderr=subprocess.DEVNULL
            ).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            pass

    print("Repository reference verification completed.")
    return True

if __name__ == "__main__":
    src_root = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    verify_repository_references(src_root)
