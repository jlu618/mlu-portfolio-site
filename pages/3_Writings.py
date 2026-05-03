import json
import re
from datetime import datetime
from pathlib import Path
from openai import OpenAI
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="Writings", page_icon="📖", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
META_PATH = ROOT / "assets" / "data" / "writings.json"
FEEDBACK_FORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSdX4vc7KLKybteTHnubqs_0tRfA1eSQ87-iKKCRFVFISOhizA/viewform"
)
WONDERLAND_CHAT_SYSTEM_PROMPT = """
You are a friendly reading companion for Mila's story "Wonderland".

Answer only questions that are directly about the story, characters, setting,
plot, themes, scenes, or writing details found in the Wonderland document.
Use the file_search results as your only source of truth.

If a question is unrelated to Wonderland, politely say:
"I can only answer questions about Wonderland and Mila's writing on this page."

If the answer is not supported by the retrieved document context, say that the
writing page does not include enough information to answer. Do not guess, invent
plot details, or use outside knowledge.

Keep answers concise, warm, and appropriate for a family portfolio website.
"""


st.markdown(
    """
<style>
.block-container { padding-top: 1.2rem; padding-bottom: 2.5rem; }
.writing-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.2rem; }
.writing-meta { opacity: 0.7; font-size: 0.9rem; margin-bottom: 0.55rem; }
.writing-summary { line-height: 1.55; margin-bottom: 0.9rem; }
.writing-chip {
  display: inline-block;
  padding: 0.12rem 0.45rem;
  margin: 0.05rem 0.18rem 0.15rem 0;
  border: 1px solid rgba(49, 51, 63, 0.18);
  border-radius: 999px;
  font-size: 0.78rem;
  opacity: 0.82;
}
.pdf-frame iframe { border-radius: 8px; }
.feedback-intro {
  padding: 1rem 0 0.4rem 0;
  max-width: 760px;
}
.feedback-intro h3 {
  margin-bottom: 0.25rem;
}
.feedback-intro p {
  line-height: 1.5;
  opacity: 0.78;
  margin-top: 0;
}
.chat-footer {
  margin-top: 0.75rem;
  padding-top: 0.35rem;
}
@media (max-width: 640px){
  .block-container { padding-left: 0.9rem; padding-right: 0.9rem; }
  button[kind="secondary"], button[kind="primary"] { width: 100%; }
}
</style>
""",
    unsafe_allow_html=True,
)


def load_meta() -> dict:
    if not META_PATH.exists():
        return {"writings": []}

    try:
        data = json.loads(META_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"writings": []}

    if isinstance(data, list):
        return {"writings": data}
    return data if isinstance(data, dict) else {"writings": []}


