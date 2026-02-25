from member2_ai.llm import generate_response
import json

def analyze_leave(leave_reason):

    prompt = f"""
    You are a college leave approval AI.

    Analyze the leave reason and respond ONLY in pure JSON.

    Return format:
    {{
      "reason_category": "Medical/Personal/Emergency/Other",
      "confidence": 0.0 to 1.0,
      "is_genuine": true/false
    }}

    Leave reason:
    "{leave_reason}"
    """

    response = generate_response(prompt)

    try:
        data = json.loads(response)
        return data
    except:
        return {
            "reason_category": "Other",
            "confidence": 0.0,
            "is_genuine": False
        }