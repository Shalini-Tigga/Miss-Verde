import streamlit as st
from utils import get_detailed_response

def chat_tab():
    st.subheader("🌿 Ask Miss Verde Anything")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""
    if "chat_count" not in st.session_state:
        st.session_state.chat_count = 0

    user_message = st.text_input("You:", value=st.session_state.chat_input, key="chat_input_box")

    if st.button("Ask Miss Verde"):
        user_message = user_message.strip()

        if user_message and (
            not st.session_state.chat_history or 
            st.session_state.chat_history[-1][1] != user_message
        ):
            # Append user message
            st.session_state.chat_history.append(("user", user_message))
            st.session_state.chat_count += 1

            # Get response
            with st.spinner("Miss Verde is thinking... 🌿"):
                verde_reply = get_detailed_response(user_message)
            st.session_state.chat_history.append(("verde", verde_reply))

            # Clear input after asking
            st.session_state.chat_input = ""
            st.rerun()

    # Render the chat history (reverse order for latest on top)
    for role, msg in reversed(st.session_state.chat_history):
        if role == "user":
            st.markdown(f'<div class="bubble-user"><strong>You:</strong><br>{msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-verde"><strong>Miss Verde:</strong><br>{msg}</div>', unsafe_allow_html=True)
