from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_tasks_from_prd(prd_text: str) -> list[str]:
    """
    Generates a list of Jira tasks from a PRD using GPT-4.

    Args:
        prd_text (str): The full PRD text.

    Returns:
        list[str]: A list of individual task descriptions.
    """
    prompt = f"""
You are a product analyst. Read the following PRD and generate a list of clear, concise Jira tasks:
---
{prd_text}
---
Only return the tasks, one per line, without numbering.
"""

    # Call OpenAI chat completion
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    # Extract response content
    content = response.choices[0].message.content.strip()

    # Parse and clean task list
    tasks = [task.strip("-•* ").strip() for task in content.split("\n") if task.strip()]
    return tasks
