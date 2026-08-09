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

    if candidate is None:
        raise ValueError(
            f"Candidate not found: {state['candidate_id']}"
        )

    state["candidate"] = candidate

    # ------------------------------------------------------
    # TECHNOLOGY STACK
    # ------------------------------------------------------

    # The candidate can have the stack coming from
    # Streamlit/API.
    #
    # If it is already present in state, use it.
    # Otherwise try to read it from candidate.

    tech_stack = state.get(
        "tech_stack",
        []
    )

    if not tech_stack:

        tech_stack = candidate.get(
            "techStack",
            []
        )

    # Clean technology names
    state["tech_stack"] = [
        str(technology).strip()
        for technology in tech_stack
        if str(technology).strip()
    ]

    # Remove duplicates while preserving order
    unique_stack = []

    seen = set()

    for technology in state["tech_stack"]:

        key = technology.lower()

        if key not in seen:

            seen.add(key)

            unique_stack.append(
                technology
            )

    state["tech_stack"] = unique_stack

    # Keep normalized stack inside candidate too
    state["candidate"]["techStack"] = (
        state["tech_stack"]
    )

    # ------------------------------------------------------
    # COMPLETED CURRICULUM DAYS
    # ------------------------------------------------------

    state["completed_days"] = get_completed_days(
        state["candidate_id"]
    )

    # ------------------------------------------------------
    # INITIAL SESSION VALUES
    # ------------------------------------------------------

    state["asked_days"] = []

    state["asked_questions"] = []

    state["history"] = []

    state["question_count"] = 0

    state["followup_pending"] = False

    state["interview_complete"] = False

    state["final_feedback"] = {}

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

    # ------------------------------------------------------
    # NO MORE UNUSED TOPICS
    # ------------------------------------------------------

    if not remaining:

        state["interview_complete"] = True

        return state

    # ------------------------------------------------------
    # RANDOM TOPIC
    # ------------------------------------------------------

    day = random.choice(
        remaining
    )

    state["asked_days"].append(
        day
    )

    # ------------------------------------------------------
    # LOAD CURRICULUM
    # ------------------------------------------------------

    lesson = get_day(
        day
    )

    if lesson is None:

        raise ValueError(
            f"Curriculum day not found: {day}"
        )

    state["current_day"] = day

    state["lesson"] = lesson

    return state


# ==========================================================
# GENERATE INTERVIEW QUESTION
# ==========================================================

def generate_interview_question(
    state: InterviewState
):

    # ------------------------------------------------------
    # GET PREVIOUS QUESTIONS
    # ------------------------------------------------------

    previous_questions = [

        item.get(
            "question",
            ""
        )

        for item in state.get(
            "history",
            []
        )

        if item.get(
            "question"
        )
    ]

    # Also include questions stored explicitly
    # in asked_questions.

    for question in state.get(
        "asked_questions",
        []
    ):

        if (
            question
            and question not in previous_questions
        ):

            previous_questions.append(
                question
            )

    # ------------------------------------------------------
    # GENERATE DYNAMIC QUESTION
    # ------------------------------------------------------

    question = generate_question(

        candidate=state["candidate"],

        lesson=state["lesson"],

        tech_stack=state.get(
            "tech_stack",
            []
        ),

        previous_questions=previous_questions,
    )

    if not question:

        raise ValueError(
            "Question generator returned an empty question."
        )

    # ------------------------------------------------------
    # SAVE QUESTION
    # ------------------------------------------------------

    state["question"] = question

    # Prevent duplicate question tracking
    if question not in state[
        "asked_questions"
    ]:

        state[
            "asked_questions"
        ].append(
            question
        )

    return state


# ==========================================================
# EVALUATE CANDIDATE ANSWER
# ==========================================================

def evaluate_candidate_answer(
    state: InterviewState
):

    result = evaluate_answer(

        state["question"],

        state["answer"],
    )

    state["evaluation"] = result

    # ------------------------------------------------------
    # SAVE COMPLETE INTERACTION
    # ------------------------------------------------------

    state["history"].append(

        {
            "question": state["question"],

            "answer": state["answer"],

            "score": result.get(
                "score",
                0
            ),

            "strengths": result.get(
                "strengths",
                []
            ),

            "weaknesses": result.get(
                "weaknesses",
                []
            ),
        }
    )

    return state


# ==========================================================
# GENERATE FOLLOW-UP QUESTION
# ==========================================================

def generate_followup_question(
    state: InterviewState
):

    followup = generate_followup(

        state["question"],

        state["answer"],

        state["evaluation"],
    )

    if not followup:

        raise ValueError(
            "Follow-up generator returned an empty question."
        )

    state["question"] = followup

    state["followup_pending"] = True

    # ------------------------------------------------------
    # TRACK FOLLOW-UP
    # ------------------------------------------------------

    if followup not in state[
        "asked_questions"
    ]:

        state[
            "asked_questions"
        ].append(
            followup
        )

    return state