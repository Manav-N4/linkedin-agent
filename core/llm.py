# pyrefly: ignore [missing-import]
import ollama

def call_llm(system_prompt: str, user_message: str) -> str:
    response = ollama.chat(
        model= "gemma2:2b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
    )
    return response["message"]["content"]

if __name__ == "__main__":
    try:
        print(call_llm("Answer using numbers only from 1-10", "Rate my outfit"))
    except ConnectionError as e:
        print("Ollama isn't running:", e)