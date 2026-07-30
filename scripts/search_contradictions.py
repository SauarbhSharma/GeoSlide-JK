#!/usr/bin/env python3
"""
Searches all codebase text files for misleading contradiction phrases.
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TARGET_PHRASES = [
    "Phase 2 Active",
    "Phase 4 Pending",
    "Phase 5 Scheduled",
    "Phase 6 Pending",
    "Not Trained",
    "No model metrics",
    "Illustrative Demo Value",
    "not calculated from the processing pipeline",
    "Critical - Demo",
    "Risk & Rainfall Modules: Demo",
    "approximately 485,000",
    "42,500",
    "68.4 km",
    "64.5 mm",
    "18.2 mm"
]

EXTENSIONS = {".tsx", ".ts", ".json", ".py", ".yaml", ".yml", ".md", ".html"}

def search_files():
    matches = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip .git, node_modules, .next, __pycache__, outputs/reports, docs/progress
        if any(skip in root for skip in [".git", "node_modules", ".next", "__pycache__", "outputs/reports"]):
            continue
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in EXTENSIONS:
                try:
                    text = p.read_text(encoding="utf-8", errors="ignore")
                    for phrase in TARGET_PHRASES:
                        if phrase.lower() in text.lower():
                            matches.append((p.relative_to(PROJECT_ROOT), phrase))
                except Exception as e:
                    pass
    return matches

if __name__ == "__main__":
    found = search_files()
    if found:
        print(f"FOUND {len(found)} MISLEADING PHRASE OCCURRENCES:")
        for path, phrase in found:
            print(f" - {path}: '{phrase}'")
    else:
        print("ZERO MISLEADING CONTRADICTION PHRASES FOUND ACROSS CODEBASE!")
