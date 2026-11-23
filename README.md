# AI Resume Screening & Match Analyzer

An AI-powered resume screening web application built with Python, Sentence-Transformers, and Streamlit. Users upload a candidate CV (PDF or DOCX) and enter a job description to extract skills, compute a weighted match score, identify missing skills, and receive actionable improvement suggestions.

## Features
- **CV Text Extraction:** Parses text from `.pdf` and `.docx` resumes.
- **Skill Detection:** Identifies technical and data science skills (e.g., Python, Machine Learning, SQL, Pandas, Docker) with alias matching.
- **Hybrid Match Scoring:** Combines exact skill overlap (60%) and semantic text similarity using `all-MiniLM-L6-v2` embeddings (40%).
- **Gap Analysis & Suggestions:** Highlights matched skills, missing skills, and resume improvement recommendations.

## Project Structure
```text
ai-resume-screener/
├── src/
│   ├── extractor.py    # PDF & DOCX text extraction
│   ├── skills.py       # Skill keyword and alias detection
│   ├── matcher.py      # Skill overlap + semantic similarity scoring
│   └── advisor.py      # Missing skills & improvement suggestions
├── app.py              # Streamlit web interface
├── requirements.txt
└── README.md