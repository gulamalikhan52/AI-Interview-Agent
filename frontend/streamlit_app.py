# import streamlit as st
# import requests
# import uuid


# # ==========================================================
# # CONFIG
# # ==========================================================

# API_URL = "http://127.0.0.1:8000"

# st.set_page_config(
#     page_title="AI Interview Agent",
#     page_icon="AI",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )


# # ==========================================================
# # CUSTOM CSS
# # ==========================================================

# st.markdown(
#     """
#     <style>

#     /* ---------- GLOBAL ---------- */

#     .stApp {
#         background:
#             radial-gradient(
#                 circle at 15% 10%,
#                 rgba(99, 102, 241, 0.12),
#                 transparent 30%
#             ),
#             radial-gradient(
#                 circle at 85% 85%,
#                 rgba(139, 92, 246, 0.10),
#                 transparent 30%
#             ),
#             #080b12;
#         color: #f1f5f9;
#     }

#     .block-container {
#         max-width: 1250px;
#         padding-top: 2rem;
#         padding-bottom: 3rem;
#     }

#     /* ---------- SIDEBAR ---------- */

#     [data-testid="stSidebar"] {
#         background: #0c1018;
#         border-right: 1px solid rgba(255,255,255,0.07);
#     }

#     [data-testid="stSidebar"] .block-container {
#         padding-top: 2rem;
#     }

#     /* ---------- HEADERS ---------- */

#     .brand {
#         font-size: 28px;
#         font-weight: 800;
#         letter-spacing: -0.8px;
#         margin-bottom: 2px;
#     }

#     .brand span {
#         color: #8b5cf6;
#     }

#     .subtitle {
#         color: #94a3b8;
#         font-size: 14px;
#         margin-bottom: 30px;
#     }

#     /* ---------- LIVE STATUS ---------- */

#     .live-status {
#         display: inline-flex;
#         align-items: center;
#         gap: 8px;
#         padding: 7px 12px;
#         border-radius: 999px;
#         background: rgba(34,197,94,0.08);
#         border: 1px solid rgba(34,197,94,0.20);
#         color: #86efac;
#         font-size: 12px;
#         font-weight: 600;
#     }

#     .live-dot {
#         width: 7px;
#         height: 7px;
#         border-radius: 50%;
#         background: #22c55e;
#         box-shadow: 0 0 10px rgba(34,197,94,0.8);
#     }

#     /* ---------- CARDS ---------- */

#     .card {
#         background: rgba(15, 20, 31, 0.88);
#         border: 1px solid rgba(255,255,255,0.07);
#         border-radius: 18px;
#         padding: 24px;
#         box-shadow: 0 18px 45px rgba(0,0,0,0.22);
#     }

#     .question-card {
#         background:
#             linear-gradient(
#                 135deg,
#                 rgba(99,102,241,0.12),
#                 rgba(139,92,246,0.05)
#             ),
#             #0f141f;
#         border: 1px solid rgba(139,92,246,0.22);
#         border-radius: 20px;
#         padding: 30px;
#         margin: 18px 0 24px 0;
#     }

#     .question-label {
#         color: #a78bfa;
#         font-size: 12px;
#         font-weight: 700;
#         text-transform: uppercase;
#         letter-spacing: 1.3px;
#         margin-bottom: 12px;
#     }

#     .question-text {
#         color: #f8fafc;
#         font-size: 22px;
#         line-height: 1.55;
#         font-weight: 600;
#     }

#     /* ---------- CHAT ---------- */

#     .chat-wrapper {
#         background: #0b1018;
#         border: 1px solid rgba(255,255,255,0.06);
#         border-radius: 18px;
#         padding: 18px;
#         margin-bottom: 20px;
#     }

#     .chat-label {
#         font-size: 11px;
#         font-weight: 700;
#         text-transform: uppercase;
#         letter-spacing: 1px;
#         color: #64748b;
#         margin-bottom: 10px;
#     }

#     /* ---------- PROFILE ---------- */

#     .profile-name {
#         font-size: 20px;
#         font-weight: 750;
#         color: #f8fafc;
#     }

#     .profile-role {
#         color: #94a3b8;
#         font-size: 13px;
#         margin-top: 3px;
#         margin-bottom: 18px;
#     }

#     .stat-box {
#         background: #111722;
#         border: 1px solid rgba(255,255,255,0.06);
#         border-radius: 12px;
#         padding: 12px;
#         margin-top: 10px;
#     }

#     .stat-label {
#         color: #64748b;
#         font-size: 11px;
#         text-transform: uppercase;
#         letter-spacing: 0.8px;
#     }

#     .stat-value {
#         color: #e2e8f0;
#         font-size: 15px;
#         font-weight: 650;
#         margin-top: 3px;
#     }

