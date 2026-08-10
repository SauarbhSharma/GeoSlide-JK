#!/usr/bin/env python3
"""
GeoSlide-JK 2.0 — V2-3F-R8A1 Manifest Generator Script
Generates outputs/reports/v2_3f_r8_output_hashes.csv from Git blobs of target commit.
Includes every covered file except the manifest itself.
"""

import sys, subprocess, hashlib, re
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def classify_path(p):
    if p in ["outputs/reports/v2_3f_r5_output_hashes.csv", "outputs/reports/v2_3f_r6_output_hashes.csv"]:
        return "CHANGED_FILE"
    elif p.startswith("outputs/reports/"):
        return "CANONICAL_OUTPUT"
    elif p.startswith("scripts/"):
        return "GENERATOR"
    elif p.startswith("tests/"):
        return "TEST"
    elif p.startswith("docs/"):
        return "DOCUMENTATION"
    elif p.startswith("configs/") or p in [".gitattributes", "requirements.txt", "apps/web/app/corridor/page.tsx"]:
        return "UI_OR_CONFIGURATION"
    else:
        return "REPRODUCTION_DEPENDENCY"

def generate_manifest(commit_ref="HEAD"):
    pattern_64 = re.compile(r"^[0-9a-f]{64}$")
    
    # List all changed files relative to main
    changed_files = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "2685a8521f8b0ba106bf993791b13630e55f3a35", commit_ref],
        cwd=PROJECT_ROOT
    ).decode("utf-8").strip().splitlines()

    entries = []
    for rel_path in sorted(changed_files):
        posix_path = rel_path.replace("\\", "/")
        if posix_path == "outputs/reports/v2_3f_r8_output_hashes.csv":
            continue
            
        try:
            blob_bytes = subprocess.check_output(
                ["git", "cat-file", "blob", f"{commit_ref}:{posix_path}"],
                cwd=PROJECT_ROOT
            )
        except Exception:
            fpath = PROJECT_ROOT / posix_path
            with open(fpath, "rb") as fh:
                blob_bytes = fh.read()

        digest = hashlib.sha256(blob_bytes).hexdigest()
        assert pattern_64.match(digest), f"Invalid 64-hex SHA-256 digest: {digest}"
        size_bytes = len(blob_bytes)
        
        alias = posix_path.replace("/", "_").replace(".", "_")
        classification = classify_path(posix_path)
        
        entries.append({
            "artifact_alias": alias,
            "file_path": posix_path,
            "sha256": digest,
            "file_size_bytes": size_bytes,
            "classification": classification
        })

    df_manifest = pd.DataFrame(entries).sort_values("file_path")
    out_csv = PROJECT_ROOT / "outputs" / "reports" / "v2_3f_r8_output_hashes.csv"
    df_manifest.to_csv(out_csv, index=False, lineterminator="\n")
    print(f"Generated R8A1 Manifest at {out_csv} with {len(df_manifest)} entries.")
    return out_csv

if __name__ == "__main__":
    target_ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    generate_manifest(target_ref)
