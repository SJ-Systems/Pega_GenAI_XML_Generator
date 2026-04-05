from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(user_prompt, context, rule_type):
    examples = "\n\n".join(context)

    return f"""
You are a Pega XML generator.

RULE TYPE: {rule_type}

STRICT RULES:
- Output ONLY XML
- No explanations
- Ensure valid XML

EXAMPLES:
{examples}

USER REQUEST:
{user_prompt}

GENERATE XML:
"""

def generate_xml(prompt, context, rule_type):
    final_prompt = build_prompt(prompt, context, rule_type)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=final_prompt,
        temperature=0
    )

    return response.output[0].content[0].text.strip()
