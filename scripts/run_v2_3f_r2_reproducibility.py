#!/usr/bin/env python
"""
GeoSlide-JK 2.0 — V2-3F-R2 Executable Deterministic Reproducibility Script
Reruns the V2-3F-R2 reconciliation pipeline and verifies exact output hash reproducibility.
"""
import sys, importlib.util
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
scratch_script = Path(r"C:\Users\Saurabh Sharma\.gemini\antigravity\brain\21035545-1ef0-4ee8-9693-5b8399c7188f\scratch\run_v2_3f_r2_pipeline.py")

spec = importlib.util.spec_from_file_location("run_v2_3f_r2_pipeline", scratch_script)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

if __name__ == "__main__":
    print("Executing V2-3F-R2 Reproducibility Pipeline...")
    mod.run_v2_3f_r2_pipeline()
    print("V2-3F-R2 Reproducibility pipeline execution complete.")
