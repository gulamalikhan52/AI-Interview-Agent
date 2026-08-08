# PROMPTS.md

# AI Interview Agent — Prompt & AI Usage Log

## 1. Project Goal

The goal of this project is to build an AI Interview Agent that
conducts personalized, multi-turn technical interviews based on
a candidate's learning journey through the AI Cohort.

The agent should:

- Identify relevant completed curriculum topics.
- Generate technical interview questions.
- Evaluate candidate answers.
- Generate contextual follow-up questions.
- Maintain interview context.
- Generate structured final feedback.

---

# 2. Question Generation

## Purpose

Generate a technical interview question based on the candidate's
profile and a completed curriculum lesson.

## Prompt

The interviewer should act as an experienced technical interviewer.

Given:

- Candidate profile
- Candidate experience
- Completed curriculum topic
- Curriculum objectives
- Tools associated with the topic

Generate one realistic technical interview question.

The question should:

- Test practical technical understanding.
- Be relevant to the selected curriculum topic.
- Consider the candidate's experience.
- Focus on engineering decisions and trade-offs.
- Avoid simple definition-based questions where possible.
- Be appropriate for a real technical interview.

Return only the interview question.

---

# 3. Answer Evaluation

## Purpose

Evaluate the candidate's response to determine their technical
understanding.

## Prompt

Act as an expert technical interviewer.

Evaluate the candidate's answer based on:

- Technical correctness
- Relevance
- Depth
- Practical engineering understanding
- Completeness

Return a structured evaluation containing:

- score from 1 to 10
- strengths
- weaknesses
- follow_up_needed

A follow-up should be generated when the candidate's answer
contains important technical gaps that should be explored further.

---

# 4. Follow-up Question Generation

## Purpose

Generate an intelligent follow-up based on the candidate's
previous answer and its evaluation.

## Prompt

Act as a technical interviewer conducting a live interview.

Given:

- Original question
- Candidate answer
- Evaluation
- Identified weaknesses

Generate one contextual follow-up question.

The follow-up should:

- Directly target a weakness.
- Build on the candidate's previous answer.
- Test deeper understanding.
- Avoid simply repeating the original question.
- Sound natural in a real technical interview.

Return only the follow-up question.

---

# 5. Final Feedback

## Purpose

Provide actionable feedback after the interview.

## Prompt

Act as an expert technical interviewer reviewing the candidate's
complete interview history.

Analyze:

- Questions asked
- Candidate answers
- Scores
- Strengths
- Weaknesses

Generate structured feedback containing:

- Overall assessment
- Technical strengths
- Technical gaps
- Recommended areas for improvement
- Recommended next steps

The feedback should be specific to the candidate's actual
interview performance.

---

# 6. Interview Context

The agent maintains state throughout the interview.

The state contains information such as:

- session ID
- candidate ID
- candidate profile
- completed curriculum days
- asked curriculum days
- current day
- current lesson
- current question
- candidate answer
- evaluation
- question count
- interview history
- follow-up state
- final feedback

This state allows the agent to maintain context across multiple
HTTP requests using the same session ID.

---

# 7. Adaptive Follow-up Strategy

The interview follows this general process:

Main Question
↓
Candidate Answer
↓
Answer Evaluation
↓
Follow-up Required?
├── Yes → Generate Follow-up
│ ↓
│ Candidate Answer
│ ↓
│ Continue Interview
│
└── No → Select Next Topic
↓
Generate Next Question

A follow-up is generated only when the evaluation identifies
a meaningful technical gap.

The system prevents an unlimited follow-up loop by tracking
whether a follow-up is currently pending.

---

# 8. Interview Completion

The interview is limited to a maximum of eight main questions.

The agent should cover multiple completed curriculum topics
rather than repeatedly asking about the same topic.

After the interview is completed, the complete interview history
is passed to the feedback generator.

The final response contains:

- completion status
- structured feedback
- strengths
- technical gaps
- recommended next steps

---

# 9. AI-Assisted Development Log

AI assistance was used during development for:

- Project architecture
- FastAPI API design
- LangGraph state management
- Prompt design
- Question generation logic
- Answer evaluation logic
- Follow-up generation
- Final feedback generation
- Streamlit frontend development
- Dependency troubleshooting
- Debugging
- Iterative testing

The generated code and prompts were tested against the actual
interview workflow and modified during development based on
observed behavior.

---

# 10. Development Verification

The interview flow was tested through the HTTP API.

The verified flow is:

Start interview
↓
Receive question
↓
Submit answer using the same session ID
↓
Evaluate answer
↓
Generate contextual follow-up when required
↓
Submit follow-up answer
↓
Generate next question
↓
Continue interview
↓
Generate final structured feedback
