# GeoSlide-JK 2.0 — "Plan My Journey" Flagship Workflow Design

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)  
> **Target Persona:** Traveller, Resident, Commercial Driver, Transport Operator

---

## 1. Workflow Vision & Objective

The **"Plan My Journey"** workflow is the primary public entry point for GeoSlide-JK 2.0. It transforms raw spatial susceptibility rasters into an intuitive, route-level travel risk assessment. 

Given an origin (e.g., Jammu) and destination (e.g., Srinagar), the workflow analyzes candidate highway polylines, samples 100m slope susceptibility ratings and 24h rainfall proxy scenarios along the route, and delivers a clear, actionable travel advisory.

---

## 2. Step-by-Step User Journey & Data Inputs

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ 1. INPUT ROUTE  │ ──► │ 2. SPATIAL MAP  │ ──► │ 3. ROUTE RISK   │ ──► │ 4. ACTIONABLE   │
│ Origin / Dest / │     │ Polyline Raster │     │ Score & Profile │     │ Travel Advisory │
│ Departure Time  │     │  Intersection   │     │   Calculation   │     │  Card Display   │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Step 1: User Input Parameters
- **Origin:** Select from major towns or enter custom location (e.g., `Jammu City`).
- **Destination:** Select from major towns or enter custom location (e.g., `Srinagar`).
- **Departure Window:** `Depart Now`, `Depart in 6 Hours`, `Depart Tomorrow Morning`.
- **Vehicle Type:** `Light Motor Vehicle (LMV)`, `Heavy Commercial Vehicle (HCV / Truck)`, `Two-Wheeler`.

### Step 2: Route Spatial Processing & Intersection
1. System identifies available highway polylines connecting origin and destination (e.g., **Primary:** NH-44 via Ramban-Banihal; **Alternative:** Mughal Road via Rajouri-Shopian).
2. Segment polyline into 500 m evaluation windows.
3. Intersect each 500 m segment with:
   - 100m Static XGBoost Susceptibility Probability (`jk_susceptibility_probability_100m.tif`)
   - 100m Dynamic 24h Rainfall Accumulation Proxy (`jk_rainfall_accum_24h_100m.tif`)
   - Historical Landslide Density & Fault Distance vectors.

### Step 3: Route Metric Calculation
- **Total Route Distance:** e.g., 247 km
- **High-Risk Segment Distance:** Count of 500m segments with susceptibility probability > 0.60 (e.g., 14.5 km out of 247 km)
- **Critical Instability Stretches:** Identify named corridor hotspots intersected (e.g., `Panthyal (Km 142.5)`, `Ramban (Km 148.0)`, `Digdol (Km 153.2)`)
- **Route Relative Risk Index ($RRI$):**
  $$RRI = \frac{1}{N} \sum_{i=1}^{N} \left( S_i \times \frac{P_{24h, i}}{P_{90, i}} \right)$$
  Where $S_i$ is static susceptibility probability and $P_{24h}/P_{90}$ is rainfall anomaly ratio.

---

## 4. UI Output Mockup: Journey Risk Card

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 🚗 ROUTE RISK ANALYSIS: JAMMU ➔ SRINAGAR (NH-44)                                        │
│ Data Freshness: Audited v1.0.0 Pipeline | Updated: Today 08:00 IST                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ OVERALL ROUTE ADVISORY: 🟧 HIGH RELATIVE INSTABILITY EXPOSURE                           │
│ Recommended Action: Delay non-essential transit along Ramban-Banihal stretch by 6 hrs.  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 📊 ROUTE METRICS SUMMARY                                                               │
│ • Total Distance: 247 km                                                               │
│ • High Instability Exposure: 14.5 km (5.8% of route)                                   │
│ • Identified Hotspot Stretches: Panthyal (Km 142.5), Ramban (Km 148.0), Digdol (Km 153.2) │
│ • 24h Rainfall Proxy: 45.0 mm (Moderate Orographic Trigger Scenario)                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 🔀 ALTERNATE ROUTE COMPARISON                                                           │
│ 1. NH-44 (Direct via Ramban): 14.5 km High Risk | RRI: 0.68 | Status: Active Advisory │
│ 2. Mughal Road (via Shopian): 8.0 km High Risk | RRI: 0.42 | Status: Lower Relative Risk│
├────────────────────────────────────────────────────────────────────────────────────────┤
│ ⚠️ MANDATORY SAFETY DISCLAIMER                                                         │
│ GeoSlide-JK provides relative risk assessments based on terrain models and rainfall     │
│ scenarios. It is a research prototype and NOT an official road closure warning.        │
│ Always consult J&K Traffic Police official advisories before traveling.                │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Mandatory Safety & Language Rules

1. **Strict Prohibition of "Safe" Claims:**
   - **FORBIDDEN:** *"This route is safe."* or *"Clear route guaranteed."*
   - **REQUIRED:** *"Route displays lower relative risk compared to NH-44"* or *"Baseline susceptibility parameters within normal thresholds."*

2. **Handling Missing Data:**
   - If a road segment lacks terrain or rainfall data, it MUST be flagged as `Insufficient Coverage`, NEVER as `Low Risk`.

3. **Distinction Between Static and Dynamic Risk:**
   - Clearly separate slope terrain vulnerability (constant) from rainfall scenario triggers (variable).
