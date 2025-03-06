#!/usr/bin/env python3
import argparse
import os
import requests
import json
import sys

# GitHub API URL
GITHUB_API_URL = "https://api.github.com/user/repos"

def create_repo(repo_name, init_readme, private, description=None):
    # Ensure GitHub token is set
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("Error: Please set your GITHUB_TOKEN environment variable.")
        sys.exit(1)

    # Define request payload
    payload = {
        "name": repo_name,
        "auto_init": init_readme,
        "private": private
    }
    
    # Add description to payload if provided
    if description:
        payload["description"] = description

    # Send request
    headers = {
        "Authorization": f"token {github_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(GITHUB_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        repo_data = response.json()
        clone_url = repo_data["clone_url"]
        print(f"Repository created successfully: {clone_url}")

        # Clone the repository
        os.system(f"git clone {clone_url}")
        print(f"Repository cloned successfully to {os.getcwd()}/{repo_name}")
        
        # If README was initialized and description was provided, update the README
        if init_readme and description:
            readme_path = f"{repo_name}/README.md"
            with open(readme_path, 'w') as f:
                f.write(f"# {repo_name}\n\n{description}")
            
            # Commit and push the updated README
            current_dir = os.getcwd()
            os.chdir(repo_name)
            os.system('git add README.md')
            os.system('git commit -m "Update README with description"')
            os.system('git push')
            os.chdir(current_dir)
            print("README updated with description")
    else:
        print("Error: Repository creation failed.")
        print(response.json())

# Argument parsing
def main():
    parser = argparse.ArgumentParser(description="Create a GitHub repository and clone it locally.")
    parser.add_argument("-n", "--name", required=True, help="Name of the repository to create")
    parser.add_argument("-r", "--readme", action="store_true", help="Initialize repository with a README")
    parser.add_argument("-p", "--private", action="store_true", help="Create the repository as private")
    parser.add_argument("-d", "--description", help="Description for the repository README")

    args = parser.parse_args()
    create_repo(args.name, args.readme, args.private, args.description)

if __name__ == "__main__":
    main()
