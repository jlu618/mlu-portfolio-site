import streamlit as st
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title="Mila Lu | Portfolio",
    layout="wide",
)
st.markdown(
    """
    <style>
    a.anchor-link {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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
ROOT = Path(__file__).resolve().parent
profile_path = ROOT / "assets" / "profile" / "mila_profile_2025.jpg"

img = Image.open(profile_path)

# Create centered layout using spacer columns
sp1, col1, col2, sp2 = st.columns([1,2,4,1], vertical_alignment="top")

with col1:
    st.image(img, width=240)

import streamlit.components.v1 as components
import textwrap

with col2:
    html = textwrap.dedent("""
    <style>
    .mila-intro { font-size:18px; line-height:1.4; }

    .mila-list {
        margin-top:18px;
        display:flex;
        flex-direction:column;
        gap:12px;
    }

    /* ⭐ Make whole card clickable */
    .mila-link {
        text-decoration:none;
        color:inherit;
    }

    .mila-item {
        position:relative;
        padding:12px 14px 12px 18px;
        border-radius:14px;
        background: rgba(255,255,255,0.55);
        backdrop-filter: blur(6px);
        transition: transform 0.12s ease, box-shadow 0.12s ease;
    }

    /* Hover feel (desktop) */
    .mila-link:hover .mila-item {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }

    /* ⭐ Soft glow line */
    .mila-item::before {
        content:"";
        position:absolute;
        left:6px;
        top:8px;
        bottom:8px;
        width:4px;
        border-radius:10px;
        background: linear-gradient(
            180deg,
            rgba(255,255,255,0.8),
            rgba(200,200,200,0.35)
        );
        box-shadow: 0 0 8px rgba(255,255,255,0.35);
    }

    .mila-item.soon {
        opacity:0.55;
        cursor:default;
    }

    .mila-title {
        font-weight:700;
    }
    </style>


    <div class="mila-intro">
    <p style="margin-top:-10px;">
        Welcome to my personal website. I’m Mila — and this is a space where I share
        my experiences, creativity, and growth. I enjoy fashion, guitar, tennis, travel,
        storytelling, and exploring new ideas. My dad and I built this site together
        to document my journey and the moments that matter to me.
    </p>

    <div class="mila-list">

        <!-- ⭐ Photos link -->
        <a class="mila-link" href="/Photos">
        <div class="mila-item">
            📸 <span class="mila-title">Photos</span> — Memories in Frames
        </div>
        </a>

        <!-- ⭐ Videos link -->
        <a class="mila-link" href="/Videos">
        <div class="mila-item">
            🎬 <span class="mila-title">Videos</span> — Moments in Motion
        </div>
        </a>

        <!-- Coming soon items (not clickable) -->
        <div class="mila-item soon">
        ✍️ <span class="mila-title">Writings</span> — Coming Soon
        </div>

        <div class="mila-item soon">
        📄 <span class="mila-title">Resume</span> — Coming Soon
        </div>

    </div>
    </div>
    """)


    components.html(html, height=460, scrolling=True)



    


st.divider()
st.markdown(
    """
    <p style="text-align:center; opacity:0.7; font-size:14px;">
    Thanks to my Dad for making this website possible.
    </p>
    """,
    unsafe_allow_html=True,
)
