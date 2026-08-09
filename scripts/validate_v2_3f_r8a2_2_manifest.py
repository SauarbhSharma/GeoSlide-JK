#!/usr/bin/env python3
"""
GeoSlide-JK 2.0 — R8A2-2 Repository Manifest Validator
Strictly validates outputs/reports/v2_3f_r8a2_2_repository_manifest.csv against target_commit.
Rejects non-hex, leading/trailing whitespace, missing/duplicate paths, CRLF, and non-lexical ordering.
"""

import sys, os, hashlib, subprocess, re
import pandas as pd
from pathlib import Path

HEX_64_REGEX = re.compile(r"^[0-9a-f]{64}$")

def validate_r8a2_2_manifest(target_commit, manifest_csv_path=None, source_root=None):
    if source_root is None:
        source_root = Path(__file__).resolve().parent.parent
    else:
        source_root = Path(source_root)

    if manifest_csv_path is None:
        manifest_csv_path = source_root / "outputs" / "reports" / "v2_3f_r8a2_2_repository_manifest.csv"

    if not manifest_csv_path.exists():
        print(f"FAIL: Manifest CSV does not exist at {manifest_csv_path}")
        return False

    with open(manifest_csv_path, "rb") as f:
        manifest_bytes = f.read()

    if b"\r\n" in manifest_bytes:
        print("FAIL: Manifest CSV contains Windows CRLF line endings! Must be LF.")
        return False

    df_man = pd.read_csv(manifest_csv_path)

    required_cols = ["artifact_alias", "file_path", "sha256", "file_size_bytes", "classification"]
    if list(df_man.columns) != required_cols:
        print(f"FAIL: Manifest columns mismatch. Expected {required_cols}, got {list(df_man.columns)}")
        return False

    paths = df_man["file_path"].tolist()
    if paths != sorted(paths):
        print("FAIL: Manifest file paths are not sorted in strict POSIX lexical order!")
        return False

    if len(paths) != len(set(paths)):
        print("FAIL: Duplicate file paths found in manifest!")
        return False

    manifest_rel_path = "outputs/reports/v2_3f_r8a2_2_repository_manifest.csv"
    if manifest_rel_path in paths:
        print(f"FAIL: Manifest file self-included in manifest: {manifest_rel_path}")
        return False

    manifest_entry_count = len(df_man)
    checked_entry_count = 0
    missing_entry_count = 0
    hash_mismatch_count = 0
    size_mismatch_count = 0
    total_discrepancy_count = 0

    for idx, row in df_man.iterrows():
        checked_entry_count += 1
        fpath = str(row["file_path"])
        digest = str(row["sha256"])
        size_reported = int(row["file_size_bytes"])

        if "\\" in fpath:
            print(f"MANIFEST_ENTRY_DISCREPANCY: Backslash in file_path at row {idx}: {fpath}")
            total_discrepancy_count += 1
            continue

        if not HEX_64_REGEX.match(digest):
            print(f"MANIFEST_ENTRY_DISCREPANCY: SHA-256 digest at row {idx} fails strict 64-hex regex: '{digest}'")
            total_discrepancy_count += 1
            continue

        try:
            content_bytes = subprocess.check_output(
                ["git", "cat-file", "-p", f"{target_commit}:{fpath}"],
                cwd=source_root, stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            missing_entry_count += 1
            total_discrepancy_count += 1
            print(f"MANIFEST_ENTRY_DISCREPANCY: File path {fpath} does not exist in commit {target_commit}")
            continue

        actual_sha = hashlib.sha256(content_bytes).hexdigest()
        actual_size = len(content_bytes)

        if digest != actual_sha:
            hash_mismatch_count += 1
            total_discrepancy_count += 1
            print(f"MANIFEST_ENTRY_DISCREPANCY: SHA-256 mismatch for {fpath}: reported={digest}, actual={actual_sha}")

        if size_reported != actual_size:
            size_mismatch_count += 1
            total_discrepancy_count += 1
            print(f"MANIFEST_ENTRY_DISCREPANCY: Size mismatch for {fpath}: reported={size_reported}, actual={actual_size}")

    is_valid = (total_discrepancy_count == 0)
    print(f"MANIFEST_VALIDATION_SUMMARY: target_commit={target_commit}, manifest_entry_count={manifest_entry_count}, checked_entry_count={checked_entry_count}, missing_entry_count={missing_entry_count}, hash_mismatch_count={hash_mismatch_count}, size_mismatch_count={size_mismatch_count}, total_discrepancy_count={total_discrepancy_count}")
    return is_valid

if __name__ == "__main__":
    tgt_commit = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    man_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    src_root = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    is_valid = validate_r8a2_2_manifest(tgt_commit, man_path, src_root)
    sys.exit(0 if is_valid else 1)

