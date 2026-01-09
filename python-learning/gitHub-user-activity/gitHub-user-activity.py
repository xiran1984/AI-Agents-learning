import json
import requests
from datetime import datetime, timedelta

def fetch_github_user_activity(username, days=30):
    """Fetch GitHub user activity for the past specified number of days."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    events = []
    page = 1

    while True:
        url = f"https://api.github.com/users/{username}/events"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for event in data:
            event_date = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            if event_date < start_date:
                return events
            events.append(event)

        page += 1

    return events

def github_event_to_description(event_json):
    event = json.loads(event_json) if isinstance(event_json, str) else event_json
    repo = event["repo"]["name"]
    id = event["id"]

    if event["type"] == "PushEvent":
            return f"Pushed a commit to {repo}"
    if event["type"] == "IssuesEvent":
        return f"Opened a new issue in {repo}"
    if event["type"] == "PullRequestEvent":
        return f"Opened a new pull request in {repo}"
    if event["type"] == "WatchEvent":
        return f"Starred {repo}"
    if event["type"] == "PullRequestReviewEvent":
        return f'Reviewed a pull request in {repo}'
    if event["type"] == "IssuesEvent":
        action = event["payload"]["action"]
        return f"{action.capitalize()} an issue in {repo}"
    return f"Performed {event['type']} in {repo}"

if __name__ == "__main__":
    username = "kamranahmedse"
    activity = fetch_github_user_activity(username, days=30)
    for event in activity:
        description = github_event_to_description(event)
        print(description)
'''
- Pushed 3 commits to kamranahmedse/developer-roadmap
- Opened a new issue in kamranahmedse/developer-roadmap
- Starred kamranahmedse/developer-roadmap
'''
