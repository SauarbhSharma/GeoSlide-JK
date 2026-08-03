# GeoSlide-JK 2.0 — Jobs-To-Be-Done (JTBD) Framework

> **Document Version:** 2.0.0-draft  
> **Status:** Strategy & Architecture Planning (Checkpoint V2-0)  
> **Framework:** Outcome-Driven Innovation (Ulwick JTBD Methodology)

---

## 1. Overview & Core Philosophy

The Jobs-To-Be-Done (JTBD) framework decomposes user needs into **Functional**, **Emotional**, and **Social** jobs. Instead of designing features (e.g., *"add a layer toggle for slope"*), GeoSlide-JK 2.0 designs workflows around core jobs (e.g., *"help a commuter decide whether to travel from Jammu to Srinagar today without getting trapped in a landslide blockade"*).

---

## 2. Jobs-To-Be-Done Matrix Across Key Stakeholders

### 1. Traveller / Commuter / Resident
- **Functional Job:** Determine if the highway route between origin and destination is at elevated risk of landslide disruption before departing, and identify safer departure times or alternate routes.
- **Emotional Job:** Feel confident, safe, and in control when traveling through mountainous terrain with family or commercial cargo.
- **Social Job:** Avoid being perceived as careless by family or employers for taking avoidable risks during bad weather.
- **Job Map Steps:**
  1. *Define:* Specify departure point (e.g., Jammu) and destination (e.g., Srinagar).
  2. *Locate:* Identify high-instability stretches along the chosen route (e.g., Panthyal, Ramban).
  3. *Assess:* Evaluate current relative risk score and 24h rainfall proxy trend.
  4. *Decide:* Choose whether to proceed now, delay by 6 hours, or take an alternate route (e.g., Mughal Road if open).
  5. *Monitor:* Receive mid-journey advisories if conditions deteriorate.

### 2. NHAI / Highway Operations Officer
- **Functional Job:** Prioritize maintenance inspections, slope stabilization interventions, and heavy machinery placement along critical highway corridors based on objective instability scores.
- **Emotional Job:** Minimize personal liability and stress associated with sudden highway closures, multi-day blockades, and public backlash.
- **Social Job:** Demonstrate proactive management and technical competence to senior ministry officials and the public.
- **Job Map Steps:**
  1. *Scan:* Review corridor strip view for high-priority chainage kilometers.
  2. *Diagnose:* Inspect underlying drivers (slope angle, fault proximity, rainfall anomaly).
  3. *Prioritize:* Rank chainage segments by Intervention Priority Score.
  4. *Dispatch:* Assign field inspection teams or maintenance contractors to top-ranked segments.
  5. *Track:* Monitor post-intervention stabilization and clear backlog.

### 3. Highway Contractor / Concessionaire
- **Functional Job:** Identify vulnerable cut-slopes and un-engineered hill faces along active road construction zones to apply preventive slope protection before heavy rains.
- **Emotional Job:** Protect field workers and expensive equipment from slope collapses and avoid financial penalties for contract delays.
- **Social Job:** Maintain a stellar safety record and compliance rating with highway authorities.

### 4. District Administration / DDMA
- **Functional Job:** Identify highly vulnerable rural settlements and cut-off prone access roads during pre-monsoon planning to pre-position food, medical supplies, and rescue teams.
- **Emotional Job:** Reassure district residents that the administration is prepared for disaster events.
- **Social Job:** Fulfill statutory obligations under the Disaster Management Act, 2005.

### 5. Emergency Responder (SDRF / NDRF)
- **Functional Job:** Navigate safely to landslide occurrence sites along non-blocked secondary routes while monitoring active secondary failure risks on surrounding slopes.
- **Emotional Job:** Ensure team safety while executing high-stakes search and rescue operations.
- **Social Job:** Maintain public trust as a dependable emergency rescue force.

### 6. Traffic Police
- **Functional Job:** Enforce highway movement restrictions and control vehicle staging at Nagrota/Udhampur/Qazigund checkpoints based on real-time segment risk.
- **Emotional Job:** Avoid managing stranded vehicles in dangerous narrow mountain passes during active rainstorms.
- **Social Job:** Maintain orderly traffic flow and public safety under challenging weather conditions.

### 7. Tourism / Transport Operator
- **Functional Job:** Optimize fleet departure schedules and vehicle routes to protect passengers and cargo while avoiding costly delays.
- **Emotional Job:** Safeguard business reputation and passenger safety.
- **Social Job:** Be recognized as a top-tier, safety-first transport logistics service in J&K.

### 8. Researcher / Technical User
- **Functional Job:** Access transparent, validated geospatial models, raster datasets, and spatial cross-validation metrics to advance landslide susceptibility research.
- **Emotional Job:** Confidence in data scientific rigor, lack of spatial data leakage, and reproducibility.
- **Social Job:** Publish peer-reviewed scientific studies validating ML applications in Himalayan terrain.

### 9. Senior Government Decision-Maker
- **Functional Job:** Allocate state infrastructure and disaster mitigation budgets to the highest-risk districts and corridors using objective data.
- **Emotional Job:** Feel assured that state investments are measurably reducing landslide vulnerability.
- **Social Job:** Report tangible disaster risk reduction achievements to government leadership and international bodies.
