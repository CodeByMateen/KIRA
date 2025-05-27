from fastapi import FastAPI
from pydantic import BaseModel
from src.kira import ask_from_kira

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/ask-kira", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    user_question = request.question
    answer = ask_from_kira(user_question)
    return {"answer": answer}
