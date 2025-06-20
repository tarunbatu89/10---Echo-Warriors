import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Initialize the OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tasks_from_prd(prd_text):
    prompt = f"""
You are a product analyst. Read the following PRD and generate a list of clear Jira tasks:
---
{prd_text}
---
Respond only with one task per line.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    # Extract and split the response into a list of tasks
    tasks = response.choices[0].message.content.strip().split("\n")
    return [task.strip("- ").strip() for task in tasks if task.strip()]
