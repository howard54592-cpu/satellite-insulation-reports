#!/usr/bin/env python3
"""
report-dispatcher 核心分发脚本
用法: python3 dispatch.py '<json_params>'
"""

import json
import os
import sys
import subprocess
import datetime

GITHUB_REPOS = {
    "daily": "howard54592-cpu/satellite-insulation-reports",
    "weekly": "howard54592-cpu/satellite-insulation-reports",
}
LOCAL_REPO_PATH = "/tmp/satellite-insulation-reports"
BRANCH = "main"


def gh_push_report(title: str, content: str, report_type: str, dry_run: bool = False) -> dict:
    """写入 GitHub 仓库"""
    now = datetime.datetime.now()
    
    if report_type == "daily":
        date_str = now.strftime("%Y-%m-%d")
        filename = f"{date_str}.md"
        remote_path = f"reports/daily/{filename}"
    elif report_type == "weekly":
        # ISO 周数
        week_str = now.strftime("%Y-W%W")
        filename = f"{week_str}-report.md"
        remote_path = f"reports/weekly/{filename}"
    else:
        date_str = now.strftime("%Y-%m-%d_%H%M")
        filename = f"{date_str}.md"
        remote_path = f"reports/misc/{filename}"

    full_content = f"# {title}\n\n{content}\n\n---\n*Generated: {now.isoformat()} by AeroFlux*"

    if dry_run:
        return {
            "status": "dry_run",
            "action": f"[DRY RUN] Would write {remote_path}",
            "content_preview": full_content[:200],
        }

    # 确保本地有仓库
    if not os.path.exists(LOCAL_REPO_PATH):
        subprocess.run(
            ["git", "clone", f"https://github.com/{GITHUB_REPOS[report_type]}.git", LOCAL_REPO_PATH],
            capture_output=True, text=True,
            env={**os.environ, "HTTP_PROXY": "http://127.0.0.1:8001", "HTTPS_PROXY": "http://127.0.0.1:8001"}
        )

    # 写入文件
    filepath = os.path.join(LOCAL_REPO_PATH, "reports", report_type if report_type != "misc" else "misc")
    os.makedirs(filepath, exist_ok=True)
    filepath = os.path.join(filepath, filename)
    
    with open(filepath, "w") as f:
        f.write(full_content)

    # Git add / commit / push
    env = {
        **os.environ,
        "HTTP_PROXY": "http://127.0.0.1:8001",
        "HTTPS_PROXY": "http://127.0.0.1:8001",
        "GITHUB_API_TOKEN": subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip(),
    }
    
    subprocess.run(["git", "config", "--global", "user.name", "AeroFlux Bot"], env=env)
    subprocess.run(["git", "config", "--global", "user.email", "aeroflux@openclaw.ai"], env=env)

    subprocess.run(["git", "-C", LOCAL_REPO_PATH, "add", filepath], env=env)
    
    commit_msg = f"Report: {title} [{report_type}] {now.strftime('%Y-%m-%d')}"
    result = subprocess.run(
        ["git", "-C", LOCAL_REPO_PATH, "commit", "-m", commit_msg],
        capture_output=True, text=True, env=env
    )
    
    push_result = subprocess.run(
        ["git", "-C", LOCAL_REPO_PATH, "push", "origin", BRANCH],
        capture_output=True, text=True, env=env
    )

    repo_url = f"https://github.com/{GITHUB_REPOS[report_type]}/blob/{BRANCH}/{remote_path}"

    return {
        "status": "ok" if push_result.returncode == 0 else "error",
        "commit_msg": commit_msg,
        "filename": filename,
        "remote_path": remote_path,
        "repo_url": repo_url,
        "push_stdout": push_result.stdout[-500:] if push_result.stdout else "",
        "push_stderr": push_result.stderr[-500:] if push_result.stderr else "",
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python3 dispatch.py '<json_params>'"}))
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"JSON parse error: {e}"}))
        sys.exit(1)

    title = params.get("title", "Untitled Report")
    content = params.get("content", "")
    report_type = params.get("report_type", "daily")
    sync_github = params.get("sync_github", False)
    dry_run = params.get("dry_run", False)

    results = []

    if sync_github:
        gh_result = gh_push_report(title, content, report_type, dry_run)
        results.append({"type": "github", **gh_result})

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
