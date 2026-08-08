from services.answer_evaluator import evaluate_answer

question = "Explain what Kubernetes readiness probe is."

answer = """
It checks whether the application is ready to receive traffic.
"""

result = evaluate_answer(question, answer)

print(result)