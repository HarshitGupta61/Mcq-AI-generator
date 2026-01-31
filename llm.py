import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MAX_CHARS = 4000  # 🔥 Prevent token overflow

def generate_mcqs(text, total_questions, retries=2):
    text = text[:MAX_CHARS]

    prompt = f"""
Generate EXACTLY {total_questions} MCQs.

STRICT RULES:
- Return ONLY valid JSON
- No markdown
- No explanation
- No numbering text
- Must be an array
- Each item must contain:
  question, options(A,B,C,D), answer

FORMAT:
[
  {{
    "question": "Question?",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "answer": "A"
  }}
]

TEXT:
{text}
"""

    for _ in range(retries):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2500
        )

        raw = response.choices[0].message.content.strip()

        try:
            mcqs = json.loads(raw)
            if isinstance(mcqs, list) and len(mcqs) == total_questions:
                return mcqs
        except json.JSONDecodeError:
            continue

    return None 