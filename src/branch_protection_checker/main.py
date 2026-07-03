from src.branch_protection_checker.checker import check_repository
from src.branch_protection_checker.github_client import GitHubClient


EXCLUDED_REPOS = {"config", "config-test"}


def main():
    client = GitHubClient()
    repos = client.get_repositories()

    # for repo in repos:
        # print(repo["name"])

    for repo in repos:
        requires_review = client.requires_approved_review(
            repository_name=repo["name"],
            branch_name=repo["default_branch"],
        )

        result = check_repository(
            repo_name=repo["name"],
            requires_review=requires_review,
            excluded_repos=EXCLUDED_REPOS,
        )

        print(f"{result.status:<8} {result.repo_name:<20} {result.reason}")
    # for repo in repos:
    #     result = check_repository(
    #         repo_name=repo["name"],
    #         requires_review=repo["requires_review"],
    #         excluded_repos=EXCLUDED_REPOS,
    #     )

    #     print(f"{result.status:<8} {result.repo_name:<20} {result.reason}")


if __name__ == "__main__":
    main()