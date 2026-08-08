from services.llm import llm


def generate_followup(
    question: str,
    answer: str,
    evaluation: dict,
) -> str:

    weaknesses = evaluation.get(
        "weaknesses",
        [],
    )

    prompt = f"""
You are a Senior AI Technical Interviewer.

Original Question:
{question}

Candidate Answer:
{answer}

Weaknesses Identified:
{weaknesses}

Generate ONE technical follow-up question.

Rules:

1. Ask exactly ONE question.
2. The follow-up must directly target a weakness in the candidate's answer.
3. Maximum 30 words.
4. Make it technically challenging but relevant.
5. Do not explain anything.
6. Do not provide the answer.
7. Do not provide hints.
8. Return ONLY the question.
9. Return plain text only.
10. NEVER return HTML.
11. NEVER return XML.
12. NEVER return Markdown.
13. NEVER use tags such as <div>, <span>, <p>, <strong>, etc.

Return ONLY the follow-up question.
"""

    response = llm.invoke(prompt)

    followup = response.content.strip()

    return followup