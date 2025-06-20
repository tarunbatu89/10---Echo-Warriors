from prd_reader import read_txt
from task_generator import generate_tasks_from_prd
from jira_client import get_jira_client, create_jira_task

def main():
    prd_content = read_txt("sample_prd.txt")
    tasks = generate_tasks_from_prd(prd_content)

    jira = get_jira_client()
    for task in tasks:
        issue = create_jira_task(jira, task)
        print(f"Created issue: {issue.key} - {task}")

if __name__ == "__main__":
    main()
