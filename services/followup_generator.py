from services.llm import llm


def generate_followup(
    question: str,
    answer: str,
    evaluation: dict,
) -> str:

    # ======================================================
    # EXTRACT WEAKNESSES
    # ======================================================

    weaknesses = evaluation.get(
        "weaknesses",
        [],
    )

    if not isinstance(
        weaknesses,
        list,
    ):
        weaknesses = [
            str(weaknesses)
        ]


    weaknesses = [

        str(weakness).strip()

        for weakness in weaknesses

        if str(weakness).strip()
    ]


    weaknesses_text = "\n".join(

        f"- {weakness}"

        for weakness in weaknesses
    )


    if not weaknesses_text:

        weaknesses_text = (
            "- Identify the most important "
            "technical gap demonstrated in the answer."
        )


    # ======================================================
    # FOLLOW-UP PROMPT
    # ======================================================

    prompt = f"""
You are a Senior AI Technical Interviewer conducting
a realistic technical interview.

Original Question:
{question}

Candidate Answer:
{answer}

Identified Technical Weaknesses:
{weaknesses_text}


Generate ONE contextual technical follow-up question.


==========================================================
RULES
==========================================================

1. Ask exactly ONE question.

2. The follow-up must directly target a specific
   technical weakness identified in the candidate's answer.

3. Build on the candidate's actual previous answer.

4. Do NOT repeat the original question.

5. Do NOT simply rephrase the original question.

6. Ask about the missing concept, incorrect assumption,
   implementation detail, trade-off, or reasoning gap.

7. The question must be technically meaningful.

8. Prefer practical engineering scenarios,
   debugging, implementation, architecture,
   trade-offs, or failure cases.

9. Maximum 30 words.

10. Do not provide the answer.

11. Do not provide hints.

12. Do not explain anything.

13. Do not greet the candidate.

14. Return ONLY the question.

15. Plain text only.

16. Never return Markdown.

17. Never return HTML.

18. Never return XML.

19. Never add labels such as:
    Question:
    Follow-up:
    Interview Question:


==========================================================
EXAMPLE
==========================================================

Original Question:
How would you design a scalable API?

Candidate Answer:
I would add more servers and use a database.

Weakness:
The candidate did not discuss load balancing,
caching, database bottlenecks, or statelessness.

Good Follow-up:
How would you prevent the database from becoming the bottleneck
as traffic increases across multiple API instances?


Return ONLY the follow-up question.
"""


    # ======================================================
    # CALL LLM
    # ======================================================

    response = llm.invoke(
        prompt
    )


    followup = response.content.strip()


    # ======================================================
    # CLEAN RESPONSE
    # ======================================================

    if followup.startswith(
        "```"
    ):

        followup = (
            followup
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

        "Follow-up:",

        "Follow-up Question:",

        "Interview Question:",

        "Technical Question:",

    ]


    for prefix in prefixes:

        if followup.lower().startswith(
            prefix.lower()
        ):

            followup = followup[
                len(prefix):
            ].strip()


    # ======================================================
    # VALIDATION
    # ======================================================

    if not followup:

        raise ValueError(
            "LLM returned an empty follow-up question."
        )


    # ======================================================
    # WORD LIMIT
    # ======================================================

    words = followup.split()


    if len(words) > 30:

        followup = " ".join(
            words[:30]
        )


        # Make sure the result still looks like
        # a question.

        if not followup.endswith(
            "?"
        ):

            followup += "?"


    return followup