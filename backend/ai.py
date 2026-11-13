import ollama

MODEL = "qwen2.5:3b"


def ask_ai(question: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Answer clearly in 2-4 sentences."},
            {"role": "user", "content": question},
        ],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    print(ask_ai("What is an API, in simple terms?"))
