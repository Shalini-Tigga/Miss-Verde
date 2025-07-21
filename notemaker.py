import streamlit as st
from utils import get_detailed_response
from xhtml2pdf import pisa
from io import BytesIO

def convert_to_pdf(source_html):
    output = BytesIO()
    pisa_status = pisa.CreatePDF(source_html, dest=output)
    if pisa_status.err:
        return None
    return output

def notemaker_tab():
    st.subheader("📚 Make Study Notes with Miss Verde")

    if "notes" not in st.session_state:
        st.session_state.notes = ""
    if "notes_count" not in st.session_state:
        st.session_state.notes_count = 0

    topic = st.text_input("Enter a topic to generate notes:", key="notes_topic")

    if st.button("Generate Notes"):
        if not topic.strip():
            st.warning("Please enter a topic.")
            return

        with st.spinner("Miss Verde is preparing your notes... 🌿"):
            prompt = (
                f"You are Miss Verde, a brilliant and kind teacher.\n"
                f"Create comprehensive, well-formatted study notes on the topic: '{topic}'.\n"
                f"Use **headings**, bullet points, and code blocks where needed.\n"
                f"Begin with 'Miss Verde's Notes:' and use a friendly tone.\n"
            )
            response = get_detailed_response(prompt)
            st.session_state.notes = response
            st.session_state.notes_count += 1  # 🌟 Count notes made

    if st.session_state.notes:
        st.markdown("""<div class='bubble-verde'>""", unsafe_allow_html=True)
        st.markdown(st.session_state.notes)
        st.markdown("</div>", unsafe_allow_html=True)

        html_notes = f"""
        <html>
        <head><meta charset='utf-8'></head>
        <body>
        <h2>Miss Verde's Notes</h2>
        {st.session_state.notes.replace('\n', '<br>')}
        </body>
        </html>
        """

        pdf_file = convert_to_pdf(html_notes)
        if pdf_file:
            st.download_button(
                label="📄 Download Notes as PDF",
                data=pdf_file.getvalue(),
                file_name="Miss_Verde_Notes.pdf",
                mime="application/pdf",
                key="download_notes_pdf"
            )