#     /* ---------- FEEDBACK ---------- */

#     .score-card {
#         text-align: center;
#         background:
#             radial-gradient(
#                 circle at center,
#                 rgba(139,92,246,0.18),
#                 transparent 65%
#             ),
#             #101521;
#         border: 1px solid rgba(139,92,246,0.22);
#         border-radius: 22px;
#         padding: 35px;
#         margin-bottom: 24px;
#     }

#     .score-label {
#         color: #94a3b8;
#         font-size: 13px;
#         text-transform: uppercase;
#         letter-spacing: 1px;
#     }

#     .score-value {
#         color: #c4b5fd;
#         font-size: 58px;
#         font-weight: 800;
#         line-height: 1.1;
#         margin-top: 8px;
#     }

#     .feedback-card {
#         background: #0f141f;
#         border: 1px solid rgba(255,255,255,0.07);
#         border-radius: 16px;
#         padding: 22px;
#         min-height: 160px;
#     }

#     .feedback-title {
#         font-size: 15px;
#         font-weight: 700;
#         color: #e2e8f0;
#         margin-bottom: 12px;
#     }

#     .feedback-item {
#         color: #94a3b8;
#         font-size: 14px;
#         line-height: 1.6;
#         margin: 7px 0;
#     }

#     /* ---------- BUTTONS ---------- */

#     .stButton > button {
#         border-radius: 10px;
#         border: 1px solid rgba(139,92,246,0.25);
#         font-weight: 650;
#         min-height: 44px;
#     }

#     /* ---------- INPUT ---------- */

#     textarea {
#         background-color: #0d121b !important;
#         color: #f8fafc !important;
#         border-radius: 14px !important;
#     }

#     /* ---------- PROGRESS ---------- */

#     .progress-container {
#         background: #111722;
#         border-radius: 999px;
#         height: 8px;
#         overflow: hidden;
#         margin-top: 10px;
#     }

#     .progress-bar {
#         height: 100%;
#         border-radius: 999px;
#         background: linear-gradient(
#             90deg,
#             #6366f1,
#             #8b5cf6
#         );
#     }

#     /* ---------- MOBILE ---------- */

#     @media (max-width: 900px) {

#         .question-text {
#             font-size: 18px;
#         }

#         .question-card {
#             padding: 22px;
#         }

#     }

#     </style>
#     """,
#     unsafe_allow_html=True,
# )


# # ==========================================================
# # SESSION STATE
# # ==========================================================

# defaults = {
#     "session_id": str(uuid.uuid4()),
#     "started": False,
#     "candidate": None,
#     "messages": [],
#     "interview_complete": False,
#     "feedback": None,
#     "question_count": 0,
# }

# for key, value in defaults.items():

#     if key not in st.session_state:
#         st.session_state[key] = value


# # ==========================================================
# # SIDEBAR
# # ==========================================================

# with st.sidebar:

#     st.markdown(
#         """
#         <div class="brand">
#             AI <span>Interviewer</span>
#         </div>
#         <div class="subtitle">
#             Adaptive technical assessment
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     if st.session_state.started:

#         st.markdown(
#             """
#             <div class="live-status">
#                 <span class="live-dot"></span>
#                 INTERVIEW LIVE
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#     st.markdown("### Candidate")

#     candidate_id = st.text_input(
#         "Candidate ID",
#         value="CAND-001",
#         disabled=st.session_state.started,
#     )

#     candidate_name = st.text_input(
#         "Name",
#         value="Sarah Johnson",
#         disabled=st.session_state.started,
#     )

#     job_role = st.text_input(
#         "Job Role",
#         value="Senior Data Engineer",
#         disabled=st.session_state.started,
#     )

#     years_experience = st.number_input(
#         "Experience",
#         min_value=0,
#         max_value=50,
#         value=9,
#         disabled=st.session_state.started,
#     )

#     st.divider()

#     if st.session_state.started:

#         st.markdown("### Interview Progress")

#         # Number of completed question cycles.
#         progress = min(
#             st.session_state.question_count / 8,
#             1.0,
#         )

#         st.progress(progress)

#         st.caption(
#             f"{st.session_state.question_count} / 8 questions completed"
#         )

#     st.divider()

#     st.caption("Session")

#     st.code(
#         st.session_state.session_id[:12],
#         language=None,
#     )


# # ==========================================================
# # LANDING PAGE
# # ==========================================================

# if not st.session_state.started:

#     col1, col2 = st.columns(
#         [1.7, 1],
#         gap="large",
#     )

#     with col1:

#         st.markdown(
#             """
#             <div style="margin-top:45px;">

