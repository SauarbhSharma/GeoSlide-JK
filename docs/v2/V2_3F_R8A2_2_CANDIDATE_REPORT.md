# GeoSlide-JK 2.0 — V2-3F-R8A2-2 Candidate Report

> **Status:** CANDIDATE READY  
> **Milestone:** V2-3F-R8A2-2 Clean Worktree Serial Recovery  

---

## Key Scientific & Architectural Corrections
1. **Clean Worktree Isolation:** Built on clean R8A1 base commit `aeb62f230cc552d5c28824b97f5d9eec7bb72584` in isolated sibling worktree `D:\Projects\GeoSlide_JK_R8A2_2`.
2. **Tracked UI Evidence Exporter:** Deterministic repository script `scripts/export_v2_3f_r8a2_2_ui_evidence.py` generating `apps/web/src/data/r8a2_2_corridor_evidence.json` without scratch dependencies.
3. **Full-Closure Repository Manifest:** `git ls-tree -r -z` enumeration covering every tracked blob in artifact commit.
4. **Path B Grid Provenance:** Classified grid as `REPOSITORY_DECLARED_IMERG_COMPATIBLE_ANALYSIS_GRID — EMPIRICAL RASTER PROVENANCE NOT PROVEN` under Path B.
5. **UI Truthfulness & Resolution:** Direct import `@/src/data/r8a2_2_corridor_evidence.json` in `apps/web/app/corridor/page.tsx` aligning 158 segments and 11 native cells.
