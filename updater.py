import os
import sys
import subprocess
import requests

try:
    # Use built-in tomllib if available (Python 3.11+)
    import tomllib
except ImportError:
    # Otherwise, fall back to the third-party 'toml' package
    import toml as tomllib

def load_current_version(pyproject_path="pyproject.toml"):
    """Load version from pyproject.toml from [project] (or [tool.poetry] as fallback)."""
    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)
    version = data.get("project", {}).get("version")
    if version is None:
        version = data.get("tool", {}).get("poetry", {}).get("version")
    return version

CURRENT_VERSION = load_current_version()

def get_latest_version():
    """
    Contact your update server (e.g. GitHub API or a custom endpoint)
    and return the latest version string.
    For demonstration, this function returns a hardcoded version.
    """
    response = requests.get("https://api.github.com/repos/ifBars/Jarvis-Mark-II/releases/latest")
    latest = response.json()["tag_name"]
    return latest

def prompt_user(prompt):
    """Prompt user and return True if user agrees."""
    while True:
        choice = input(f"{prompt} [y/n]: ").lower().strip()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            print("Please respond with 'y' or 'n'.")

def perform_update():
    """
    Run pip install to upgrade the package.
    Assumes your package is hosted on GitHub.
    """
    package_name = "rivalsjarvis"
    repo_url = "https://github.com/ifBars/Jarvis-Mark-II.git"
    branch = "main"

    update_cmd = [
        sys.executable, "-m", "pip", "install", "-U",
        f"git+{repo_url}@{branch}#egg={package_name}"
    ]
    print("Updating package with command:")
    print(" ".join(update_cmd))
    try:
        subprocess.check_call(update_cmd)
    except subprocess.CalledProcessError as e:
        print("Update failed:", e)
        return False
    return True

def check_for_update():
    """
    Check if a new version is available.
    If yes, prompt the user, perform update if confirmed,
    and restart the application.
    """
    print(f"Current version: {CURRENT_VERSION}")
    latest_version = get_latest_version()
    print(f"Latest version from github: {latest_version}")
    if latest_version == CURRENT_VERSION:
        print("You are already running the latest version.")
        return False
    else:
        print(f"A new version is available: {latest_version} (current: {CURRENT_VERSION})")
        if prompt_user("Would you like to update?"):
            if perform_update():
                print("Update successful. Restarting...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("Update failed.")
        else:
            print("Update canceled by user.")
    return True
