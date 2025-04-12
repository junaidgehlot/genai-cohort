from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()
client = OpenAI()
client.api_key =  os.getenv("OPENAI_API_KEY") 

def get_weather(city: str):
        url = f"https://wttr.in/{city}?format=%C+%t"
        response = requests.get(url)
        if response.status_code == 200:
                return f"The weather in {city} is {response.text}."
        return "Something went wrong"

available_tools={
    "get_weather": {
        "fn": get_weather,
        "descrition": "takes a city name and returns the current weather of the city"
    }
}

system_prompt = """
    You an helpful ai assistant who is specialized in resolving user query
    You work on start, plan, action ,observe mode.
    For the giver user query and available tools analyze, plan the step by step execution, based in the planning 
    select the relevant tool from the available tool. and based in the tool selection you perform an action to call the tool.
    wait for the observation and based in the observation from the tool, call resove the user query.

    1. Follow the strict JSON output as per output schema
    2. Always performa one step at a timer and wait for nect input
    3. Carefully analyse the user query


    Output Format:
    {{step: 'string', content: "string", "function": "the name of function if the step is action", "input": "the input prameter for the function"}}

    Available Tools:
    {{tool for tool in }}

    Example:
    User Query: What is the weather of new your
    Output: {{"step": 'plan', 'content': "the user isi nterested the weather data of new york"}}
    Output: {{"step": 'plan', 'content': "From the available tool i should call get_weather"}}
    Output: {{"step": 'action', 'function': "get_weather", input: "new york"}}
    Output: {{"step": 'observe', 'output': "12 degree Cel"}}
    Output: {{"step": 'output', 'output': "The weather for new york seems to be 12 degrees",}}
    
"""


messages = [
    {"role": "system", "content": system_prompt}
]



while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": 'json_object'},
        messages=messages 
    )
    
    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role": 'assistant', "content": json.dumps(parsed_response)})

    if parsed_response.get('step') == 'plan':
        print(parsed_response.get('content'))
        continue

    if parsed_response.get('step') == 'action':
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get('input')

        if available_tools.get(tool_name, False) != False:
            output = available_tools[tool_name].get("fn")(tool_input)
            messages.append({'role': "assistant", "content": json.dumps({"step": "observe", "output": output})})
            continue

    if parsed_response.get('step') == 'output':
        print(parsed_response.get('output'))
        break


    

        

