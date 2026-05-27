import json
import os

from groq import Groq
from dotenv import load_dotenv

from utils.schemas import IntentSchema

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are a research intent extraction system.

Return ONLY valid JSON.

Schema:

{
  "core_problem": "",
  "methodology_needed": [],
  "domain": "",
  "temporal_preference": "",
  "expanded_queries": []
}
"""

def extract_intent(query: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0.1,
        max_tokens=300
    )

    content = (
        response
        .choices[0]
        .message
        .content
    )

    parsed = json.loads(content)

    validated = IntentSchema(**parsed)

    return validated.dict()