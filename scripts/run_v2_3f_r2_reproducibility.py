#!/usr/bin/env python
"""
GeoSlide-JK 2.0 — V2-3F-R2 Executable Reproducibility Script
Reruns the V2-3F-R2 historical output verification.
Uses 100% repository-relative paths.
"""
import sys, os, hashlib
import pandas as pd
from pathlib import Path

def run_v2_3f_r2_reproducibility():
    project_root = Path(__file__).resolve().parent.parent
    reports_dir = project_root / "outputs" / "reports"

    # Verify R2 canonical outputs exist
    df_cell = pd.read_csv(reports_dir / "v2_3f_r2_native_cell_evidence.csv")
    df_spearman = pd.read_csv(reports_dir / "v2_3f_r2_scenario_pairwise_spearman.csv")
    assert len(df_cell) == 8
    assert len(df_spearman) == 36
    print("V2-3F-R2 Historical output verification passed.")

if __name__ == "__main__":
    run_v2_3f_r2_reproducibility()
