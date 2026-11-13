from fastapi import FastAPI
from pydantic import BaseModel
from ai import ask_ai
from db import find_answer, save_answer


app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/ask")
def ask(body: Question):
    saved = find_answer(body.question)
    if saved:
        return{"question": body.question, "answer": saved, "cached": True}
    answer = ask_ai(body.question)
    save_answer(body.question, answer)
    return {"question": body.question, "answer": answer, "cached": False}