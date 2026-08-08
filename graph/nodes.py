import random

from graph.state import InterviewState

from retriever.candidate import (
    get_candidate,
    get_completed_days,
)

from retriever.curriculum import get_day

from services.question_generator import generate_question
from services.answer_evaluator import evaluate_answer
from services.followup_generator import generate_followup


# ==========================================================
# LOAD CANDIDATE
# ==========================================================

def load_candidate(state: InterviewState):
    candidate = get_candidate(
        state["candidate_id"]
    )

    state["candidate"] = candidate

    state["completed_days"] = get_completed_days(
        state["candidate_id"]
    )

    state["asked_days"] = []

    state["followup_pending"] = False

    return state


# ==========================================================
# SELECT TOPIC
# ==========================================================

def select_topic(state: InterviewState):

    remaining = [
        day
        for day in state["completed_days"]
        if day not in state["asked_days"]
    ]

    if not remaining:
        state["interview_complete"] = True
        return state

    day = random.choice(remaining)

    state["asked_days"].append(day)

    lesson = get_day(day)

    state["current_day"] = day
    state["lesson"] = lesson

    return state


# ==========================================================
# GENERATE INTERVIEW QUESTION
# ==========================================================

def generate_interview_question(state: InterviewState):

    state["question"] = generate_question(
        state["candidate"],
        state["lesson"],
    )

    return state


# ==========================================================
# EVALUATE CANDIDATE ANSWER
# ==========================================================

def evaluate_candidate_answer(state: InterviewState):

    result = evaluate_answer(
        state["question"],
        state["answer"],
    )

    state["evaluation"] = result

    # Save complete evaluation in history
    state["history"].append(
        {
            "question": state["question"],
            "answer": state["answer"],
            "score": result["score"],
            "strengths": result["strengths"],
            "weaknesses": result["weaknesses"],
        }
    )

    # Do NOT increment question_count here.
    #
    # If a follow-up is required, the main question
    # is not considered completely finished yet.
    #
    # question_count is incremented by the application
    # after the complete interaction is finished.

    return state


# ==========================================================
# GENERATE FOLLOW-UP QUESTION
# ==========================================================

def generate_followup_question(state: InterviewState):

    followup = generate_followup(
        state["question"],
        state["answer"],
        state["evaluation"],
    )

    state["question"] = followup

    state["followup_pending"] = True

    return state