from pydantic import BaseModel


class StartInterviewRequest(BaseModel):
    session_id: str
    candidate_id: str


class SubmitAnswerRequest(BaseModel):
    session_id: str
    answer: str