from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from graph.graph import graph

from models.session import sessions

from services.answer_evaluator import evaluate_answer
from services.followup_generator import generate_followup
from services.feedback_generator import generate_feedback
from services.question_generator import generate_question

from retriever.curriculum import get_day


# ==========================================================
# APP
# ==========================================================

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
# NORMALIZE TECHNOLOGY STACK
# ==========================================================

def normalize_tech_stack(
    tech_stack,
) -> list[str]:

    if not isinstance(
        tech_stack,
        list,
    ):
        return []

    cleaned = []

    seen = set()

    for technology in tech_stack:

        if technology is None:
            continue

        technology = str(
            technology
        ).strip()

        if not technology:
            continue

        key = technology.lower()

        if key in seen:
            continue

        seen.add(key)

        cleaned.append(
            technology
        )

    return cleaned


# ==========================================================
# BUILD FINAL FEEDBACK
# ==========================================================

def build_feedback_response(
    feedback: dict,
):

    return {
        "summary": feedback.get(
            "summary",
            "",
        ),

        "strengths": feedback.get(
            "strengths",
            [],
        ),

        "gaps": feedback.get(
            "gaps",
            [],
        ),

        "next": feedback.get(
            "next",
            [],
        ),
    }


# ==========================================================
# GENERATE NEXT QUESTION
# ==========================================================

