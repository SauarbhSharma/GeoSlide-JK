# GeoSlide-JK 2.0 — Prioritized Development Roadmap & Implementation Plan

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)

---

## 1. Multi-Phase Implementation Roadmap

The development of GeoSlide-JK 2.0 is structured into **seven sequential phases** designed to deliver immediate high-impact user value while protecting scientific integrity and data safety:

```
┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐
│ PHASE 1   │──►│ PHASE 2   │──►│ PHASE 3   │──►│ PHASE 4   │──►│ PHASE 5   │──►│ PHASE 6   │──►│ PHASE 7   │
│ UI & IA   │   │ NH-44     │   │ Pre-      │   │ Advisory  │   │ Journey   │   │ Saathi AI │   │ Inst.     │
│ Redesign  │   │ Corridor  │   │ Monsoon   │   │ Telemetry │   │ Planning  │   │ Assistant │   │ Pilot     │
└───────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘   └───────────┘
```

---

## 2. Phase-by-Phase Detailed Specifications

### Phase 1: Product & Interface Redesign (Current MVP Focus)
- **User Value:** High | **Technical Effort:** Low-Medium | **Data Dependency:** None (Uses existing v1.0.0 data)
- **Deliverables:**
  - Implement Entry Modal ("How are you using GeoSlide-JK today?")
  - Implement 4 Role-Based View Modes (Traveller, Highway Ops, District Admin, Research)
  - Remove UI duplicates (dual district selectors, redundant sidebars)
  - Floating collapsible drawers for map canvas
- **Acceptance Criteria:** `npm run build` succeeds; 100% clean navigation across all 4 modes; map canvas area increased to >75% of screen width.

### Phase 2: NH-44 Corridor Intelligence Pilot
- **User Value:** Very High | **Technical Effort:** Medium | **Data Dependency:** Existing NH-44 vector + 100m rasters
- **Deliverables:**
  - 500m fixed chainage segmentation along NH-44 (Udhampur to Banihal)
  - Calculate Landslide Hazard Score ($LHS$), Disruption Impact Score ($DIS$), and Intervention Priority Score ($IPS$)
  - Linear Corridor Strip View & Intervention Queue Table
- **Acceptance Criteria:** Interactive chainage strip view renders 590 segments; priority queue outputs top 10 actionable segments.

### Phase 3: Pre-Monsoon Preparedness Outlook
- **User Value:** High | **Technical Effort:** Medium | **Data Dependency:** Monsoon climatology overlay
- **Deliverables:**
  - District Preparedness Ranking & Settlement Isolation Risk Map
  - Drainage & Culvert Clearing Checklist for DDMA
- **Acceptance Criteria:** 20 districts ranked by pre-monsoon vulnerability; isolated settlement layer toggleable.

### Phase 4: Operational Advisory & Telemetry Integration
- **User Value:** High | **Technical Effort:** High | **Data Dependency:** Category B/C telemetry
- **Deliverables:**
  - Structured 9-field JSON advisory API (`/api/v2/advisories`)
  - Color-coded advisory cards (Green/Yellow/Orange/Red)
- **Acceptance Criteria:** Advisory payload validates against schema; research disclaimers displayed on all cards.

### Phase 5: Journey Planning & Route-Risk Comparison
- **User Value:** Very High | **Technical Effort:** High | **Data Dependency:** Routing engine
- **Deliverables:**
  - Origin-Destination geocoding (Jammu to Srinagar)
  - Route polyline risk extraction & alternate route comparison (NH-44 vs Mughal Road)
- **Acceptance Criteria:** Journey query returns relative risk index ($RRI$) and high-risk km count.

### Phase 6: GeoSlide Saathi Multilingual Assistant
- **User Value:** Medium-High | **Technical Effort:** High | **Data Dependency:** LLM API
- **Deliverables:**
  - Grounded RAG assistant with citation enforcement and hallucination safeguards
- **Acceptance Criteria:** Saathi refuses unverified live road closure queries and cites GeoSlide database.

### Phase 7: Institutional Pilot & Enterprise Deployment
- **User Value:** Very High | **Technical Effort:** Medium | **Data Dependency:** Formal MOU
- **Deliverables:**
  - NHAI & SDMA enterprise portal deployment and official training
- **Acceptance Criteria:** Active institutional pilot on NH-44 corridor.

---

## 3. Impact vs. Effort Matrix

```
  HIGH IMPACT │  [PHASE 1: UI Redesign]           [PHASE 2: NH-44 Corridor]
              │  (Quick Win - Build First)        (Flagship MVP Focus)
              │
              │  [PHASE 3: Pre-Monsoon Prep]      [PHASE 5: Journey Planning]
              │  (High Value Operational)         (High Public Utility)
              ├─────────────────────────────────────────────────────────────
              │  [PHASE 4: Advisories]            [PHASE 6: Saathi AI]
   LOW IMPACT │  (Requires Telemetry)             (Future Capability)
              └─────────────────────────────────────────────────────────────
                                 LOW EFFORT ──────► HIGH EFFORT
```

---

## 4. Recommended Smallest High-Impact MVP

The smallest MVP that can be demonstrated without making unsupported claims consists of:
1. **Phase 1 UI & IA Redesign:** Role-based mode selector (Traveller vs NHAI vs Research).
2. **Phase 2 NH-44 Corridor Intelligence:** 500m chainage strip view and Intervention Priority Queue for NH-44 using existing 100m static susceptibility rasters.
