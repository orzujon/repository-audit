# from src.branch_protection_checker.checker import check_repository
from src.branch_protection_checker.github_client import GitHubClient

# def test_good_repo_passes():
#     result = check_repository("good-service-1", True, {"config"})

#     assert result.status == "PASS"


# def test_bad_repo_fails():
#     result = check_repository("bad-service-1", False, {"config"})

#     assert result.status == "FAIL"


# def test_excluded_repo_is_skipped():
#     result = check_repository("config", False, {"config"})

#     assert result.status == "SKIPPED"

def test_requires_review_false_when_no_protection():
    client = GitHubClient()
    client.get_branch_protection = lambda repo, branch: None

    result = client.requires_approved_review("bad-service-1", "main")

    assert result is False


def test_requires_review_true_when_approval_count_is_one():
    client = GitHubClient()
    client.get_branch_protection = lambda repo, branch: {
        "required_pull_request_reviews": {
            "required_approving_review_count": 1
        }
    }

    result = client.requires_approved_review("good-service-1", "main")

    assert result is True