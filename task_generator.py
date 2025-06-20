import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tasks_from_prd(prd_text):
    prompt = f"""
You are a technical product analyst.

Your task is to read the following Product Requirements Document (PRD) and:
- Identify high-level Epics (1 per core feature).
- For each Epic, create 1–3 relevant user stories.
- For each story, break it down into 2–5 subtasks (backend, frontend, API, testing, etc.).
- Classify each story's estimated complexity as Low, Medium, or High.

Return the result in this structured format:

EPIC: <epic name>
    STORY: <story title> [Complexity: <Low|Medium|High>]
        - Subtask 1
        - Subtask 2
        ...

---

PRD:
{prd_text}
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    # The response text contains the structured Epics → Stories → Subtasks
    return response.choices[0].message.content.strip()
