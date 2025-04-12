import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
client.api_key =  os.getenv("OPENAI_API_KEY") 

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and the resove it

For a given user input, analyse the input and break down the problem step by step.

Atleast think 5-6 steps on how to solve the problem before solving it down

teh steps are you get a user input, you analyse, you think, you agaon think for several time ans then return the out output with explanation and then finally you validate the output as well before giving the final result

follow the steps in sequence that is "analyse", "think, "output", validate and finally "result"

Rules:
1. follow thw strict JSON output as per output schema
2. always performa one step at a timer and wait for nect input
3. Carefully analyse the user query

Output Format:
{{step: 'string', content: "string"}}

example:
Input: what is 2+2
Output: {{output:"Alright, The user is interested in maths query and he is asking a basic aritghmatic operation"}}
Output:{{step: "think", content: 'To perform the addition i must go from left to right and add all the operands'}}
Output:{{step: "output", content: '4'}}
Output:{{step: "validate", content: 'seems like 4 is corrent answer for 2 + 2'}}
Output:{{step: "result", content: '2 + 2 is and thet is calculated by adding all numbers'}}


"""


messages = [
    {"role": "system", "content": system_prompt},
]
user_input = input(">")
messages.append( {"role": "user", "content": user_input})

while True:  
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": 'json_object'},
        messages = messages
    )

    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({"role": "assistant", "content":json.dumps(parsed_response)})
    if parsed_response.get('step') != 'result':
        print(parsed_response.get("content"))
        continue
   
    print(parsed_response.get("content"))
    break
        


    
