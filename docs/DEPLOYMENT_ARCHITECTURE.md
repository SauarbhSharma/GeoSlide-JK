# GeoSlide-JK Deployment Architecture

## Production Stack

```
┌─────────────────────────────────────────────────────────┐
│                   Render Web Service                     │
│                   (Free Plan, Docker)                    │
│                                                          │
│   ┌─────────────────────┐    ┌────────────────────────┐ │
│   │   Next.js v14        │    │   FastAPI (uvicorn)    │ │
│   │   Port: $PORT        │    │   Port: 8000           │ │
│   │   (public-facing)    │    │   (internal only)      │ │
│   │                      │    │                        │ │
│   │   Serves:            │    │   Serves:              │ │
│   │   - React SSR pages  │    │   - /api/v1/* REST     │ │
│   │   - Static assets    │    │   - Raster tile server │ │
│   │   - MapLibre GL JS   │    │   - Point sampling     │ │
│   │                      │    │   - GeoJSON boundaries │ │
│   │   Rewrites:          │    │   - Location check     │ │
│   │   /api/* → :8000     │    │   - Health/status      │ │
│   └─────────────────────┘    └────────────────────────┘ │
│                                                          │
│   ┌──────────────────────────────────────────────────┐  │
│   │            Processed Data Assets                  │  │
│   │   - Susceptibility rasters (prob + class)         │  │
│   │   - Dynamic hazard rasters (index + class)        │  │
│   │   - Rainfall proxy rasters (24h, P90, anomaly)    │  │
│   │   - District boundaries (GeoJSON)                 │  │
│   │   - Vector layers (Parquet)                       │  │
│   └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│           Streamlit Community Cloud (Optional)           │
│   - Minimal wrapper: embeds Render URL via iframe        │
│   - Secret: GEOSLIDE_PUBLIC_APP_URL                      │
│   - No independent dashboard or calculations             │
└─────────────────────────────────────────────────────────┘
```

## Routing

| Browser Request | Handled By | Internal Target |
|:---|:---|:---|
| `/` | Next.js | SSR home page |
| `/explorer` | Next.js | SSR explorer page |
| `/districts` | Next.js | SSR districts page |
| `/rainfall` | Next.js | SSR rainfall page |
| `/location-check` | Next.js | SSR location check page |
| `/transparency` | Next.js | SSR transparency page |
| `/status` | Next.js | SSR status page |
| `/api/v1/*` | Next.js rewrite | → FastAPI :8000 |
| `/api/v1/tiles/{layer}/{z}/{x}/{y}.png` | Next.js rewrite | → FastAPI tile server |

## Security Headers

- `Content-Security-Policy: frame-ancestors 'self' https://*.streamlit.app`
- `X-Content-Type-Options: nosniff`

## Asset Strategy

### Committed to Git (< 100 MB each)
- Susceptibility probability/class rasters (~16 MB / ~0.6 MB)
- Dynamic hazard index/class rasters (~16 MB / ~0.6 MB)
- Rainfall proxy rasters (~14 MB each × 3)
- District/UT boundary GeoJSON
- Vector layers (Parquet)

### NOT committed (exceeds GitHub 100 MB limit)
- Terrain COGs: elevation (216 MB), slope (231 MB), aspect (231 MB), hillshade (50 MB)
- The application degrades gracefully — terrain layer toggles return "data unavailable"

## Free Plan Limitations

1. **512 MB RAM** — sufficient for small raster tile serving
2. **Cold starts** — service spins down after 15 min of inactivity
3. **No terrain layers** — elevation/slope/aspect/hillshade COGs too large for Git
4. **Single worker** — concurrent request capacity limited
