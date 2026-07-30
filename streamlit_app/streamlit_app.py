"""
GeoSlide-JK — Streamlit Wrapper
Embeds the authoritative Next.js + FastAPI application hosted on Render.
This is NOT an independent dashboard. The full application runs at the public URL.
"""
import streamlit as st

st.set_page_config(
    page_title="GeoSlide-JK — Landslide Intelligence",
    page_icon="🏔️",
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
    st.error(
        "⚠️ **Configuration Required**\n\n"
        "The `GEOSLIDE_PUBLIC_APP_URL` secret is not configured.\n\n"
        "Set it in **Streamlit Community Cloud → App Settings → Secrets**:\n\n"
        "```toml\n"
        'GEOSLIDE_PUBLIC_APP_URL = "https://geoslide-jk.onrender.com"\n'
        "```\n\n"
        "This URL should point to the deployed GeoSlide-JK application on Render."
    )
    st.stop()

# Display the authoritative application
st.components.v1.iframe(APP_URL, height=900, scrolling=True)

st.markdown(
    f'<p style="text-align:center; color:#94a3b8; font-size:0.85rem; margin-top:0.5rem;">'
    f'<a href="{APP_URL}" target="_blank" style="color:#38bdf8;">Open GeoSlide-JK in full screen ↗</a>'
    f' &nbsp;|&nbsp; GeoSlide-JK is a research decision-support prototype and is not an official government warning system.'
    f'</p>',
    unsafe_allow_html=True,
)
