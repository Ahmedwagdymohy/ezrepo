# ezrepo

A command-line tool for creating GitHub repositories.

## Usage 

ezrepo -n "REPO_NAME" [-p] [-r] -d "DESCRIPTION"

Options:
- `-n, --name`: Name of the repository to create (required)
- `-p, --private`: Create a private repository (default is public)
- `-r, --readme`: Initialize the repository with a README
- `-d, --description`: Add a description to the repository README



# Configuration

Before using ezrepo, set your GitHub token as an environment variable:

export GITHUB_TOKEN=your_github_token

> Note: You can generate a GitHub token by going to https://github.com/settings/tokens then copy it and export as above.

