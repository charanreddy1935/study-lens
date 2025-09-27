import streamlit as st
from qachat import run_Chat
from ivextract import run_invoice_extractor
from chat import run_Document
from learning_companion import run
from adaptive import run_adaptive_learning
from Gamification import run_gamification

# -------------------------
# Dark Theme & CSS
# -------------------------
def set_dark_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    body, .stApp {
        background: #0f0f0f;
        color: #f5f5f5;
        font-family: 'Inter', sans-serif;
        font-size: 16px;
    }

    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(20, 20, 20, 0.95), rgba(30, 30, 30, 0.95));
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 20px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        padding: 14px 18px;
        margin: 6px 0;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e0e0e0;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .stButton > button:hover {
        background: rgba(52, 152, 219, 0.15);
        border-color: rgba(52, 152, 219, 0.4);
        transform: translateX(8px);
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.2);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.25), rgba(41, 128, 185, 0.25));
        border-left: 4px solid #3498db;
        color: #ffffff;
        font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, rgba(52, 152, 219, 0.35), rgba(41, 128, 185, 0.35));
        transform: translateX(8px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }

    /* Chat bubbles */
    .user-message {
        background: linear-gradient(135deg, #3498db, #2980b9);
        color: #fff;
        padding: 14px 18px;
        border-radius: 18px;
        margin: 8px 0;
        float: right;
        clear: both;
        max-width: 75%;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }

    .bot-message {
        background: linear-gradient(135deg, #34495e, #2c3e50);
        color: #fff;
        padding: 14px 18px;
        border-radius: 18px;
        margin: 8px 0;
        float: left;
        clear: both;
        max-width: 75%;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
    }

    /* Glass-morphism card */
    .card {
        padding: 28px;
        background: rgba(35, 35, 35, 0.75);
        border-radius: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
    }

    .card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
        border-color: rgba(52, 152, 219, 0.4);
    }

    /* Animated header */
    @keyframes gradient {
        0% {background-position:0% 50%;}
        50% {background-position:100% 50%;}
        100% {background-position:0% 50%;}
    }

    .animated-header {
        background: linear-gradient(270deg, #3498db, #2980b9, #2ecc71, #e74c3c);
        background-size: 400% 400%;
        animation: gradient 12s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .card {
            padding: 20px;
            margin-bottom: 16px;
        }
        .stButton > button {
            padding: 12px 14px;
            font-size: 0.9rem;
        }
        .animated-header {
            font-size: 2.2rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# Home Page Intro
# -------------------------
def show_intro():
    st.markdown("""
    <div style='text-align:center;padding:50px 0;'>
        <h1 class='animated-header' style='font-size:3.2rem;font-weight:700;margin-bottom:20px;'>Welcome to Study Lens! 🚀</h1>
        <p style='color: #e0e0e0; font-size:1.25rem; opacity:0.9; margin-bottom:48px; line-height:1.6;'>
        Your AI-powered learning companion designed to adapt to your unique learning style and needs.
        </p>
    </div>
    """, unsafe_allow_html=True)

    features = [
        {"icon":"💬","title":"Q&A Chat","desc":"Get instant, accurate answers to your questions with AI-powered chat.","color":"#3498db"},
        {"icon":"📄","title":"Invoice Extractor","desc":"Effortlessly extract key data from invoices and documents.","color":"#e74c3c"},
        {"icon":"📚","title":"Document Chat","desc":"Interact with your documents to extract insights and answers.","color":"#2ecc71"},
        {"icon":"🧠","title":"Learning Companion","desc":"Personalized study plans and interactive quizzes tailored to you.","color":"#f1c40f"},
        {"icon":"📊","title":"Adaptive Learning","desc":"Customized learning paths that evolve with your progress.","color":"#1abc9c"},
        {"icon":"🏆","title":"Gamification","desc":"Earn points, badges, and rewards as you learn.","color":"#e67e22"},
    ]

    cols = st.columns(2)
    for i, f in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div class='card'>
                <div style='display:flex;align-items:start;'>
                    <div style='font-size:2.8rem;margin-right:20px;opacity:0.9;'>{f['icon']}</div>
                    <div>
                        <h3 style='color:{f["color"]};margin-bottom:10px;font-size:1.4rem;font-weight:600;'>{f['title']}</h3>
                        <p style='color:rgba(255,255,255,0.9);line-height:1.6;font-size:1rem;'>{f['desc']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# -------------------------
# Main App
# -------------------------
def main():
    st.set_page_config(page_title="Study Lens", layout="wide", initial_sidebar_state="expanded")
    set_dark_theme()

    # Session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"

    # Sidebar
    with st.sidebar:
       
        
        st.markdown(
        "<div class='sidebar-logo'>", unsafe_allow_html=True
         )
        st.image("learnMate.png", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # CSS
        st.markdown("""
           <style>
           .sidebar-logo {
           width: 70%;
           max-width: 120px;
          aspect-ratio: 1/1;
          margin: 0 auto 20px auto;
           border-radius: 50%;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        }
         .sidebar-logo img {
        object-fit: cover;
        object-position: center;
        border-radius: 50%;
       }
       </style>
      """, unsafe_allow_html=True)



        
        st.markdown("""
        <div style='text-align:center;padding:24px 0;margin-bottom:24px;'>
            <h2 style='color:#ffffff;font-size:1.8rem;margin:12px 0;font-weight:700;'>Study Lens</h2>
            <p style='color:rgba(255,255,255,0.75);font-size:0.95rem;'>Your AI Learning Companion</p>
        </div>
        """, unsafe_allow_html=True)

        menu_items = [
            ("🏠", "Home"),
            ("💬", "Q&A Chat"),
            ("📄", "Invoice Extractor"),
            ("📚", "Document Chat"),
            ("🧠", "Learning Companion"),
            ("📊", "Adaptive Learning"),
            ("🏆", "Gamification"),
        ]
        for icon, page in menu_items:
            is_active = st.session_state.current_page == page
            if st.button(f"{icon} {page}", key=f"nav_{page}", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state.current_page = page

    # Main content
    st.markdown("<div style='padding:24px;background:rgba(255,255,255,0.03);border-radius:16px;backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    page_funcs = {
        "Q&A Chat": run_Chat,
        "Invoice Extractor": run_invoice_extractor,
        "Document Chat": run_Document,
        "Learning Companion": run,
        "Adaptive Learning": run_adaptive_learning,
        "Gamification": run_gamification,  
    }

    if st.session_state.current_page == "Home":
        show_intro()
    elif st.session_state.current_page in page_funcs:
        with st.spinner("Loading your learning experience..."):
            page_funcs[st.session_state.current_page]()

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    main()