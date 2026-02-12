import streamlit as st
import pdfplumber
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_sm")

# Extract text from PDF
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Extract skills
def extract_skills(text, skills_list):
    doc = nlp(text.lower())
    found_skills = []

    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return list(set(found_skills))

# UI
st.title("📄 AI Resume Analyzer & Job Recommender")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:

    resume_text = extract_text(uploaded_file)

    st.subheader("Resume Text Extracted ✅")

    skills_df = pd.read_csv("skills.csv")
    skills_list = skills_df["Skill"].tolist()

    extracted_skills = extract_skills(resume_text, skills_list)

    st.subheader("💡 Extracted Skills")
    st.write(extracted_skills)

    # Job Recommendation
    recommended_jobs = skills_df[
        skills_df["Skill"].isin(extracted_skills)
    ]["Job Role"].unique()

    st.subheader("🎯 Recommended Job Roles")
    st.write(recommended_jobs)