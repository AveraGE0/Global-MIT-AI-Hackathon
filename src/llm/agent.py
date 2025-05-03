import requests
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", None)
AGENT_URL = os.getenv("AGENT_URL", None)
IAM_URL = os.getenv("IAM_URL",None)

'''
trend = "Italian Brainrot"
trend_search = f"What is {trend}"
payload_scoring = {"messages":[{"content":trend_search,"role":"user"}]}
'''

def agent_call(payload):
    token_response = requests.post(IAM_URL, data={"apikey":
     API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    response_scoring = requests.post(AGENT_URL, json=payload,
     headers={'Authorization': 'Bearer ' + mltoken})

    full_text = ""

    for line in response_scoring.iter_lines(decode_unicode=True):
        if line and line.startswith("data: "):
            try:
                json_data = json.loads(line[len("data: "):])
                delta = json_data["choices"][0].get("delta", {})
                content = delta.get("content", "")
                full_text += content
            except (json.JSONDecodeError, IndexError, KeyError):
                continue

    explanation = re.sub(r'(?s)^.*\]\s*', '', full_text)

    return explanation

response = agent_call(payload_scoring)
print(response)