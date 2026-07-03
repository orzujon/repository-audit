def get_repositories():
    return [
        {"name": "good-service-1", "requires_review": True},
        {"name": "good-service-2", "requires_review": True},
        {"name": "bad-service-1", "requires_review": False},
        {"name": "config", "requires_review": False},
    ]