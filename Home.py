import streamlit as st
from pathlib import Path
from PIL import Image
import streamlit.components.v1 as components
import textwrap
import base64

st.set_page_config(
    page_title="Mila Lu | Portfolio",
    layout="wide",
)

st.markdown("""
<style>
/* Intro paragraph (same DOM as Streamlit, no iframe) */
.mila-intro{
  font-size: clamp(14px, 2.2vw, 18px);
  line-height: 1.55;
  margin-top: 5px;              /* aligns with top of photo better */
  max-width: 52ch;              /* keeps line length nice on wide screens */
  margin-bottom: 22px;   
}

.mila-intro p{
  margin: 0;                    /* remove default paragraph margin */
}

/* Mobile tweaks */
@media (max-width: 640px){
  .mila-intro{
    margin-top: 0px;
    max-width: 100%;
  }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Make st.page_link look like your Mila cards */
a[data-testid="stPageLink-NavLink"]{
  text-decoration: none !important;
  color: inherit !important;
  display: block;
  margin-bottom: 12px;
}

a[data-testid="stPageLink-NavLink"] > div{
  position: relative;
  padding: 12px 14px 12px 18px;
  border-radius: 14px;
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(6px);
  transition: transform 0.12s ease, box-shadow 0.12s ease;
}

/* Soft glow line */
a[data-testid="stPageLink-NavLink"] > div::before{
  content:"";
  position:absolute;
  left:6px;
  top:8px;
  bottom:8px;
  width:4px;
  border-radius:10px;
  background: linear-gradient(180deg, rgba(255,255,255,0.8), rgba(200,200,200,0.35));
  box-shadow: 0 0 8px rgba(255,255,255,0.35);
}

/* Hover feel */
a[data-testid="stPageLink-NavLink"]:hover > div{
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------- Centered Title ----------
st.markdown(
    """
    <div style="display:flex; justify-content:center; width:100%;">
        <div style="text-align:center;">
            <h1 style="margin-bottom:4px;">Mila Lu</h1>
            <p style="font-size:15px; opacity:0.7; margin-top:0;">
                Stories • Growth • Memories
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.write("")  # spacing

# ---------- Centered Profile + Text (side by side) ----------
import streamlit as st
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
profile_path = ROOT / "assets" / "profile" / "mila_profile_2025.jpg"

# --- Responsive sizing CSS (works for st.image because it renders an <img>) ---
st.markdown("""
<style>
/* target the first image in the first column area is hard, so we use a wrapper class */
.mila-profile-host img {
  width: clamp(140px, 28vw, 240px) !important;
  height: auto !important;
  border-radius: 18px !important;
  object-fit: cover !important;
  display:block;
  margin-left:auto;
  margin-right:auto;
}

/* Phone portrait */
@media (max-width: 480px) and (orientation: portrait) {
  .mila-profile-host img { width: 160px !important; }
}

/* Phone landscape */
@media (max-width: 900px) and (orientation: landscape) {
  .mila-profile-host img { width: 140px !important; }
}
</style>
""", unsafe_allow_html=True)

sp1, col1, col2, sp2 = st.columns([1,2,4,1], vertical_alignment="top")

@st.cache_data(show_spinner=False)
def load_profile(path: str):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    return im

with col1:
    st.markdown('<div class="mila-profile-host">', unsafe_allow_html=True)

    # ✅ show spinner while it loads/decodes (especially first time on mobile)
    with st.spinner("Loading..."):
        st.image(load_profile(str(profile_path)))

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown(
        """
        <div class="mila-intro">
          <p>
            Welcome to my personal website. I’m Mila — and this is a space where I share
            my experiences, hobbies, and ideas. I enjoy fashion, guitar, tennis, traveling,
            hiking, and exploring new ideas. My dad and I built this site together
            to document my journey and the moments that matter to me.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link("pages/1_Photos.py", label="📸  Photos — Memories in Frames")
    st.page_link("pages/2_Videos.py", label="🎬  Videos — Moments in Motion")
    st.page_link("pages/3_Writings.py", label="✍️  Writings — Coming Soon")
    # st.page_link("pages/4_Resume.py", label="📄  Resume — Coming Soon")


st.divider()
st.markdown(
    """
    <p style="text-align:center; opacity:0.7; font-size:14px;">
    Thanks to my Dad for making this website possible.
    </p>
    """,
    unsafe_allow_html=True,
)
