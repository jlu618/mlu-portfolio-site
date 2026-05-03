import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Summarize the Wonderland story in 5 bullet points.",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [st.secrets["WONDERLAND_VECTOR_STORE_ID"]],
    }],
)

print(response.output_text)