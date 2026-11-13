import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv() 

client = MongoClient(os.environ["MONGODB_URI"])
db = client["ask_my_docs"]
questions = db["questions"]

def find_answer(question: str) -> str | None:
    doc = questions.find_one({"question": question})
    if doc:
        return doc["answer"]
    return None

def save_answer(question: str, answer: str) -> None:
    questions.insert_one({"question": question, "answer": answer})