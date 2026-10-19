import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPEN_AI_API_KEY")

if not api_key:
    raise ValueError("OPEN_AI_API_KEY is not set in the environment variables.")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4",
    input="Hello, world!"
)

print(response.output_text)