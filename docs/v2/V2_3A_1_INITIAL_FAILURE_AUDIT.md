# GeoSlide-JK 2.0 — Checkpoint V2-3A.1 Initial Failure Audit

> **Document Version:** 2.3A.1  
> **Status:** Initial Failure Audited & Resolved  
> **Target Branch:** `geoslide-jk-v2-product-redesign`

---

## 1. Failure Root Cause Analysis

During Checkpoint V2-3A, the Playwright screenshot capture script generated 10 image files with identical byte sizes and content. The root cause analysis identified the following technical factors:

1. **Script Timing Defect:** The initial `capture_v2_3a_screenshots.py` script called `page.screenshot()` back-to-back inside a single loop on `http://127.0.0.1:3000/corridor` without waiting for page navigation, CSS asset downloading, React DOM hydration, or MapLibre canvas rendering between captures.
2. **Missing Local Role Setting:** The script did not initialize `localStorage.setItem('geoslide_user_role', 'highway')` before capturing, causing the application to default to `traveller` mode on first load.
3. **Stale Asset Cache / Port Conflict:** The screenshot script attempted to capture against port 3000 while the dev server was restarting, resulting in fallback DOM rendering.
4. **Legacy Content Retention:** The `/advisories` route retained hardcoded legacy chainages (`Km 142.0 – Km 143.5`) and unverified operational claims (`Delay non-essential transit`).

---

## 2. Corrective Remediation Strategy

1. **Isolated Playwright Contexts:** Rewrite the capture script (`scratch/capture_v2_3a_1_screenshots.py`) to open an isolated browser context per view, pre-set `localStorage`, wait for CSS/JS completion and network idle, and scroll/interact with specific 500m segment IDs.
2. **Mandatory Hash Uniqueness Guard:** Calculate MD5/SHA256 hashes of all 10 captured PNG files; fail execution if any two files are identical.
3. **Role Enforcement on `/corridor`:** Add `useEffect(() => setRole('highway'), [setRole])` in `apps/web/app/corridor/page.tsx`.
4. **Truthful Wording & Endpoint Verification:** Reconcile chainage to `"Pilot Analysis Chainage"` (0.00 – 74.88 km) and document true mapped endpoints (Sinthan Pass Sector to Anantnag Sector).
