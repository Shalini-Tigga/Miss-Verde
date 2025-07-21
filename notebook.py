# notebook.py

import streamlit as st
import datetime

def notebook_tab():
    st.markdown("### 🗒️ Your Personal Notebook")
    st.markdown("_Jot down thoughts, goals, or anything on your mind._")

    if 'user_notes' not in st.session_state:
        st.session_state.user_notes = ""

    st.session_state.user_notes = st.text_area("📝 Start typing...", value=st.session_state.user_notes, height=300)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🧹 Clear"):
            st.session_state.user_notes = ""

    with col2:
        if st.download_button("📥 Download Notes", st.session_state.user_notes, file_name=f"notebook_{datetime.date.today()}.txt"):
            st.success("Downloaded successfully!")
