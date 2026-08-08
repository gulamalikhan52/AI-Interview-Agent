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
# EVALUATE ANSWER
# ==========================================================

def evaluate_answer(
    question: str,
    answer: str,
) -> dict:
    """
    Evaluate a candidate's technical answer.
    """

    prompt_template = load_evaluator_prompt()

    prompt = prompt_template.format(
        question=question,
        answer=answer,
    )

    response = llm.invoke(prompt)

    content = response.content.strip()

    # Remove accidental markdown code fences
    if content.startswith("```"):
        content = content.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

    try:
        result = json.loads(content)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid JSON: {content}"
        ) from exc

    # ======================================================
    # Validate required fields
    # ======================================================

    required_fields = [
        "score",
        "strengths",
        "weaknesses",
        "follow_up_needed",
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(
                f"Evaluator response missing field: {field}"
            )

    return result