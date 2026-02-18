import json
from pathlib import Path
from datetime import datetime

import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(page_title="My Photo Scrapbook", page_icon="📸", layout="wide")

# --- Paths ---
ROOT = Path(__file__).resolve().parents[1]
PHOTOS_DIR = ROOT / "assets" / "photos"
META_PATH = ROOT / "assets" / "data" / "photos.json"

st.title("Photos")

# --- Load metadata ---
if not META_PATH.exists():
    st.error(f"Missing metadata file: {META_PATH}")
    st.stop()

with META_PATH.open("r", encoding="utf-8") as f:
    items = json.load(f)

if not isinstance(items, list):
    st.error("photos.json should be a JSON list (array) of photo objects.")
    st.stop()

# --- Utilities ---
def safe_date(s: str) -> datetime:
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return datetime(1900, 1, 1)

@st.cache_data(show_spinner=False)
def load_image(rel_path: str):
    img_path = PHOTOS_DIR / rel_path
    img = Image.open(img_path)
    img = ImageOps.exif_transpose(img)
    return img

def file_exists(rel_path: str) -> bool:
    return (PHOTOS_DIR / rel_path).exists()

def album_of(rel_path: str) -> str:
    parts = rel_path.split("/")
    return parts[0] if len(parts) > 1 else "other"

def open_details(photo_key: str):
    st.session_state.selected_photo_key = photo_key

def close_details():
    st.session_state.selected_photo_key = None

# --- Pro mobile CSS (compact + tappable) ---
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

# --- Sidebar filters ---
st.sidebar.header("Filter")

albums = sorted({album_of(x.get("file", "")) for x in items if x.get("file")})
album_labels = {"life": "Life", "model": "Model", "other": "Other"}
album_options = ["All"] + [album_labels.get(a, a.title()) for a in albums]
label_to_album = {album_labels.get(a, a.title()): a for a in albums}
label_to_album["All"] = "ALL"

album_pick = st.sidebar.selectbox("Album", album_options)
album_key = label_to_album.get(album_pick, "ALL")

all_tags = sorted({t for x in items for t in x.get("tags", []) if isinstance(t, str)})
selected_tags = st.sidebar.multiselect("Tags", all_tags)

sort_mode = st.sidebar.selectbox("Sort", ["Newest first", "Oldest first", "A → Z"])
thumbs_per_row = st.sidebar.slider("Photos per row", 2, 6, 4)

# --- Filter items ---
filtered = items

if album_key != "ALL":
    filtered = [x for x in filtered if album_of(x.get("file", "")) == album_key]

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

# --- Selected item state (key, not whole dict) ---
# Using a stable key fixes "sometimes needs two clicks" issues.
if "selected_photo_key" not in st.session_state:
    st.session_state.selected_photo_key = None

def key_for_item(x: dict) -> str:
    # file path is unique in your dataset; perfect as a stable key
    return str(x.get("file", "")).strip()

items_by_key = {key_for_item(x): x for x in items if key_for_item(x)}

# =========================
# Details modal (no scrolling, mobile-friendly)
# =========================
sel_key = st.session_state.selected_photo_key
if sel_key and sel_key in items_by_key:
    x = items_by_key[sel_key]
    rel = x.get("file", "")
    title = x.get("title", "Untitled")
    date = x.get("date", "")
    tags = x.get("tags", [])
    story = (x.get("story") or "").strip()

    with st.dialog(title, width="large"):
        left, right = st.columns([3, 2], gap="large")

        with left:
            if file_exists(rel):
                st.image(load_image(rel), use_container_width=True)
            else:
                st.error(f"Missing file: {rel}")

        with right:
            if title:
                st.markdown(f"### **{title}**")
            if date:
                st.markdown(f"🗓️ **Date:** {date}")
            if tags:
                st.markdown("🏷️ " + " · ".join(tags))

            st.markdown("### Story")
            st.write(story if story else "No story yet — add one in photos.json!")

            st.button("Close", type="primary", on_click=close_details, use_container_width=True)

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
            if file_exists(rel):
                st.image(load_image(rel), use_container_width=True)
            else:
                st.error("Missing image")

            # Title outside image box
            st.markdown(f"**{title}**")

            # Use on_click callback -> more responsive (no double click)
            st.button(
                "View details",
                key=f"select_{k}",
                on_click=open_details,
                args=(k,),
                use_container_width=True,
            )


