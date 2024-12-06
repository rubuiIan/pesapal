import os
import shutil
import hashlib
import time
import difflib

# --- Repository Initialization ---
def init_repository():
    if os.path.exists(".repo"):
        print("Repository already initialized!")
        return

    os.mkdir(".repo")
    os.mkdir(".repo/staging")
    os.mkdir(".repo/commits")
    os.mkdir(".repo/branches")

    with open(".repo/HEAD", "w") as head_file:
        head_file.write("refs/heads/main")
    
    print("Initialized empty repository in the current directory.")

# --- Staging and Commit ---
def add_to_staging(file_path):
    if not os.path.exists(".repo"):
        print("Error: Repository not initialized. Run 'init' first.")
        return
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return
    
    staging_path = os.path.join(".repo", "staging", os.path.basename(file_path))
    shutil.copy(file_path, staging_path)
    print(f"File '{file_path}' added to staging area.")

def commit_files(message):
    if not os.path.exists(".repo"):
        print("Error: Repository not initialized. Run 'init' first.")
        return

    # Get the current branch from the .repo/HEAD file
    with open(".repo/HEAD", "r") as head_file:
        current_branch = head_file.read().strip().split('/')[-1]

    staging_path = os.path.join(".repo", "staging")
    commits_path = os.path.join(".repo", "commits", current_branch)

    # Check if staging area is empty
    if not os.listdir(staging_path):
        print("Error: No files to commit.")
        return

    # Ensure the branch directory exists
    if not os.path.exists(commits_path):
        os.makedirs(commits_path)

    # Generates a unique commit ID
    commit_id = hashlib.sha1(str(time.time()).encode()).hexdigest()[:10]

    # Create a new commit folder within the branch folder
    commit_dir = os.path.join(commits_path, commit_id)
    os.mkdir(commit_dir)

    # Move files from staging to the commit folder
    for file_name in os.listdir(staging_path):
        src = os.path.join(staging_path, file_name)
        dest = os.path.join(commit_dir, file_name)
        shutil.move(src, dest)

    # Create a commit message file
    with open(os.path.join(commit_dir, "message.txt"), "w") as msg_file:
        msg_file.write(message)

    print(f"Committed files with ID: {commit_id} to branch '{current_branch}'")

def display_commit_log():
    if not os.path.exists(".repo"):
        print("Error: Repository not initialized. Run 'init' first.")
        return

    commits_path = os.path.join(".repo", "commits")

    # Check if there are any commits
    if not os.listdir(commits_path):
        print("No commits found.")
        return

    print("Commit History:\n")
    for commit_id in sorted(os.listdir(commits_path), reverse=True):
        commit_dir = os.path.join(commits_path, commit_id)
        message_file = os.path.join(commit_dir, "message.txt")

        # Read and display commit message
        with open(message_file, "r") as f:
            message = f.read().strip()

        print(f"Commit ID: {commit_id}")
        print(f"Message: {message}")
        print("-" * 40)

# --- Branching Functionality ---
def create_branch(branch_name):
    if not os.path.exists(".repo"):
        print("Error: Repository not initialized. Run 'init' first.")
        return
    
    branches_path = os.path.join(".repo", "branches")
    
    # Ensure the branches folder exists
    if not os.path.exists(branches_path):
        os.mkdir(branches_path)

    # Check if the branch already exists
    if os.path.exists(os.path.join(branches_path, branch_name)):
        print(f"Error: Branch '{branch_name}' already exists.")
        return
    
    # Create the new branch
    with open(os.path.join(branches_path, branch_name), "w") as branch_file:
        branch_file.write("refs/heads/main")
    print(f"Branch '{branch_name}' created.")

def list_branches():
    if not os.path.exists(".repo"):
        print("Error: Repository not initialized. Run 'init' first.")
        return
    
    branches_path = os.path.join(".repo", "branches")
    
    # Ensure the branches folder exists
    if not os.path.exists(branches_path):
        print("No branches found.")
        return
    
    branches = os.listdir(branches_path)
    if not branches:
        print("No branches found.")
    else:
        print("Branches:")
        for branch in branches:
            print(f"  {branch}")

def switch_branch(branch_name):
    if not os.path.exists(".repo"):
        print("Error: Repository not initialized. Run 'init' first.")
        return
    
    branches_path = os.path.join(".repo", "branches")
    current_branch_file = os.path.join(".repo", "HEAD")

    # Check if the branch exists
    if not os.path.exists(os.path.join(branches_path, branch_name)):
        print(f"Error: Branch '{branch_name}' does not exist.")
        return
    
    # Switch to the new branch by updating the HEAD
    with open(current_branch_file, "w") as head_file:
        head_file.write(f"refs/heads/{branch_name}")
    print(f"Switched to branch '{branch_name}'.")

