"""
GeoSlide-JK — Streamlit Companion Wrapper
Embeds the authoritative Next.js + FastAPI application hosted on Render.
This is NOT an independent dashboard. The full application runs at the public URL.
"""
from pathlib import Path
from PIL import Image
import streamlit as st

EMBLEM_PATH = Path(__file__).parent / "assets" / "geoslide-jk-emblem.png"
page_icon_asset = "🏔️"
if EMBLEM_PATH.exists():
    try:
        page_icon_asset = Image.open(EMBLEM_PATH)
    except Exception:
        pass

st.set_page_config(
    page_title="GeoSlide-JK | Landslide Risk Intelligence",
    page_icon=page_icon_asset,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide default Streamlit chrome for clean embedding
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp > header {display: none;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Get the public application URL from Streamlit secrets or environment
APP_URL = None

# Try Streamlit secrets first
try:
    APP_URL = st.secrets.get("GEOSLIDE_PUBLIC_APP_URL", None)
except Exception:
    pass

# Fallback to environment variable
if not APP_URL:
    import os
    APP_URL = os.environ.get("GEOSLIDE_PUBLIC_APP_URL", None)

if not APP_URL:
    # Default to public Render URL if no secret is set
    APP_URL = "https://geoslide-jk.onrender.com"

# Display the authoritative application via full-screen iframe wrapper
try:
    st.components.v1.iframe(APP_URL, height=900, scrolling=True)
except Exception:
    st.error(
        "⚠️ **GeoSlide-JK Service Connection Notice**\n\n"
        f"Unable to render iframe preview directly. [Click here to launch GeoSlide-JK full screen]({APP_URL})"
    )

st.markdown(
    f'<p style="text-align:center; color:#94a3b8; font-size:0.85rem; margin-top:0.5rem;">'
    f'<a href="{APP_URL}" target="_blank" style="color:#38bdf8;">Open GeoSlide-JK in full screen ↗</a>'
    f' &nbsp;|&nbsp; GeoSlide-JK is a research decision-support prototype and is not an official government warning system.'
    f'</p>',
    unsafe_allow_html=True,
)
