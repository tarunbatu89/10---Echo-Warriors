from jira import JIRA
import os
from dotenv import load_dotenv

load_dotenv()
ASSIGNEE_EMAIL = "Naman Mehra"

def get_jira_client():
    return JIRA(
        server=os.getenv("JIRA_URL"),
        basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    )

def get_account_id(jira, email):
    users = jira.search_users(query=email)
    for user in users:
        # Some Jira workspaces hide email in API, this may fail
        if hasattr(user, "emailAddress") and user.emailAddress == email:
            return user.accountId

    # Optional: fallback by name
    for user in users:
        if user.displayName.lower() in email.lower():
            return user.accountId

    raise ValueError(f"No Jira user found with email: {email}")

def create_jira_task(jira, summary, description, issue_type="Task", parent=None, epic_link=None):
    issue_dict = {
        'project': {'key': os.getenv("JIRA_PROJECT_KEY")},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issue_type},
    }

    # If it's a subtask, set the parent
    if issue_type == "Sub-task" and parent:
        issue_dict['parent'] = {'key': parent}

    # If it's a story and needs to be linked to an Epic
    if issue_type == "Story" and epic_link:
        issue_dict['customfield_10008'] = epic_link  # This is commonly the "Epic Link" field
        # You may need to confirm your Jira's Epic Link field ID
    try:
        account_id = get_account_id(jira, ASSIGNEE_EMAIL)
        issue_dict['assignee'] = {'accountId': account_id}
        print(f" Assigned to: {ASSIGNEE_EMAIL}")
    except Exception as e:
        print(f"Warning: Could not assign to {ASSIGNEE_EMAIL}: {e}")

    return jira.create_issue(fields=issue_dict)