from graph.state import InterviewState


def evaluation_router(
    state: InterviewState,
):
    """
    Decide whether the candidate needs a follow-up
    question or should move to the next question.
    """

    evaluation = state.get(
        "evaluation",
        {},
    )

    if evaluation.get(
        "follow_up_needed",
        False,
    ):
        return "follow_up"

    return "next"