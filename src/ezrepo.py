#!/usr/bin/env python3
import argparse
import os
import requests
import json
import sys
import subprocess
import getpass

# GitHub API URL
GITHUB_API_URL = "https://api.github.com/user/repos"

def get_github_token():
    """Get GitHub token from environment or prompt user"""
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("GitHub token not found in environment variables.")
        print("\nYou can generate a GitHub token by visiting: https://github.com/settings/tokens")
        print("The token needs 'repo' permissions to create repositories.\n")
        
        # Ask user if they want to set up the token now
        setup_now = input("Would you like to set up your GitHub token now? (y/n): ")
        
        if setup_now.lower() == 'y':
            github_token = getpass.getpass("Please paste your GitHub token: ")
            
            if not github_token:
                print("No token provided. Exiting.")
                sys.exit(1)
                
            # Determine which shell configuration file to use
            shell_config = None
            home = os.path.expanduser("~")
            
            if os.path.exists(f"{home}/.bashrc"):
                shell_config = f"{home}/.bashrc"
            elif os.path.exists(f"{home}/.zshrc"):
                shell_config = f"{home}/.zshrc"
                
            if shell_config:
                try:
                    # Check if token is already in the config
                    with open(shell_config, 'r') as f:
                        content = f.read()
                        
                    if "export GITHUB_TOKEN" in content:
                        # Update existing token
                        with open(shell_config, 'r') as f:
                            lines = f.readlines()
                            
                        with open(shell_config, 'w') as f:
                            for line in lines:
                                if "export GITHUB_TOKEN" in line:
                                    f.write(f"export GITHUB_TOKEN={github_token}\n")
                                else:
                                    f.write(line)
                        print(f"Updated existing GITHUB_TOKEN in {shell_config}")
                    else:
                        # Add new token
                        with open(shell_config, 'a') as f:
                            f.write("\n# GitHub token for ezrepo\n")
                            f.write(f"export GITHUB_TOKEN={github_token}\n")
                        print(f"Added GITHUB_TOKEN to {shell_config}")
                    
                    # Set the token for the current session
                    os.environ["GITHUB_TOKEN"] = github_token
                    print(f"\nToken has been added to {shell_config}")
                    print("For this session, the token has been set automatically.")
                    print("For future sessions, please run 'source ~/.bashrc' or restart your terminal.")
                    
                    return github_token
                except Exception as e:
                    print(f"Error writing to shell config: {e}")
                    print("Please set the token manually:")
                    print(f"export GITHUB_TOKEN={github_token}")
            else:
                print("Could not find shell configuration file (.bashrc or .zshrc).")
                print("Please manually add the following line to your shell configuration:")
                print(f"export GITHUB_TOKEN={github_token}")
                
            # Set for current session anyway
            os.environ["GITHUB_TOKEN"] = github_token
            return github_token
        else:
            print("Token setup skipped. Exiting.")
            sys.exit(1)
    
    return github_token

def create_repo(repo_name, init_readme, private, description=None):
    # Ensure GitHub token is set
    github_token = get_github_token()

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