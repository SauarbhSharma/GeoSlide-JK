# GeoSlide-JK 2.0 — Product Vision & Strategic Positioning

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)  
> **Target Release:** GeoSlide-JK v2.0  
> **Tagline:** *Landslide and Road-Corridor Risk Intelligence Platform for Jammu & Kashmir*

---

## 1. Executive Summary & Paradigm Shift

The original **GeoSlide-JK v1.0.0** release established a scientifically rigorous, data-driven geospatial foundation for Jammu and Kashmir (J&K), incorporating a 100 m master reference grid, a 30-predictor XGBoost susceptibility model (5-fold spatial district-block ROC-AUC: 0.8694), dynamic 24-hour rainfall proxy scenario modeling, and multi-scale tile rendering services.

However, an evidence-based audit of stakeholder feedback and user experience reveals that while v1.0.0 is technically robust, its interface remains **feature-centric, raw-data heavy, and tailored primarily for geospatial researchers**. 

**GeoSlide-JK 2.0** transitions the platform from a *static geospatial visualization dashboard* into an **outcome-oriented, role-based decision intelligence platform**. It shifts the focus from answering *"What is the raw susceptibility probability of this raster pixel?"* to answering *"What specific operational decision or travel action should be taken right now, by whom, and with what level of confidence?"*

---

## 2. Core Questions Answered by GeoSlide-JK 2.0

Every view, card, advisory, and workflow in GeoSlide-JK 2.0 is designed to explicitly answer seven fundamental operational questions:

1. **Where is the risk?** — Pinpoint exact administrative zones, 100 m grid cells, and highway chainage kilometers.
2. **Which road stretch is affected?** — Map slope instability directly onto major transport corridors (e.g., NH-44 Panthyal–Ramban–Banihal stretch).
3. **When could the risk increase?** — Differentiate static baseline susceptibility from short-range (6–72h) or seasonal rainfall triggers.
4. **Who may be affected?** — Identify exposed commuters, vulnerable rural settlements, transport operators, and highway maintenance crews.
5. **What decision should the user take?** — Provide clear actionable guidance (e.g., "Postpone non-essential transit along NH-44 Ramban stretch until 18:00 hrs").
6. **What action should an authority initiate?** — Offer actionable intervention queues for NHAI officers and DDMA response teams (e.g., "Deploy clearing equipment to Chainage km 142.5").
7. **What is the confidence and freshness of the information?** — Explicitly state data age, missing input disclaimers, and model confidence ratings.

---

## 3. Recommended Product Positioning & Positioning Matrix

### Product Title
**GeoSlide-JK 2.0 — Landslide and Road-Corridor Risk Intelligence Platform**

### Core Objective Statement
> *"GeoSlide-JK 2.0 integrates multi-source geospatial data, machine-learning susceptibility modeling, and dynamic rainfall scenarios to deliver actionable risk intelligence, route advisories, and corridor maintenance prioritization across Jammu & Kashmir."*

---

## 4. Flagship Dual Outcomes

GeoSlide-JK 2.0 pivots around two flagship user outcomes:

```
                                  ┌─────────────────────────────────────────────────────────┐
                                  │                     GEOSLIDE-JK 2.0                     │
                                  │      Landslide & Corridor Risk Intelligence Platform    │
                                  └────────────────────────────┬────────────────────────────┘
                                                               │
                     ┌─────────────────────────────────────────┴─────────────────────────────────────────┐
                     ▼                                                                                   ▼
      ┌─────────────────────────────┐                                                     ┌─────────────────────────────┐
      │     PUBLIC FLAGSHIP OUTCOME  │                                                     │   AUTHORITY FLAGSHIP OUTCOME│
      │      "Plan My Journey"      │                                                     │    "Manage My Corridor"    │
      ├─────────────────────────────┤                                                     ├─────────────────────────────┤
      │ • Route-level risk strip    │                                                     │ • Corridor strip view       │
      │ • High-risk stretch counts  │                                                     │ • Chainage-indexed priority │
      │ • Relative risk comparison  │                                                     │ • Work-order queue          │
      │ • Clear action advisories   │                                                     │ • Resource deployment       │
      └─────────────────────────────┘                                                     └─────────────────────────────┘
```

### A. Public Outcome: *"Plan My Journey"*
- **Target User:** Commuters, tourists, commercial truck drivers, transport operators between Jammu, Srinagar, Banihal, and district hubs.
- **Value Delivered:** Provides relative risk scoring across alternate routes, highlights high-instability highway segments, and delivers clear safety advisories before departure.

### B. Authority Outcome: *"Manage My Corridor"*
- **Target User:** NHAI Regional Officers, Highway Concessionaires, District Disaster Management Authorities (DDMA), and Traffic Police.
- **Value Delivered:** Provides a chainage-indexed strip view of critical transport corridors (e.g., NH-44), ranks segments by disruption impact and intervention priority, and streamlines pre-monsoon mitigation planning.

---

## 5. Non-Negotiable Operational Safeguards

GeoSlide-JK 2.0 adheres strictly to the following scientific and legal boundaries:

1. **Relative Risk vs. Safety Guarantees:** The platform shall NEVER mark any road stretch as "Safe" or "Guaranteed Clear." It shall use terms such as *"Lower Relative Risk"* or *"Normal Baseline Risk"* to prevent false security.
2. **Research Advisory Designation:** All live advisories retain the explicit disclaimer: *"Research Advisory — Not an Official Government Warning."* Official evacuations or road closures remain strictly under the purview of state authorities.
3. **No Synthetic Misrepresentation:** Areas with missing data or incomplete coverage MUST be categorized as `Insufficient Data`, NEVER as `Low Risk`.
4. **Data Isolation:** Predictor isolation rules from v1.0.0 remain strictly enforced; targets, coordinate grids, and NLSM benchmark rasters remain excluded from training features.