def generate_next_question(
    state: dict,
):

    # ------------------------------------------------------
    # FIND AVAILABLE TOPICS
    # ------------------------------------------------------

    remaining_days = [

        day

        for day in state.get(
            "completed_days",
            [],
        )

        if day not in state.get(
            "asked_days",
            [],
        )
    ]

    # ------------------------------------------------------
    # IF ALL TOPICS HAVE BEEN USED
    # ------------------------------------------------------

    if not remaining_days:

        # We can reuse a curriculum topic.
        #
        # The question itself will still be different
        # because previous questions are passed to the LLM.

        completed_days = state.get(
            "completed_days",
            [],
        )

        if not completed_days:

            return None

        remaining_days = completed_days


    # ------------------------------------------------------
    # SELECT TOPIC
    # ------------------------------------------------------

    import random

    day = random.choice(
        remaining_days
    )


    # Only add the day once.

    if day not in state.get(
        "asked_days",
        [],
    ):

        state[
            "asked_days"
        ].append(
            day
        )


    # ------------------------------------------------------
    # LOAD LESSON
    # ------------------------------------------------------

    lesson = get_day(
        day
    )

    if lesson is None:

        raise ValueError(
            f"Curriculum day not found: {day}"
        )


    state[
        "current_day"
    ] = day

    state[
        "lesson"
    ] = lesson


    # ------------------------------------------------------
    # PREVIOUS QUESTIONS
    # ------------------------------------------------------

    previous_questions = list(
        state.get(
            "asked_questions",
            [],
        )
    )


    # Also collect questions from history.

    for item in state.get(
        "history",
        [],
    ):

        question = item.get(
            "question",
            "",
        )

        if (
            question
            and question not in previous_questions
        ):

            previous_questions.append(
                question
            )


    # ------------------------------------------------------
    # GENERATE QUESTION
    # ------------------------------------------------------

    question = generate_question(

        candidate=state[
            "candidate"
        ],

        lesson=lesson,

        tech_stack=state.get(
            "tech_stack",
            [],
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

    state[
        "question"
    ] = question


    if question not in state.get(
        "asked_questions",
        [],
    ):

        state[
            "asked_questions"
        ].append(
            question
        )


    return question


# ==========================================================
# INTERVIEW ENDPOINT
# ==========================================================

@app.post("/api/interview")
def interview(
    request: InterviewRequest,
):

    session_id = request.sessionId


    # ======================================================
    # START NEW INTERVIEW
    # ======================================================

    if session_id not in sessions:

        if request.candidate is None:

            raise HTTPException(
                status_code=400,

                detail=(
                    "Candidate information is required "
                    "when starting a new interview."
                ),
            )


        candidate = request.candidate


        member = candidate.get(
            "member",
            {},
        )


        candidate_id = member.get(
            "id",
            session_id,
        )


        # --------------------------------------------------
        # TECHNOLOGY STACK
        # --------------------------------------------------

        tech_stack = normalize_tech_stack(
            candidate.get(
                "techStack",
                [],
            )
        )


        if not tech_stack:

            raise HTTPException(
                status_code=400,

                detail=(
                    "Technology stack is required. "
                    "Please provide at least one technology."
                ),
            )


        candidate[
            "techStack"
        ] = tech_stack


        # ==================================================
        # INITIAL STATE
        # ==================================================

        state = {

            "session_id": session_id,

            "candidate_id": candidate_id,

            "candidate": candidate,

            "tech_stack": tech_stack,

            "completed_days": [],

            "asked_days": [],

            "current_day": 0,

            "lesson": {},

            "question": "",

            "answer": "",

            "evaluation": {},

            "question_count": 0,

            "asked_questions": [],

            "followup_pending": False,

            "history": [],

            "interview_complete": False,

            "final_feedback": {},
        }


        # ==================================================
        # RUN INITIAL GRAPH
        # ==================================================

        try:

            state = graph.invoke(
                state
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,

                detail=(
                    "Failed to start interview: "
                    f"{exc}"
                ),
            )


        question = state.get(
            "question",
            "",
        )


        if not question:

            raise HTTPException(
                status_code=500,

                detail=(
                    "The interview graph "
                    "did not generate a question."
                ),
            )


        # --------------------------------------------------
        # TRACK FIRST QUESTION
        # --------------------------------------------------

        if question not in state[
            "asked_questions"
        ]:

            state[
                "asked_questions"
            ].append(
                question
            )


        # --------------------------------------------------
        # SAVE SESSION
        # --------------------------------------------------

        sessions[
            session_id
        ] = state


        print(
            "=========================================="
        )

        print(
            "NEW INTERVIEW"
        )

        print(
            "SESSION:",
            session_id,
        )

        print(
            "CANDIDATE:",
            candidate_id,
        )

        print(
            "TECH STACK:",
            tech_stack,
        )

        print(
            "FIRST QUESTION:",
            question,
        )

        print(
            "=========================================="
        )

        return {
          "reply": question,
          "done": False,
          "follow_up": False,
        }


    # ======================================================
    # LOAD EXISTING SESSION
    # ======================================================

    state = sessions[
        session_id
    ]


    # ======================================================
    # CHECK COMPLETION
    # ======================================================

    if state.get(
        "interview_complete",
        False,
    ):

        return {

            "reply": "Interview completed.",

            "done": True,

            "feedback": build_feedback_response(
                state.get(
                    "final_feedback",
                    {},
                )
            ),
        }


    # ======================================================
    # ANSWER REQUIRED
    # ======================================================

    if request.message is None:

        raise HTTPException(
            status_code=400,

            detail=(
                "message is required "
                "for an existing interview."
            ),
        )


    answer = request.message.strip()


    if not answer:

        raise HTTPException(
            status_code=400,

            detail="Answer cannot be empty.",
        )


    # ======================================================
    # SAVE ANSWER
    # ======================================================

    state[
        "answer"
    ] = answer


    # ======================================================
    # EVALUATE ANSWER
    # ======================================================

    try:

        evaluation = evaluate_answer(

            state["question"],

            answer,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,

            detail=(
                "Failed to evaluate answer: "
                f"{exc}"
            ),
        )


    state[
        "evaluation"
    ] = evaluation


    # ======================================================
    # SAVE HISTORY
    # ======================================================

    state[
        "history"
    ].append(

        {

            "question": state[
                "question"
            ],

            "answer": answer,

            "score": evaluation.get(
                "score",
                0,
            ),

            "strengths": evaluation.get(
                "strengths",
                [],
            ),

            "weaknesses": evaluation.get(
                "weaknesses",
                [],
            ),
        }
    )


    # ======================================================
    # FOLLOW-UP NEEDED?
    # ======================================================

    if evaluation.get(
        "follow_up_needed",
        False,
    ):

        try:

            followup = generate_followup(

                state["question"],

                answer,

                evaluation,
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,

                detail=(
                    "Failed to generate follow-up: "
                    f"{exc}"
                ),
            )


        if not followup:

            raise HTTPException(
                status_code=500,

                detail=(
                    "Follow-up generator "
                    "returned an empty question."
                ),
            )


        state[
            "question"
        ] = followup


        state[
            "followup_pending"
        ] = True


        if followup not in state[
            "asked_questions"
        ]:

            state[
                "asked_questions"
            ].append(
                followup
            )


        sessions[
            session_id
        ] = state


        print(
            "=========================================="
        )

        print(
            "FOLLOW-UP QUESTION"
        )

        print(
            followup
        )

        print(
            "=========================================="
        )


        return {
          "reply": followup,
          "done": False,
         "follow_up": True,
}

    # ======================================================
    # NORMAL QUESTION COMPLETED
    # ======================================================

    state[
        "followup_pending"
    ] = False


    state[
        "question_count"
    ] += 1


    # ======================================================
    # MAX QUESTIONS
    # ======================================================

    MAX_QUESTIONS = 8


    if state[
        "question_count"
    ] >= MAX_QUESTIONS:

        try:

            feedback = generate_feedback(
                state["history"]
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,

                detail=(
                    "Failed to generate final feedback: "
                    f"{exc}"
                ),
            )


        state[
            "interview_complete"
        ] = True


        state[
            "final_feedback"
        ] = feedback


        sessions[
            session_id
        ] = state


        return {

            "reply": "Interview completed.",

            "done": True,

            "feedback": build_feedback_response(
                feedback
            ),
        }


    # ======================================================
    # GENERATE NEXT QUESTION
    # ======================================================

    try:

        next_question = generate_next_question(
            state
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,

            detail=(
                "Failed to generate next question: "
                f"{exc}"
            ),
        )


    if not next_question:

        try:

            feedback = generate_feedback(
                state["history"]
            )

        except Exception as exc:

            raise HTTPException(
                status_code=500,

                detail=(
                    "Failed to generate final feedback: "
                    f"{exc}"
                ),
            )


        state[
            "interview_complete"
        ] = True


        state[
            "final_feedback"
        ] = feedback


        sessions[
            session_id
        ] = state


        return {

            "reply": "Interview completed.",

            "done": True,

            "feedback": build_feedback_response(
                feedback
            ),
        }


    # ======================================================
    # SAVE SESSION
    # ======================================================

    sessions[
        session_id
    ] = state


    # ======================================================
    # DEBUG
    # ======================================================

    print(
        "=========================================="
    )

    print(
        "NEXT QUESTION"
    )

    print(
        "SESSION:",
        session_id,
    )

    print(
        "QUESTION COUNT:",
        state["question_count"],
    )

    print(
        "TECH STACK:",
        state.get(
            "tech_stack",
            [],
        ),
    )

    print(
        "CURRENT DAY:",
        state.get(
            "current_day",
            0,
        ),
    )

    print(
        "PREVIOUS QUESTIONS:",
        len(
            state.get(
                "asked_questions",
                [],
            )
        ),
    )

    print(
        "QUESTION:",
        next_question,
    )

    print(
        "=========================================="
    )


    return {
       "reply": next_question,
        "done": False,
        "follow_up": False,
    }