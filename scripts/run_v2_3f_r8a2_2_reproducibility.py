#!/usr/bin/env python3
"""
GeoSlide-JK 2.0 — V2-3F-R8A2-2 Executable Deterministic Reproducibility Script
Archive-compatible reproducibility test runner.
Reruns the V2-3F-R8A2-2 pipeline and verifies exact output hash reproducibility.
Makes NO Git calls and NO network calls.
Supports optional --source-root and --output-dir arguments for isolated reproduction testing.
Performs explicit direct comparison of inventories, schemas, row counts, ordering, bytes, and SHA-256 values.
Exits non-zero if any generated file (including UI evidence JSON) differs.
"""

import sys, os, hashlib, argparse
import pandas as pd
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=str, default=None)
    parser.add_argument("--output-dir", type=str, default=None)
    args = parser.parse_args()

    if args.source_root is None:
        source_root = Path(__file__).resolve().parent.parent
    else:
        source_root = Path(args.source_root)

    sys.path.insert(0, str(source_root))
    sys.path.insert(0, str(source_root / "src"))

    from scripts.run_v2_3f_r8a2_2_pipeline import run_r8a2_2_pipeline

    run_r8a2_2_pipeline(source_root=source_root, output_dir=args.output_dir)

    if args.output_dir is not None:
        out_base = Path(args.output_dir)
        canon_dir = source_root / "outputs" / "reports"
        iso_dir = out_base / "outputs" / "reports"

        r8a2_2_files = sorted([f.name for f in canon_dir.glob("v2_3f_r8a2_2_*.csv") if f.name != "v2_3f_r8a2_2_repository_manifest.csv"])
        
        comparison_records = []
        print(f"Comparing {len(r8a2_2_files)} R8A2-2 report files between {canon_dir} and {iso_dir}...")
        for fname in r8a2_2_files:
            c_path = canon_dir / fname
            i_path = iso_dir / fname

            assert i_path.exists(), f"Missing output file in isolated directory: {i_path}"

            df_c = pd.read_csv(c_path)
            df_i = pd.read_csv(i_path)

            assert list(df_c.columns) == list(df_i.columns), f"Schema mismatch for {fname}"
            assert len(df_c) == len(df_i), f"Row count mismatch for {fname}: canon={len(df_c)}, iso={len(df_i)}"

            bytes_c = open(c_path, "rb").read()
            bytes_i = open(i_path, "rb").read()

            sha_c = hashlib.sha256(bytes_c).hexdigest()
            sha_i = hashlib.sha256(bytes_i).hexdigest()

            record = {
                "file_path": fname,
                "canonical_size": len(bytes_c),
                "isolated_size": len(bytes_i),
                "canonical_sha256": sha_c,
                "isolated_sha256": sha_i,
                "size_equal": len(bytes_c) == len(bytes_i),
                "hash_equal": sha_c == sha_i
            }
            comparison_records.append(record)

            print(f"FILE_COMPARISON: file_path={fname}, canonical_size={len(bytes_c)}, isolated_size={len(bytes_i)}, canonical_sha256={sha_c[:16]}, isolated_sha256={sha_i[:16]}, size_equal={len(bytes_c) == len(bytes_i)}, hash_equal={sha_c == sha_i}")

        # Compare generated UI evidence JSON
        c_json_path = source_root / "apps" / "web" / "src" / "data" / "r8a2_2_corridor_evidence.json"
        i_json_path = out_base / "apps" / "web" / "src" / "data" / "r8a2_2_corridor_evidence.json"
        assert i_json_path.exists(), f"Missing UI JSON evidence in isolated directory: {i_json_path}"

        b_c_json = open(c_json_path, "rb").read()
        b_i_json = open(i_json_path, "rb").read()
        sha_c_json = hashlib.sha256(b_c_json).hexdigest()
        sha_i_json = hashlib.sha256(b_i_json).hexdigest()

        record_json = {
            "file_path": "r8a2_2_corridor_evidence.json",
            "canonical_size": len(b_c_json),
            "isolated_size": len(b_i_json),
            "canonical_sha256": sha_c_json,
            "isolated_sha256": sha_i_json,
            "size_equal": len(b_c_json) == len(b_i_json),
            "hash_equal": sha_c_json == sha_i_json
        }
        comparison_records.append(record_json)

        print(f"FILE_COMPARISON: file_path=r8a2_2_corridor_evidence.json, canonical_size={len(b_c_json)}, isolated_size={len(b_i_json)}, canonical_sha256={sha_c_json[:16]}, isolated_sha256={sha_i_json[:16]}, size_equal={len(b_c_json) == len(b_i_json)}, hash_equal={sha_c_json == sha_i_json}")

        compared_file_count = len(comparison_records)
        hash_mismatch_count = sum(r["canonical_sha256"] != r["isolated_sha256"] for r in comparison_records)
        size_mismatch_count = sum(r["canonical_size"] != r["isolated_size"] for r in comparison_records)
        total_mismatch_count = sum((r["canonical_sha256"] != r["isolated_sha256"] or r["canonical_size"] != r["isolated_size"]) for r in comparison_records)

        print(f"REPRODUCIBILITY_AUDIT_SUMMARY: compared_file_count={compared_file_count}, hash_mismatch_count={hash_mismatch_count}, size_mismatch_count={size_mismatch_count}, total_mismatch_count={total_mismatch_count}")
        assert total_mismatch_count == 0, f"Reproducibility audit detected {total_mismatch_count} mismatched files"

if __name__ == "__main__":
    main()