def parse_date(date_str: str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None


def pretty_date(date_str: str) -> str:
    parsed = parse_date(date_str)
    return parsed.strftime("%b %d, %Y") if parsed else (date_str or "")


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


def drive_preview_url(url_or_id: str) -> str | None:
    file_id = get_drive_id(url_or_id)
    if not file_id:
        return None
    return f"https://drive.google.com/file/d/{file_id}/preview"


def drive_view_url(url_or_id: str) -> str:
    file_id = get_drive_id(url_or_id)
    if file_id:
        return f"https://drive.google.com/file/d/{file_id}/view"
    return url_or_id


def item_id(item: dict) -> str:
    return str(item.get("id") or get_drive_id(item.get("file", "")) or item.get("title", "")).strip()


def item_tags(item: dict) -> list[str]:
    tags = item.get("tags", [])
    return tags if isinstance(tags, list) else []


def meta_line(item: dict) -> str:
    parts = []
    if item.get("type"):
        parts.append(str(item.get("type")))
    if item.get("date"):
        parts.append(pretty_date(item.get("date")))
    if item.get("pages"):
        parts.append(f"{item.get('pages')} pages")
    return " - ".join(parts)


def select_writing(writing_id: str):
    st.query_params["writing"] = writing_id
    st.rerun()


def clear_selection():
    st.query_params.clear()
    st.rerun()

def show_feedback_section():
    st.divider()

    st.markdown("#### Share Feedback")
    st.caption("Leave a kind note, favorite scene, question, or encouragement for the author.")

    components.iframe(
        f"{FEEDBACK_FORM_URL}?embedded=true",
        height=520,
        scrolling=True,
    )

    st.link_button(
        "Open form in new tab",
        FEEDBACK_FORM_URL,
        use_container_width=True,
    )


meta = load_meta()
writings = meta.get("writings", [])

if not META_PATH.exists():
    st.error("Missing assets/data/writings.json")
    st.stop()

if not writings:
    st.title("Writings")
    st.info("No writing has been added yet.")
    st.stop()

writings_by_id = {item_id(item): item for item in writings if item_id(item)}
selected_id = st.query_params.get("writing")

if selected_id and selected_id in writings_by_id:
    writing = writings_by_id[selected_id]
    preview_url = drive_preview_url(writing.get("file", ""))

    st.button("Back to writings", on_click=clear_selection)
    st.title(writing.get("title", "Untitled"))

    if writing.get("summary"):
        st.markdown(writing.get("summary"))

    line = meta_line(writing)
    if line:
        st.caption(line)

    tags = item_tags(writing)
    if tags:
        st.markdown(
            "".join(f"<span class='writing-chip'>{tag}</span>" for tag in tags),
            unsafe_allow_html=True,
        )

    st.link_button("Open in Google Drive", drive_view_url(writing.get("file", "")))
    st.divider()

    if preview_url:
        st.markdown('<div class="pdf-frame">', unsafe_allow_html=True)
        components.iframe(preview_url, height=820, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("This writing does not have a valid Google Drive file URL.")
        st.code(writing.get("file", ""))

    st.stop()

st.title("Writings")

all_tags = sorted({tag for item in writings for tag in item_tags(item)})
all_types = sorted({item.get("type") for item in writings if item.get("type")})

with st.sidebar:
    st.header("Filter")
    type_pick = st.selectbox("Type", ["All"] + all_types) if all_types else "All"
    selected_tags = st.multiselect("Tags", all_tags) if all_tags else []
    sort_mode = st.selectbox("Sort", ["Newest first", "Oldest first", "Title A-Z"])

filtered = writings
if type_pick != "All":
    filtered = [item for item in filtered if item.get("type") == type_pick]
if selected_tags:
    filtered = [
        item
        for item in filtered
        if set(selected_tags).issubset(set(item_tags(item)))
    ]

if sort_mode == "Newest first":
    filtered = sorted(
        filtered,
        key=lambda item: parse_date(item.get("date", "")) or datetime.min,
        reverse=True,
    )
elif sort_mode == "Oldest first":
    filtered = sorted(
        filtered,
        key=lambda item: parse_date(item.get("date", "")) or datetime.min,
    )
else:
    filtered = sorted(filtered, key=lambda item: str(item.get("title", "")).lower())

if not filtered:
    st.info("No writings match your filters.")
    st.stop()

cols_per_row = 2
rows = (len(filtered) + cols_per_row - 1) // cols_per_row
idx = 0

for _ in range(rows):
    cols = st.columns(cols_per_row, gap="large")
    for col in cols:
        if idx >= len(filtered):
            break

        writing = filtered[idx]
        idx += 1
        writing_id = item_id(writing)

        with col:
            with st.container(border=True):
                st.markdown(
                    f"<div class='writing-title'>{writing.get('title', 'Untitled')}</div>",
                    unsafe_allow_html=True,
                )

                line = meta_line(writing)
                if line:
                    st.markdown(
                        f"<div class='writing-meta'>{line}</div>",
                        unsafe_allow_html=True,
                    )

                if writing.get("summary"):
                    st.markdown(
                        f"<div class='writing-summary'>{writing.get('summary')}</div>",
                        unsafe_allow_html=True,
                    )

                tags = item_tags(writing)
                if tags:
                    st.markdown(
                        "".join(f"<span class='writing-chip'>{tag}</span>" for tag in tags),
                        unsafe_allow_html=True,
                    )

                left, right = st.columns(2)
                with left:
                    st.button(
                        "Read on site",
                        key=f"read_{writing_id}",
                        on_click=select_writing,
                        args=(writing_id,),
                        use_container_width=True,
                    )
                with right:
                    st.link_button(
                        "Open PDF",
                        drive_view_url(writing.get("file", "")),
                        use_container_width=True,
                    )


# ---------- Chat about Wonderland (vector DB + LLM) ----------
st.markdown("### 💬 Ask about Wonderland")

if "OPENAI_API_KEY" not in st.secrets or "WONDERLAND_VECTOR_STORE_ID" not in st.secrets:
    st.info("Wonderland chat is not configured yet.")
else:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    vector_store_id = st.secrets["WONDERLAND_VECTOR_STORE_ID"]

    if "wonderland_messages" not in st.session_state:
        st.session_state.wonderland_messages = []

    for msg in st.session_state.wonderland_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.markdown('<div class="chat-footer">', unsafe_allow_html=True)
    with st.form("wonderland_chat_form", clear_on_submit=True):
        question_col, ask_col = st.columns([5, 1], vertical_alignment="bottom")
        with question_col:
            question = st.text_input(
                "Ask a question about Wonderland",
                placeholder="What would you like to know about Wonderland?",
            )
        with ask_col:
            submitted = st.form_submit_button("Ask", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if submitted and question.strip():
        question = question.strip()
        st.session_state.wonderland_messages.append({
            "role": "user",
            "content": question,
        })

        with st.spinner("Thinking..."):
            response = client.responses.create(
                model="gpt-4.1-mini",
                instructions=WONDERLAND_CHAT_SYSTEM_PROMPT,
                input=question,
                tools=[{
                    "type": "file_search",
                    "vector_store_ids": [vector_store_id],
                }],
            )

            answer = response.output_text

        st.session_state.wonderland_messages.append({
            "role": "assistant",
            "content": answer,
        })
        st.rerun()

show_feedback_section()
