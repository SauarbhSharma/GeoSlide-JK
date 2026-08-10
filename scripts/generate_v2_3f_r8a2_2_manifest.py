#!/usr/bin/env python3
"""
GeoSlide-JK 2.0 — R8A2-2 Repository Manifest Generator
Enumerates 100% of tracked Git blobs in the target artifact commit using git ls-tree -r -z.
Explicitly excludes outputs/reports/v2_3f_r8a2_2_repository_manifest.csv.
"""

import sys, os, hashlib, subprocess, re
import pandas as pd
from pathlib import Path

def generate_r8a2_2_manifest(target_commit, output_manifest_path=None, source_root=None):
    if source_root is None:
        source_root = Path(__file__).resolve().parent.parent
    else:
        source_root = Path(source_root)

    if output_manifest_path is None:
        output_manifest_path = source_root / "outputs" / "reports" / "v2_3f_r8a2_2_repository_manifest.csv"

    # Enumerate all tracked blobs in target_commit using git ls-tree -r -z
    raw_tree = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", target_commit],
        cwd=source_root
    )

    entries = raw_tree.split(b"\x00")
    manifest_rows = []

    manifest_rel_path = "outputs/reports/v2_3f_r8a2_2_repository_manifest.csv"

    for entry in entries:
        if not entry:
            continue

        parts = entry.decode("utf-8", errors="surrogateescape").split("\t")
        if len(parts) != 2:
            continue

        meta_part, rel_path = parts[0], parts[1]
        mode, entry_type, blob_sha = meta_part.split(" ")

        if rel_path == manifest_rel_path:
            continue

        assert entry_type == "blob", f"Non-blob entry detected in tree: {rel_path} ({entry_type})"

        # Retrieve exact content bytes of blob from target_commit
        content_bytes = subprocess.check_output(
            ["git", "cat-file", "-p", f"{target_commit}:{rel_path}"],
            cwd=source_root
        )

        ext_sha256 = hashlib.sha256(content_bytes).hexdigest()
        file_size = len(content_bytes)

        if rel_path.startswith("outputs/reports/"):
            classification = "CANONICAL_OUTPUT"
        elif rel_path.startswith("configs/"):
            classification = "CONFIGURATION"
        elif rel_path.startswith("src/"):
            classification = "SOURCE_CODE"
        elif rel_path.startswith("scripts/"):
            classification = "BUILD_SCRIPT"
        elif rel_path.startswith("tests/"):
            classification = "TEST_SUITE"
        elif rel_path.startswith("docs/"):
            classification = "DOCUMENTATION"
        elif rel_path.startswith("apps/"):
            classification = "WEB_APPLICATION"
        else:
            classification = "DATA_OR_RESOURCE"

        alias = rel_path.replace("/", "_").replace(".", "_")

        manifest_rows.append({
            "artifact_alias": alias,
            "file_path": rel_path,
            "sha256": ext_sha256,
            "file_size_bytes": file_size,
            "classification": classification
        })

    df_man = pd.DataFrame(manifest_rows).sort_values("file_path")
    
    output_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    df_man.to_csv(output_manifest_path, index=False, lineterminator="\n")

    print(f"Generated R8A2-2 Manifest at {output_manifest_path} with {len(df_man)} entries (out of {len(entries)-1} eligible blobs).")
    return len(df_man)

if __name__ == "__main__":
    tgt_commit = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    src_root = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    generate_r8a2_2_manifest(tgt_commit, out_path, src_root)
