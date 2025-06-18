# Install required packages before running:
# pip install streamlit google-generativeai PyPDF2

import os
import PyPDF2
import streamlit as st
import google.generativeai as genai

# Set your Gemini API Key
GOOGLE_API_KEY = "AIzaSyCV0OBzvLSCzr-Cep9rcw3Uq1gP3CF2oTo"  # 🔐 Replace this with your actual Gemini API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Summarize using Gemini
def summarize_content(text):
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
Summarize the following study material into 4–5 concise bullet points:

{text}

Return only the summary points.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# Generate Quiz using Gemini
def generate_quiz_from_summary(summary):
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
Based on the following summary, generate 2 multiple-choice quiz questions.
Each question should have 4 options (a, b, c, d) and include the correct answer at the end.

Summary:
{summary}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# Streamlit UI
st.set_page_config(page_title="📚 Study Assistant – Quiz Generator", layout="centered")

st.title("📘 Study Assistant: Quiz Question Generator")
st.markdown("Upload a study material PDF and get a summary with quiz questions.")

uploaded_file = st.file_uploader("📄 Upload PDF File", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("🔍 Extracting and processing..."):
        # Step 1: Extract PDF Text
        text = extract_text_from_pdf(uploaded_file)

        # Step 2: Summarize
        summary = summarize_content(text)

        # Step 3: Generate Quiz
        quiz = generate_quiz_from_summary(summary)

    st.subheader("📌 Summary")
    st.markdown(summary)

    st.subheader("📝 Quiz Questions")
    st.markdown(quiz)
