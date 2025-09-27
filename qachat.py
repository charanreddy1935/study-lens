import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ---------------------------
# Setup
# ---------------------------
load_dotenv()
api_key = os.getenv("GOOGLE-API-KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro-latest")

# ---------------------------
# Run Chat Function
# ---------------------------
def run_Chat():
    # Custom styled header
    st.markdown("""
        <h2 style='color: #fff; margin-bottom: 20px; text-align: center; 
                 font-family: Inter, Arial, sans-serif;'>AI Q&A Chat</h2>
    """, unsafe_allow_html=True)

    # Initialize session state for memory
    if "chat_session" not in st.session_state:
        # Start a persistent Gemini chat session
        st.session_state.chat_session = model.start_chat(history=[])

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input box
    input_text = st.text_input("Ask your question:", key="input", placeholder="Type your question here...")
    submit = st.button("Submit")

    chat_placeholder = st.container()

    # If user submits a question
    if submit and input_text:
        # Add user message to chat
        st.session_state.chat_history.append(("You", input_text))

        # Get Gemini response from persistent chat session
        response = st.session_state.chat_session.send_message(input_text, stream=True)

        bot_response = ""
        for chunk in response:
            if hasattr(chunk, "text"):
                bot_response += chunk.text

        if bot_response.strip():
            st.session_state.chat_history.append(("Bot", bot_response))

    # ---------------------------
    # Display Chat
    # ---------------------------
    with chat_placeholder:
        for role, text in st.session_state.chat_history:
            if role == "You":
                st.markdown(f"""
                    <div style='text-align: right; background: linear-gradient(135deg, #2c3e50, #3498db); 
                         color: #ffffff; padding: 14px; border-radius: 12px; margin: 8px 0; 
                         box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2); border-radius: 12px;'>{text}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='text-align: left; background: #1a1a1a; color: #ffffff; 
                         padding: 14px; border-radius: 12px; margin: 8px 0; 
                         border: 1px solid #333;'>{text}</div>
                """, unsafe_allow_html=True)

        # Auto-scroll to bottom
        st.markdown("<div id='scroll_anchor'></div>", unsafe_allow_html=True)
        st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    run_Chat()
