import json
from pathlib import Path

from services.llm import llm


# ==========================================================
# LOAD FEEDBACK PROMPT
# ==========================================================

PROMPT_FILE = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "feedback.md"
)


def load_feedback_prompt() -> str:
    """
    Load the final interview feedback prompt.
    """

    if not PROMPT_FILE.exists():
        raise FileNotFoundError(
            f"Feedback prompt not found: {PROMPT_FILE}"
        )

    return PROMPT_FILE.read_text(
        encoding="utf-8"
    )


# ==========================================================
# GENERATE FEEDBACK
# ==========================================================

def generate_feedback(history: list) -> dict:
    """
    Generate structured final feedback from the
    complete interview history.
    """

    prompt_template = load_feedback_prompt()

    history_text = json.dumps(
        history,
        indent=2,
        ensure_ascii=False,
    )

    prompt = prompt_template.format(
        interview_history=history_text,
    )

    response = llm.invoke(prompt)

    text = response.content.strip()

    # ------------------------------------------------------
    # Remove accidental markdown code fences
    # ------------------------------------------------------

    if text.startswith("```"):
        text = text.replace(
            "```json",
            "",
        ).replace(
            "```",
            "",
        ).strip()

    # ------------------------------------------------------
    # Parse JSON
    # ------------------------------------------------------

    try:

        feedback = json.loads(text)

    except json.JSONDecodeError:

        feedback = {
            "summary": "Unable to generate structured feedback.",
            "strengths": [],
            "gaps": [
                "The final feedback response could not be parsed."
            ],
            "next": [
                "Review the interview responses manually."
            ],
        }

    # ------------------------------------------------------
    # Ensure required fields exist
    # ------------------------------------------------------

    feedback.setdefault(
        "summary",
        "",
    )

    feedback.setdefault(
        "strengths",
        [],
    )

    feedback.setdefault(
        "gaps",
        [],
    )

    feedback.setdefault(
        "next",
        [],
    )

    # ------------------------------------------------------
    # Ensure correct data types
    # ------------------------------------------------------

    if not isinstance(
        feedback["strengths"],
        list,
    ):
        feedback["strengths"] = []

    if not isinstance(
        feedback["gaps"],
        list,
    ):
        feedback["gaps"] = []

    if not isinstance(
        feedback["next"],
        list,
    ):
        feedback["next"] = []

    if not isinstance(
        feedback["summary"],
        str,
    ):
        feedback["summary"] = str(
            feedback["summary"]
        )

    return feedback