#             <div style="
#                 color:#a78bfa;
#                 font-size:13px;
#                 font-weight:700;
#                 text-transform:uppercase;
#                 letter-spacing:1.5px;
#                 margin-bottom:12px;
#             ">
#                 AI-POWERED TECHNICAL ASSESSMENT
#             </div>

#             <div style="
#                 font-size:48px;
#                 font-weight:800;
#                 line-height:1.05;
#                 letter-spacing:-2px;
#                 color:#f8fafc;
#             ">
#                 Think like an<br>
#                 <span style="color:#8b5cf6;">
#                 AI Engineer.
#                 </span>
#             </div>

#             <div style="
#                 color:#94a3b8;
#                 font-size:17px;
#                 line-height:1.7;
#                 margin-top:22px;
#                 max-width:650px;
#             ">
#                 A personalized technical interview that adapts
#                 to your answers, challenges your understanding,
#                 and identifies the areas you should improve.
#             </div>

#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#     with col2:

#         st.markdown(
#             """
#             <div class="card" style="margin-top:45px;">

#             <div style="
#                 color:#a78bfa;
#                 font-size:12px;
#                 font-weight:700;
#                 letter-spacing:1px;
#                 text-transform:uppercase;
#             ">
#                 INTERVIEW FORMAT
#             </div>

#             <h3 style="color:#f8fafc;">
#                 Adaptive Interview
#             </h3>

#             <p style="color:#94a3b8; line-height:1.6;">
#                 Questions are generated from the candidate's
#                 completed learning journey.
#             </p>

#             <hr style="border-color:#1e293b;">

#             <p style="color:#94a3b8;">
#                 • Technical questions
#             </p>

#             <p style="color:#94a3b8;">
#                 • Intelligent follow-ups
#             </p>

#             <p style="color:#94a3b8;">
#                 • Context-aware evaluation
#             </p>

#             <p style="color:#94a3b8;">
#                 • Final performance feedback
#             </p>

#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#     st.write("")

#     if st.button(
#         "Start Technical Interview",
#         type="primary",
#         use_container_width=True,
#     ):

#         candidate = {
#             "member": {
#                 "id": candidate_id,
#                 "name": candidate_name,
#                 "jobRole": job_role,
#                 "yearsExperience": years_experience,
#             }
#         }

#         try:

#             with st.spinner(
#                 "Preparing your personalized interview..."
#             ):

#                 response = requests.post(
#                     f"{API_URL}/api/interview",
#                     json={
#                         "sessionId": st.session_state.session_id,
#                         "candidate": candidate,
#                     },
#                     timeout=120,
#                 )

#             if response.status_code != 200:

#                 st.error(
#                     f"Backend error: {response.status_code}"
#                 )

#                 st.code(response.text)

#             else:

#                 data = response.json()

#                 st.session_state.started = True
#                 st.session_state.candidate = candidate

#                 st.session_state.messages = [
#                     {
#                         "role": "interviewer",
#                         "content": data["reply"],
#                     }
#                 ]

#                 st.rerun()

#         except requests.exceptions.ConnectionError:

#             st.error(
#                 "Unable to connect to the FastAPI backend."
#             )

#             st.info(
#                 "Make sure FastAPI is running on port 8000."
#             )

#         except requests.exceptions.Timeout:

#             st.error(
#                 "The interviewer took too long to respond."
#             )

#         except Exception as e:

#             st.error(
#                 f"Unexpected error: {e}"
#             )


# # ==========================================================
# # INTERVIEW SCREEN
# # ==========================================================

# elif (
#     st.session_state.started
#     and not st.session_state.interview_complete
# ):

#     # ------------------------------------------------------
#     # Top Header
#     # ------------------------------------------------------

#     header_left, header_right = st.columns(
#         [3, 1]
#     )

#     with header_left:

#         st.markdown(
#             """
#             <div class="brand">
#                 Technical <span>Interview</span>
#             </div>

#             <div class="subtitle">
#                 Answer clearly. Explain your reasoning.
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#     with header_right:

#         st.markdown(
#             """
#             <div style="text-align:right;">
#                 <div class="live-status">
#                     <span class="live-dot"></span>
#                     LIVE
#                 </div>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )


#     # ------------------------------------------------------
#     # Question number
#     # ------------------------------------------------------

#     st.caption(
#         f"QUESTION {min(st.session_state.question_count + 1, 8)} / 8"
#     )


#     # ------------------------------------------------------
#     # Current Question
#     # ------------------------------------------------------

#     current_question = ""

#     if st.session_state.messages:

#         for message in reversed(
#             st.session_state.messages
#         ):

#             if message["role"] == "interviewer":

#                 current_question = message["content"]

#                 break


#     st.markdown(
#         f"""
#         <div class="question-card">

#             <div class="question-label">
#                 Interviewer Question
#             </div>

