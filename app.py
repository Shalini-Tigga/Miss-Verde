import streamlit as st
from chat import chat_tab
from homework_solver import homework_tab
from quiz import quiz_tab
from notemaker import notemaker_tab
from notebook import notebook_tab
from utils import set_theme
import random

st.set_page_config(page_title="Miss Verde", layout="wide")

# 🌿 Custom CSS
def apply_custom_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

apply_custom_css()

# 🌙 Theme Toggle
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
st.sidebar.markdown("### Theme")
st.session_state.dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)

# 🎨 Apply theme
set_theme(st.session_state.dark_mode)

# 🌿 Persistent header
st.markdown("<h1 class='verde-title'>Miss Verde 🌿</h1><hr>", unsafe_allow_html=True)

# 🌸 Landing page logic
if "show_landing" not in st.session_state:
    st.session_state.show_landing = True

if st.session_state.show_landing:
    st.markdown(
        """
        <div class='landing-box'>
            <h1>🎉 <span class='verde-title'>Welcome to Miss Verde</span> 🌿</h1>
            <p class='tagline'>Your AI Teacher & Study BFF</p>
            <p class='desc'>Learn. Quiz. Grow. Let’s bloom together 💚</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Start Learning 🌸"):
        st.session_state.show_landing = False
        st.rerun()
    st.stop()

# 🏆 Recap Summary Popup
def check_milestone_popup():
    chat = st.session_state.get("chat_count", 0)
    notes = st.session_state.get("notes_count", 0)
    score = st.session_state.get("quiz_score", 0)

    if not st.session_state.get("popup_shown", False):
        if chat >= 5 or notes >= 5 or score >= 5:
            with st.popover("🎉 Milestone Unlocked!"):
                st.markdown("### 🏆 Final Recap Summary")
                st.markdown(f"**🗨️ You asked {chat} questions**")
                st.markdown(f"**📝 Made {notes} notes**")
                st.markdown(f"**🧠 Quiz Score: {score}/{st.session_state.get('quiz_total', 0)}**")
                st.success("You're doing amazing 🌿 Keep it up!")
            st.session_state.popup_shown = True

check_milestone_popup()

# 🧭 Sidebar Navigation
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "💬 Chat"
if 'view' not in st.session_state:
    st.session_state.view = "main"

st.sidebar.markdown("### 📚 Choose a Mode")
selected = st.sidebar.radio(
    "Go to",
    ["💬 Chat", "📄 Upload Homework", "❓ Quiz", "📝 Notemaking", "🗒️ Personal Notebook"],
    index=["💬 Chat", "📄 Upload Homework", "❓ Quiz", "📝 Notemaking", "🗒️ Personal Notebook"].index(st.session_state.active_tab),
    label_visibility="collapsed"
)
st.session_state.active_tab = selected

# 🔀 Page Routing
if selected == "🗒️ Personal Notebook":
    notebook_tab()
else:
    if selected == "💬 Chat":
        chat_tab()
    elif selected == "📄 Upload Homework":
        homework_tab()
    elif selected == "❓ Quiz":
        quiz_tab()
    elif selected == "📝 Notemaking":
        notemaker_tab()
