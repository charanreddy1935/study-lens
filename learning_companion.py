import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

# Initialize model + persistent chat
model = genai.GenerativeModel("gemini-pro-latest")
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])


def _extract_text_from_response(response):
    """
    Safely extract text from a google.generativeai response object.
    Supports single text, multi-part, candidates, and streamed responses.
    """
    # 1) Try direct accessor
    try:
        return response.text
    except Exception:
        pass

    # 2) response.result.parts
    try:
        result = getattr(response, "result", None)
        if result is not None and hasattr(result, "parts"):
            out = []
            for p in result.parts:
                if hasattr(p, "text"):
                    out.append(p.text)
                elif isinstance(p, str):
                    out.append(p)
            if out:
                return "".join(out)
    except Exception:
        pass

    # 3) candidates -> content.parts
    try:
        candidates = getattr(response, "candidates", None)
        if candidates:
            out = []
            for cand in candidates:
                content = getattr(cand, "content", None)
                if content and hasattr(content, "parts"):
                    for p in content.parts:
                        if hasattr(p, "text"):
                            out.append(p.text)
                        elif isinstance(p, str):
                            out.append(p)
            if out:
                return "".join(out)
    except Exception:
        pass

    # 4) Streamed iterable
    try:
        out = []
        for chunk in response:
            if hasattr(chunk, "text"):
                out.append(chunk.text)
            elif isinstance(chunk, str):
                out.append(chunk)
        if out:
            return "".join(out)
    except Exception:
        pass

    # 5) Fallback
    return str(response)


def generate_learning_content(user_input, user_profile, chat=None):
    """
    Generate a learning plan + quiz using Gemini.
    Uses the provided chat object (to preserve memory) or starts a new one.
    """
    if chat is None:
        chat = model.start_chat(history=[])

    prompt = f"""
    Based on the user's profile: {user_profile}, generate a comprehensive learning path for the topic: {user_input}.
    Please include:
    1. A detailed lesson plan that explains the concept fully, with examples and illustrations.
    2. A set of 5 quiz questions based on the lesson, each with multiple-choice options and fully explained answers.
    """

    response = chat.send_message(prompt)
    return _extract_text_from_response(response)


def run():
    st.header("📚 Personalized Learning Companion")

    # Initialize profile in session
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}

    # Collect user info
    name = st.text_input("What's your name?", key="name_input")
    if name:
        st.session_state.user_profile["name"] = name

    learning_goal = st.text_input("What do you want to learn today?", key="goal_input")
    submit = st.button("Generate Learning Path")

    if submit and learning_goal:
        user_profile = st.session_state.user_profile
        learning_content = generate_learning_content(
            learning_goal, user_profile, chat=st.session_state.chat
        )

        if learning_content:
            st.subheader("✨ Here's your personalized learning content:")
            st.write(learning_content)
        else:
            st.error("⚠️ Sorry, we couldn't generate a proper response. Please try again.")

        # Store in profile
        st.session_state.user_profile["learning_goal"] = learning_goal
        st.session_state.user_profile["learning_content"] = learning_content


if __name__ == "__main__":
    run()
