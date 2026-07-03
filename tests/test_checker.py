from src.branch_protection_checker.checker import check_repository


def test_good_repo_passes():
    result = check_repository("good-service-1", True, {"config"})

    assert result.status == "PASS"


def test_bad_repo_fails():
    result = check_repository("bad-service-1", False, {"config"})

    assert result.status == "FAIL"


def test_excluded_repo_is_skipped():
    result = check_repository("config", False, {"config"})

    assert result.status == "SKIPPED"