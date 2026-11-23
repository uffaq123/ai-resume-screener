import re

SKILL_ALIASES = {
    "python": "Python",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Deep Learning",
    "sql": "SQL",
    "mysql": "SQL",
    "postgresql": "SQL",
    "postgres": "SQL",
    "sqlite": "SQL",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "git": "Git",
    "github": "GitHub",
    "docker": "Docker",
    "aws": "AWS",
    "data analysis": "Data Analysis",
    "nlp": "NLP",
    "natural language processing": "NLP",
}


def extract_skills(text: str) -> list[str]:
    """Return a sorted list of unique skills found in the input text."""
    if not text:
        return []

    lowered = text.lower()
    found = set()

    for alias, canonical_name in SKILL_ALIASES.items():
        # Match whole words/phrases rather than substrings inside other words
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        if re.search(pattern, lowered):
            found.add(canonical_name)

    return sorted(found)