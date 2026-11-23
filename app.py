import streamlit as st
from src.advisor import generate_suggestions
from src.extractor import extract_resume_text
from src.matcher import evaluate_match
from src.skills import extract_skills

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
)

st.title("AI Resume Screening & Match Analyzer")
st.write(
    "Upload a candidate CV (PDF or DOCX) and paste a job description to see "
    "identified skills, a match score, missing skills, and improvement tips."
)

col1, col2 = st.columns(2)

with col1:
  uploaded_cv = st.file_uploader(
      "1. Upload CV (PDF or DOCX)",
      type=["pdf", "docx"],
  )

with col2:
  jd_text = st.text_area(
      "2. Paste Job Description",
      height=220,
      placeholder=(
          "Example: Looking for a candidate with Python, Machine Learning,"
          " SQL, Pandas, and Git experience..."
      ),
  )

if st.button("Analyze Match", type="primary"):
  if not uploaded_cv:
    st.warning("Please upload a CV in PDF or DOCX format.")
  elif not jd_text.strip():
    st.warning("Please paste a job description.")
  else:
    try:
      cv_text = extract_resume_text(uploaded_cv, uploaded_cv.name)
    except Exception as exc:
      st.error(f"Error reading CV file: {exc}")
      st.stop()

    if not cv_text.strip():
      st.error(
          "No readable text was found in the CV. If it is a scanned image PDF,"
          " try a text-based PDF or DOCX file."
      )
      st.stop()

    with st.spinner("Analyzing skills and semantic similarity..."):
      result = evaluate_match(cv_text, jd_text)
      suggestions = generate_suggestions(cv_text, result)
      cv_all_skills = extract_skills(cv_text)

    st.divider()

    # Score summary cards
    m1, m2, m3 = st.columns(3)
    m1.metric("Overall Match Score", f"{result['final_score']}%")
    m2.metric("Skill Match Score (60%)", f"{result['skill_score']}%")
    m3.metric("Semantic Similarity (40%)", f"{result['semantic_score']}%")

    # Matched vs. Missing skills
    s1, s2 = st.columns(2)
    with s1:
      st.subheader("Matched Skills")
      if result["matched_skills"]:
        st.success(", ".join(result["matched_skills"]))
      else:
        st.info("No overlapping skills detected yet.")

    with s2:
      st.subheader("Missing Skills")
      if result["missing_skills"]:
        st.error(", ".join(result["missing_skills"]))
      else:
        st.success("All detected job skills are present in the CV!")

    # Additional skills found on CV
    if result["extra_cv_skills"]:
      st.subheader("Additional Skills Found on CV")
      st.write(", ".join(result["extra_cv_skills"]))

    # Improvement suggestions
    st.subheader("Improvement Suggestions")
    for tip in suggestions:
      st.markdown(f"- {tip}")

    # Optional expandable debug/inspection view
    with st.expander("Inspect Extracted CV Text & Detected Skills"):
      st.write("**All Skills Detected in CV:**", ", ".join(cv_all_skills) or "None")
      st.text_area("Extracted CV Text", value=cv_text, height=180)