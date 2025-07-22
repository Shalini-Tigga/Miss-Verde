from huggingface_hub import InferenceClient
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN") 
client = InferenceClient(model="meta-llama/Llama-3.1-8B-Instruct", token=HF_TOKEN)

def chunk_text(text, chunk_size=1200):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def get_detailed_response(prompt, system_instruction="You are Miss Verde, a kind teacher."):
    chunks = chunk_text(prompt)
    responses = []

    for chunk in chunks:
        full_prompt = f"{system_instruction}\n\n{chunk.strip()}\n\nContinue explaining if needed."
        try:
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=700,
                temperature=0.7
            )
            answer = resp.choices[0].message.content.strip()
            responses.append(answer)
        except Exception as e:
            responses.append(f"❌ Error: {e}")
            break

    return "\n\n".join(responses)

def set_theme(dark_mode):
    dark_css = """
    <style>
    :root {
        --bg-color: #1e1e1e;
        --text-color: #e0e0e0;
        --card-color: #2e2e2e;
        --accent-color: #90ee90;
    }

    body, .stApp, .block-container {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }

    .stButton>button {
        background-color: var(--card-color);
        color: var(--text-color);
        border: 1px solid var(--accent-color);
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--accent-color) !important;
    }
    </style>
    """

    light_css = """
    <style>
    :root {
        --bg-color: #ffffff;
        --text-color: #000000;
        --card-color: #f5f5f5;
        --accent-color: #228b22;
    }

    body, .stApp, .block-container {
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
    }

    .stButton>button {
        background-color: var(--card-color);
        color: var(--text-color);
        border: 1px solid var(--accent-color);
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--accent-color) !important;
    }
    </style>
    """

    st.markdown(dark_css if dark_mode else light_css, unsafe_allow_html=True)
