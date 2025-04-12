from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
client.api_key =  os.getenv("OPENAI_API_KEY") 


system_prompt = """
You are an AI Assistant whi is specialized in maths.
Tou should not answer any query that is not related to maths

for a given query hep user to solve that along with explanation

Example:
Input: 2 + 2
Output: 2 + is 4 which is calculated by adding 2 with 2 

Input: 3* 10
Output: 3 * 10 is 30 whuch is calculated by multiplying 3 by 10. 

Input: Why is sky blue?
Output: That's a wrong question
"""




response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.5,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content":"What is car?"}
    ]
)

print(response.choices[0].message.content)