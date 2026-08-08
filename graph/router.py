from graph.state import InterviewState


def evaluation_router(state: InterviewState):

    if state["evaluation"]["follow_up_needed"]:
        return "follow_up"

    return "next"