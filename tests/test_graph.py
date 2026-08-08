from graph.graph import graph

state = {
    "session_id": "ABC123",
    "candidate_id": "CAND-001",

    "candidate": {},
    "completed_days": [],

    "current_day": 0,
    "lesson": {},

    "question": "",
    "answer": "",

    "evaluation": {},

    "question_count": 0,

    "history": [],

    "interview_complete": False,
}

# Generate first question

state = graph.invoke(state)

print("\nQuestion:\n")
print(state["question"])

answer = input("\nYour Answer:\n")

state["answer"] = answer

state = graph.invoke(state)

print("\nEvaluation\n")

print(state["evaluation"])

if state["evaluation"]["follow_up_needed"]:

    print("\nFollow-up Question\n")

    print(state["question"])