from member2_ai.llm import generate_response
import json

prompt = """
You are a college leave approval AI.

Analyze the leave reason and respond ONLY in pure JSON.

Return format:
{
  "reason_category": "Medical/Personal/Emergency/Other",
  "confidence": 0.0 to 1.0,
  "is_genuine": true/false
}

Leave reason:
"I am suffering from high fever and doctor advised 3 days rest."
"""

response = generate_response(prompt)

print("RAW OUTPUT:\n", response)

try:
    data = json.loads(response)
    print("\nPARSED JSON:\n", data)
    print("TYPE:", type(data))
except:
    print("⚠ JSON Parsing Failed")