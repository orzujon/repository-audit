from dataclasses import dataclass


@dataclass
class RepoCheckResult:
    repo_name: str
    status: str
    reason: str


def check_repository(repo_name: str, requires_review: bool, excluded_repos: set[str]) -> RepoCheckResult:
    if repo_name in excluded_repos:
        return RepoCheckResult(repo_name, "SKIPPED", "repository is excluded")

    if requires_review:
        return RepoCheckResult(repo_name, "PASS", "approved review is required")

    return RepoCheckResult(repo_name, "FAIL", "approved review is not required")