#             <div class="question-text">
#                 {current_question}
#             </div>

#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


#     # ------------------------------------------------------
#     # Conversation History
#     # ------------------------------------------------------

#     with st.expander(
#         "View conversation history",
#         expanded=False,
#     ):

#         for message in st.session_state.messages:

#             if message["role"] == "interviewer":

#                 st.markdown("**Interviewer**")

#             else:

#                 st.markdown("**You**")

#             st.write(message["content"])

#             st.divider()


#     # ------------------------------------------------------
#     # Answer
#     # ------------------------------------------------------

#     st.markdown(
#         """
#         <div class="chat-label">
#             YOUR RESPONSE
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )

#     answer = st.text_area(
#         "",
#         placeholder=(
#             "Explain your approach, architecture, "
#             "trade-offs, and reasoning..."
#         ),
#         height=190,
#         label_visibility="collapsed",
#         key="answer_box",
#     )


#     # ------------------------------------------------------
#     # Submit
#     # ------------------------------------------------------

#     if st.button(
#         "Submit Answer",
#         type="primary",
#         use_container_width=True,
#     ):

#         if not answer.strip():

#             st.warning(
#                 "Please provide an answer before submitting."
#             )

#             st.stop()


#         # Save candidate response
#         st.session_state.messages.append(
#             {
#                 "role": "candidate",
#                 "content": answer,
#             }
#         )


#         try:

#             with st.spinner(
#                 "Evaluating your response..."
#             ):

#                 response = requests.post(
#                     f"{API_URL}/api/interview",
#                     json={
#                         "sessionId": st.session_state.session_id,
#                         "message": answer,
#                     },
#                     timeout=120,
#                 )


#             if response.status_code != 200:

#                 st.error(
#                     f"Backend error: {response.status_code}"
#                 )

#                 st.code(response.text)

#                 st.stop()


#             data = response.json()


#             # ------------------------------------------------
#             # COMPLETED
#             # ------------------------------------------------

#             if data.get("done") is True:

#                 st.session_state.interview_complete = True

#                 st.session_state.feedback = data.get(
#                     "feedback",
#                     {},
#                 )

#                 st.session_state.messages.append(
#                     {
#                         "role": "interviewer",
#                         "content": data.get(
#                             "reply",
#                             "Interview completed.",
#                         ),
#                     }
#                 )

#                 st.rerun()


#             # ------------------------------------------------
#             # NEXT QUESTION
#             # ------------------------------------------------

#             next_question = data.get(
#                 "reply",
#                 "",
#             )

#             st.session_state.messages.append(
#                 {
#                     "role": "interviewer",
#                     "content": next_question,
#                 }
#             )

#             st.session_state.question_count += 1

#             st.rerun()


#         except requests.exceptions.ConnectionError:

#             st.error(
#                 "Unable to connect to the FastAPI backend."
#             )

#         except requests.exceptions.Timeout:

#             st.error(
#                 "The backend took too long to respond."
#             )

#         except Exception as e:

#             st.error(
#                 f"Unexpected error: {e}"
#             )


# # ==========================================================
# # FINAL FEEDBACK
# # ==========================================================

# else:

#     feedback = (
#         st.session_state.feedback
#         or {}
#     )

#     st.markdown(
#         """
#         <div style="
#             text-align:center;
#             padding:25px 0 10px 0;
#         ">

#         <div style="
#             color:#86efac;
#             font-size:12px;
#             font-weight:700;
#             letter-spacing:1.5px;
#         ">
#             INTERVIEW COMPLETE
#         </div>

#         <div style="
#             color:#f8fafc;
#             font-size:40px;
#             font-weight:800;
#             margin-top:8px;
#         ">
#             Performance Review
#         </div>

#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


#     # ------------------------------------------------------
#     # Score
#     # ------------------------------------------------------

#     score = feedback.get(
#         "overall_score",
#         feedback.get("score", "N/A"),
#     )

#     st.markdown(
#         f"""
#         <div class="score-card">

#             <div class="score-label">
#                 Overall Performance
#             </div>

#             <div class="score-value">
#                 {score}
#                 <span style="
#                     font-size:24px;
#                     color:#64748b;
#                 ">
#                     / 10
#                 </span>
#             </div>

#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


#     # ------------------------------------------------------
#     # Summary
#     # ------------------------------------------------------

#     summary = feedback.get(
#         "summary",
#         "Your interview has been evaluated.",
#     )

#     st.markdown(
#         f"""
#         <div class="card" style="margin-bottom:20px;">

#             <div class="feedback-title">
#                 Overall Assessment
#             </div>

#             <div class="feedback-item">
#                 {summary}
#             </div>

#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


#     # ------------------------------------------------------
#     # Three Feedback Columns
#     # ------------------------------------------------------

