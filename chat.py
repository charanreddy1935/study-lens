import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document # type: ignore
from collections import defaultdict
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE-API-KEY"))

user_interactions = defaultdict(int)

keywords_books = ["Title", "Author", "Chapter", "Summary", "Introduction", "Conclusion", "Page Number", "References", "Abstract", "Publication Date"]
keywords_academic = ["Title", "Abstract", "Introduction", "Methodology", "Results", "Discussion", "Conclusion", "References", "Figures", "Tables", "Keywords", "Author"]
keywords_invoices = ["Invoice Number", "Date", "Total Amount", "Due Date", "Billing Address", "Shipping Address", "Item Description", "Quantity", "Unit Price", "Subtotal", "Tax", "Discount"]
keywords_business = ["Executive Summary", "Objectives", "Introduction", "Scope", "Findings", "Recommendations", "Action Plan", "Appendix", "Budget", "Timeline", "Contacts"]
keywords_general = ["Summary", "Introduction", "Key Points", "Conclusion", "Date", "Author", "Contact Information", "Action Items", "Notes", "Appendix"]

keywords = keywords_books 

executor = ThreadPoolExecutor()

def run_Document():
    # Custom styled header
    st.markdown("""
        <h2 style='color: #fff; margin-bottom: 20px; text-align: center; 
                 font-family: Inter, Arial, sans-serif;'>Chat with Documents</h2>
        <p style='color: #fff; text-align: center; margin-bottom: 30px; 
                  font-family: Inter, Arial, sans-serif;'>
            Upload multiple documents and start a chat about their content.
        </p>
    """, unsafe_allow_html=True)
    
    # Document type selection container
    st.markdown("""
        <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; 
                    margin-bottom: 20px; border: 1px solid #333;'>
            <p style='color: #fff; margin-bottom: 10px; font-size: 16px;'>Select the document type:</p>
    """, unsafe_allow_html=True)
    
    doc_type = st.selectbox(
        "",
        ["Books", "Academic Papers", "Invoices", "Business Documents", "General Documents"],
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

    if doc_type == "Books":
        keywords = keywords_books
    elif doc_type == "Academic Papers":
        keywords = keywords_academic
    elif doc_type == "Invoices":
        keywords = keywords_invoices
    elif doc_type == "Business Documents":
        keywords = keywords_business
    elif doc_type == "General Documents":
        keywords = keywords_general

    # File upload container
    st.markdown("""
        <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; 
                    margin-bottom: 20px; border: 1px solid #333;'>
            <p style='color: #fff; margin-bottom: 10px; font-size: 16px;'>Upload your documents:</p>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("", type=["pdf", "docx"], 
                                    accept_multiple_files=True,
                                    label_visibility="collapsed")

    if uploaded_files:
        st.markdown("</div>", unsafe_allow_html=True)  # Close upload container
        
        # File list container
        st.markdown("""
            <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; 
                        margin-bottom: 20px; border: 1px solid #333;'>
                <h3 style='color: #fff; margin-bottom: 15px; font-size: 18px; 
                          font-family: Inter, Arial, sans-serif;'>Uploaded Files:</h3>
        """, unsafe_allow_html=True)
        
        extracted_text = ""
        for uploaded_file in uploaded_files:
            st.markdown(f"""
                <div style='background: #2c3e50; padding: 10px 15px; border-radius: 8px; 
                          margin-bottom: 8px; color: #fff;'>
                    📄 {uploaded_file.name}
                </div>
            """, unsafe_allow_html=True)
            file_text = asyncio.run(extract_relevant_sections_async(uploaded_file, keywords))
            if file_text:
                extracted_text += file_text + "\n"
            else:
                st.markdown(f"""
                    <div style='background: #ff4444; color: #fff; padding: 10px 15px; 
                              border-radius: 8px; margin-top: 5px;'>
                        ⚠️ Failed to extract text from {uploaded_file.name}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if extracted_text:
            # Question input container
            st.markdown("""
                <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; 
                          margin-bottom: 20px; border: 1px solid #333;'>
                    <p style='color: #fff; margin-bottom: 10px; font-size: 16px;'>
                        Ask a question or generate a quiz from the documents:
                    </p>
            """, unsafe_allow_html=True)
            
            input_prompt = st.text_input("", key="doc_input", label_visibility="collapsed")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                quiz_generation = st.checkbox("Generate Quiz from Document", 
                                           help="Toggle this to generate a quiz instead of asking questions")
            with col2:
                submit_button = st.button("Submit", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

            if submit_button:
                if input_prompt and not quiz_generation:
                    st.markdown("""
                        <div class='loading-spinner'></div>
                        <div class='loading-text'>Analyzing documents...</div>
                    """, unsafe_allow_html=True)
                    
                    update_keyword_priorities(input_prompt)
                    response = get_gemini_response(input_prompt, extracted_text)
                    
                    # Response container
                    st.markdown("""
                        <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; 
                                  margin-top: 20px; border: 1px solid #333;'>
                            <h3 style='color: #fff; margin-bottom: 15px; font-family: Inter, Arial, sans-serif;'>
                                AI Response
                            </h3>
                            <div style='color: #fff; background: #2c3e50; padding: 15px; border-radius: 8px;'>
                    """, unsafe_allow_html=True)
                    st.write(response)
                    st.markdown("</div></div>", unsafe_allow_html=True)

                if quiz_generation:
                    st.markdown("""
                        <div class='loading-spinner'></div>
                        <div class='loading-text'>Generating quiz...</div>
                    """, unsafe_allow_html=True)
                    
                    quiz = generate_quiz_from_document(extracted_text)
                    
                    # Quiz container
                    st.markdown("""
                        <div style='background: #1a1a1a; padding: 20px; border-radius: 12px; 
                                  margin-top: 20px; border: 1px solid #333;'>
                            <h3 style='color: #fff; margin-bottom: 20px; font-family: Inter, Arial, sans-serif;'>
                                Generated Quiz
                            </h3>
                    """, unsafe_allow_html=True)
                    
                    if quiz:
                        for i, qa in enumerate(quiz):
                            st.markdown(f"""
                                <div style='margin-bottom: 20px;'>
                                    <div style='color: #fff; background: #2c3e50; padding: 15px; 
                                              border-radius: 8px; margin-bottom: 10px;'>
                                        <strong>Q{i+1}:</strong> {qa['question']}
                                    </div>
                                    <div style='color: #fff; background: #34495e; padding: 15px; 
                                              border-radius: 8px; margin-left: 20px;'>
                                        <strong>A{i+1}:</strong> {qa['answer']}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                            <div style='color: #ff4444; padding: 15px; text-align: center;'>
                                No quiz could be generated from the provided documents.
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("</div>", unsafe_allow_html=True)  # Close upload container if no files

async def extract_relevant_sections_async(uploaded_file, keywords):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, extract_relevant_sections, uploaded_file, keywords)

def extract_relevant_sections(uploaded_file, keywords):
    text = ""
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file)
    return text.strip()

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(uploaded_file):
    text = ""
    try:
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
    return text

def update_keyword_priorities(query):
    for keyword in keywords:
        if keyword.lower() in query.lower():
            user_interactions[keyword] += 1  

def get_gemini_response(prompt, document_text):
    model = genai.GenerativeModel("gemini-pro-latest")
    chat = model.start_chat()

    response = chat.send_message(f"Document: {document_text}\n\nQuestion: {prompt}")

    return response.text



def generate_quiz_from_document(document_text):
    prompt = f"Based on the following text, generate a quiz with multiple questions and detailed answers:\n\n{document_text}"
    model = genai.GenerativeModel("gemini-pro-latest")
    chat = model.start_chat()

    
    response = chat.send_message(prompt)

    
    st.write("Raw AI Response:")
    st.write(response.text)  

    
    quiz = []

    
    response_lines = response.text.split('\n')
    
    current_question = ""
    current_answer = ""
    
    for line in response_lines:
        if line.startswith("Q:"):  
            if current_question:  
                quiz.append({"question": current_question, "answer": current_answer})
            current_question = line.replace("Q:", "").strip()
            current_answer = ""
        elif line.startswith("A:"):  
            current_answer = line.replace("A:", "").strip()
        else:
            if current_answer:
                current_answer += " " + line.strip()

    
    if current_question:
        quiz.append({"question": current_question, "answer": current_answer})

    
    if quiz:
        return quiz
    else:
        st.write("No quiz could be generated. Please check the AI response.")
        return None

