import subprocess
from nano_tools.decorator import tool


def _git(args: list[str], cwd: str = ".") -> str:
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True, text=True, timeout=30, cwd=cwd
        )
        out = result.stdout.strip()
        err = result.stderr.strip()
        if result.returncode != 0 and err:
            return f"git error: {err}"
        return out or "(no output)"
    except FileNotFoundError:
        return "Error: git not installed or not in PATH"
    except Exception as e:
        return f"Error: {e}"


@tool
def git_status(repo_path: str) -> str:
    """Show working tree status of a git repository.
    repo_path: Path to the git repository
    """
    return _git(["status", "--short"], cwd=repo_path)


@tool
def git_diff(repo_path: str) -> str:
    """Show unstaged changes in a git repository.
    repo_path: Path to the git repository
    """
    diff = _git(["diff"], cwd=repo_path)
    if len(diff) > 8000:
        return diff[:8000] + "\n[truncated]"
    return diff


@tool
def git_log(repo_path: str) -> str:
    """Show recent commit history (last 10 commits).
    repo_path: Path to the git repository
    """
    return _git(["log", "--oneline", "-10"], cwd=repo_path)


@tool
def git_commit(repo_path: str, message: str) -> str:
    """Stage all changes and create a git commit.
    repo_path: Path to the git repository
    message: Commit message
    """
    add = _git(["add", "-A"], cwd=repo_path)
    commit = _git(["commit", "-m", message], cwd=repo_path)
    return f"{add}\n{commit}".strip()


@tool
def git_read_file(repo_path: str, file_path: str, ref: str) -> str:
    """Read a file at a specific git ref (branch, commit, tag).
    repo_path: Path to the git repository
    file_path: Relative path to the file within the repo
    ref: Git ref e.g. HEAD, main, abc1234
    """
    return _git(["show", f"{ref}:{file_path}"], cwd=repo_path)
