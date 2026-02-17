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

# --- Selected item state ---
if "selected_photo" not in st.session_state:
    st.session_state.selected_photo = None

# ✅ Detail view placeholder BEFORE the gallery (so it shows at the top)
detail_container = st.container()

with detail_container:
    if st.session_state.selected_photo:
        x = st.session_state.selected_photo
        rel = x.get("file", "")
        title = x.get("title", "Untitled")
        date = x.get("date", "")
        tags = x.get("tags", [])
        story = (x.get("story") or "").strip()

        st.markdown(f"## {title}")

        left, right = st.columns([3, 2], vertical_alignment="top")

        with left:
            if file_exists(rel):
                st.image(load_image(rel), use_container_width=True)
            else:
                st.error(f"Missing file: {rel}")

        with right:
            if date:
                st.markdown(f"🗓️ **Date:** {date}")
            if tags:
                st.markdown("🏷️ " + " · ".join(tags))

            st.markdown("### Story")
            st.write(story if story else "No story yet — add one in photos.json!")

            if st.button("Close", key="close_detail", use_container_width=True):
                st.session_state.selected_photo = None
                st.rerun()


        st.divider()
    else:
        st.caption("Click **View Details** to view it larger with its story.")

# =========================
# Gallery
# =========================
st.subheader("Gallery")

cols = st.columns(thumbs_per_row)

for i, x in enumerate(filtered):
    rel = x.get("file", "")
    title = x.get("title", "Untitled")

    with cols[i % thumbs_per_row]:
        with st.container(border=True):
            if file_exists(rel):
                st.image(load_image(rel), use_container_width=True)
            else:
                st.error("Missing image")

            # ✅ Title as bold text (no box)
            st.markdown(f"**{title}**")

            # ✅ Clickable action without "Open"/"Favorites" wording
            if st.button("View details", key=f"select_{rel}", use_container_width=True):
                st.session_state.selected_photo = x
                st.rerun()

