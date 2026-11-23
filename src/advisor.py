import re


def generate_suggestions(cv_text: str, match_result: dict) -> list[str]:
    """Generate actionable resume improvement tips from match results and CV text."""
    suggestions = []
    missing = match_result.get("missing_skills", [])
    final_score = match_result.get("final_score", 0.0)

    if missing:
        suggestions.append(
            f"Add missing skills required by the job if you have used them: {', '.join(missing)}."
        )
        suggestions.append(
            f"Highlight or build a small project showing hands-on work with {missing[0]}."
        )

    # Check if the CV mentions measurable numbers or percentages
    if not re.search(r"\b\d+%|\b\d+\+", cv_text):
        suggestions.append(
            "Include measurable results in your experience or projects (for example, accuracy gains, speedups, or dataset sizes)."
        )

    # Check for common resume sections
    lowered_cv = cv_text.lower()
    for section in ["skills", "projects", "experience", "education"]:
        if section not in lowered_cv:
            suggestions.append(
                f"Add a clear '{section.title()}' section so your background is easy to scan."
            )

    if final_score >= 80 and not missing:
        suggestions.append(
            "Strong match overall—tailor your summary lines to echo key phrasing from the job description."
        )

    if not suggestions:
        suggestions.append(
            "Your CV covers the core requirements well. Double-check that your strongest relevant project is near the top."
        )

    return suggestions