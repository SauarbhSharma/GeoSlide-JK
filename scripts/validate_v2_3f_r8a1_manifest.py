#!/usr/bin/env python3
"""
GeoSlide-JK 2.0 — V2-3F-R8A1 Manifest Validator Script
Validates outputs/reports/v2_3f_r8_output_hashes.csv against Git blobs.
Verifies format, completeness, ordering, byte counts, and SHA-256 digests.
"""

import sys, subprocess, hashlib, re
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def validate_manifest(commit_ref="HEAD"):
    pattern_64 = re.compile(r"^[0-9a-f]{64}$")
    manifest_path = PROJECT_ROOT / "outputs" / "reports" / "v2_3f_r8_output_hashes.csv"

    if not manifest_path.exists():
        print(f"FAIL: Manifest path does not exist: {manifest_path}")
        return False

    df_manifest = pd.read_csv(manifest_path)
    
    # 1. No self-inclusion
    if "outputs/reports/v2_3f_r8_output_hashes.csv" in df_manifest["file_path"].values:
        print("FAIL: Manifest self-inclusion detected!")
        return False

    # 2. Lexical ordering check
    paths = df_manifest["file_path"].tolist()
    if paths != sorted(paths):
        print("FAIL: Manifest entries are not lexically sorted!")
        return False

    # 3. Unique paths check
    if len(paths) != len(set(paths)):
        print("FAIL: Duplicate file_path detected in manifest!")
        return False

    # 4. Git blob verification for every entry
    for _, r in df_manifest.iterrows():
        posix_path = r["file_path"]
        digest = str(r["sha256"]).strip()
        size_bytes = int(r["file_size_bytes"])

        # Check 64-char hex format
        if not pattern_64.match(digest):
            print(f"FAIL: Digest not 64-char lowercase hex for {posix_path}: {digest}")
            return False

        # Absolute path check
        if posix_path.startswith("/") or ":" in posix_path:
            print(f"FAIL: Absolute or machine path detected: {posix_path}")
            return False

        # Read Git blob
        try:
            blob_bytes = subprocess.check_output(
                ["git", "cat-file", "blob", f"{commit_ref}:{posix_path}"],
                cwd=PROJECT_ROOT
            )
        except Exception as e:
            print(f"FAIL: Unable to read Git blob for {posix_path} at commit {commit_ref}: {e}")
            return False

        real_sha = hashlib.sha256(blob_bytes).hexdigest()
        if digest != real_sha:
            print(f"FAIL: SHA mismatch for {posix_path}: manifest={digest}, actual={real_sha}")
            return False

        if size_bytes != len(blob_bytes):
            print(f"FAIL: Size mismatch for {posix_path}: manifest={size_bytes}, actual={len(blob_bytes)}")
            return False

    # 5. Check closure completeness against git diff-tree
    changed_files = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "2685a8521f8b0ba106bf993791b13630e55f3a35", commit_ref],
        cwd=PROJECT_ROOT
    ).decode("utf-8").strip().splitlines()

    expected_set = set(f.replace("\\", "/") for f in changed_files if f.replace("\\", "/") != "outputs/reports/v2_3f_r8_output_hashes.csv")
    manifest_set = set(paths)

    missing = expected_set - manifest_set
    if missing:
        print(f"FAIL: Changed files missing from manifest: {missing}")
        return False

    print(f"PASS: Manifest validation successful for commit {commit_ref} ({len(df_manifest)} covered files).")
    return True

if __name__ == "__main__":
    target_ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    success = validate_manifest(target_ref)
    sys.exit(0 if success else 1)
