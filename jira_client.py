from jira import JIRA
import os
from dotenv import load_dotenv

load_dotenv()

def get_jira_client():
    return JIRA(
        server=os.getenv("JIRA_URL"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )

def create_jira_task(jira, summary):
    issue_dict = {
        'project': {'key': os.getenv("JIRA_PROJECT_KEY")},
        'summary': summary,
        'description': 'Auto-created from PRD',
        'issuetype': {'name': 'Task'}
    }
    return jira.create_issue(fields=issue_dict)
