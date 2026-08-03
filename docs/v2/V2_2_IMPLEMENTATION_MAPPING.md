# GeoSlide-JK 2.0 — Phase 1 UI & IA Implementation Mapping

> **Document Version:** 2.2.0  
> **Status:** Checkpoint V2-2 Active Implementation  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## Implementation Mapping Table

| Planning Recommendation | Component / Page to Update | Planned Changes | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **1. Role-Based Entry Experience** | `apps/web/components/layout/RoleSelectionModal.tsx` | Create modal & dedicated page asking *"How are you using GeoSlide-JK today?"* with 4 role cards (Traveller, Highway Ops, District Admin, Research). Persist role preference in `localStorage`. | User can switch modes seamlessly; role selection persists across reloads; modal triggers from global Header. |
| **2. Global Header Role Switcher** | `apps/web/components/layout/Header.tsx` | Add role mode switcher dropdown & "Change Mode" button next to official GeoSlide-JK logo. Update top navigation tabs dynamically based on selected role mode. | Active mode clearly displayed in header; navigation tabs update according to selected role without breaking existing URL paths. |
| **3. Traveller / Resident Mode** | `apps/web/app/page.tsx`, `apps/web/components/dashboard/TravellerDashboard.tsx` | Build plain-language citizen home dashboard featuring "Check My Area" quick action, "Plan My Journey" preview, and plain-language risk advisories. | No raw probability numbers in primary view; plain-language risk ratings ("High Instability") with practical precautions. |
| **4. Highway Operations Mode (NHAI)** | `apps/web/components/dashboard/HighwayOpsDashboard.tsx`, `apps/web/app/corridor/page.tsx` | Build operational dashboard shell with NH-44 corridor overview, 500m segment concept, static road-segment landslide exposure, and priority segment queue. | Uses term *"Static Road-Segment Landslide Exposure"*; displays 500m segment chainage data without claiming live road closures. |
| **5. District Administration Mode** | `apps/web/components/dashboard/DistrictAdminDashboard.tsx` | Build DDMA preparedness dashboard displaying district vulnerability ranking, vulnerable rural settlements, and pre-monsoon inspection checklists. | Renders district vulnerability profiles and isolation risk overlays for all 20 J&K UT districts. |
| **6. Research / Technical Mode** | `apps/web/components/dashboard/ResearchDashboard.tsx` | Preserve 100% full access to 100m MapLibre GIS explorer, 30-feature XGBoost model metrics, feature importance, raster tile microservices, and system status. | Unrestricted access to raw float32 geotiff values, spatial CV ROC-AUC metrics (0.8694), and endpoint status matrix. |
| **7. Plan My Journey Preview** | `apps/web/app/journey/page.tsx` | Create journey planning preview shell with origin/destination dropdowns, departure time, vehicle type selector, and research-based relative risk comparison. | Labels results *"Research-based route exposure comparison"*; displays non-operational disclaimers; no "safe route" claims. |
| **8. NH-44 Corridor Monitor Shell** | `apps/web/app/corridor/page.tsx` | Create NH-44 corridor monitoring shell displaying 500m segments (Udhampur to Banihal), chainage markers, and technical details drawer. | Renders 500m segment static susceptibility exposure; labels output *"Static Road-Segment Landslide Exposure"*. |
| **9. Research Advisory Cards** | `apps/web/components/common/AdvisoryCard.tsx`, `apps/web/app/advisories/page.tsx` | Build standardized 4-tier advisory card component (Green / Yellow / Orange / Red) with 9 schema fields and research disclaimer. | Includes *"Research Advisory — Not an Official Government Warning"*; handles missing data gracefully. |
| **10. UI Duplication Removal** | `apps/web/app/page.tsx`, `apps/web/components/map/MapContainer.tsx` | Remove duplicate right 320px panel and left sidebar layer toggles from home view. Replace with floating, collapsible `Map Layers` drawer. | Map canvas area increased to $\ge 70\%$ of screen width when drawers are collapsed; single authoritative layer drawer. |
