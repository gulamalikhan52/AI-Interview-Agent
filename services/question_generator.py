from services.llm import llm


def generate_question(candidate: dict, lesson: dict) -> str:

    member = candidate.get("member", {})

    name = member.get("name", "Candidate")
    job_role = member.get("jobRole", "Technical Professional")
    years_experience = member.get("yearsExperience", 0)

    lesson_title = lesson.get(
        "title",
        lesson.get("topic", "Technical Concepts"),
    )

    objectives = lesson.get(
        "objectives",
        [],
    )

    objectives_text = "\n".join(
        f"- {objective}"
        for objective in objectives
    )

    prompt = f"""
You are a Senior AI Technical Interviewer.

Candidate Information:

Name:
{name}

Job Role:
{job_role}

Years of Experience:
{years_experience}

Interview Topic:
{lesson_title}

Learning Objectives:
{objectives_text}

Your task is to generate ONE technical interview question.

Rules:

1. Ask exactly ONE question.
2. The question must be technically relevant to the topic.
3. Adjust the difficulty according to the candidate's experience.
4. The question should test understanding, reasoning, architecture, implementation,
   or practical decision-making.
5. Do not provide the answer.
6. Do not provide hints.
7. Do not explain anything.
8. Do not greet the candidate.
9. Return ONLY the question.
10. Return plain text only.
11. NEVER return HTML.
12. NEVER return XML.
13. NEVER return Markdown.
14. NEVER use tags such as <div>, <span>, <p>, <strong>, etc.

Example of correct output:

How would you design a scalable multi-agent system for processing large volumes of documents?

Return ONLY the question.
"""

    response = llm.invoke(prompt)

    question = response.content.strip()

    return question