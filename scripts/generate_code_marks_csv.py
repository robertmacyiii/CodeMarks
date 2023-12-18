import argparse
import datetime
import os
import subprocess
import csv

def list_files_in_git_repo(repo_path, subdirectory):
    """
    List all files in a git repository under a specified subdirectory.

    Args:
    repo_path (str): Path to the local git repository.
    subdirectory (str): Subdirectory in the git repository to list files from.

    Returns:
    list: List of file paths under the specified subdirectory.
    """
    files_list = []
    for root, dirs, files in os.walk(os.path.join(repo_path, subdirectory)):
        for file in files:
            files_list.append(os.path.relpath(os.path.join(root, file), repo_path))

    return files_list

def get_current_commit_sha(repo_path):
    """
    Get the current git commit SHA of the repository.

    Args:
    repo_path (str): Path to the local git repository.

    Returns:
    str: Current git commit SHA.
    """
    try:
        commit_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo_path).decode('utf-8').strip()
        return commit_sha
    except subprocess.CalledProcessError:
        return None

def write_csv_file(repo_url_stem, repo_path, file_paths, commit_sha, output_file):
    """
    Write a CSV file containing information about the files in the git repository.

    Args:
    repo_url_stem (str): The stem of the github URL for this repository file.
    repo_path (str): Path to the local git repository.
    file_paths (list): List of file paths in the git repository.
    commit_sha (str): Current git commit SHA.
    output_file (str): Path to the CSV file to be written.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File Name', 'File Path', 'Commit SHA', 'File Size (Bytes)', 'Github Link', 'Status Last Updated', 'Read Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for file_path in file_paths:
            file_size = os.path.getsize(os.path.join(repo_path, file_path))
            file_url = f"{repo_url_stem}/{file_path}"
            writer.writerow({
                'File Name': os.path.basename(file_path),
                'File Path': file_path,
                'Commit SHA': commit_sha,
                'File Size (Bytes)': file_size,
                'Github Link': file_url,
                'Status Last Updated': str(datetime.date.today()),
                'Read Status': '',
            })

def main():
    parser = argparse.ArgumentParser(description='Process git repository details.')
    parser.add_argument('repo_path', type=str, help='Path to the local git repository')
    parser.add_argument('subdirectory', type=str, help='Subdirectory in the git repository')
    parser.add_argument('owner', type=str, help='Owner or organization of the Github repository')
    parser.add_argument('branch', type=str, help='Branch to track')
    parser.add_argument('--output', type=str, default='output.csv', help='Path to the output CSV file')

    args = parser.parse_args()

    repo_path = args.repo_path
    repo_name = repo_path.split('/')[-1]
    subdirectory = args.subdirectory
    owner = args.owner
    branch = args.branch
    output_file = args.output

    file_paths = list_files_in_git_repo(repo_path, subdirectory)
    commit_sha = get_current_commit_sha(repo_path)

    repo_url_stem = f"github.com/{owner}/{repo_name}/blob/{branch}"

    if commit_sha is not None:
        write_csv_file(repo_url_stem, repo_path, file_paths, commit_sha, output_file)
        print(f"CSV file generated at {output_file}")
    else:
        print("Error: Unable to determine current git commit SHA.")

if __name__ == '__main__':
    main()