#     col1, col2, col3 = st.columns(
#         3,
#         gap="medium",
#     )


#     with col1:

#         strengths = feedback.get(
#             "strengths",
#             [],
#         )

#         items = "".join(
#             f'<div class="feedback-item">• {item}</div>'
#             for item in strengths
#         )

#         st.markdown(
#             f"""
#             <div class="feedback-card">

#                 <div class="feedback-title">
#                     Strengths
#                 </div>

#                 {items}

#             </div>
#             """,
#             unsafe_allow_html=True,
#         )


#     with col2:

#         gaps = feedback.get(
#             "gaps",
#             feedback.get(
#                 "weaknesses",
#                 [],
#             ),
#         )

#         items = "".join(
#             f'<div class="feedback-item">• {item}</div>'
#             for item in gaps
#         )

#         st.markdown(
#             f"""
#             <div class="feedback-card">

#                 <div class="feedback-title">
#                     Knowledge Gaps
#                 </div>

#                 {items}

#             </div>
#             """,
#             unsafe_allow_html=True,
#         )


#     with col3:

#         next_steps = feedback.get(
#             "next",
#             feedback.get(
#                 "recommendations",
#                 [],
#             ),
#         )

#         items = "".join(
#             f'<div class="feedback-item">• {item}</div>'
#             for item in next_steps
#         )

#         st.markdown(
#             f"""
#             <div class="feedback-card">

#                 <div class="feedback-title">
#                     Recommended Next Steps
#                 </div>

#                 {items}

#             </div>
#             """,
#             unsafe_allow_html=True,
#         )


#     # ------------------------------------------------------
#     # Hiring Recommendation
#     # ------------------------------------------------------

#     recommendation = feedback.get(
#         "hiring_recommendation",
#         "",
#     )

#     if recommendation:

#         st.write("")

#         st.markdown(
#             f"""
#             <div class="card" style="text-align:center;">

#                 <div class="feedback-title">
#                     Hiring Recommendation
#                 </div>

#                 <div style="
#                     font-size:20px;
#                     font-weight:750;
#                     color:#c4b5fd;
#                     margin-top:10px;
#                 ">
#                     {recommendation}
#                 </div>

#             </div>
#             """,
#             unsafe_allow_html=True,
#         )


#     st.write("")

#     # ------------------------------------------------------
#     # New Interview
#     # ------------------------------------------------------

#     if st.button(
#         "Start New Interview",
#         type="primary",
#         use_container_width=True,
#     ):

#         st.session_state.session_id = str(
#             uuid.uuid4()
#         )

#         st.session_state.started = False
#         st.session_state.candidate = None
#         st.session_state.messages = []
#         st.session_state.interview_complete = False
#         st.session_state.feedback = None
#         st.session_state.question_count = 0

#         st.rerun()

import html
import re
import streamlit as st
import requests
import uuid


# ==========================================================
# CONFIG
# ==========================================================

