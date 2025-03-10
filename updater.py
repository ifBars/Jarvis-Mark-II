import os
import sys
import subprocess
import requests
import configparser

def get_remote_commit():
    """
    Contact the GitHub API to get the latest commit SHA on the 'main' branch.
    """
    url = "https://api.github.com/repos/ifBars/Jarvis-Mark-II/commits/main"
    response = requests.get(url)
    if response.status_code != 200:
        print(_("Error: Received status code {0} from {1}").format(response.status_code, url))
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
        print(_("Failed to get local commit: {0}").format(e))
        return None

def prompt_user(prompt):
    """Prompt user and return True if user agrees."""
    while True:
        choice = input("{0} [y/n]: ".format(prompt)).lower().strip()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            print(_("Please respond with 'y' or 'n'."))

def perform_update():
    """
    Perform a git pull to update the repository.
    Assumes this script is executed in the repository's root directory.
    """
    branch = "main"
    pull_cmd = ["git", "pull", "origin", branch]
    print(_("Updating Jarvis with command:"))
    print(" ".join(pull_cmd))
    try:
        subprocess.check_call(pull_cmd)
    except subprocess.CalledProcessError as e:
        print(_("Update failed: {0}").format(e))
        return False
    return True

def check_for_update():
    """
    Check if the remote commit differs from the local commit.
    If yes, prompt the user and perform a git pull update if confirmed,
    then restart the application.
    """
    local_commit = get_local_commit()
    remote_commit = get_remote_commit()
    if local_commit is None or remote_commit is None:
        print(_("Could not determine commit information; skipping update check."))
        return False

    print(_("Local commit: {0}").format(local_commit))
    print(_("Remote commit: {0}").format(remote_commit))
    
    if local_commit == remote_commit:
        print(_("Your Jarvis is up-to-date."))
        return False
    else:
        print(_("A new commit is available."))
        if prompt_user(_("Would you like to update?")):
            if perform_update():
                print(_("Update successful. Restarting..."))
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print(_("Update failed."))
        else:
            print(_("Update canceled by user."))
    return True