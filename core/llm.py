from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq()

import time
import groq

def call_llm(system_prompt: str, user_message: str) -> str:
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model= "openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=4096
            )
            return response.choices[0].message.content
        except groq.RateLimitError as e:
            print(f"Rate limit hit! Sleeping 10 seconds (attempt {attempt+1}/5)...\nError: {e}")
            last_err = e
            time.sleep(10)
    raise last_err