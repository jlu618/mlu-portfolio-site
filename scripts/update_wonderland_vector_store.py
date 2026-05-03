import time
from pathlib import Path
import streamlit as st
from openai import OpenAI

api_key = st.secrets["OPENAI_API_KEY"]
print("API KEY:", api_key[:10] if api_key else "None")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
print("Client initialized:", client)

# =========================
# Settings
# =========================

# First time: leave this blank: ""
VECTOR_STORE_ID = "vs_69f7977495148191935f490ac85ec4f0" # Wonderland id

VECTOR_STORE_NAME = "Wonderland Story"
PDF_PATH = Path("assets/writings_local/Wonderland_test.pdf")


# =========================
# Safety checks
# =========================

if not PDF_PATH.exists():
    raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

if PDF_PATH.suffix.lower() != ".pdf":
    raise ValueError("This script expects a PDF file.")


# =========================
# Create or reuse vector store
# =========================

if VECTOR_STORE_ID.strip():
    vector_store_id = VECTOR_STORE_ID.strip()
    print(f"Reusing vector store: {vector_store_id}")
else:
    vector_store = client.vector_stores.create(name=VECTOR_STORE_NAME)
    vector_store_id = vector_store.id
    print("Created new vector store:")
    print(vector_store_id)


# =========================
# Remove old files from vector store
# =========================

existing_files = client.vector_stores.files.list(
    vector_store_id=vector_store_id
)

if existing_files.data:
    print("Removing old files from vector store...")

for existing_file in existing_files.data:
    print(f"Removing: {existing_file.id}")
    client.vector_stores.files.delete(
        vector_store_id=vector_store_id,
        file_id=existing_file.id,
    )


# =========================
# Upload latest PDF
# =========================

print(f"Uploading PDF: {PDF_PATH}")

with PDF_PATH.open("rb") as f:
    uploaded_file = client.files.create(
        file=f,
        purpose="assistants",
    )

print("Uploaded file ID:")
print(uploaded_file.id)


# =========================
# Attach PDF to vector store
# =========================

vector_file = client.vector_stores.files.create(
    vector_store_id=vector_store_id,
    file_id=uploaded_file.id,
)

print("Attached file to vector store.")
print("Indexing...")


# =========================
# Wait for indexing
# =========================

while True:
    status = client.vector_stores.files.retrieve(
        vector_store_id=vector_store_id,
        file_id=uploaded_file.id,
    )

    print("Status:", status.status)

    if status.status == "completed":
        break

    if status.status in ["failed", "cancelled"]:
        raise RuntimeError(f"Indexing failed: {status.last_error}")

    time.sleep(2)


# =========================
# Done
# =========================

print("\nDone!")
print("Use this vector_store_id in writings.json:")
print(vector_store_id)