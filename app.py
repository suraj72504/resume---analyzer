import streamlit as st
import pdfplumber
import pandas as pd
import spacy
import subprocess
import sys

# -----------------------------
# Fix spaCy model auto install
# -----------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📄 AI Resume Analyzer & Job Recommender")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

# -----------------------------
# Function to extract text
# -----------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# -----------------------------
# Extract skills
# -----------------------------
def extract_skills(text, skills_list):
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills

# -----------------------------
# Main Logic
# -----------------------------
if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("📜 Resume Text Extracted")
    st.write(resume_text)

    # Load skills dataset
    skills_df = pd.read_csv("skills.csv")

    skills_list = skills_df["Skill"].tolist()

    extracted_skills = extract_skills(resume_text, skills_list)

    st.subheader("💡 Extracted Skills")
    st.write(extracted_skills)

    # -----------------------------
    # Job Recommendation
    # -----------------------------
    recommended_jobs = skills_df[
        skills_df["Skill"].isin(extracted_skills)
    ]["Job Role"].unique()

    st.subheader("🎯 Recommended Job Roles")
    st.write(recommended_jobs)
