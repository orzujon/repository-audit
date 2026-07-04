import argparse

from src.branch_protection_checker.checker import check_repository
from src.branch_protection_checker.github_client import GitHubClient
from src.branch_protection_checker.snapshot import load_snapshot, save_snapshot


EXCLUDED_REPOS = {"config", "config-test"}


def parse_args():
    parser = argparse.ArgumentParser(description="GitHub branch protection checker")

    parser.add_argument(
        "--mode",
        choices=["audit", "fix", "reset"],
        default="audit",
        help="Choose audit, fix, or reset mode",
    )

    return parser.parse_args()


def print_header(mode):
    print(f"Running in {mode.upper()} mode")
    print("-" * 60)


def run_reset(client):
    snapshot = load_snapshot()

    for repo_state in snapshot:
        repo_name = repo_state["name"]
        branch_name = repo_state["branch"]
        originally_required_review = repo_state["requires_review"]

        currently_requires_review = client.requires_approved_review(
            repository_name=repo_name,
            branch_name=branch_name,
        )

        if not originally_required_review and currently_requires_review:
            client.disable_branch_protection(repo_name, branch_name)


def run_audit(client, repos):
    for repo in repos:
        repo_name = repo["name"]
        branch_name = repo["default_branch"]

        if repo_name in EXCLUDED_REPOS:
            result = check_repository(repo_name, False, EXCLUDED_REPOS)
            print(f"{result.status:<8} {result.repo_name:<25} {result.reason}")
            continue

        review_check = client.safe_requires_approved_review(repo_name, branch_name)

        if not review_check["success"]:
            print(f"{'ERROR':<8} {repo_name:<25} {review_check['error']}")
            continue

        result = check_repository(
            repo_name=repo_name,
            requires_review=review_check["requires_review"],
            excluded_repos=EXCLUDED_REPOS,
        )

        print(f"{result.status:<8} {result.repo_name:<25} {result.reason}")


def run_fix(client, repos):
    snapshot_data = []

    for repo in repos:
        repo_name = repo["name"]
        branch_name = repo["default_branch"]

        if repo_name in EXCLUDED_REPOS:
            continue

        review_check = client.safe_requires_approved_review(repo_name, branch_name)

        if not review_check["success"]:
            print(f"{'ERROR':<8} {repo_name:<25} {review_check['error']}")
            continue

        requires_review = review_check["requires_review"]

        snapshot_data.append(
            {
                "name": repo_name,
                "branch": branch_name,
                "requires_review": requires_review,
            }
        )

        if not requires_review:
            client.enable_branch_protection(repo_name, branch_name)

    save_snapshot(snapshot_data)


def main():
    args = parse_args()
    print_header(args.mode)

    client = GitHubClient()

    if args.mode == "reset":
        run_reset(client)
        return

    repos = client.get_repositories()

    if args.mode == "audit":
        run_audit(client, repos)

    if args.mode == "fix":
        run_fix(client, repos)


if __name__ == "__main__":
    main()