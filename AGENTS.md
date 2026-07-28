# GeoSlide-JK Agent Execution Guidelines

This file governs the automated and agentic execution environment for the **GeoSlide-JK** project. All agents working in this repository MUST comply strictly with these rules.

---

## 1. Absolute Workspace Boundaries

1. **WRITABLE PROJECT WORKSPACE**:
   `D:\Projects\GeoSlide_JK`
   - ALL code, scripts, configurations, documentation, test suites, intermediate outputs, tiles, logs, models, and reports MUST be created and stored exclusively in this folder.

2. **READ-ONLY RAW DATA WORKSPACE**:
   `C:\Users\Saurabh Sharma\Downloads\J&K`
   - This folder is **STRICTLY READ-ONLY**.
   - NEVER create, modify, rename, move, extract into, or delete any file or directory inside this raw data folder.
   - NEVER write temporary, interim, or log files into the raw data workspace.
   - Access raw data ONLY via read operations and configurable glob paths.

---

## 2. Phased Development Discipline

1. **One Phase at a Time**:
   - Work must progress strictly according to the phase sequence defined in `IMPLEMENTATION_PLAN.md`.
   - Do NOT jump ahead to future phases (e.g., do not build UI components or train ML models during Phase 0).

2. **Phase Completion Reporting**:
   - At the conclusion of every phase, produce a detailed status report in `docs/progress/PHASE_<N>_REPORT.md`.
   - STOP and wait for explicit user review and approval before beginning the next phase.

---

## 3. Data Integrity & Safety Rules

1. **No Raw Data Modification**:
   - Raw source archives (.zip) must never be extracted in-place within the raw data folder.
   - Any extraction needed MUST be directed to `D:\Projects\GeoSlide_JK\data\interim\` or `data/raw/`.

2. **Ambiguity Prevention**:
   - When resolving datasets, if multiple ambiguous candidates match a glob pattern, log the ambiguity and halt processing for that component. Never silently select an arbitrary file.

3. **No-Data vs Low Risk**:
   - Areas with missing data or incomplete coverage MUST be categorized as `Insufficient Data`, NEVER as `Low Risk`.

4. **NLSM Benchmark Isolation**:
   - The pre-existing NLSM susceptibility raster (`JammuandKashmir_Susceptibility.tif_NLSM_...`) must ONLY be used for validation and comparative benchmarks. It must NEVER be used as an input feature for training susceptibility models.

5. **No Synthetic Misrepresentation**:
   - Live status endpoints and research advisories must accurately report data freshness. Demo or mock data must be explicitly labeled as `Demo`.

---

## 4. Code & Architecture Standards

1. **Python Runtime**: Python 3.11+.
2. **CRS Standards**:
   - Processing / Distance CRS: `EPSG:32643` (UTM Zone 43N).
   - Web Delivery CRS: `EPSG:4326` (WGS 84).
3. **Configuration Driven**:
   - All paths, grid parameters, feature thresholds, rainfall triggers, and risk matrices MUST be declared in `configs/*.yaml`. No magic numbers or hardcoded local paths in source code.
