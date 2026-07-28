# Security and Data Governance Rules

---

## 1. Primary Rule of Data Isolation

The raw dataset directory `C:\Users\Saurabh Sharma\Downloads\J&K` is **STRICTLY READ-ONLY**.

### Enforced Restrictions:
1. **NO WRITES**: No script, process, test, or subagent may create, modify, rename, move, or delete any file or directory in `C:\Users\Saurabh Sharma\Downloads\J&K`.
2. **NO IN-PLACE EXTRACTION**: Zip archives in the raw data folder must NEVER be unzipped within `C:\Users\Saurabh Sharma\Downloads\J&K`. Extraction MUST target `D:\Projects\GeoSlide_JK\data\interim\`.
3. **NO TEMPORARY FILES**: Scratch files, lock files, or temporary cache files must be stored in `D:\Projects\GeoSlide_JK\outputs\` or `D:\Projects\GeoSlide_JK\data\`.
4. **AUTOMATED TEST ENFORCEMENT**: Unit tests in `tests/test_paths_and_safety.py` will programmatically verify that write access to the raw directory is denied/prevented by the code base.

---

## 2. Product Framing & Research Advisories

1. **Research Prototype Disclaimer**:
   - The application must explicitly display a banner:
     > *"GeoSlide-JK is an explainable landslide susceptibility and rainfall-triggered risk-nowcasting research prototype. It does not constitute an official warning system."*
2. **Data Freshness Disclosure**:
   - The system UI and API responses must explicitly disclose data timestamp, source, and latency.
   - Demo playback datasets (e.g. July 2026 sample) must be clearly tagged as `Demo Mode`.

---

## 3. Data Licensing & Redistribution

1. **Restricted Datasets**:
   - High-resolution IMD gridded rainfall data, official survey shapefiles, and GSI lithology datasets are subject to institutional usage guidelines.
   - Raw data files MUST NOT be committed to git or uploaded to public repositories.
2. **Repository Exclusion**:
   - `.gitignore` MUST explicitly exclude `data/raw/`, `data/interim/`, `data/processed/`, `.env`, and all raw source archives.
