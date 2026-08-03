# GeoSlide-JK 2.0 — Road-Risk Scoring Architecture & Metric Design

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)

---

## 1. Multi-Dimensional Scoring Framework

Rather than collapsing complex geotechnical, traffic, and spatial variables into a single opaque index, GeoSlide-JK 2.0 establishes **three decoupled operational scores** plus a **Data Confidence Score**:

```
                       ┌─────────────────────────────────────────────────────────┐
                       │           GEOSLIDE-JK 2.0 SCORING FRAMEWORK             │
                       └────────────────────────────┬────────────────────────────┘
                                                    │
         ┌──────────────────────────────┬───────────┴──────────────┬──────────────────────────────┐
         ▼                              ▼                          ▼                              ▼
┌─────────────────┐            ┌─────────────────┐        ┌─────────────────┐            ┌─────────────────┐
│ 1. LANDSLIDE    │            │ 2. ROAD         │        │ 3. INTERVENTION │            │ 4. DATA         │
│ HAZARD SCORE    │     ×      │ DISRUPTION      │   =    │ PRIORITY SCORE  │    WITH    │ CONFIDENCE      │
│     (LHS)       │            │ IMPACT SCORE    │        │     (IPS)       │            │ SCORE (DCS)     │
│ Range: [0.0,1.0]│            │    (DIS)        │        │ Range: [0.0,5.0]│            │ Range: [0%,100%]│
└─────────────────┘            └─────────────────┘        └─────────────────┘            └─────────────────┘
```

---

## 2. Detailed Mathematical Formulations

### 1. Landslide Hazard Score (LHS)
Measures the physical slope instability exposure of a highway segment based on static ML susceptibility and dynamic rainfall scenario triggers.

$$LHS = \min \left( 1.0, \, S_{static} \times \left[ 1.0 + \alpha \max\left(0, \frac{P_{24h} - P_{90}}{P_{90}}\right) \right] \right)$$

- $S_{static} \in [0.0, 1.0]$: XGBoost 100m raster susceptibility probability averaged over segment width.
- $P_{24h}$: 24-hour rainfall accumulation scenario value (mm).
- $P_{90}$: Baseline IMD 90th percentile proxy value (mm).
- $\alpha = 0.5$: Rainfall anomaly scaling coefficient.

### 2. Road Disruption Impact Score (DIS)
Measures the operational consequences of a potential blockade on the segment ($DIS \in [1.0, 5.0]$).

$$DIS = w_1 \cdot T_{volume} + w_2 \cdot A_{detour} + w_3 \cdot E_{isolation}$$

- $T_{volume} \in [1, 5]$: Traffic volume weight (NH-44 main trunk = 5.0; local feeder = 2.0).
- $A_{detour} \in [1, 5]$: Detour availability (No alternate route available = 5.0; easy local detour = 1.0).
- $E_{isolation} \in [1, 5]$: Population isolation risk (Cuts off major district hospital / town = 5.0).
- Weights: $w_1 = 0.4$, $w_2 = 0.4$, $w_3 = 0.2$.

### 3. Intervention Priority Score (IPS)
Combines physical hazard with operational impact to rank segments in authority maintenance queues.

$$IPS = LHS \times DIS \quad \in [0.0, \, 5.0]$$

- **IPS Category Tiers:**
  - `0.0 – 1.0`: Low Priority (Green)
  - `1.1 – 2.0`: Moderate Priority (Yellow)
  - `2.1 – 3.5`: High Priority (Orange)
  - `3.6 – 5.0`: Critical Priority (Red)

### 4. Data Confidence Score (DCS)
Quantifies the completeness and spatial resolution of underlying data inputs for the segment ($DCS \in [0\%, 100\%]$).

$$DCS = 100\% \times \left( 1 - \frac{\text{Count of Missing Core Feature Layers}}{\text{Total Required Feature Layers (30)}} \right)$$

---

## 3. Strict Rule: No-Data != Low Risk

A critical data-safety rule enforced in GeoSlide-JK 2.0:
> **"Areas with missing raster coverage, unmapped geological features, or missing rainfall telemetry MUST be explicitly assigned a Data Confidence Score of <50% and flagged as `INSUFFICIENT DATA`, NEVER classified as `LOW RISK`."**

Classifying an unmapped or data-missing mountain stretch as "Low Risk" introduces catastrophic liability if a slope failure occurs.

---

## 4. Segment Length Recommendation for NH-44 Pilot

| Option | Resolution | Pros | Cons | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Option A** | 250 m | High spatial precision | Overly granular; creates 1,180 segments | Too dense for executive review |
| **Option B** | **500 m** | **Optimal balance of engineering precision & UX** | Requires 590 segments across NH-44 | **RECOMMENDED FOR NH-44 PILOT** |
| **Option C** | 1,000 m (1 km) | Easy alignment with km markers | Smooths out localized 100m instability hotspots | May miss narrow 100m cut-slope failures |
| **Option D** | Variable Chainage | Aligns with NHAI engineering contracts | Irregular lengths complicate statistical aggregation | Secondary phase enhancement |

**Final Recommendation:** Use **500 m fixed operational segments** for the NH-44 pilot corridor, mapped directly to standard highway chainage (e.g. Km 142.0 to 142.5).
