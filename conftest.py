
# Configure tests so that they can be automatically submitted to the 
# LTI platform after execution.

import os
import json
import urllib.request
import pytest

def get_repo_description_and_url():
    """Fetches repository metadata using the automatic GITHUB_TOKEN inside Codespaces."""
    repo_slug = os.environ.get("GITHUB_REPOSITORY")  # e.g., 'username/repo-name'
    token = os.environ.get("GITHUB_TOKEN")

    # Disable if missing basic GitHub Codespaces environment variables
    if not repo_slug or not token:
        return None, None

    default_url = f"https://github.com/{repo_slug}"
    api_url = f"https://api.github.com/repos/{repo_slug}"
    
    req = urllib.request.Request(
        api_url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "pytest-lti-bridge"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode("utf-8"))
            context_code = data.get("description", "").strip()
            
            # Disable if description is completely empty
            if not context_code:
                return None, default_url
                
            html_url = data.get("html_url", default_url)
            return context_code, html_url
    except Exception:
        # Disable if the API fetch fails
        return None, default_url


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Fires automatically right after pytest completes execution."""
    
    # 1. Fetch contextCode and repo link
    context_code, repo_url = get_repo_description_and_url()

    # 2. Check if automated submission should be disabled
    if not context_code:
        terminalreporter.write_sep("=", "Automated submission disabled")
        return

    # 3. Calculate grade
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    errors = len(terminalreporter.stats.get("error", []))
    total = passed + failed + errors

    grade = (round((passed / total), 2) if total > 0 else 0.0) * 100

    # 4. Construct payload
    payload = {
        "contextCode": context_code,
        "grade": grade,
        "comment": f"Automated submission from <a target='_blank' href='{repo_url}'>{repo_url}</a> ({passed}/{total} tests passed)"
    }

    worker_url = "https://test.jmadar.workers.dev/update-grade"

    # --- Debug Output Header ---
    terminalreporter.write_sep("=", "LTI Telemetry Debug Info")
    terminalreporter.write_line(f"Target URL: {worker_url}")
    terminalreporter.write_line(f"Payload:    {json.dumps(payload)}")

    # 5. Send Request
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            worker_url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "pytest-lti-bridge"  # <-- Added User-Agent header
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            res_code = response.getcode()
            res_body = response.read().decode("utf-8")
            
            terminalreporter.write_line(f"Status:     {res_code} OK")
            terminalreporter.write_line(f"Response:   {res_body}")
            terminalreporter.write_sep("=", "Grade Submitted Successfully")

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        terminalreporter.write_line(f"Status:     HTTP Error {e.code} - {e.reason}")
        terminalreporter.write_line(f"Response:   {error_body}")  # <-- Fixed string interpolation
        terminalreporter.write_sep("=", "Grade Submission Failed", red=True)

    except Exception as e:
        terminalreporter.write_line(f"Status:     Network/Script Error ({e})")
        terminalreporter.write_sep("=", "Grade Submission Failed", red=True)

