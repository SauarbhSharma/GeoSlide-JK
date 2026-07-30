# GeoSlide-JK Public Deployment Runbook

## 1. Local Pre-Flight Verification

### Python Unit Tests
```bash
python tests/run_all_tests.py
```

### Next.js Production Build
```bash
cd apps/web
npm run build
```

### Local Docker Build & Test
```bash
docker build -t geoslide-jk:production .
docker run -p 10000:10000 -e PORT=10000 geoslide-jk:production
```

Verify in local browser:
- Health check: `http://localhost:10000/api/v1/health`
- Next.js UI: `http://localhost:10000/`

---

## 2. Render Web Service Setup

1. Log into [Render Dashboard](https://dashboard.render.com).
2. Click **New +** → **Web Service**.
3. Connect GitHub repository: `SauarbhSharma/GeoSlide-JK`
4. Branch: `main`
5. Select **Runtime: Docker**.
6. Set **Plan: Free** (0.5 CPU, 512 MB RAM).
7. Environment Variables:
   - `PORT`: `10000`
   - `NODE_ENV`: `production`
   - `NEXT_PUBLIC_API_BASE_URL`: `""`
8. Health Check Path: `/api/v1/health`
9. Click **Create Web Service**.

---

## 3. Streamlit Community Cloud Setup

1. Log into [Streamlit Community Cloud](https://share.streamlit.io).
2. Click **New app**.
3. Select repository `SauarbhSharma/GeoSlide-JK`, branch `main`, main file `streamlit_app/streamlit_app.py`.
4. Open **Advanced settings...** → **Secrets**.
5. Add secret:
   ```toml
   GEOSLIDE_PUBLIC_APP_URL = "https://geoslide-jk.onrender.com"
   ```
6. Click **Deploy!**.

---

## 4. Post-Deployment Verification

Verify public Render URL:
1. `GET /api/v1/health` → `200 OK`
2. `GET /api/v1/status` → `200 OK`
3. `GET /api/v1/tiles/susceptibility_prob/8/181/102.png` → `200 OK (image/png)`
4. Open `https://geoslide-jk.onrender.com` in browser.
5. Verify MapLibre map renders with CARTO basemap and J&K boundary.
6. Toggle susceptibility probability, class, dynamic hazard index, and class layers.
