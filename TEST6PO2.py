import os
import pytest
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
REPO_NAME = os.getenv("REPO_NAME")
BASE_URL = "https://api.github.com"

@pytest.fixture(scope="function")
def headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

def test_github_repo_operations(headers):
    # Создание репозитория
    create_url = f"{BASE_URL}/user/repos"
    payload = {
        "name": REPO_NAME,
        "description": "Test repository created via API",
        "private": False
    }
    response = requests.post(create_url, headers=headers, json=payload)
    assert response.status_code == 201, f"Failed to create repo: {response.text}"
    assert response.json()["name"] == REPO_NAME, "Repo name mismatch"

    # Проверка наличия репозитория
    repos_url = f"{BASE_URL}/users/{GITHUB_USER}/repos"
    response = requests.get(repos_url, headers=headers)
    assert response.status_code == 200, f"Failed to list repos: {response.text}"
    repo_names = [repo["name"] for repo in response.json()]
    assert REPO_NAME in repo_names, f"Repository {REPO_NAME} not found in user repos"

    # Удаление репозитория
    delete_url = f"{BASE_URL}/repos/{GITHUB_USER}/{REPO_NAME}"
    response = requests.delete(delete_url, headers=headers)
    assert response.status_code == 204, f"Failed to delete repo: {response.text}"