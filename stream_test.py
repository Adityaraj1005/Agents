import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

stream=client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[{"role":"user","content":"Explain what is an API is in 100 words.No need to mention number of words."}],
    stream=True,
)

full_response=""

for chunk in stream:
    piece=chunk.choices[0].delta.content
    if piece:
        print(piece,end="",flush=True)
        full_response+=piece

print("\Full response:")
print(full_response)