from sentence_transformers import SentenceTransformer, util
from src.skills import extract_skills

# Load embedding model once when matcher is imported
_MODEL_NAME = "all-MiniLM-L6-v2"
_embedder = None


def _get_embedder() -> SentenceTransformer:
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(_MODEL_NAME)
    return _embedder


def evaluate_match(cv_text: str, jd_text: str) -> dict:
    """Compare CV and job description text and return match score & skill breakdown."""
    cv_skills = set(extract_skills(cv_text))
    jd_skills = set(extract_skills(jd_text))

    matched_skills = sorted(cv_skills & jd_skills)
    missing_skills = sorted(jd_skills - cv_skills)
    extra_cv_skills = sorted(cv_skills - jd_skills)

    # 1. Skill overlap score (0 to 100)
    if jd_skills:
        skill_score = (len(matched_skills) / len(jd_skills)) * 100.0
    else:
        skill_score = 0.0

    # 2. Semantic similarity score using embeddings (0 to 100)
    embedder = _get_embedder()
    cv_embedding = embedder.encode(cv_text, convert_to_tensor=True)
    jd_embedding = embedder.encode(jd_text, convert_to_tensor=True)
    cosine_sim = float(util.cos_sim(cv_embedding, jd_embedding)[0][0])
    semantic_score = max(0.0, min(100.0, cosine_sim * 100.0))

    # 3. Weighted combined score (60% skills + 40% semantic context)
    final_score = round((0.6 * skill_score) + (0.4 * semantic_score), 1)

    return {
        "final_score": final_score,
        "skill_score": round(skill_score, 1),
        "semantic_score": round(semantic_score, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_cv_skills": extra_cv_skills,
    }