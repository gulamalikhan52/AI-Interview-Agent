from langgraph.graph import StateGraph, END

from graph.state import InterviewState

from graph.nodes import (
    load_candidate,
    select_topic,
    generate_interview_question,
    evaluate_candidate_answer,
    generate_followup_question,
)

from graph.router import evaluation_router


# ==========================================================
# CREATE GRAPH
# ==========================================================

builder = StateGraph(
    InterviewState
)


# ==========================================================
# NODES
# ==========================================================

builder.add_node(
    "load_candidate",
    load_candidate,
)

builder.add_node(
    "select_topic",
    select_topic,
)

builder.add_node(
    "generate_question",
    generate_interview_question,
)

builder.add_node(
    "evaluate",
    evaluate_candidate_answer,
)

builder.add_node(
    "follow_up",
    generate_followup_question,
)


# ==========================================================
# ENTRY POINT
# ==========================================================

builder.set_entry_point(
    "load_candidate"
)


# ==========================================================
# INITIAL INTERVIEW FLOW
# ==========================================================

builder.add_edge(
    "load_candidate",
    "select_topic",
)

builder.add_edge(
    "select_topic",
    "generate_question",
)


# ==========================================================
# QUESTION GENERATION → END
# ==========================================================

# The API handles the next request after the candidate
# submits the answer.

builder.add_edge(
    "generate_question",
    END,
)


# ==========================================================
# EVALUATION
# ==========================================================

builder.add_edge(
    "evaluate",
    END,
)


# ==========================================================
# FOLLOW-UP
# ==========================================================

builder.add_edge(
    "follow_up",
    END,
)


# ==========================================================
# COMPILE
# ==========================================================

graph = builder.compile()