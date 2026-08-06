# GeoSlide-JK — Duplicate Component & Interface Redundancy Audit

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)  
> **Scope:** Full UX/UI Audit of Existing Next.js Frontend Application (`apps/web`)

---

## 1. Summary of Identified UI Redundancies

An in-depth component-level audit of the GeoSlide-JK v1.0.0 frontend interface (`apps/web`) identified **seven major structural redundancies** that clutter the user interface, reduce available map viewport space, and create cognitive overload for non-geospatial users:

1. **Dual District Selectors:** The home page (`/`) contains a district dropdown inside the left `Sidebar` component *and* duplicates the exact same 20-district interactive selector list in the right-side `Statewide District Overview` panel.
2. **Duplicate Layer Toggle Controls:** Layer visibility toggles (e.g., `jk_districts`, `susceptibility_prob`, `nh44`) exist inside the left `Sidebar` component *and* are re-implemented as floating overlay controls inside the `MapContainer` component.
3. **Repeated Lat/Lon Preset Dropdowns:** The exact same list of 5 example locations (`Panthyal NH-44, Ramban`, `Jammu City Center`, `Srinagar Aerodrome`, `Kupwara North Slopes`, `Kishtwar Chenab Valley`) is hardcoded in both `app/rainfall/page.tsx` and `app/location-check/page.tsx`.
4. **Duplicate Release & Model Status Banners:** The green release status banner (*"GeoSlide-JK v1.0.0 Live: The static XGBoost susceptibility model..."*) is rendered on `/`, `/explorer`, `/districts`, `/rainfall`, `/transparency`, and `/status`, consuming 50–70px of vertical height on every single page.
5. **Redundant Route Pages:** `/explorer` duplicates over 90% of the main `/` (Statewide Command Centre) page layout with identical map, sidebar, and status controls, creating artificial navigation fragmentation.
6. **Permanent Fixed-Width Right Panel:** On desktop screens (≥1280px), the right-side panel consumes 320px of permanent horizontal space, squeezing the central map canvas to less than 50% of screen width.
7. **Raw Uninterpreted Numbers:** Key metrics are displayed as raw technical floating-point values (e.g., `Probability: 0.8694`, `Anomaly Ratio: 1.82x`, `Grid: EPSG:32643`) without accompanying operational interpretation or decision guidance.

---

## 2. Component-by-Component Duplication Matrix

| Component / Feature | Location A | Location B | Problem | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **District Selector** | `components/layout/Sidebar.tsx` | `app/page.tsx` (Right Panel) | Identical list of 20 districts in two places on the same screen. | Retain single unified district selector in top control bar or mode header. Remove right panel duplicate. |
| **Layer Toggles** | `components/layout/Sidebar.tsx` | `components/map/MapContainer.tsx` | User can toggle layers from left panel OR right map overlay, creating out-of-sync state risks. | Consolidate into a single, clean floating `Map Layers` drawer on the map canvas. |
| **Location Presets** | `app/rainfall/page.tsx` | `app/location-check/page.tsx` | Duplicate array constant `PRESET_LOCATIONS` hardcoded in two separate page files. | Extract `PRESET_LOCATIONS` into `@/lib/constants.ts` and merge `/rainfall` into `/location-check`. |
| **Release Banner** | `app/page.tsx` | `app/explorer/page.tsx`, `app/districts/page.tsx`, etc. | Banner is repeated on 6 separate pages, wasting vertical screen space. | Render release banner ONLY in top global Header or System Status page. |
| **Phase 2–6 Lifecycle List** | `app/status/page.tsx` | `README.md`, `app/transparency/page.tsx` | 7-step phase pipeline list duplicated across documentation and live pages. | Keep in `app/status/page.tsx` only under Research Mode. |

---

## 3. Visual Clutter & Map Viewport Impact

On a standard 1080p desktop display (1920 × 1080 px):
- Global Header: **72 px height**
- Research Disclaimer Banner: **48 px height**
- Release Status Banner: **52 px height**
- KPI Summary Cards Bar: **84 px height**
- Timeline Slider Bar: **60 px height**
- Left Sidebar Width: **280 px**
- Right Overview Panel Width: **320 px**

**Net Result:** Out of a 1920 × 1080 viewport (2,073,600 total pixels), the actual Map Canvas receives only **1320 × 764 px (1,008,480 pixels)**, representing **less than 49% of the available screen area**.

---

## 4. UI Simplification Plan for GeoSlide-JK 2.0

1. **Collapsible Floating Control Drawers:** Convert permanent left/right sidebars into floating, collapsible drawers that collapse to zero width when the user is exploring the map.
2. **Unified Navigation Structure:** Consolidate the 7 separate pages into **4 Role-Based Modes** (Traveller, Highway Operations, District Admin, Research Mode).
3. **Contextual Action Cards:** Replace generic KPI cards with role-specific action cards that explain *what to do* rather than just *what the raw number is*.
