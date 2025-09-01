from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {
            "role": "user",
            "content": "In which year did OpenAI launch GPT-4?"
        }
    ]
)

print(response.choices[0].message.content.strip())