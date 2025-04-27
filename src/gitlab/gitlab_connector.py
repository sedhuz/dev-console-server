import requests
from datetime import datetime
import src.config.config_handler as GitlabConfig
import src.gitlab.mr_custom_fields_handler as MrCustomFieldsHandler

# —— Constants ——————————————————————————————————————————————————————————————
ZBGIT_PROJECTS = ["zohobooks_server"]  # List of projects that use zbgit domain


def get_gitlab_connector(base_url=None, token=None, project_id=None):
    if base_url is None:
        base_url = GitlabConfig.get_gitlab_url()
    if token is None:
        token = GitlabConfig.get_gitlab_access_token()
    if project_id is None:
        project_id = GitlabConfig.get_gitlab_project_id()

    return GitlabConnector(base_url, token, project_id)


class GitlabConnector:
    def __init__(self, base_url, token, project_id):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.project_id = project_id
        self.headers = {"PRIVATE-TOKEN": token}

    def test_connection(self):
        url = f"{self.base_url}/api/v4/user"
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            return False

    def get_merge_requests(self):
        url = f"{self.base_url}/api/v4/merge_requests"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            return None

        merge_requests = response.json()
        # return merge_requests
        return _format_merge_requests(merge_requests)


# —— Helpers ——————————————————————————————————————————————————————————————————


def _format_merge_requests(merge_requests):
    formatted_merge_requests = []
    for merge_request in merge_requests:
        # —— Uppercase labels —————————————————————————————————
        labels = [label.upper() for label in merge_request.get("labels", [])]

        # —— Switch web_url for books —————————————————————————
        if merge_request and "web_url" in merge_request:
            for project in ZBGIT_PROJECTS:
                if project in merge_request["web_url"]:
                    merge_request["web_url"] = merge_request["web_url"].replace(
                        "https://git", "https://zbgit"
                    )
                    break

        # —— Format time ——————————————————————————————————————
        created_at = merge_request.get("created_at")
        updated_at = merge_request.get("updated_at")
        created_at_formatted = format_time_ago(created_at)
        updated_at_formatted = format_time_ago(updated_at)
        # —— Format merge request —————————————————————————————
        title = merge_request.get("title")
        title_formatted = (
            title.replace("[BUGFIX]", "").replace("[HOTFIX]", "").replace("[PATCH]", "")
        )
        title_formatted = title_formatted.strip()
        formatted_merge_requests.append(
            {
                # —— Main data ————————————————————————————————————
                "id": merge_request.get("id"),
                "iid": merge_request.get("iid"),
                "title": title,
                "title_formatted": title_formatted,
                "state": merge_request.get("state"),
                "branch": merge_request.get("source_branch"),
                "web_url": merge_request.get("web_url"),
                # —— Additional data ——————————————————————————————
                "labels": labels,
                "upvotes": merge_request.get("upvotes"),
                "is_draft": merge_request.get("draft"),
                "is_bugfix": "[BUGFIX]" in title and not merge_request.get("draft"),
                "is_hotfix": "[HOTFIX]" in title and not merge_request.get("draft"),
                "is_patch": "[PATCH]" in title and not merge_request.get("draft"),
                "is_open": merge_request.get("state") == "opened",
                "is_closed": merge_request.get("state") == "closed",
                "is_merged": merge_request.get("state") == "merged",
                "has_conflicts": merge_request.get("has_conflicts"),
                # —— Custom fields ————————————————————————————————
                "custom_fields": MrCustomFieldsHandler.get_mr_custom_fields(
                    merge_request.get("iid")
                ),
                # —— Time —————————————————————————————————————————
                "created_at": merge_request.get("created_at"),
                "created_at_formatted": created_at_formatted,
                "updated_at": merge_request.get("updated_at"),
                "updated_at_formatted": updated_at_formatted,
            }
        )
    return formatted_merge_requests


def format_time_ago(time_str):
    if not time_str:
        return "Unknown time"

    try:
        time = datetime.fromisoformat(time_str)
    except ValueError:
        return "Invalid time format"

    now = datetime.now(time.tzinfo)  # Match timezone
    time_diff = now - time

    seconds = time_diff.total_seconds()

    if seconds < 60:
        return f"{int(seconds)} sec{'s' if seconds != 1 else ''} ago"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{int(minutes)} min{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{int(hours)} hr{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = seconds // 86400
        return f"{int(days)} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:  # 30 days approx
        weeks = seconds // 604800
        return f"{int(weeks)} week{'s' if weeks != 1 else ''} ago"
    elif seconds < 31536000:  # 365 days approx
        months = seconds // 2592000
        return f"{int(months)} month{'s' if months != 1 else ''} ago"
    else:
        years = seconds // 31536000
        return f"{int(years)} year{'s' if years != 1 else ''} ago"
