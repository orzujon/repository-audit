from src.branch_protection_checker.checker import check_repository
from src.branch_protection_checker.fake_client import get_repositories


EXCLUDED_REPOS = {"config", "config-test"}


def main():
    repos = get_repositories()

    for repo in repos:
        result = check_repository(
            repo_name=repo["name"],
            requires_review=repo["requires_review"],
            excluded_repos=EXCLUDED_REPOS,
        )

        print(f"{result.status:<8} {result.repo_name:<20} {result.reason}")


if __name__ == "__main__":
    main()