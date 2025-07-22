import streamlit as st
import PyPDF2
from huggingface_hub import InferenceClient
import os
from utils import get_detailed_response
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN") 
client = InferenceClient(model="meta-llama/Llama-3.1-8B-Instruct", token=HF_TOKEN)

def extract_text(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:  # assume plain text
        return str(file.read(), "utf-8")

def get_solution(text):
    prompt = (
        "A student has uploaded the following homework question(s):\n\n"
        f"{text.strip()}\n\n"
        "Please explain the solution in detail, step by step, in a way a student can understand."
    )
    return get_detailed_response(prompt)

def homework_tab():
    st.subheader("📄 Upload Homework")
    
    if "uploaded_text" not in st.session_state:
        st.session_state.uploaded_text = ""
    if "solution_text" not in st.session_state:
        st.session_state.solution_text = ""

    uploaded_file = st.file_uploader("Upload your homework (PDF or TXT)", type=["pdf", "txt"])

    if uploaded_file:
        with st.spinner("Miss Verde is reading your homework..."):
            st.session_state.uploaded_text = extract_text(uploaded_file)

    if st.session_state.uploaded_text:
        st.text_area("📜 Homework Preview", st.session_state.uploaded_text, height=300)

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🧠 Get Solution"):
                with st.spinner("Miss Verde is solving it for you..."):
                    st.session_state.solution_text = get_solution(st.session_state.uploaded_text)

        with col2:
            if st.button("🧼 Clear"):
                st.session_state.uploaded_text = ""
                st.session_state.solution_text = ""

    if st.session_state.solution_text:
        st.markdown("### ✅ Miss Verde’s Explanation")
        st.markdown(st.session_state.solution_text)