import os

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="AI Interview Agent",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(99, 102, 241, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 85% 85%,
                rgba(139, 92, 246, 0.10),
                transparent 30%
            ),
            #080b12;
        color: #f1f5f9;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #0c1018;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* ---------- HEADERS ---------- */

    .brand {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin-bottom: 2px;
    }

    .brand span {
        color: #8b5cf6;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 30px;
    }

    /* ---------- LIVE STATUS ---------- */

    .live-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.20);
        color: #86efac;
        font-size: 12px;
        font-weight: 600;
    }

    .live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 10px rgba(34,197,94,0.8);
    }

    /* ---------- CARDS ---------- */

    .card {
        background: rgba(15, 20, 31, 0.88);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.22);
    }

    .question-card {
        background:
            linear-gradient(
                135deg,
                rgba(99,102,241,0.12),
                rgba(139,92,246,0.05)
            ),
            #0f141f;
        border: 1px solid rgba(139,92,246,0.22);
        border-radius: 20px;
        padding: 30px;
        margin: 18px 0 24px 0;
    }

    .question-label {
        color: #a78bfa;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        margin-bottom: 12px;
    }

    .question-text {
        color: #f8fafc;
        font-size: 22px;
        line-height: 1.55;
        font-weight: 600;
    }

    /* ---------- CHAT ---------- */

    .chat-wrapper {
        background: #0b1018;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 20px;
    }

    .chat-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748b;
        margin-bottom: 10px;
    }

    /* ---------- PROFILE ---------- */

    .profile-name {
        font-size: 20px;
        font-weight: 750;
        color: #f8fafc;
    }

    .profile-role {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 3px;
        margin-bottom: 18px;
    }

    .stat-box {
        background: #111722;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 12px;
        margin-top: 10px;
    }

    .stat-label {
        color: #64748b;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .stat-value {
        color: #e2e8f0;
        font-size: 15px;
        font-weight: 650;
        margin-top: 3px;
    }

    /* ---------- FEEDBACK ---------- */

    .score-card {
        text-align: center;
        background:
            radial-gradient(
                circle at center,
                rgba(139,92,246,0.18),
                transparent 65%
            ),
            #101521;
        border: 1px solid rgba(139,92,246,0.22);
        border-radius: 22px;
        padding: 35px;
        margin-bottom: 24px;
    }

    .score-label {
        color: #94a3b8;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .score-value {
        color: #c4b5fd;
        font-size: 58px;
        font-weight: 800;
        line-height: 1.1;
        margin-top: 8px;
    }

    .feedback-card {
        background: #0f141f;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 22px;
        min-height: 160px;
    }

    .feedback-title {
        font-size: 15px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 12px;
    }

    .feedback-item {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.6;
        margin: 7px 0;
    }

    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 10px;
        border: 1px solid rgba(139,92,246,0.25);
        font-weight: 650;
        min-height: 44px;
    }

    /* ---------- INPUT ---------- */

    textarea {
        background-color: #0d121b !important;
        color: #f8fafc !important;
        border-radius: 14px !important;
    }

    /* ---------- PROGRESS ---------- */

    .progress-container {
        background: #111722;
        border-radius: 999px;
        height: 8px;
        overflow: hidden;
        margin-top: 10px;
    }

    .progress-bar {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(
            90deg,
            #6366f1,
            #8b5cf6
        );
    }

    /* ---------- MOBILE ---------- */

    @media (max-width: 900px) {

        .question-text {
            font-size: 18px;
        }

        .question-card {
            padding: 22px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# HELPERS
# ==========================================================

def clean_text(value):
    """Convert LLM/API output to safe plain text for the UI."""
    if value is None:
        return ""
    value = str(value)
    value = re.sub(r"<[^>]*>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def safe_list(value):
    if not isinstance(value, list):
        return []
    return [clean_text(item) for item in value if clean_text(item)]


def reset_interview():
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.started = False
    st.session_state.candidate = None
    st.session_state.messages = []
    st.session_state.interview_complete = False
    st.session_state.feedback = None
    st.session_state.question_count = 0
    if "answer_box" in st.session_state:
        del st.session_state["answer_box"]


# ==========================================================
# SESSION STATE
# ==========================================================

defaults = {
    "session_id": str(uuid.uuid4()),
    "started": False,
    "candidate": None,
    "messages": [],
    "interview_complete": False,
    "feedback": None,
    "question_count": 0,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            AI <span>Interviewer</span>
        </div>
        <div class="subtitle">
            Adaptive technical assessment
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.started:

        st.markdown(
            """
            <div class="live-status">
                <span class="live-dot"></span>
                INTERVIEW LIVE
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Candidate")

    candidate_id = st.text_input(
        "Candidate ID",
        value="CAND-001",
        disabled=st.session_state.started,
    )

    candidate_name = st.text_input(
        "Name",
        value="Sarah Johnson",
        disabled=st.session_state.started,
    )

    job_role = st.text_input(
        "Job Role",
        value="Senior Data Engineer",
        disabled=st.session_state.started,
    )

    years_experience = st.number_input(
        "Experience",
        min_value=0,
        max_value=50,
        value=9,
        disabled=st.session_state.started,
    )

    st.divider()

    if st.session_state.started:

        st.markdown("### Interview Progress")

        # Number of completed question cycles.
        progress = min(
            st.session_state.question_count / 8,
            1.0,
        )

        st.progress(progress)

        st.caption(
            f"{st.session_state.question_count} / 8 questions completed"
        )

    st.divider()

    st.caption("Session")

    st.code(
        st.session_state.session_id[:12],
        language=None,
    )


# ==========================================================
# LANDING PAGE
# ==========================================================

if not st.session_state.started:

    col1, col2 = st.columns(
        [1.7, 1],
        gap="large",
    )

    with col1:

        st.markdown(
            """
            <div style="margin-top:45px;">

            <div style="
                color:#a78bfa;
                font-size:13px;
                font-weight:700;
                text-transform:uppercase;
                letter-spacing:1.5px;
                margin-bottom:12px;
            ">
                AI-POWERED TECHNICAL ASSESSMENT
            </div>

            <div style="
                font-size:48px;
                font-weight:800;
                line-height:1.05;
                letter-spacing:-2px;
                color:#f8fafc;
            ">
                Think like an<br>
                <span style="color:#8b5cf6;">
                AI Engineer.
                </span>
            </div>

            <div style="
                color:#94a3b8;
                font-size:17px;
                line-height:1.7;
                margin-top:22px;
                max-width:650px;
            ">
                A personalized technical interview that adapts
                to your answers, challenges your understanding,
                and identifies the areas you should improve.
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="card" style="margin-top:45px;">

            <div style="
                color:#a78bfa;
                font-size:12px;
                font-weight:700;
                letter-spacing:1px;
                text-transform:uppercase;
            ">
                INTERVIEW FORMAT
            </div>

            <h3 style="color:#f8fafc;">
                Adaptive Interview
            </h3>

            <p style="color:#94a3b8; line-height:1.6;">
                Questions are generated from the candidate's
                completed learning journey.
            </p>

            <hr style="border-color:#1e293b;">

            <p style="color:#94a3b8;">
                • Technical questions
            </p>

            <p style="color:#94a3b8;">
                • Intelligent follow-ups
            </p>

            <p style="color:#94a3b8;">
                • Context-aware evaluation
            </p>

            <p style="color:#94a3b8;">
                • Final performance feedback
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    if st.button(
        "Start Technical Interview",
        type="primary",
        use_container_width=True,
    ):

        candidate = {
            "member": {
                "id": candidate_id,
                "name": candidate_name,
                "jobRole": job_role,
                "yearsExperience": years_experience,
            }
        }

        try:

            with st.spinner(
                "Preparing your personalized interview..."
            ):

                response = requests.post(
                    f"{API_URL}/api/interview",
                    json={
                        "sessionId": st.session_state.session_id,
                        "candidate": candidate,
                    },
                    timeout=120,
                )

            if response.status_code != 200:

                st.error(
                    f"Backend error: {response.status_code}"
                )

                st.code(response.text)

            else:

                data = response.json()

                st.session_state.started = True
                st.session_state.candidate = candidate

                first_question = clean_text(data.get("reply", ""))

                if not first_question:
                    st.error("The backend did not return an interview question.")
                    st.stop()

                st.session_state.messages = [
                    {
                        "role": "interviewer",
                        "content": first_question,
                    }
                ]

                st.rerun()

        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to the FastAPI backend."
            )

            st.info(
                "Make sure FastAPI is running on port 8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The interviewer took too long to respond."
            )

        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )


# ==========================================================
# INTERVIEW SCREEN
# ==========================================================

elif (
    st.session_state.started
    and not st.session_state.interview_complete
):

    # ------------------------------------------------------
    # Top Header
    # ------------------------------------------------------

    header_left, header_right = st.columns(
        [3, 1]
    )

    with header_left:

        st.markdown(
            """
            <div class="brand">
                Technical <span>Interview</span>
            </div>

            <div class="subtitle">
                Answer clearly. Explain your reasoning.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with header_right:

        st.markdown(
            """
            <div style="text-align:right;">
                <div class="live-status">
                    <span class="live-dot"></span>
                    LIVE
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # ------------------------------------------------------
    # Question number
    # ------------------------------------------------------

    st.caption(
        f"QUESTION {min(st.session_state.question_count + 1, 8)} / 8"
    )


    # ------------------------------------------------------
    # Current Question
    # ------------------------------------------------------

    current_question = ""

    if st.session_state.messages:

        for message in reversed(
            st.session_state.messages
        ):

            if message["role"] == "interviewer":

                current_question = message["content"]

                break


    # Escape the LLM-generated question before putting it inside HTML.
    # This prevents accidental <div>, <span>, etc. from appearing as UI tags.
    safe_question = html.escape(
        clean_text(current_question or "Waiting for the next question...")
    )

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-label">
                Interviewer Question
            </div>
            <div class="question-text">
                {safe_question}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ------------------------------------------------------
    # Conversation History
    # ------------------------------------------------------

    with st.expander(
        "View conversation history",
        expanded=False,
    ):

        for message in st.session_state.messages:

            if message["role"] == "interviewer":

                st.markdown("**Interviewer**")

            else:

                st.markdown("**You**")

            st.write(message["content"])

            st.divider()


    # ------------------------------------------------------
    # Answer
    # ------------------------------------------------------

    st.markdown(
        """
        <div class="chat-label">
            YOUR RESPONSE
        </div>
        """,
        unsafe_allow_html=True,
    )

    answer = st.text_area(
        "",
        placeholder=(
            "Explain your approach, architecture, "
            "trade-offs, and reasoning..."
        ),
        height=190,
        label_visibility="collapsed",
        key="answer_box",
    )


    # ------------------------------------------------------
    # Submit
    # ------------------------------------------------------

    if st.button(
        "Submit Answer",
        type="primary",
        use_container_width=True,
    ):

        if not answer.strip():

            st.warning(
                "Please provide an answer before submitting."
            )

            st.stop()


        # Save candidate response
        st.session_state.messages.append(
            {
                "role": "candidate",
                "content": answer,
            }
        )


        try:

            with st.spinner(
                "Evaluating your response..."
            ):

                response = requests.post(
                    f"{API_URL}/api/interview",
                    json={
                        "sessionId": st.session_state.session_id,
                        "message": answer,
                    },
                    timeout=120,
                )


            if response.status_code != 200:

                st.error(
                    f"Backend error: {response.status_code}"
                )

                st.code(response.text)

                st.stop()


            data = response.json()


            # ------------------------------------------------
            # COMPLETED
            # ------------------------------------------------

            if data.get("done") is True:

                st.session_state.interview_complete = True

                st.session_state.feedback = data.get(
                    "feedback",
                    {},
                )

                st.session_state.messages.append(
                    {
                        "role": "interviewer",
                        "content": data.get(
                            "reply",
                            "Interview completed.",
                        ),
                    }
                )

                st.rerun()


            # ------------------------------------------------
            # NEXT QUESTION
            # ------------------------------------------------

            next_question = clean_text(
                data.get("reply", "")
            )

            st.session_state.messages.append(
                {
                    "role": "interviewer",
                    "content": next_question,
                }
            )

            st.session_state.question_count += 1

            st.rerun()


        except requests.exceptions.ConnectionError:

            st.error(
                "Unable to connect to the FastAPI backend."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The backend took too long to respond."
            )

        except Exception as e:

            st.error(
                f"Unexpected error: {e}"
            )


# ==========================================================
# FINAL FEEDBACK
# ==========================================================

else:

    feedback = st.session_state.feedback or {}

    # Backend schema: overall_score, strengths, weaknesses,
    # recommended_topics, hiring_recommendation.
    score = feedback.get(
        "overall_score",
        feedback.get("score", 0),
    )

    strengths = safe_list(feedback.get("strengths", []))
    weaknesses = safe_list(
        feedback.get("weaknesses", feedback.get("gaps", []))
    )
    recommended_topics = safe_list(
        feedback.get(
            "recommended_topics",
            feedback.get(
                "next",
                feedback.get("recommendations", []),
            ),
        )
    )
    recommendation = clean_text(
        feedback.get(
            "hiring_recommendation",
            "Needs Improvement",
        )
    ) or "Needs Improvement"

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:25px 0 10px 0;
        ">
            <div style="
                color:#86efac;
                font-size:12px;
                font-weight:700;
                letter-spacing:1.5px;
            ">
                INTERVIEW COMPLETE
            </div>
            <div style="
                color:#f8fafc;
                font-size:40px;
                font-weight:800;
                margin-top:8px;
            ">
                Performance Review
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------
    # Score
    # ------------------------------------------------------

    try:
        numeric_score = float(score)
        numeric_score = max(0.0, min(numeric_score, 10.0))
        score_display = (
            f"{numeric_score:.1f}"
            if numeric_score % 1
            else f"{int(numeric_score)}"
        )
    except (TypeError, ValueError):
        score_display = "0"

    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">Overall Performance</div>
            <div class="score-value">
                {html.escape(score_display)}
                <span style="font-size:24px;color:#64748b;">/ 10</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------
    # Overall Assessment
    # ------------------------------------------------------

    summary = clean_text(feedback.get("summary", ""))
    if summary:
        st.markdown("### Overall Assessment")
        st.info(summary)

    # ------------------------------------------------------
    # Feedback columns
    # ------------------------------------------------------

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("### Strengths")
        if strengths:
            for item in strengths:
                st.markdown(f"- {item}")
        else:
            st.caption("No strengths were returned.")

    with col2:
        st.markdown("### Knowledge Gaps")
        if weaknesses:
            for item in weaknesses:
                st.markdown(f"- {item}")
        else:
            st.caption("No weaknesses were returned.")

    with col3:
        st.markdown("### Recommended Next Steps")
        if recommended_topics:
            for item in recommended_topics:
                st.markdown(f"- {item}")
        else:
            st.caption("No recommended topics were returned.")

    # ------------------------------------------------------
    # Hiring Recommendation
    # ------------------------------------------------------

    st.write("")
    st.markdown("### Hiring Recommendation")

    if recommendation == "Proceed to Next Round":
        st.success(recommendation)
    elif recommendation == "Reject":
        st.error(recommendation)
    else:
        st.warning(recommendation)

    # ------------------------------------------------------
    # New Interview
    # ------------------------------------------------------

    st.write("")

    if st.button(
        "Start New Interview",
        type="primary",
        use_container_width=True,
    ):
        try:
            requests.delete(
                f"{API_URL}/session/{st.session_state.session_id}",
                timeout=10,
            )
        except Exception:
            pass

        reset_interview()
        st.rerun()