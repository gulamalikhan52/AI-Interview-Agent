import json
from pathlib import Path

from services.llm import llm


# ==========================================================
# LOAD EVALUATOR PROMPT
# ==========================================================

PROMPT_FILE = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "evaluator.md"
)


def load_evaluator_prompt() -> str:
    """
    Load the answer evaluator prompt.
    """

    if not PROMPT_FILE.exists():

        raise FileNotFoundError(
            f"Evaluator prompt not found: {PROMPT_FILE}"
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

    # Remove Markdown code fences if the LLM
    # accidentally returns them.

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
# VALIDATE EVALUATION
# ==========================================================

def validate_evaluation(
    result: dict,
) -> dict:

    required_fields = [
        "score",
        "strengths",
        "weaknesses",
        "follow_up_needed",
    ]

    # ------------------------------------------------------
    # REQUIRED FIELDS
    # ------------------------------------------------------

    for field in required_fields:

        if field not in result:

            raise ValueError(
                f"Evaluator response missing field: {field}"
            )


    # ------------------------------------------------------
    # SCORE
    # ------------------------------------------------------

    score = result["score"]

    if isinstance(
        score,
        bool,
    ):

        raise ValueError(
            "Evaluation score must be an integer."
        )


    try:

        score = int(score)

    except (
        TypeError,
        ValueError,
    ):

        raise ValueError(
            "Evaluation score must be an integer."
        )


    if score < 0 or score > 10:

        raise ValueError(
            "Evaluation score must be between 0 and 10."
        )


    result["score"] = score


    # ------------------------------------------------------
    # STRENGTHS
    # ------------------------------------------------------

    if not isinstance(
        result["strengths"],
        list,
    ):

        result["strengths"] = [
            str(result["strengths"])
        ]


    result["strengths"] = [

        str(item).strip()

        for item in result["strengths"]

        if str(item).strip()
    ]


    # ------------------------------------------------------
    # WEAKNESSES
    # ------------------------------------------------------

    if not isinstance(
        result["weaknesses"],
        list,
    ):

        result["weaknesses"] = [
            str(result["weaknesses"])
        ]


    result["weaknesses"] = [

        str(item).strip()

        for item in result["weaknesses"]

        if str(item).strip()
    ]


    # ------------------------------------------------------
    # FOLLOW-UP FLAG
    # ------------------------------------------------------

    follow_up_needed = result[
        "follow_up_needed"
    ]


    if isinstance(
        follow_up_needed,
        str,
    ):

        follow_up_needed = (
            follow_up_needed.lower()
            in {
                "true",
                "yes",
                "1",
            }
        )


    result[
        "follow_up_needed"
    ] = bool(
        follow_up_needed
    )


    return result


# ==========================================================
# EVALUATE ANSWER
# ==========================================================

def evaluate_answer(
    question: str,
    answer: str,
) -> dict:

    # ======================================================
    # LOAD PROMPT
    # ======================================================

    prompt_template = (
        load_evaluator_prompt()
    )


    # ======================================================
    # INSERT INTERVIEW DATA
    # ======================================================

    prompt = prompt_template.format(

        question=question,

        answer=answer,
    )


    # ======================================================
    # CALL LLM
    # ======================================================

    response = llm.invoke(
        prompt
    )


    content = response.content.strip()


    # ======================================================
    # CLEAN RESPONSE
    # ======================================================

    content = clean_json_response(
        content
    )


    # ======================================================
    # PARSE JSON
    # ======================================================

    try:

        result = json.loads(
            content
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            "LLM returned invalid JSON "
            "from the answer evaluator: "
            f"{content}"
        ) from exc


    # ======================================================
    # VALIDATE RESULT
    # ======================================================

    return validate_evaluation(
        result
    )