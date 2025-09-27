import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google AI
genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

def get_gemini_response(input_prompt, image_data, user_input):
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content([input_prompt, image_data[0], user_input])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def run_invoice_extractor():
    # Custom styled header
    st.markdown("""
        <h2 style='color: #fff; margin-bottom: 20px; text-align: center; 
                 font-family: Inter, Arial, sans-serif;'>Invoice Extractor</h2>
    """, unsafe_allow_html=True)

    # Custom styled container for upload
    st.markdown("""
        <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #333;'>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Invoice (Image)", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        st.markdown("</div>", unsafe_allow_html=True)  # Close the upload container
        
        # Image container with dark theme
        st.markdown("""
            <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid #333;'>
        """, unsafe_allow_html=True)
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice", use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Question input section
        st.markdown("""
            <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid #333;'>
                <p style='color: #fff; margin-bottom: 10px; font-size: 16px;'>Ask a question about the invoice:</p>
        """, unsafe_allow_html=True)
        user_input = st.text_input("", key="input", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        input_prompt = """
        You are an expert in understanding invoices.
        You will receive input images as invoices &
        you will have to answer questions based on the input image
        """

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            analyze_button = st.button("Analyze Invoice", use_container_width=True)

        if analyze_button:
            with st.spinner(""):
                st.markdown("""
                    <div class='loading-spinner'></div>
                    <div class='loading-text'>Analyzing invoice...</div>
                """, unsafe_allow_html=True)
                
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(input_prompt, image_data, user_input)
            
            # Result container with dark theme
            st.markdown("""
                <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; margin: 20px 0; border: 1px solid #333;'>
                    <h3 style='color: #fff; margin-bottom: 15px; font-family: Inter, Arial, sans-serif;'>Analysis Result</h3>
                    <div style='color: #fff; background: #2c3e50; padding: 15px; border-radius: 8px;'>
            """, unsafe_allow_html=True)
            st.write(response)
            st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("</div>", unsafe_allow_html=True)  # Close the upload container if no file

#if __name__ == "__main__":
#    run_invoice_extractor()