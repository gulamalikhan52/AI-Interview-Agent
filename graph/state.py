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

    # True when the current question is a follow-up
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