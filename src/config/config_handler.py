import os
from dotenv import load_dotenv
import json

load_dotenv()

APP_PORT_KEY = "APP_PORT"
APP_HOST_KEY = "APP_HOST"
APP_CLIENT_URLS_KEY = "APP_CLIENT_URLS"
APP_DEBUG_KEY = "APP_DEBUG"
CONFIG_FILE_PATH = "gitlab_config.json"

GITLAB_URL_KEY = "url"
GITLAB_ACCESS_TOKEN_KEY = "token"
GITLAB_PROJECT_ID_KEY = "project_id"


def _get_gitlab_config():
    with open(CONFIG_FILE_PATH, "r") as file:
        return json.load(file)


def _set_gitlab_config(config):
    with open(CONFIG_FILE_PATH, "w") as file:
        json.dump(config, file, indent=4)


# —— Getters ——————————————————————————————————————————————————
# —— App configs ——————————————
def get_app_port():
    return os.getenv(APP_PORT_KEY)


def get_app_host():
    return os.getenv(APP_HOST_KEY)


def get_app_client_urls():
    client_urls = os.getenv(APP_CLIENT_URLS_KEY).split(",")
    return client_urls


def get_app_debug():
    return os.getenv(APP_DEBUG_KEY, "false").lower == "true"


# —— Gitlab configs ———————————
def get_gitlab_url():
    return _get_gitlab_config()[GITLAB_URL_KEY]


def get_gitlab_access_token():
    return _get_gitlab_config()[GITLAB_ACCESS_TOKEN_KEY]


def get_gitlab_project_id():
    return _get_gitlab_config()[GITLAB_PROJECT_ID_KEY]


def is_gitlab_configured():
    config = _get_gitlab_config()
    return all(
        [
            config[GITLAB_URL_KEY],
            config[GITLAB_ACCESS_TOKEN_KEY],
            config[GITLAB_PROJECT_ID_KEY],
        ]
    )


# —— Setters ——————————————————————————————————————————————————
# —— Gitlab configs ———————————
def set_gitlab_url(url):
    if not isinstance(url, str) or not url:
        raise ValueError("GITLAB_URL must be a non-empty string.")
    config = _get_gitlab_config()
    config[GITLAB_URL_KEY] = url
    _set_gitlab_config(config)


def set_gitlab_access_token(token):
    if not isinstance(token, str) or not token:
        raise ValueError("GITLAB_ACCESS_TOKEN must be a non-empty string.")
    config = _get_gitlab_config()
    config[GITLAB_ACCESS_TOKEN_KEY] = token
    _set_gitlab_config(config)


def set_gitlab_project_id(project_id):
    if not isinstance(project_id, str) or not project_id.isdigit():
        raise ValueError("GITLAB_PROJECT_ID must be a numeric string.")
    config = _get_gitlab_config()
    config[GITLAB_PROJECT_ID_KEY] = project_id
    _set_gitlab_config(config)
