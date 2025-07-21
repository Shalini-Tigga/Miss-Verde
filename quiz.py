import streamlit as st
import time
from utils import get_detailed_response

def generate_mcq(topic):
    prompt = (
        f"You are Miss Verde, a friendly and smart teacher.\n"
        f"Create ONE multiple-choice question on the topic: '{topic}'.\n"
        "Format exactly like this:\n\n"
        "Question: <your question>\n"
        "A. Option A\nB. Option B\nC. Option C\nD. Option D\n"
        "Correct Answer: <A/B/C/D>\n\n"
        "Keep it short, clear, and helpful."
    )
    return get_detailed_response(prompt)

def parse_mcq(response_text):
    lines = response_text.strip().splitlines()
    question = ""
    options = []
    answer = ""

    for line in lines:
        if not question and line.lower().startswith("question:"):
            question = line.split(":", 1)[1].strip()
        elif line.strip().startswith(("A.", "B.", "C.", "D.")):
            options.append(line.strip())
        elif "Correct Answer:" in line:
            answer = line.split("Correct Answer:")[-1].strip().upper()

    return question, options, answer

def quiz_tab():
    st.subheader("🧠 Miss Verde's Quiz Time")

    if "quiz_total" not in st.session_state:
        st.session_state.quiz_total = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_question" not in st.session_state:
        st.session_state.quiz_question = ""
        st.session_state.quiz_options = []
        st.session_state.correct_answer = ""
        st.session_state.user_answer = ""
        st.session_state.feedback = ""
        st.session_state.start_time = 0

    topic = st.text_input("Enter a topic for the quiz:", key="quiz_topic")

    if st.button("Generate Question"):
        with st.spinner("Miss Verde is preparing your quiz..."):
            response = generate_mcq(topic)
            q, opts, ans = parse_mcq(response)
            st.session_state.quiz_question = q
            st.session_state.quiz_options = opts
            st.session_state.correct_answer = ans
            st.session_state.user_answer = ""
            st.session_state.feedback = ""
            st.session_state.start_time = time.time()

    if st.session_state.quiz_question:

        st.markdown(f"**{st.session_state.quiz_question}**")

        for option in st.session_state.quiz_options:
            option_key = option[0]  # A/B/C/D
            if st.button(option, key=f"option_{option_key}"):
                st.session_state.user_answer = option_key
                elapsed = time.time() - st.session_state.start_time
                st.session_state.quiz_total += 1

                if elapsed > 30:
                    st.session_state.feedback = "⏱️ Time's up! Try to be quicker next time."
                elif st.session_state.user_answer == st.session_state.correct_answer:
                    st.session_state.feedback = "✅ Correct! Great job 🌿"
                    st.session_state.quiz_score += 1
                else:
                    st.session_state.feedback = f"❌ Oops! The correct answer was {st.session_state.correct_answer}."


    if st.session_state.feedback:
        st.markdown(f'<div class="bubble-verde"><strong>Miss Verde:</strong><br>{st.session_state.feedback}</div>', unsafe_allow_html=True)
        st.markdown(f"**Score:** {st.session_state.quiz_score}/{st.session_state.quiz_total}")

        if st.button("Try Another Question"):
            st.session_state.quiz_question = ""
            st.session_state.quiz_options = []
            st.session_state.correct_answer = ""
            st.session_state.user_answer = ""
            st.session_state.feedback = ""
            st.session_state.start_time = 0
