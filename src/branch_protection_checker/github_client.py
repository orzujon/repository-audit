import os
import requests

from dotenv import load_dotenv

load_dotenv()


class GitHubClient:

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.org = os.getenv("GITHUB_ORG")
        self.api_url = os.getenv("GITHUB_API_URL")
    
    def get_repositories(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            }

        url = f"{self.api_url}/orgs/{self.org}/repos"

        response = requests.get(url, headers=headers)

        response.raise_for_status()

        return response.json()

    def get_branch_protection(self, repository_name, branch_name):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

        url = (
            f"{self.api_url}/repos/"
            f"{self.org}/{repository_name}/branches/{branch_name}/protection"
        )

        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            return None

        response.raise_for_status()

        return response.json()

    def requires_approved_review(self, repository_name, branch_name):
        protection = self.get_branch_protection(repository_name, branch_name)

        if protection is None:
            return False

        review_settings = protection.get("required_pull_request_reviews")

        if review_settings is None:
            return False

        required_count = review_settings.get("required_approving_review_count", 0)

        return required_count >= 1

    def enable_branch_protection(self, repository_name, branch_name):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

        url = (
            f"{self.api_url}/repos/"
            f"{self.org}/{repository_name}/branches/{branch_name}/protection"
        )

        payload = {
            "required_status_checks": None,
            "enforce_admins": False,
            "required_pull_request_reviews": {
                "required_approving_review_count": 1
            },
            "restrictions": None
        }

        response = requests.put(url, headers=headers, json=payload)

        response.raise_for_status()

        print(f"{'FIXED':<8} {repository_name:<25} branch protection enabled")

    def disable_branch_protection(self, repository_name, branch_name):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
        }

        url = (
            f"{self.api_url}/repos/"
            f"{self.org}/{repository_name}/branches/{branch_name}/protection"
        )

        response = requests.delete(url, headers=headers)

        response.raise_for_status()

        print(f"RESET     {repository_name}")

    def safe_requires_approved_review(self, repository_name, branch_name):
        try:
            requires_review = self.requires_approved_review(
                repository_name=repository_name,
                branch_name=branch_name,
            )

            return {
                "success": True,
                "requires_review": requires_review,
                "error": None,
            }

        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code

            return {
                "success": False,
                "requires_review": False,
                "error": f"HTTP {status_code}: {error.response.reason}",
            }

        except Exception as error:
            return {
                "success": False,
                "requires_review": False,
                "error": str(error),
            }