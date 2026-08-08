from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

from graph.graph import graph

from models.session import sessions

from services.answer_evaluator import evaluate_answer
from services.followup_generator import generate_followup
from services.feedback_generator import generate_feedback
from services.question_generator import generate_question

from retriever.curriculum import get_day


app = FastAPI(
    title="AI Interview Agent",
    version="1.0.0",
)


# ==========================================================
# REQUEST MODEL
# ==========================================================

class InterviewRequest(BaseModel):
    sessionId: str
    candidate: dict | None = None
    message: str | None = None


# ==========================================================
# HOME
# ==========================================================

@app.get("/")
def home():
    return {
        "message": "AI Interview Agent Running"
    }


# ==========================================================
# MAIN INTERVIEW ENDPOINT
# POST /api/interview
# ==========================================================

@app.post("/api/interview")
def interview(request: InterviewRequest):

    session_id = request.sessionId

    # ======================================================
    # START INTERVIEW
    # ======================================================

    if session_id not in sessions:

        # Candidate is required for first request
        if request.candidate is None:
            raise HTTPException(
                status_code=400,
                detail="candidate is required when starting a new interview."
            )

        state = {
            "session_id": session_id,

            "candidate_id": request.candidate.get(
                "member", {}
            ).get(
                "id",
                session_id
            ),

            "candidate": request.candidate,

            "completed_days": [],
            "asked_days": [],

            "current_day": 0,
            "lesson": {},

            "question": "",
            "answer": "",

            "evaluation": {},

            "question_count": 0,

            "history": [],

            "interview_complete": False,

            "final_feedback": {},

            "followup_pending": False,
        }

        # ==================================================
        # RUN LANGGRAPH
        # ==================================================

        state = graph.invoke(state)

        # ==================================================
        # SAVE FIRST SELECTED TOPIC
        # ==================================================

        if state["current_day"] not in state["asked_days"]:
            state["asked_days"].append(
                state["current_day"]
            )

        sessions[session_id] = state

        # ==================================================
        # FIRST RESPONSE
        # ==================================================

        return {
            "reply": state["question"],
            "done": False,
        }


    # ======================================================
    # EXISTING SESSION
    # ======================================================

    state = sessions[session_id]


    # ======================================================
    # INTERVIEW ALREADY COMPLETED
    # ======================================================

    if state.get("interview_complete", False):

        return {
            "reply": "Interview completed.",
            "done": True,
            "feedback": state.get(
                "final_feedback",
                {}
            ),
        }


    # ======================================================
    # MESSAGE REQUIRED
    # ======================================================

    if request.message is None:

        raise HTTPException(
            status_code=400,
            detail="message is required for an existing interview session."
        )


    # ======================================================
    # SAVE CANDIDATE ANSWER
    # ======================================================

    state["answer"] = request.message


    # ======================================================
    # FOLLOW-UP ANSWER
    # ======================================================

    if state["followup_pending"]:

        evaluation = evaluate_answer(
            state["question"],
            state["answer"],
        )

        state["evaluation"] = evaluation


        # --------------------------------------------------
        # SAVE FOLLOW-UP TO HISTORY
        # --------------------------------------------------

        state["history"].append(
            {
                "question": state["question"],
                "answer": state["answer"],
                "score": evaluation["score"],
                "strengths": evaluation["strengths"],
                "weaknesses": evaluation["weaknesses"],
            }
        )


        # --------------------------------------------------
        # FOLLOW-UP COMPLETED
        # --------------------------------------------------

        state["followup_pending"] = False

        state["question_count"] += 1


    # ======================================================
    # MAIN QUESTION ANSWER
    # ======================================================

    else:

        evaluation = evaluate_answer(
            state["question"],
            state["answer"],
        )

        state["evaluation"] = evaluation


        # --------------------------------------------------
        # SAVE MAIN QUESTION TO HISTORY
        # --------------------------------------------------

        state["history"].append(
            {
                "question": state["question"],
                "answer": state["answer"],
                "score": evaluation["score"],
                "strengths": evaluation["strengths"],
                "weaknesses": evaluation["weaknesses"],
            }
        )


        # --------------------------------------------------
        # GENERATE FOLLOW-UP
        # --------------------------------------------------

        if evaluation["follow_up_needed"]:

            followup = generate_followup(
                state["question"],
                state["answer"],
                evaluation,
            )

            state["question"] = followup

            state["followup_pending"] = True

            sessions[session_id] = state

            return {
                "reply": followup,
                "done": False,
            }


        # --------------------------------------------------
        # MAIN QUESTION COMPLETED
        # --------------------------------------------------

        state["question_count"] += 1


    # ======================================================
    # INTERVIEW COMPLETE?
    # ======================================================
    print("====================================")
    print("QUESTION COUNT:", state["question_count"])
    print("ASKED DAYS:", state["asked_days"])
    print("HISTORY LENGTH:", len(state["history"]))
    print("FOLLOWUP PENDING:", state["followup_pending"])
    print("====================================")  
    MAX_QUESTIONS = 8

    if state["question_count"] >= MAX_QUESTIONS:

        feedback = generate_feedback(
            state["history"]
        )

        state["interview_complete"] = True

        state["final_feedback"] = feedback

        sessions[session_id] = state


        # --------------------------------------------------
        # FINAL RESPONSE
        # --------------------------------------------------

        return {
            "reply": "Interview completed.",
            "done": True,
            "feedback": {
                "summary": feedback.get(
                    "summary",
                    ""
                ),

                "strengths": feedback.get(
                    "strengths",
                    []
                ),

                "gaps": feedback.get(
                    "gaps",
                    feedback.get(
                        "weaknesses",
                        []
                    )
                ),

                "next": feedback.get(
                    "next",
                    feedback.get(
                        "recommendations",
                        []
                    )
                ),
            },
        }


    # ======================================================
    # FIND NEXT TOPIC
    # ======================================================

    remaining = [
        day
        for day in state["completed_days"]
        if day not in state["asked_days"]
    ]


    # ------------------------------------------------------
    # REUSE TOPICS IF ALL HAVE BEEN ASKED
    # ------------------------------------------------------

    if not remaining:

        remaining = state["completed_days"]


    # ======================================================
    # SAFETY CHECK
    # ======================================================

    if not remaining:

        feedback = generate_feedback(
            state["history"]
        )

        state["interview_complete"] = True

        state["final_feedback"] = feedback

        sessions[session_id] = state

        return {
            "reply": "Interview completed.",
            "done": True,
            "feedback": {
                "summary": feedback.get(
                    "summary",
                    ""
                ),

                "strengths": feedback.get(
                    "strengths",
                    []
                ),

                "gaps": feedback.get(
                    "gaps",
                    feedback.get(
                        "weaknesses",
                        []
                    )
                ),

                "next": feedback.get(
                    "next",
                    feedback.get(
                        "recommendations",
                        []
                    )
                ),
            },
        }


    # ======================================================
    # SELECT NEXT TOPIC
    # ======================================================

    next_day = random.choice(
        remaining
    )


    # ------------------------------------------------------
    # ADD TOPIC ONLY ONCE
    # ------------------------------------------------------

    if next_day not in state["asked_days"]:

        state["asked_days"].append(
            next_day
        )


    # ======================================================
    # LOAD LESSON
    # ======================================================

    lesson = get_day(
        next_day
    )

    state["current_day"] = next_day

    state["lesson"] = lesson


    # ======================================================
    # GENERATE NEXT QUESTION
    # ======================================================

    question = generate_question(
        state["candidate"],
        lesson,
    )

    state["question"] = question


    # ======================================================
    # SAVE SESSION
    # ======================================================

    sessions[session_id] = state


    # ======================================================
    # RETURN NEXT QUESTION
    # ======================================================

    return {
        "reply": question,
        "done": False,
    }