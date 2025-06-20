from prd_reader import read_txt
from task_generator import generate_tasks_from_prd
from jira_client import get_jira_client, create_jira_task

def main():
    prd_content = read_txt("sample_prd.txt")
    structured_output = generate_tasks_from_prd(prd_content)

    jira = get_jira_client()

    lines = structured_output.split("\n")
    current_epic = None
    current_story = None
    current_description = []

    epic_key = None
    story_key = None

    for line in lines:
        stripped = line.strip()

        # New EPIC
        if stripped.startswith("EPIC:"):
            current_epic = stripped.replace("EPIC:", "").strip()
            epic_issue = create_jira_task(jira, current_epic, "Auto-generated Epic from PRD", issue_type="Epic")
            epic_key = epic_issue.key
            print(f"\n✅ Created Epic: {epic_key} - {current_epic}")

        # New STORY
        elif stripped.startswith("STORY:"):
            # Save previous story if it exists
            if current_story:
                description_text = "\n".join(current_description).strip()
                story_issue = create_jira_task(
                    jira,
                    current_story,
                    description_text,
                    issue_type="Story",
                    epic_link=epic_key
                )
                story_key = story_issue.key
                print(f"  🟩 Created Story: {story_key} under Epic {epic_key}")
                
                # Create subtasks
                for sub in current_description:
                    subtask_summary = sub.lstrip("-– ").strip()
                    if subtask_summary:
                        subtask = create_jira_task(
                            jira,
                            subtask_summary,
                            f"Auto-created subtask for story: {current_story}",
                            issue_type="Sub-task",
                            parent=story_key
                        )
                        print(f"    🔹 Subtask: {subtask.key} - {subtask_summary}")

                # Reset for next story
                current_description = []

            # Start new story
            current_story = stripped.replace("STORY:", "").split("[")[0].strip()
            current_description = []

        # Subtasks
        elif current_story and (stripped.startswith("-") or stripped.startswith("–")):
            current_description.append(stripped)

    # Handle last story after loop
    if current_story:
        description_text = "\n".join(current_description).strip()
        story_issue = create_jira_task(
            jira,
            current_story,
            description_text,
            issue_type="Story",
            epic_link=epic_key
        )
        story_key = story_issue.key
        print(f"  🟩 Created Story: {story_key} under Epic {epic_key}")
        
        for sub in current_description:
            subtask_summary = sub.lstrip("-– ").strip()
            if subtask_summary:
                subtask = create_jira_task(
                    jira,
                    subtask_summary,
                    f"Auto-created subtask for story: {current_story}",
                    issue_type="Sub-task",
                    parent=story_key
                )
                print(f"    🔹 Subtask: {subtask.key} - {subtask_summary}")

if __name__ == "__main__":
    main()
