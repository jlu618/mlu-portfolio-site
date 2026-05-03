# pages/1_Photos.py
import json
from pathlib import Path
from datetime import datetime

import streamlit as st
import re

ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "assets" / "data" / "photos.json"

# =========================
# Page config
# =========================
st.set_page_config(page_title="My Photo Scrapbook", page_icon="📸", layout="wide")

st.title("Photos")

# =========================
# Load metadata
# =========================
if not META_PATH.exists():
    st.error(f"Missing metadata file: {META_PATH}")
    st.stop()

with META_PATH.open("r", encoding="utf-8") as f:
    items = json.load(f)

if not isinstance(items, list):
    st.error("photos.json should be a JSON list (array) of photo objects.")
    st.stop()

# =========================
# Utilities
# =========================
def safe_date(s: str) -> datetime:
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return datetime(1900, 1, 1)

def key_for_item(x: dict) -> str:
    # In your data, file path is a stable unique key
    return str(x.get("file", "")).strip()

def open_details(photo_key: str):
    st.session_state.selected_photo_key = photo_key

def get_drive_id(url: str) -> str | None:
    match = re.search(r"/d/([^/]+)", url)
    return match.group(1) if match else None

def google_drive_image_url(url: str, width: int = 1200) -> str:
    file_id = get_drive_id(url)
    if not file_id:
        return url
    return f"https://drive.google.com/thumbnail?id={file_id}&sz=w{width}"

# =========================
# Pro mobile CSS
# =========================
st.markdown(
    """
<style>
.block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; }
@media (max-width: 640px){
  .block-container { padding-left: 0.9rem; padding-right: 0.9rem; }
  button[kind="secondary"], button[kind="primary"] { width: 100%; }
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# Sidebar filters
# =========================
st.sidebar.header("Filter")

all_tags = sorted({t for x in items for t in x.get("tags", []) if isinstance(t, str)})
selected_tags = st.sidebar.multiselect("Tags", all_tags)

sort_mode = st.sidebar.selectbox("Sort", ["Newest first", "Oldest first", "A - Z"])
thumbs_per_row = st.sidebar.slider("Photos per row", 2, 6, 4)

# =========================
# Filter items
# =========================
filtered = items

if selected_tags:
    filtered = [x for x in filtered if set(selected_tags).issubset(set(x.get("tags", [])))]

if sort_mode == "Newest first":
    filtered = sorted(filtered, key=lambda x: safe_date(x.get("date", "")), reverse=True)
elif sort_mode == "Oldest first":
    filtered = sorted(filtered, key=lambda x: safe_date(x.get("date", "")))
else:
    filtered = sorted(filtered, key=lambda x: str(x.get("title", "")).lower())

if not filtered:
    st.info("No photos match your filters. Try clearing tags.")
    st.stop()

# =========================
# Selected item state (stable key)
# =========================
if "selected_photo_key" not in st.session_state:
    st.session_state.selected_photo_key = None

items_by_key = {key_for_item(x): x for x in items if key_for_item(x)}

# =========================
# Dialog popup
# =========================
@st.dialog("Photo Details", width="large")
def details_dialog(x: dict):
    rel = x.get("file", "")
    title = x.get("title", "Untitled")
    date = x.get("date", "")
    tags = x.get("tags", [])
    story = (x.get("story") or "").strip()

    st.markdown(f"## **{title}**")

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.image(
            google_drive_image_url(rel, width=1600),
            use_container_width=True
        )
    with right:
        if date:
            st.markdown(f"🗓️ **Date:** {date}")
        if tags:
            st.markdown("🏷️ " + " · ".join(tags))

        st.markdown("### Story")
        st.write(story if story else "No story yet — add one in photos.json!")

    # No Close button — use the dialog's built-in X to close

# If a photo is selected, open the dialog
sel_key = st.session_state.get("selected_photo_key")
if sel_key and sel_key in items_by_key:
    details_dialog(items_by_key[sel_key])

# =========================
# Gallery
# =========================
st.subheader("Gallery")
st.caption("Tap **View details** to open the photo instantly in a pop-up (great on mobile).")

cols = st.columns(thumbs_per_row, gap="large")

for i, x in enumerate(filtered):
    rel = x.get("file", "")
    title = x.get("title", "Untitled")
    k = key_for_item(x)

    with cols[i % thumbs_per_row]:
        with st.container(border=True):
            st.image(
                google_drive_image_url(rel, width=800),
                use_container_width=True
            )

            st.markdown(f"**{title}**")

            st.button(
                "View details",
                key=f"select_{k}",
                on_click=open_details,
                args=(k,),
                use_container_width=True,
            )