def merge_branches(branch1, branch2):
    if not os.path.exists(".repo"):
        print("Error: Repository not initialized. Run 'init' first.")
        return

    branches_path = os.path.join(".repo", "branches")

    # Check if branches exist in .repo/branches
    if not os.path.exists(os.path.join(branches_path, branch1)):
        print(f"Error: Branch '{branch1}' does not exist.")
        return
    if not os.path.exists(os.path.join(branches_path, branch2)):
        print(f"Error: Branch '{branch2}' does not exist.")
        return

    print(f"Merging changes from '{branch1}' into '{branch2}'...")

    branch1_path = os.path.join(".repo", "commits", branch1)
    branch2_path = os.path.join(".repo", "commits", branch2)

    # Create branch directories if they do not exist
    if not os.path.exists(branch1_path):
        os.mkdir(branch1_path)
    if not os.path.exists(branch2_path):
        os.mkdir(branch2_path)

    branch1_commits = sorted(os.listdir(branch1_path), reverse=True)
    branch2_commits = sorted(os.listdir(branch2_path), reverse=True)

    conflict_files = []
    merged_commit_id = hashlib.sha1(str(time.time()).encode()).hexdigest()[:10]
    merged_commit_dir = os.path.join(branch2_path, merged_commit_id)
    os.mkdir(merged_commit_dir)

    for commit_id in branch1_commits:
        commit_dir = os.path.join(branch1_path, commit_id)
        if os.path.exists(commit_dir):
            for file_name in os.listdir(commit_dir):
                src = os.path.join(commit_dir, file_name)
                dest = os.path.join(branch2_path, merged_commit_id, file_name)

                if os.path.exists(dest):
                    with open(src, 'r') as file1, open(dest, 'r') as file2:
                        if file1.read() != file2.read():
                            print(f"Conflict detected in file: {file_name}")
                            conflict_files.append(file_name)
                            continue
                shutil.copy(src, dest)

    with open(os.path.join(merged_commit_dir, "message.txt"), "w") as msg_file:
        msg_file.write(f"Merged changes from '{branch1}' into '{branch2}'")

    if conflict_files:
        print("\nMerge completed with conflicts:")
        for conflict_file in conflict_files:
            print(f"  {conflict_file}")
    else:
        print("\nMerge completed successfully with no conflicts.")

    print(f"Merged commit created: {merged_commit_id}")

# --- Diff Functionality ---
def get_commit_files(branch, commit_id):
    commit_path = os.path.join(".repo", "commits", branch, commit_id)
    if not os.path.exists(commit_path):
        return []
    return os.listdir(commit_path)

def diff_commits(branch1, commit1, branch2, commit2):
    # Get files in both commits
    commit1_files = get_commit_files(branch1, commit1)
    commit2_files = get_commit_files(branch2, commit2)

    # Compare files that exist in both commits
    common_files = set(commit1_files).intersection(commit2_files)

    for file in common_files:
        file1_path = os.path.join(".repo", "commits", branch1, commit1, file)
        file2_path = os.path.join(".repo", "commits", branch2, commit2, file)

        with open(file1_path, "r") as f1, open(file2_path, "r") as f2:
            diff = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1_path, tofile=file2_path)
            for line in diff:
                print(line)

    print(f"Compared commits {commit1} (branch {branch1}) and {commit2} (branch {branch2})")

# --- Clone Repository ---
def clone_repository(remote_path):
    if not os.path.exists(remote_path):
        print(f"Error: Remote repository '{remote_path}' not found.")
        return

    repo_name = os.path.basename(remote_path)
    if os.path.exists(repo_name):
        print(f"Error: Local directory '{repo_name}' already exists.")
        return

    shutil.copytree(remote_path, repo_name)
    print(f"Cloned repository from '{remote_path}' to '{repo_name}'.")

# --- Main Command Handling ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [args]")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "init":
        init_repository()
    elif command == "add":
        if len(sys.argv) < 3:
            print("Error: No file specified to add.")
        else:
            add_to_staging(sys.argv[2])
    elif command == "commit":
        if len(sys.argv) < 3:
            print("Error: No commit message provided.")
        else:
            commit_files(" ".join(sys.argv[2:]))
    elif command == "log":
        display_commit_log()
    elif command == "branch":
        if len(sys.argv) < 3:
            print("Error: No branch name provided.")
        else:
            create_branch(sys.argv[2])
    elif command == "list-branches":
        list_branches()
    elif command == "switch":
        if len(sys.argv) < 3:
            print("Error: No branch name provided.")
        else:
            switch_branch(sys.argv[2])
    elif command == "merge":
        if len(sys.argv) < 4:
            print("Error: Provide two branches to merge.")
        else:
            merge_branches(sys.argv[2], sys.argv[3])
    elif command == "diff":
        if len(sys.argv) < 5:
            print("Error: Provide two commits to compare.")
        else:
            diff_commits(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif command == "clone":
        if len(sys.argv) < 3:
            print("Error: No remote repository path provided.")
        else:
            clone_repository(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
