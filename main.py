import json
import sys
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq()

MODEL_NAME = "openai/gpt-oss-120b"
TEMPERATURE = 0
MAX_RETRIES = 2
SYSTEM_PROMPT = """You are a strict validation engine.

Your role is to evaluate a user profile JSON object using widely accepted real-world standards.
All validation decisions must be grounded strictly in the provided input.

Rules of operation:
- Apply validation only to fields that are present in the input.
- Never infer, guess, autocomplete, or fabricate missing values.
- Do not invent new fields, constraints, or rules.
- If multiple issues apply, report all of them.
- Errors represent hard violations.
- Warnings represent soft concerns and should not invalidate the input.

Validation intent (high-level only):

Hard validation (errors):
- Name must be non-empty.
- Email must be standard internet email format.
- Age must be realistic positive human ages.
- Country must be internationally standardized ISO-2 country identifiers.
- Phone number must be globally recognized E.164 phone numbering standards.

Soft validation (warnings):
- Age that are unusually young should be flagged as warnings.
- Very short name should be flagged as warnings.
- Email that appear disposable or temporary should be flagged as warnings.
- Phone number whose country code does not align with the provided country should be flagged as warnings.

Output contract (non-negotiable):
- Return ONLY valid JSON.
- The output must match this schema exactly:

{
  "is_valid": boolean,
  "errors": string[],
  "warnings": string[]
}

Additional constraints:
- Do not include explanations, reasoning, markdown, comments, or extra text.
- Do not restate input values unless required for an error or warning.
- If no errors or warnings exist, return empty arrays.

""".strip()
def call_llm(raw_json: str) -> str:
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Validate the following user profile:\n<json>\n{raw_json}\n</json>"
            }
        ],
        temperature=TEMPERATURE,
        top_p=1,
        max_completion_tokens=1024,
        stream=False
    )

    return completion.choices[0].message.content.strip()

def is_valid_schema(obj) -> bool:
    if not isinstance(obj, dict):
        return False

    if set(obj.keys()) != {"is_valid", "errors", "warnings"}:
        return False

    if not isinstance(obj["is_valid"], bool):
        return False

    if not isinstance(obj["errors"], list) or not isinstance(obj["warnings"], list):
        return False

    if not all(isinstance(e, str) for e in obj["errors"]):
        return False

    if not all(isinstance(w, str) for w in obj["warnings"]):
        return False

    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_user.py <input.json>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_json = f.read()
    except Exception as e:
        print(f"Failed to read input file: {e}", file=sys.stderr)
        sys.exit(1)

    for attempt in range(MAX_RETRIES + 1):
        response = call_llm(raw_json)

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            if attempt == MAX_RETRIES:
                raise RuntimeError("LLM failed to return valid JSON")
            continue

        if is_valid_schema(parsed):
            print(json.dumps(parsed, indent=2))
            return

        if attempt == MAX_RETRIES:
            raise RuntimeError("LLM returned JSON but violated schema")

if __name__ == "__main__":
    main()