#!/usr/bin/env python3
"""
GeoSlide-JK Data Audit Runner
Executes non-destructive discovery and outputs audit manifests to outputs/reports/
"""

import sys
import os
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from geoslide.audit.discovery import DataDiscoveryEngine, PathConfig

def main():
    print("=== GeoSlide-JK Data Discovery & Audit ===")
    
    try:
        path_config = PathConfig()
        print(f"Project Root (Writable):  {path_config.project_root}")
        print(f"Raw Data Root (Read-Only): {path_config.raw_root}")
        
        engine = DataDiscoveryEngine(path_config=path_config)
        report = engine.run_full_discovery()
        
        json_p, md_p = engine.write_reports(report)
        
        print("\nAudit Summary:")
        print(f"  - Verified Categories:         {report['summary']['verified']}")
        print(f"  - Multi-match/Tile Categories: {report['summary']['multiple_matches']}")
        print(f"  - Missing Categories:         {report['summary']['missing']}")
        print(f"\nManifest saved to: {json_p}")
        print(f"Markdown report saved to: {md_p}")
        print("\nData audit completed safely (Source datasets untouched).")
        
    except Exception as e:
        print(f"\nCRITICAL ERROR during data audit: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
