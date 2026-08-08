from services.feedback_generator import generate_feedback

history = [

    {
        "question": "What is RAG?",
        "answer": "RAG combines retrieval with generation.",
        "score": 8,
    },

    {
        "question": "Explain Docker.",
        "answer": "Docker creates lightweight containers.",
        "score": 6,
    },

    {
        "question": "Explain Kubernetes readiness probe.",
        "answer": "It checks if the application is ready to receive traffic.",
        "score": 5,
    }

]

feedback = generate_feedback(history)

print("\n========== FINAL FEEDBACK ==========\n")

print(feedback)