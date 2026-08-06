# GeoSlide-JK 2.0 — Executive Strategy & Actionable Recommendation

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## Executive Answers to the 10 Core Strategic Questions

### 1. What problem will GeoSlide-JK 2.0 solve?
**Answer:** GeoSlide-JK v1.0.0 delivered a scientifically sound geospatial backend, but presented raw data rasters and technical metrics that were difficult for commuters, highway operators, and disaster officials to interpret. **GeoSlide-JK 2.0 solves the gap between raw geospatial data and actionable decision-making** by converting pixel-level probabilities into role-specific travel advisories, chainage-indexed highway risk scores, and pre-monsoon maintenance queues.

### 2. Who are the primary beneficiaries?
**Answer:**
1. **Citizens & Commuters:** Travelers along mountain highways who need clear relative risk advisories before departing.
2. **NHAI & Highway Operations Officers:** Engineers needing to prioritize slope inspection and maintenance along critical corridors like NH-44.
3. **District Administration & DDMA:** Disaster officials planning pre-monsoon staging and relief for vulnerable rural communities.

### 3. Which two workflows should be built first?
**Answer:**
1. **Public Flagship Workflow: *"Plan My Journey"*** — Origin-destination route risk scoring and travel advisory display.
2. **Authority Flagship Workflow: *"Manage My Corridor"*** — Chainage-indexed strip view (500m segments) and Intervention Priority Queue for NH-44.

### 4. What can be delivered using current verified data?
**Answer:** All core 100m static susceptibility probability layers, 5-class susceptibility ratings, administrative district boundaries, 10 static vector layers (NH-44, landslides, faults, settlements), and 100m deployment terrain COGs are 100% processed, verified, and ready for immediate UI integration.

### 5. What must wait for authoritative data or formal authorization?
**Answer:** Live traffic road closure feeds (requires J&K Traffic Police API), automated mass SMS alerts (requires SDMA authorization), structural pavement quality ratings (requires NHAI RAMS data), and real-time radar telemetry (requires live IMD NetCDF feeds).

### 6. What should be removed or simplified in the current UI?
**Answer:**
- Remove the permanent right-side 320px panel on desktop; replace with floating, collapsible drawers.
- Remove duplicate district selectors and layer toggles.
- Merge `/explorer` into `/` (Statewide Command Centre) as a unified full-screen map mode.
- Merge `/rainfall` into `/location-check` ("Check My Area").
- Remove raw uninterpreted numbers (e.g. `Probability 0.8694`) from public views; replace with plain-language action cards.

### 7. What should the recommended NH-44 pilot contain?
**Answer:**
- A 500m fixed-chainage linear strip view for the 295 km NH-44 corridor (focusing on Udhampur-Banihal km 120–195).
- Three decoupled scores: Landslide Hazard Score ($LHS$), Disruption Impact Score ($DIS$), and Intervention Priority Score ($IPS$).
- An automated top-10 Intervention Priority Queue table with action deadlines and assigned engineering units.

### 8. What is the commercial proposition?
**Answer:** Basic public safety and travel advisories remain **100% FREE AND UNRESTRICTED** for all residents and commuters. Commercialization is focused on an **Annual Enterprise Subscription for Highway Operators (NHAI/Concessionaires)** for the "Manage My Corridor" maintenance prioritization module (Model 2).

### 9. What should the next coding checkpoint implement?
**Answer:** **Checkpoint V2-2:** Implement the Phase 1 UI & Information Architecture redesign in `apps/web` (Entry modal, 4 role-based modes, floating map drawers, removal of duplicate components) without altering backend API services or scientific model weights.

### 10. What must NOT be claimed publicly?
**Answer:**
- NEVER claim that any road or route is "Safe" or "Guaranteed Clear." Use *"Lower Relative Risk"* only.
- NEVER claim deterministic time-of-failure prediction (e.g. *"Slide will occur at 14:00"*).
- NEVER classify unmapped or data-missing areas as "Low Risk"; label them as `INSUFFICIENT COVERAGE`.
- ALWAYS display: *"Research Advisory — Not an Official Government Warning."*
