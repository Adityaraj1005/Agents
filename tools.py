from datetime import datetime
from Utilities.utilities import log
import requests
import json


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url=f"https://wttr.in/{city}?format=3"
    response=requests.get(url,timeout=10)
    response.raise_for_status()
    return response.text

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current date and time as a formatted string.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type" : "function",
        "function" : {
            "name" : "get_city_weather",
            "description" : "Returns the current weather for a given city.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "city" : {
                        "type" : "string",
                        "description" : "City to get the weather for.",
                    }
                },
                "required": ["city"],
            },
        }
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
}

def run_tool(tool_call):
      func_name = tool_call.function.name
      func_args={}
                
      try:
          func_args = json.loads(tool_call.function.arguments or "{}")
          log(f" {func_name}({func_args})")
          fn=FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
          result = fn(**func_args)
      except Exception as e:
          result=f"Error while running {func_name} : {e}"
    
      log(f" {result}")
      return str(result)