import streamlit as st
import pdfplumber
import pandas as pd

st.title("📄 AI Resume Analyzer & Job Recommender")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text

def extract_skills(text, skills_list):
    found_skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills

if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("📜 Resume Text Extracted")
    st.write(resume_text)

    skills_df = pd.read_csv("skills.csv")

    skills_list = skills_df["Skill"].tolist()

    extracted_skills = extract_skills(resume_text, skills_list)

    st.subheader("💡 Extracted Skills")
    st.write(extracted_skills)

    recommended_jobs = skills_df[
        skills_df["Skill"].isin(extracted_skills)
    ]["Job Role"].unique()

    st.subheader("🎯 Recommended Job Roles")
    st.write(recommended_jobs)
