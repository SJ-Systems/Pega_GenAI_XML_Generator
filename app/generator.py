from openai import OpenAI

client = OpenAI()

def generate_xml(prompt, context):
    context_text = "\n\n".join(context)

    final_prompt = f"""
You are a Pega XML generator.

STRICT RULES:
- Output ONLY XML
- No explanation
- Ensure valid XML

REFERENCE XML:
{context_text}

USER REQUEST:
{prompt}

GENERATE XML:
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=final_prompt,
        temperature=0
    )

    return response.output[0].content[0].text.strip()
