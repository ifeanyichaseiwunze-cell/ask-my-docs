from fastapi import FastAPI
from pydantic import BaseModel
from ai import ask_ai

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/ask")
def ask(body: Question):
    answer = ask_ai(body.question)
    return {"question": body.question, "answer": answer}
