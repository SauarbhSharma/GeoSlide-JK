# Streamlit Wrapper Configuration

## Overview

The Streamlit deployment (`streamlit_app/streamlit_app.py`) is configured as a **minimal iframe wrapper** that embeds the authoritative Render-hosted Next.js + FastAPI application.

It does NOT contain independent widgets, duplicate maps, hardcoded metrics, or standalone calculations.

---

## Configuration Secret

Set the public application URL in **Streamlit Community Cloud → App Settings → Secrets**:

```toml
GEOSLIDE_PUBLIC_APP_URL = "https://geoslide-jk.onrender.com"
```

---

## Implementation Details

- **Entrypoint**: `streamlit_app/streamlit_app.py`
- **Dependencies**: `streamlit_app/requirements.txt` (`streamlit>=1.30.0`)
- **Layout**: `wide`, sidebar collapsed
- **CSS Styling**: Hides Streamlit header, footer, and menu for a clean full-viewport iframe experience.
- **Error Handling**: If `GEOSLIDE_PUBLIC_APP_URL` is absent, displays a clear configuration instruction warning instead of crashing.
- **Fallback Link**: Includes a direct link below the iframe: *"Open GeoSlide-JK in full screen ↗"*.
