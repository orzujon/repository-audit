# Branch Protection Checker

A small Python audit tool that checks whether repositories in a GitHub organisation require an approved pull request review before merging.

The script reports each repository as:

```text
PASS     Approved review is required
FAIL     Approved review is not required
SKIPPED  Repository is excluded
```

## What it checks

For every repository in the configured GitHub organisation, the tool:

* Lists all repositories in the organisation
* Checks the default branch for branch protection
* Verifies whether at least one approved review is required before merging
* Skips repositories in the exclusion list
* Prints a clear audit result to the console

This tool is read-only. It does not change repository settings.

## Project structure

```text
branch-protection-checker/
├── src/
│   └── branch_protection_checker/
│       ├── checker.py
│       ├── github_client.py
│       └── main.py
├── tests/
│   ├── test_checker.py
│   └── test_github_client.py
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Setup

Clone the repository:

```bash
git clone <your-repo-url>
cd branch-protection-checker
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
copy .env.example .env
```

Update `.env`:

```env
GITHUB_TOKEN=your_github_token_here
GITHUB_ORG=your_github_org_here
GITHUB_API_URL=https://api.github.com
```

For GitHub Enterprise, update the API URL, for example:

```env
GITHUB_API_URL=https://your-github-enterprise-url/api/v3
```

## Exclusions

Repositories can be excluded from the audit.

Example:

```python
EXCLUDED_REPOS = {
    "config",
    "config-test",
}
```

Excluded repositories return:

```text
SKIPPED
```

## Run the audit

```bash
python -m src.branch_protection_checker.main
```

Example output:

```text
PASS     good-service-1       approved review is required
PASS     good-service-2       approved review is required
FAIL     bad-service-1        approved review is not required
SKIPPED  config               repository is excluded
```

## Run tests

```bash
pytest
```

Expected result:

```text
5 passed
```

## How it works

```text
main.py
  ↓
GitHubClient
  ↓
GitHub REST API
  ↓
requires_approved_review()
  ↓
checker.py
  ↓
PASS / FAIL / SKIPPED
  ↓
Console output
```

## Responsibilities

### `main.py`

Application entry point.

It connects everything together:

* Loads repositories
* Checks each repository
* Prints the result

### `github_client.py`

Handles GitHub communication.

It:

* Lists repositories in the organisation
* Reads branch protection settings
* Converts GitHub protection data into `True` or `False`

### `checker.py`

Contains the core business logic.

It decides whether a repository should be:

* `PASS`
* `FAIL`
* `SKIPPED`

### `tests/`

Contains unit tests for the checker and GitHub client logic.

The tests do not call the real GitHub API.

## GitHub token permissions

The token should have read-only access where possible.

Recommended fine-grained token permissions:

```text
Repository access: selected repositories
Administration: read-only
Contents: read-only
Metadata: read-only
```

Do not commit your `.env` file.

## Notes

This script checks classic branch protection rules using the GitHub REST API endpoint for branch protection.

It does not currently check GitHub Rulesets.

## Future improvements

Possible next steps:

* Add CSV or JSON report output
* Support GitHub Rulesets
* Add GitHub Actions workflow
* Move exclusions into `.env`
* Add better error handling and logging
* Add summary totals for PASS / FAIL / SKIPPED


<img width="1536" height="1024" alt="Application Login with REST API" src="https://github.com/user-attachments/assets/62fc9e88-7cad-4c09-80b2-fb8f32ac6fcc" />
<img width="1536" height="1024" alt="f683fbaa-a3e0-41f7-9141-650ac4fefe36" src="https://github.com/user-attachments/assets/a4733276-3e1d-47a5-9ee8-a54cacf80401" />
