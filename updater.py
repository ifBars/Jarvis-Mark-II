import os
import sys
import subprocess
import requests
import configparser

def load_current_version(version_ini_path="version.ini"):
    """
    Load the current version from a version.ini file.
    The file should have a [version] section with a key 'current'.
    """
    config = configparser.ConfigParser()
    config.read(version_ini_path)
    try:
        version = config["version"]["current"]
    except KeyError:
        raise RuntimeError("version.ini is missing the [version] section or 'current' key.")
    return version

CURRENT_VERSION = load_current_version()

def get_remote_commit():
    """
    Contact the GitHub API to get the latest commit SHA on the 'main' branch.
    """
    url = "https://api.github.com/repos/ifBars/Jarvis-Mark-II/commits/main"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from {url}")
        return None
    data = response.json()
    remote_sha = data.get("sha")
    return remote_sha

def get_local_commit():
    """
    Get the current commit SHA from the local repository using git rev-parse.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        local_sha = result.stdout.strip()
        return local_sha
    except subprocess.CalledProcessError as e:
        print("Failed to get local commit:", e)
        return None

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
    Perform a git pull to update the repository.
    Assumes this script is executed in the repository's root directory.
    """
    branch = "main"
    pull_cmd = ["git", "pull", "origin", branch]
    print("Updating repository with command:")
    print(" ".join(pull_cmd))
    try:
        subprocess.check_call(pull_cmd)
    except subprocess.CalledProcessError as e:
        print("Update failed:", e)
        return False
    return True

def check_for_update():
    """
    Check if the remote commit differs from the local commit.
    If yes, prompt the user and perform a git pull update if confirmed,
    then restart the application.
    """
    print(f"Current version (from version.ini): {CURRENT_VERSION}")
    local_commit = get_local_commit()
    remote_commit = get_remote_commit()
    if local_commit is None or remote_commit is None:
        print("Could not determine commit information; skipping update check.")
        return False

    print(f"Local commit: {local_commit}")
    print(f"Remote commit: {remote_commit}")
    
    if local_commit == remote_commit:
        print("Your repository is up-to-date.")
        return False
    else:
        print("A new commit is available.")
        if prompt_user("Would you like to update?"):
            if perform_update():
                print("Update successful. Restarting...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("Update failed.")
        else:
            print("Update canceled by user.")
    return True