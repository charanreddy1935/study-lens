import streamlit as st
import google.generativeai as genai

def _extract_text_from_response(response):
    """
    Safely extract text from a google.generativeai response object.
    Supports single text, multi-part, candidates, and streamed responses.
    """
    try:
        return response.text
    except Exception:
        pass

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

    return str(response)

def generate_learning_content(user_input, user_profile, chat=None):
    """
    Generate a learning plan + quiz using Gemini.
    Uses the provided chat object (to preserve memory) or starts a new one.
    """
    if chat is None:
        chat = genai.GenerativeModel("gemini-pro-latest").start_chat(history=[])

    prompt = f"""
    Based on the user's profile: {user_profile}, generate a comprehensive learning path for the topic: {user_input}.
    Please include:
    1. A detailed lesson plan that explains the concept fully, with examples and illustrations.
    2. A set of 5 quiz questions based on the lesson, each with multiple-choice options and fully explained answers.
    """

    try:
        response = chat.send_message(prompt)
        return _extract_text_from_response(response)
    except Exception as e:
        return f"Error generating content: {str(e)}"

def run():
    st.header("📚 Personalized Learning Companion")

    # Initialize profile in session
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}

    # Collect user info
    name = st.text_input("Enter your name", key="name_input", label_visibility="visible", help="Provide your name to personalize your learning experience")
    if name:
        st.session_state.user_profile["name"] = name

    learning_goal = st.text_input("What do you want to learn today?", key="goal_input", label_visibility="visible", help="Enter the topic you want to explore")
    submit = st.button("Generate Learning Path", width="stretch")

    if submit and learning_goal:
        user_profile = st.session_state.user_profile
        learning_content = generate_learning_content(
            learning_goal, user_profile, chat=st.session_state.chat
        )

        if learning_content and not learning_content.startswith("Error"):
            st.subheader("✨ Here's your personalized learning content:")
            st.write(learning_content)
        else:
            st.error(f"⚠️ Sorry, we couldn't generate a proper response. {learning_content}")

        # Store in profile
        st.session_state.user_profile["learning_goal"] = learning_goal
        st.session_state.user_profile["learning_content"] = learning_content