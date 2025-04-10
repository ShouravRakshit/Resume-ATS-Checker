import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2 as pdf
import json

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

def input_pdf_text(file):
    reader = pdf.PdfReader(file)
    text = ""
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += str(page_obj.extract_text())
    return text

input_prompt = """
Hey, act like a highly skilled ATS with deep understanding of tech fields like software engineering,
data science, data analytics, and big data engineering. Evaluate the following resume based on the
job description provided. Consider the competitive nature of the job market and provide the best assistance
to improve the resume. Assign a percentage match and list the missing keywords with high accuracy.

Resume:
{text}

Job Description:
{jd}

Return your response as a single JSON string with the structure:
{{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
"""

st.title("Smart ATS")
st.text("Improve Your Resume using ATS insights")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type="pdf", help="Please upload a PDF file")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd:
        resume_text = input_pdf_text(uploaded_file)
        # Format the prompt with actual resume text and job description
        formatted_prompt = input_prompt.format(text=resume_text, jd=jd)
        response = get_gemini_response(formatted_prompt)
        
        # Optionally: Try to extract and load JSON from the response if it's well-formed
        try:
            result = json.loads(response)
            st.subheader("Parsed ATS Response (JSON)")
            st.json(result)
        except json.JSONDecodeError:
            st.subheader("Raw ATS Response")
            st.text(response)
    else:
        st.warning("Please provide both a job description and a resume file.")
