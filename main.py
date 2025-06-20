from prd_reader import read_txt
from task_generator import generate_tasks_from_prd
from jira_client import get_jira_client, create_jira_task

def main():
    prd_content = read_txt("sample_prd.txt")
    structured_output = generate_tasks_from_prd(prd_content)

    jira = get_jira_client()

    lines = structured_output.split("\n")
    current_story = None
    current_description = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("STORY:"):
            # Save previous story if exists
            if current_story:
                description_text = "\n".join(current_description).strip()
                issue = create_jira_task(jira, current_story, description_text)
                print(f"Created issue: {issue.key} - {current_story}")

            # Start new story
            current_story = stripped.replace("STORY:", "").split("[")[0].strip()
            current_description = []  # reset
        elif current_story and (stripped.startswith("-") or stripped.startswith("–")):
            current_description.append(stripped)

    # Handle last story
    if current_story:
        description_text = "\n".join(current_description).strip()
        issue = create_jira_task(jira, current_story, description_text)
        print(f"Created issue: {issue.key} - {current_story}")

if __name__ == "__main__":
    main()
