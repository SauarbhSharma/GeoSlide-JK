# GeoSlide-JK 2.0 — Role-Based Information Architecture & Wireframe Specifications

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)

---

## 1. Application Entry Screen: *"How are you using GeoSlide-JK today?"*

Upon initial launch, GeoSlide-JK 2.0 presents a clean, uncluttered modal entry interface that routes users to their relevant persona workspace:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   WELCOME TO GEOSLIDE-JK 2.0                           │
│                       Landslide & Road-Corridor Risk Intelligence Platform             │
│                                                                                        │
│                      How would you like to use GeoSlide-JK today?                      │
│                                                                                        │
│   ┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────────────┐   │
│   │   🚗 TRAVELLER /       │  │   🛣️ HIGHWAY          │  │   🏛️ DISTRICT          │   │
│   │      COMMUTER          │  │      OPERATIONS (NHAI) │  │      ADMINISTRATION    │   │
│   ├────────────────────────┤  ├────────────────────────┤  ├────────────────────────┤   │
│   │ • Plan My Journey      │  │ • Corridor Monitor     │  │ • District Overview    │   │
│   │ • Check My Area        │  │ • Chainage Risk Map    │  │ • Vulnerable Areas     │   │
│   │ • Route Advisories     │  │ • Maintenance Queue    │  │ • Pre-Monsoon Prep     │   │
│   └────────────────────────┘  └────────────────────────┘  └────────────────────────┘   │
│                                                                                        │
│   ┌────────────────────────┐  ┌────────────────────────┐                              │
│   │   🚑 EMERGENCY         │  │   🔬 RESEARCH &        │                              │
│   │      RESPONSE (SDRF)   │  │      TECHNICAL AUDIT   │                              │
│   ├────────────────────────┤  ├────────────────────────┤                              │
│   │ • Incident Staging     │  │ • Full GIS Explorer    │                              │
│   │ • Access Road Status   │  │ • Model Transparency   │                              │
│   │ • Rescue Route Check   │  │ • System Health        │                              │
│   └────────────────────────┘  └────────────────────────┘                              │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mode Navigation & Menu Structure

### Mode 1: Traveller / Commuter Mode (Public Unauthenticated)
- **Primary View:** Plan My Journey (Origin–Destination Route Risk)
- **Secondary View:** Check My Area (Point / Lat-Lon Instability Query)
- **Tertiary View:** Active Travel Advisories (Corridor Status Summary)
- **Navigation Tabs:** `Plan My Journey` | `Check My Area` | `Travel Advisories` | `Help & Guidance`

### Mode 2: Highway Operations / NHAI Mode (Authenticated / Official)
- **Primary View:** Corridor Monitor (NH-44 Strip View & Chainage Index)
- **Secondary View:** Maintenance Priorities (Intervention Queue Table)
- **Tertiary View:** Pre-Monsoon Corridor Outlook
- **Navigation Tabs:** `Corridor Strip View` | `Maintenance Queue` | `Inspection Log` | `Corridor Reports`

### Mode 3: District Administration Mode (Authenticated / Official)
- **Primary View:** District Preparedness Overview (20-District Vulnerability Ranking)
- **Secondary View:** Community Vulnerability & Isolation Risk Map
- **Navigation Tabs:** `District Overview` | `Vulnerable Settlements` | `Pre-Monsoon Readiness` | `Resource Staging`

### Mode 4: Research & Technical Mode (Public / Academic)
- **Primary View:** Full GIS Spatial Explorer (100m Raster MapLibre Canvas)
- **Secondary View:** Model & Methodology Transparency (XGBoost Metrics & Feature Importance)
- **Tertiary View:** System & Data Status (FastAPI Endpoint Health & Pipeline Logs)
- **Navigation Tabs:** `Full GIS Explorer` | `Model Transparency` | `Data & Pipeline Status`

---

## 3. Desktop Wireframe Descriptions

### Traveller Mode Desktop Layout (1920 × 1080 px)
- **Header (64px):** Compact GeoSlide-JK Emblem | "GeoSlide-JK 2.0" | Mode Switcher Dropdown | Research Advisory Badge
- **Left Panel (360px):**
  - Search Form: Origin (e.g. Jammu) & Destination (e.g. Srinagar)
  - Departure Time Picker & Vehicle Type (Light / Heavy Cargo)
  - "Analyze Route Risk" primary action button
  - Route Risk Summary Card: Overall Relative Risk Rating (Yellow / Watch)
  - High-Risk Stretch Count: "3 critical stretches detected (Panthyal, Ramban, Digdol)"
- **Center Canvas (Flex):**
  - Clean MapLibre Map displaying highlighted route polyline color-coded by 500m segment risk
  - Hover popups displaying segment name, elevation, slope angle, and instability rating
- **Bottom Drawer (Collapsible):**
  - Route Risk Strip View (Horizontal profile showing elevation & susceptibility along route km)

### Highway Operations Mode Desktop Layout (1920 × 1080 px)
- **Header (64px):** Emblem | "GeoSlide-JK Corridor Manager (NH-44)" | Segment Filter | Export PDF Report Button
- **Top Strip View (180px):**
  - Linear chainage strip from Km 0 (Jammu) to Km 295 (Srinagar)
  - Color-coded segments: Green (<0.35), Yellow (0.35-0.55), Orange (0.55-0.75), Red (>0.75)
  - Clickable chainage markers (e.g. Km 142.5 Panthyal)
- **Main Viewport (Split 60/40):**
  - Left (60%): High-Resolution 100m MapLibre Map zoomed to selected chainage segment
  - Right (40%): Intervention Priority Queue Table listing top 10 vulnerable segments, required mitigation action (e.g., "Install slope mesh / clear toe-drainage"), assigned section engineer, and priority score.

---

## 4. Mobile Wireframe Descriptions (375 × 812 px Smartphone)

- **Header (48px):** Compact Emblem | "GeoSlide-JK 2.0" | Hamburger Menu
- **Single Column Flow:**
  1. Compact Route Risk Card (e.g., "Jammu → Srinagar: Moderate Relative Risk")
  2. "Plan Journey" Input Drawer (Tap to change origin/destination)
  3. Interactive Map (Takes 50% screen height, touch-optimized panning)
  4. Expandable Advisory Card (Color-coded yellow/orange with simple bullet points)
- **Bottom Navigation Bar (56px):** 4 Touch Tabs (`Journey` | `Map` | `Advisories` | `Help`)
