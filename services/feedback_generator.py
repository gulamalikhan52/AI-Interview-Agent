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
# CLEAN JSON RESPONSE
# ==========================================================

def clean_json_response(
    content: str,
) -> str:

    content = content.strip()

    # Remove accidental Markdown code fences.

    if content.startswith("```"):

        content = (
            content
            .replace(
                "```json",
                ""
            )
            .replace(
                "```JSON",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )

    return content


# ==========================================================
# VALIDATE FEEDBACK
# ==========================================================

def validate_feedback(
    feedback: dict,
) -> dict:

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    summary = feedback.get(
        "summary",
        "",
    )


    if not isinstance(
        summary,
        str,
    ):

        summary = str(
            summary
        )


    feedback[
        "summary"
    ] = summary.strip()


    # ------------------------------------------------------
    # STRENGTHS
    # ------------------------------------------------------

    strengths = feedback.get(
        "strengths",
        [],
    )


    if not isinstance(
        strengths,
        list,
    ):

        strengths = [
            str(strengths)
        ]


    feedback[
        "strengths"
    ] = [

        str(item).strip()

        for item in strengths

        if str(item).strip()
    ]


    # ------------------------------------------------------
    # GAPS
    # ------------------------------------------------------

    gaps = feedback.get(
        "gaps",
        [],
    )


    if not isinstance(
        gaps,
        list,
    ):

        gaps = [
            str(gaps)
        ]


    feedback[
        "gaps"
    ] = [

        str(item).strip()

        for item in gaps

        if str(item).strip()
    ]


    # ------------------------------------------------------
    # NEXT STEPS
    # ------------------------------------------------------

    next_steps = feedback.get(
        "next",
        [],
    )


    if not isinstance(
        next_steps,
        list,
    ):

        next_steps = [
            str(next_steps)
        ]


    feedback[
        "next"
    ] = [

        str(item).strip()

        for item in next_steps

        if str(item).strip()
    ]


    return feedback


# ==========================================================
# GENERATE FEEDBACK
# ==========================================================

def generate_feedback(
    history: list,
) -> dict:

    # ======================================================
    # VALIDATE HISTORY
    # ======================================================

    if not history:

        return {

            "summary": (
                "No interview responses were recorded."
            ),

            "strengths": [],

            "gaps": [],

            "next": [],
        }


    # ======================================================
    # LOAD PROMPT
    # ======================================================

    prompt_template = (
        load_feedback_prompt()
    )


    # ======================================================
    # SERIALIZE HISTORY
    # ======================================================

    history_text = json.dumps(

        history,

        indent=2,

        ensure_ascii=False,
    )


    # ======================================================
    # CREATE PROMPT
    # ======================================================

    prompt = prompt_template.format(

        interview_history=history_text,
    )


    # ======================================================
    # CALL LLM
    # ======================================================

    response = llm.invoke(
        prompt
    )


    text = response.content.strip()


    # ======================================================
    # CLEAN RESPONSE
    # ======================================================

    text = clean_json_response(
        text
    )


    # ======================================================
    # PARSE JSON
    # ======================================================

    try:

        feedback = json.loads(
            text
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            "LLM returned invalid JSON "
            "from the feedback generator: "
            f"{text}"
        ) from exc


    # ======================================================
    # VALIDATE
    # ======================================================

    return validate_feedback(
        feedback
    )