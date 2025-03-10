import os 
import json

from dotenv import load_dotenv
from github import Github

load_dotenv()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
            )
        )
    )
#-------------------------Tracking documents update--------------------#
GITHUB_TOKEN = os.getenv("GITHUB")
REPO_LINKS_FILE = os.path.join(BASE_DIR, "urls", "repo_links.json")


# read the repos' name in .json
try:
    with open(REPO_LINKS_FILE, "r", encoding="utf-8") as file:
        repo_names = json.load(file)  # Đọc danh sách repo từ file
        if not isinstance(repo_names, list) or not repo_names:
            raise ValueError("⚠️ Invalid repo_names.json format! Expected a non-empty list.")
except FileNotFoundError:
    raise FileNotFoundError(f"⚠️ {REPO_LINKS_FILE} not found!")
except json.JSONDecodeError:
    raise ValueError(f"⚠️ {REPO_LINKS_FILE} contains invalid JSON!")

g = Github(GITHUB_TOKEN)

def get_latest_accepted_prs():
    all_latest_prs = []  

    for repo_name in repo_names:
        try:
            repo = g.get_repo(repo_name)  
            if repo.private and "repo" not in g.oauth_scopes:
                print(f"⚠️ Skipping {repo_name}: Private repository requires 'repo' scope in token!")
                continue
            pull_requests = repo.get_pulls(state="closed", sort="updated", direction="desc")
            seen_prs = set()
            count = 0
            for pr in pull_requests:
                if pr.merged_at is None:
                    continue
                if pr.number in seen_prs:
                    continue
                seen_prs.add(pr.number)
                files = pr.get_files()
                changed_files = [file.filename for file in files]

                all_latest_prs.append({
                    "repo": repo_name,
                    "number": pr.number,
                    "title": pr.title,
                    "merged_at": pr.merged_at.isoformat(),
                    "url": pr.html_url,
                    "changed_files": changed_files
                })

                count += 1
                if count >= 3:
                    break
        except Exception as e:
            print(f"⚠️ Error fetching PRs from {repo_name}: {e}")

    return all_latest_prs
