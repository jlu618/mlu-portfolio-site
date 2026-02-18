import streamlit as st
from pathlib import Path
from PIL import Image
import streamlit.components.v1 as components
import textwrap

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

with col2:
    html = textwrap.dedent("""
    <style>
    /* ===== Responsive base ===== */
    :root{
    --intro-fs: clamp(14px, 2.2vw, 18px);
    --title-fs: clamp(18px, 3.2vw, 28px);
    --card-fs:  clamp(14px, 2.1vw, 16px);
    --gap: clamp(10px, 2vw, 12px);
    }

    /* Your intro text */
    .mila-intro { 
    font-size: var(--intro-fs);
    line-height: 1.45;
    }

    /* Cards list */
    .mila-list {
    margin-top: 16px;
    display: flex;
    flex-direction: column;
    gap: var(--gap);
    }

    .mila-link { text-decoration:none; color:inherit; }

    .mila-item {
    position: relative;
    padding: 12px 14px 12px 18px;
    border-radius: 14px;
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(6px);
    transition: transform 0.12s ease, box-shadow 0.12s ease;
    font-size: var(--card-fs);
    }

    .mila-link:hover .mila-item {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }

    .mila-item::before {
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

    .mila-item.soon { opacity:0.55; cursor:default; }

    .mila-title { font-weight:700; }

    /* ===== Phone portrait ===== */
    @media (max-width: 480px) and (orientation: portrait) {
    :root{
        --intro-fs: 15px;
        --card-fs:  15px;
    }
    .mila-item { padding: 12px 12px 12px 16px; }
    }

    /* ===== Phone landscape ===== */
    @media (max-width: 900px) and (orientation: landscape) {
    :root{
        --intro-fs: 14px;
        --card-fs:  14px;
        --gap: 10px;
    }
    /* Make the paragraph less tall so it doesn't feel “cramped” */
    .mila-intro p { margin-top: -6px; }
    .mila-list { margin-top: 10px; }
    }

    /* ===== Small tablets ===== */
    @media (min-width: 481px) and (max-width: 900px) {
    :root{
        --intro-fs: 16px;
        --card-fs:  15px;
    }
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
    <a class="mila-link" href="/Photos">
        <div class="mila-item">📸 <span class="mila-title">Photos</span> — Memories in Frames</div>
    </a>

    <a class="mila-link" href="/Videos">
        <div class="mila-item">🎬 <span class="mila-title">Videos</span> — Moments in Motion</div>
    </a>

    <div class="mila-item soon">✍️ <span class="mila-title">Writings</span> — Coming Soon</div>
    <div class="mila-item soon">📄 <span class="mila-title">Resume</span> — Coming Soon</div>
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
