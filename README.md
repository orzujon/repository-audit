# Branch Protection Checker

A Python tool to audit and optionally fix GitHub repository branch protection.

It checks whether each repository requires at least one approved pull request review before merging.

## What it does

* Lists repositories in a GitHub organisation.
* Checks branch protection on the default branch.
* Reports repositories as `PASS`, `FAIL`, `SKIPPED`, or `ERROR`.
* Can fix non-compliant repositories.
* Takes a snapshot before fixing.
* Can reset repositories back to their previous state using the snapshot.

## Modes

### Audit

Read-only check.

```bash
python -m src.branch_protection_checker.main --mode audit
```

Example:

```text
PASS     good-service-1            approved review is required
FAIL     bad-service-1             approved review is not required
SKIPPED  config                    repository is excluded
ERROR    private-repo              HTTP 403: Forbidden
```

### Fix

Fixes repositories that do not require approved reviews.

```bash
python -m src.branch_protection_checker.main --mode fix
```

This will:

* Check all repositories.
* Save current state to `branch_protection_snapshot.json`.
* Enable branch protection only where review approval is missing.
* Skip excluded repositories.

Example:

```text
FIXED    bad-service-1             branch protection enabled
FIXED    bad-service-2             branch protection enabled
ERROR    private-repo              HTTP 403: Forbidden
Snapshot saved to branch_protection_snapshot.json
```

### Reset

Restores repositories back to the state saved in the snapshot.

```bash
python -m src.branch_protection_checker.main --mode reset
```

This uses:

```text
branch_protection_snapshot.json
```

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file:

```env
GITHUB_TOKEN=your_github_token
GITHUB_ORG=your_github_org
GITHUB_API_URL=https://api.github.com
```

For GitHub Enterprise:

```env
GITHUB_API_URL=https://your-github-enterprise-url/api/v3
```

## Token permissions

For audit only:

```text
Administration: Read-only
Metadata: Read-only
Contents: Read-only
```

For fix/reset:

```text
Administration: Read and write
Metadata: Read-only
Contents: Read-only
```

## Exclusions

Update excluded repositories in `main.py`:

```python
EXCLUDED_REPOS = {"config", "config-test"}
```

Excluded repositories are never fixed.

## Run tests

```bash
pytest
```

## Notes

* This tool uses classic GitHub branch protection rules.
* It does not currently check GitHub Rulesets.
* `.env` should never be committed.
* `branch_protection_snapshot.json` is used for rollback after fix mode.



<img width="1536" height="1024" alt="Application Login with REST API" src="https://github.com/user-attachments/assets/62fc9e88-7cad-4c09-80b2-fb8f32ac6fcc" />
<img width="1536" height="1024" alt="f683fbaa-a3e0-41f7-9141-650ac4fefe36" src="https://github.com/user-attachments/assets/a4733276-3e1d-47a5-9ee8-a54cacf80401" />
