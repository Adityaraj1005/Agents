from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import os
import json

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "Always respond under 20 words."
    }
]

while True:
    user_input = input("\nADI: ")
    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        break

    messages.append({"role": "user", "content": user_input})

    
    #chained tool Calling
    while True:
        response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages,
                tools=TOOLS,
            )
        
        msg = response.choices[0].message
        if not msg.tool_calls:
            break

        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments or "{}")
            result = FUNCTION_NAME_TO_FUNCTION_MAP[func_name](**func_args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    
    
    messages.append({"role": "assistant", "content": msg.content})
    print("Assistant: " + msg.content)