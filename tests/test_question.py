from retriever.candidate import get_candidate
from retriever.curriculum import get_day
from services.question_generator import generate_question

candidate = get_candidate("CAND-001")

lesson = get_day(22)

question = generate_question(candidate, lesson)

print("\nGenerated Question:\n")
print(question)