import json
import re
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Videos", page_icon="🎬", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "assets" / "data" / "videos.json"


def load_meta():
    if not META_PATH.exists():
        return {"videos": []}
    try:
        return json.loads(META_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"videos": []}


def get_drive_id(url_or_id: str) -> str | None:
    if not url_or_id:
        return None

    file_match = re.search(r"drive\.google\.com/file/d/([^/]+)", url_or_id)
    if file_match:
        return file_match.group(1)

    id_match = re.search(r"[?&]id=([^&]+)", url_or_id)
    if id_match:
        return id_match.group(1)

    return url_or_id if re.fullmatch(r"[-\w]{20,}", url_or_id) else None


def google_drive_video_preview_url(url_or_id: str) -> str | None:
    file_id = get_drive_id(url_or_id)
    if not file_id:
        return None
    return f"https://drive.google.com/file/d/{file_id}/preview"


def show_drive_video(video: dict, height: int = 360):
    source = video.get("drive_id") or video.get("file", "")
    preview_url = google_drive_video_preview_url(source)

    if not preview_url:
        st.warning("Preview unavailable")
        st.code(source or "Missing Google Drive file URL")
        return

    components.iframe(preview_url, height=height)


def parse_date(date_str: str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None


def pretty_date(date_str: str):
    d = parse_date(date_str)
    return d.strftime("%b %d, %Y") if d else (date_str or "")


st.title("🎬 Videos")

if not META_PATH.exists():
    st.error("Missing assets/data/videos.json")
    st.stop()

meta = load_meta()
videos = meta.get("videos", [])

st.divider()


@st.dialog("Video Details", width="large")
def details_dialog(video: dict):
    st.markdown(f"## **{video.get('title', 'Untitled')}**")

    if video.get("date"):
        st.caption(pretty_date(video.get("date")))

    show_drive_video(video, height=420)

    tags = ", ".join(video.get("tags", []))
    if tags:
        st.caption(tags)

    st.caption("Story")
    st.write(video.get("story") or "")


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

        video = videos[idx]
        idx += 1

        with col:
            st.markdown(f"**{video.get('title', 'Untitled')}**")

            if video.get("date"):
                st.caption(pretty_date(video.get("date")))

            show_drive_video(video, height=320)

            tag_line = ", ".join(video.get("tags", []))
            if tag_line:
                st.caption(tag_line)

            video_id = video.get("id") or get_drive_id(video.get("file", "")) or idx

            if st.button("View details", key=f"view_{video_id}", use_container_width=True):
                details_dialog(video)
