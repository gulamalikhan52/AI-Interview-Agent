from services.llm import llm


def generate_question(
    candidate: dict,
    lesson: dict,
    tech_stack: list[str] | None = None,
    previous_questions: list[str] | None = None,
) -> str:

    # ======================================================
    # CANDIDATE INFORMATION
    # ======================================================

    member = candidate.get(
        "member",
        {}
    )

    name = member.get(
        "name",
        "Candidate"
    )

    job_role = member.get(
        "jobRole",
        "Technical Professional"
    )

    years_experience = member.get(
        "yearsExperience",
        0
    )


    # ======================================================
    # TECHNOLOGY STACK
    # ======================================================

    tech_stack = tech_stack or []


    cleaned_stack = []

    seen_stack = set()


    for technology in tech_stack:

        technology = str(
            technology
        ).strip()


        if not technology:
            continue


        key = technology.lower()


        if key in seen_stack:
            continue


        seen_stack.add(key)

        cleaned_stack.append(
            technology
        )


    if cleaned_stack:

        technology_text = ", ".join(
            cleaned_stack
        )

    else:

        technology_text = (
            "No specific technology stack provided."
        )


    # ======================================================
    # CURRICULUM INFORMATION
    # ======================================================

    lesson_title = lesson.get(
        "title",
        lesson.get(
            "topic",
            "Technical Concepts"
        ),
    )


    objectives = lesson.get(
        "objectives",
        [],
    )


    if not isinstance(
        objectives,
        list,
    ):

        objectives = [
            str(objectives)
        ]


    objectives_text = "\n".join(

        f"- {objective}"

        for objective in objectives
    )


    # ======================================================
    # PREVIOUS QUESTIONS
    # ======================================================

    previous_questions = (
        previous_questions or []
    )


    cleaned_previous_questions = []

    seen_questions = set()


    for question in previous_questions:

        question = str(
            question
        ).strip()


        if not question:
            continue


        key = question.lower()


        if key in seen_questions:
            continue


        seen_questions.add(key)

        cleaned_previous_questions.append(
            question
        )


    if cleaned_previous_questions:

        previous_questions_text = "\n".join(

            f"- {question}"

            for question in cleaned_previous_questions
        )

    else:

        previous_questions_text = (
            "No previous questions. "
            "This is the first question."
        )


    # ======================================================
    # QUESTION GENERATION PROMPT
    # ======================================================

    prompt = f"""
You are a Senior AI Technical Interviewer conducting
a realistic adaptive technical interview.

Candidate Information:

Name:
{name}

Job Role:
{job_role}

Years of Experience:
{years_experience}

Technology Stack:
{technology_text}

Current Curriculum Topic:
{lesson_title}

Learning Objectives:
{objectives_text}

Previous Questions Already Asked:
{previous_questions_text}


Your task is to generate ONE NEW technical interview question.


==========================================================
CORE REQUIREMENTS
==========================================================

1. Ask exactly ONE technical question.

2. The question must be primarily about a technology
   from the candidate's actual technology stack.

3. The candidate's technology stack is a HARD constraint.
   Never make an unrelated technology the subject of the
   question.

4. The current curriculum topic may provide conceptual
   context, but it must NOT override the technology stack.

5. If the curriculum topic is about a technology that is
   NOT present in the candidate's technology stack, do NOT
   ask a question about that technology. Instead, adapt the
   underlying engineering concept to a technology that IS
   present in the candidate's stack.

6. Never introduce Kubernetes, Docker, AWS, Azure, GCP,
   React, Spring Boot, FastAPI, or any other technology
   unless it is present in the candidate's technology stack.

5. Adjust difficulty according to the candidate's
   years of experience.

6. Test engineering understanding, reasoning,
   implementation, architecture, debugging,
   scalability, security, performance, or
   technical decision-making.

7. Prefer practical engineering scenarios over
   definition-based questions.

8. Include trade-offs when they naturally fit the topic.

9. The question must be different from every previous
   question.

10. Do not merely change a few words from a previous
    question.

11. Do not ask the same concept in a different sentence
    if the previous question already tested it.

12. Select a different angle, scenario, implementation
    problem, failure case, architecture decision,
    or trade-off.

13. Do not provide the answer.

14. Do not provide hints.

15. Do not explain the topic.

16. Do not greet the candidate.

17. Keep the question under 50 words.

18. Return ONLY the question.

19. Plain text only.

20. Never return Markdown.

21. Never return HTML.

22. Never return XML.

23. Never add labels such as:
    Question:
    Interview Question:
    Answer:


==========================================================
ADAPTATION RULE
==========================================================

The question should combine these factors:

Candidate Experience
+
Technology Stack
+
Current Curriculum Topic
+
Learning Objectives
+
Previous Questions


The technology stack is the primary technology boundary.

For example:

If the candidate stack is:
Python, FastAPI

and the curriculum topic is API design, ask about API
design using Python or FastAPI.

If the candidate stack is:
Java, Spring Boot

and the curriculum topic is API design, ask about API
design using Java or Spring Boot.

If the candidate stack is:
Python

and the curriculum topic happens to be Kubernetes,
DO NOT ask a Kubernetes question. Adapt the engineering
concept to Python, or ask a Python engineering question
that tests a related concept.

Never make an out-of-stack technology the primary subject
of the question.


==========================================================
QUESTION VARIATION
==========================================================

Rotate between different question styles when appropriate:

- Practical implementation
- Debugging
- Architecture
- System design
- Performance
- Scalability
- Security
- Failure handling
- Trade-offs
- Code/design decisions
- Production scenarios
- Optimization
- Reliability


Do not repeatedly use the same question style.


==========================================================
EXAMPLE
==========================================================

Candidate Stack:

Python, FastAPI, PostgreSQL


Current Topic:

Backend API Design


Bad:

What is FastAPI?


Also bad:

How would you design a FastAPI API?


Better:

Your FastAPI service receives thousands of concurrent
requests and PostgreSQL becomes the bottleneck. How
would you diagnose the issue and redesign the request
flow?


Another possible question:

Your FastAPI endpoint occasionally returns stale data.
How would you investigate the caching strategy and decide
where consistency should be enforced?


Stack-bound example:

Candidate Stack:

Python


Current Topic:

Kubernetes


Bad:

How would you configure a Kubernetes deployment for
a Python service?


Better:

Your Python service handles increasing concurrent
requests and response latency is rising. How would you
diagnose the bottleneck and improve the service?


The curriculum can provide the engineering concept,
but the question must remain inside the candidate's
technology stack.


==========================================================
FINAL VALIDATION
==========================================================

Before returning the question, verify:

1. The primary technology in the question exists in the
   candidate's Technology Stack.
2. No unrelated technology is introduced as the subject.
3. The question is still technically meaningful.
4. The question is not a duplicate of a previous question.

If the current curriculum topic conflicts with the
candidate's technology stack, prioritize the technology
stack and adapt the engineering concept.

==========================================================
FINAL INSTRUCTION
==========================================================

Generate ONE new technical interview question now.

Return ONLY the question.
"""


    # ======================================================
    # CALL LLM
    # ======================================================

    response = llm.invoke(
        prompt
    )


    # ======================================================
    # EXTRACT RESPONSE
    # ======================================================

    question = response.content.strip()


    # ======================================================
    # CLEAN ACCIDENTAL FORMATTING
    # ======================================================

    # Remove code fences if the model accidentally returns them.

    if question.startswith(
        "```"
    ):

        question = (
            question
            .replace(
                "```text",
                ""
            )
            .replace(
                "```",
                ""
            )
            .strip()
        )


    # Remove accidental labels.

    prefixes = [

        "Question:",

        "Interview Question:",

        "Technical Question:",

    ]


    for prefix in prefixes:

        if question.lower().startswith(
            prefix.lower()
        ):

            question = question[
                len(prefix):
            ].strip()


    # ======================================================
    # VALIDATION
    # ======================================================

    if not question:

        raise ValueError(
            "LLM returned an empty interview question."
        )


    # ======================================================
    # BASIC DUPLICATE PROTECTION
    # ======================================================

    normalized_question = (
        question
        .lower()
        .strip()
        .replace(
            "?",
            ""
        )
        .replace(
            ".",
            ""
        )
    )


    for previous in cleaned_previous_questions:

        normalized_previous = (
            previous
            .lower()
            .strip()
            .replace(
                "?",
                ""
            )
            .replace(
                ".",
                ""
            )
        )


        if (
            normalized_question
            == normalized_previous
        ):

            raise ValueError(
                "LLM generated a duplicate "
                "interview question."
            )


    return question