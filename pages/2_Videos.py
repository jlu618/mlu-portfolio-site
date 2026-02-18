import json
from pathlib import Path
from datetime import datetime

import streamlit as st

# =========================
# Page config
# =========================
st.set_page_config(page_title="Videos", page_icon="🎬", layout="wide")

# =========================
# Paths  ⭐ UPDATED FOR /assets/
# =========================
ROOT = Path(__file__).resolve().parents[1]

ASSETS_DIR = ROOT / "assets"
DATA_DIR = ASSETS_DIR / "data"
VIDEOS_DIR = ASSETS_DIR / "videos"
META_PATH = DATA_DIR / "videos.json"


# =========================
# Helpers
# =========================
def load_meta():
    if not META_PATH.exists():
        return {"videos": []}
    try:
        return json.loads(META_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"videos": []}


def video_path(file_name: str):
    return VIDEOS_DIR / file_name


def parse_date(date_str: str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None


def pretty_date(date_str: str):
    d = parse_date(date_str)
    return d.strftime("%b %d, %Y") if d else (date_str or "—")


# =========================
# Header
# =========================
st.title("🎬 Videos")

meta = load_meta()
videos = meta.get("videos", [])

if not META_PATH.exists():
    st.error("Missing assets/data/videos.json")
    st.stop()

st.divider()

# =========================
# Dialog popup
# =========================
@st.dialog("Video Details", width="large")
def details_dialog(v):
    st.markdown(f"## **{v.get('title','Untitled')}**")

    if v.get("date"):
        st.caption(pretty_date(v.get("date")))

    fp = video_path(v.get("file", ""))

    if not fp.exists():
        st.error(f"Video not found: {fp}")
        return

    st.video(str(fp))

    tags = ", ".join(v.get("tags", []))
    if tags:
        st.caption(tags)

    st.caption("Story")
    st.write(v.get("story") or "—")

# =========================
# Gallery grid
# =========================
if not videos:
    st.info("No videos found in videos.json")
    st.stop()

cols_per_row = 3
rows = (len(videos) + cols_per_row - 1) // cols_per_row
idx = 0

for _ in range(rows):
    cols = st.columns(cols_per_row, gap="large")

    for col in cols:
        if idx >= len(videos):
            break

        v = videos[idx]
        idx += 1

        with col:
            st.markdown(f"**{v.get('title','Untitled')}**")

            if v.get("date"):
                st.caption(pretty_date(v.get("date")))

            fp = video_path(v.get("file", ""))

            if fp.exists():
                st.video(str(fp))
            else:
                st.warning("Preview unavailable")
                st.code(f"Expected: assets/videos/{v.get('file')}")

            tag_line = ", ".join(v.get("tags", []))
            if tag_line:
                st.caption(tag_line)

            vid = v.get("id")

            if st.button("View details", key=f"view_{vid}", use_container_width=True):
                details_dialog(v)
