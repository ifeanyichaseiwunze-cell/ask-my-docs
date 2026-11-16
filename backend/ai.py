import ollama

MODEL = "qwen2.5:3b"


def ask_ai(question: str, context: str = "") -> str:
    system_prompt = (
        "Your are a helpful assistant. Answer using ONLY the contect below. "
        "If the answer is not in the contect, say: I dont know based on the information ive been provided. "
        "Answer in 2-4 sentences. \n\n"
        "Contect:\n" + context
    )
    response = ollama.chat(
        model = MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content":question},
        ],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    print(ask_ai("What is an API, in simple terms?"))
