#!/usr/bin/env python3
"""
GeoSlide-JK 2.0 — Tracked UI Evidence Exporter (V2-3F-R8A2-2)
Deterministically exports R8A2-2 native cell mappings and segment evidence into:
apps/web/src/data/r8a2_2_corridor_evidence.json

Works inside Git archive without .git, makes no network calls, and performs no magic fallback.
Supports optional --source-root and --output-dir arguments for isolated reproduction testing.
Exits nonzero if the generated JSON differs from the committed artifact when --output-dir comparison is run.
"""

import sys, os, json, hashlib, argparse
import pandas as pd
from pathlib import Path

def export_r8a2_2_ui_evidence(source_root=None, output_dir=None, compare_existing=False):
    if source_root is None:
        source_root = Path(__file__).resolve().parent.parent
    else:
        source_root = Path(source_root)

    if output_dir is None:
        out_json_path = source_root / "apps" / "web" / "src" / "data" / "r8a2_2_corridor_evidence.json"
    else:
        out_base = Path(output_dir)
        out_json_path = out_base / "apps" / "web" / "src" / "data" / "r8a2_2_corridor_evidence.json"

    if compare_existing:
        if not out_json_path.exists():
            raise FileNotFoundError(f"EXPORT_REFERENCE_NOT_FOUND: Reference evidence JSON does not exist at {out_json_path} for comparison mode.")

    if output_dir is None:
        reports_dir = source_root / "outputs" / "reports"
    else:
        out_base = Path(output_dir)
        reports_dir = out_base / "outputs" / "reports" if (out_base / "outputs" / "reports").exists() else source_root / "outputs" / "reports"

    seg_inv_path = source_root / "outputs" / "reports" / "v2_3a_final_segment_inventory.csv"
    map_path = reports_dir / "v2_3f_r8a2_2_segment_native_cell_mapping.csv"
    cell_path = reports_dir / "v2_3f_r8a2_2_native_cell_evidence.csv"

    df_seg = pd.read_csv(seg_inv_path)
    df_map = pd.read_csv(map_path)
    df_cells = pd.read_csv(cell_path)

    ui_data = {
        "summary": {
            "total_segments": len(df_seg),
            "occupied_native_cells": len(df_cells),
            "latitude_rows_count": int(df_cells["raster_row_index"].nunique()),
            "longitude_columns_count": int(df_cells["raster_column_index"].nunique()),
            "path_b_disclosure": "REPOSITORY_DECLARED_IMERG_COMPATIBLE_ANALYSIS_GRID — EMPIRICAL RASTER PROVENANCE NOT PROVEN",
            "milestone_status": "V2-3F-R8A2-2 CANDIDATE"
        },
        "cells": df_cells.to_dict(orient="records"),
        "segments": df_map.to_dict(orient="records")
    }

    new_content = json.dumps(ui_data, indent=2)

    if compare_existing:
        existing_content = out_json_path.read_text(encoding="utf-8")
        if existing_content != new_content:
            raise ValueError(f"EXPORT_COMPARISON_MISMATCH: Generated evidence JSON differs from existing file at {out_json_path}")
        print(f"Compared R8A2-2 UI Evidence JSON equality at {out_json_path}.")
        return

    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)

    print(f"Exported R8A2-2 UI Evidence JSON to {out_json_path} ({len(df_seg)} segments, {len(df_cells)} cells).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=str, default=None)
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--compare-existing", action="store_true", default=False)
    args = parser.parse_args()
    export_r8a2_2_ui_evidence(args.source_root, args.output_dir, args.compare_existing)
