from typing import TypedDict


class InterviewState(TypedDict):

    # ======================================================
    # SESSION
    # ======================================================

    session_id: str
    candidate_id: str

    # ======================================================
    # CANDIDATE
    # ======================================================

    candidate: dict

    # Technologies selected by the candidate
    # Example:
    # ["Python", "FastAPI", "LangGraph", "Docker"]
    tech_stack: list[str]

    # ======================================================
    # CURRICULUM
    # ======================================================

    completed_days: list[int]

    asked_days: list[int]

    current_day: int

    lesson: dict

    # ======================================================
    # CURRENT INTERVIEW TURN
    # ======================================================

    question: str

    answer: str

    evaluation: dict

    # ======================================================
    # INTERVIEW PROGRESS
    # ======================================================

    question_count: int

    # Questions already generated during this session.
    #
    # This is extremely important because the LLM
    # receives this list and is instructed not to repeat
    # previous questions.
    asked_questions: list[str]

    # True when the current question is a follow-up.
    followup_pending: bool

    # ======================================================
    # CONVERSATION HISTORY
    # ======================================================

    history: list

    # ======================================================
    # INTERVIEW STATUS
    # ======================================================

    interview_complete: bool

    # ======================================================
    # FINAL RESULT
    # ======================================================

    final_feedback: dict