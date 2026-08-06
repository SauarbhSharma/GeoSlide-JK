# GeoSlide-JK 2.0 — "Manage My Corridor" Flagship Workflow Design

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)  
> **Target Persona:** NHAI Regional Officers, Highway Concessionaires, DDMA, Traffic Police

---

## 1. Workflow Vision & Pilot Scope

The **"Manage My Corridor"** workflow is the primary official/authority interface for GeoSlide-JK 2.0. It provides an operational, chainage-indexed management dashboard for critical transport corridors.

### Pilot Corridor Definition
- **Corridor:** **NH-44 Jammu–Udhampur–Ramban–Banihal–Srinagar**
- **Length:** 295 km
- **Focus Sub-Corridor:** **Udhampur to Banihal (Km 120.0 to Km 195.0)** — Known as the most landslide-vulnerable mountainous section of NH-44 in the Himalayas.

---

## 2. Chainage-Indexed Corridor Strip View

The core visualization is a linear, interactive **Corridor Strip View** indexed by highway chainage kilometers:

```
[Km 0: Jammu] ═══════ [Km 65: Udhampur] ═══[🟩]═══ [Km 142.5: Panthyal] ══[🟥]══ [Km 148: Ramban] ══[🟧]══ [Km 180: Banihal] ═══════ [Km 295: Srinagar]
                                                   ▲                             ▲
                                                   │                             │
                                        Critical Chainage: Km 142.5    Critical Chainage: Km 148.0
                                        Hazard Score: 0.88             Hazard Score: 0.74
                                        Priority: #1                   Priority: #2
```

### Chainage Segmentation Strategy
- **Segment Length:** 500 m fixed operational segments (590 total segments across NH-44).
- **Segment Metadata:**
  - Chainage Range (e.g. `Km 142.0 – Km 142.5`)
  - Local Name / Landmark (`Panthyal Cut-Slope`)
  - Landslide Hazard Score ($LHS \in [0, 1]$)
  - Road Disruption Impact Score ($DIS \in [1, 5]$)
  - Intervention Priority Score ($IPS = LHS \times DIS$)
  - Current Maintenance Status (`Needs Inspection`, `Work In Progress`, `Mitigation Completed`)

---

## 3. Intervention Priority Queue Table

The authority dashboard presents an automated, score-ranked **Intervention Queue**:

| Priority Rank | Chainage (Km) | Location Name | Hazard Score | Disruption Impact | Priority Score | Recommended Mitigation Action | Action Deadline | Assigned Officer / Agency | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **Km 142.5** | Panthyal Overhang | 0.88 | 5.0 (High Traffic) | **4.40 (Critical)** | Deploy slope netting & rockfall barrier; inspect toe catch-drains | 24 Hours | Er. A. K. Sharma (NHAI PIU Ramban) | `Needs Inspection` |
| **#2** | **Km 148.0** | Ramban Bypass Cut | 0.74 | 5.0 (Single Lane) | **3.70 (High)** | Shotcrete application on fractured shale slope; clear debris | 48 Hours | Project Director, NHAI Ramban | `Work Scheduled` |
| **#3** | **Km 153.2** | Digdol Slide Area | 0.72 | 4.5 (High Freight) | **3.24 (High)** | Inspect drainage channels; clear culvert blockage | 48 Hours | Executive Engineer, PWD Ramban | `In Progress` |
| **#4** | **Km 165.8** | Ramsu Mudslide Zone | 0.61 | 4.0 (Moderate Slope) | **2.44 (Moderate)** | Monitor bench stability; pre-position loader bulldozer | 72 Hours | Concessionaire Maintenance Team | `Monitoring` |

---

## 4. Operational Workflow & Action Loop

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               OPERATIONAL ACTION LOOP                                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. AUTOMATED SCAN: System calculates IPS score across all 590 corridor segments.       │
│ 2. ALERT TRIGGER: Segments with IPS > 3.0 automatically enter High Priority Queue.     │
│ 3. DISPATCH: NHAI officer assigns section engineer via dashboard toggle.               │
│ 4. FIELD EVIDENCE: Engineer uploads pre-intervention slope photograph & report.        │
│ 5. RE-EVALUATION: Mitigation status updated to 'Stabilized'; segment score re-indexed.  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Downloadable Corridor Mitigation Report

The dashboard provides a 1-click **Export PDF Corridor Report** for regional meetings:
- Executive Summary of Corridor Instability Exposure
- Top 10 Priority Segments with Maps & Chainage Indexes
- Rainfall Anomaly Scenario Impact Table
- Signed Maintenance Action Plan & Assignment Verification
