from dotenv import load_dotenv
import os
from github import Github
from orgs import orgs
from repo import store_repo
import time

start = time.time()

load_dotenv()
gh = Github(os.getenv("GITHUB_ACCESS_TOKEN"))

repos = [repo for org in orgs for repo in gh.get_organization(org).get_repos()]
print(f"Time to load repos {time.time() - start}s")
print(f"{gh.rate_limiting[0]} request remaining out of {gh.rate_limiting[1]}s")

for repo in repos:
    start_repo = time.time()

    i = 0

    while gh.rate_limiting[0] < 10:
        exp_backoff = min(2 ** i, 64)
        print(f"Rate Limit reached with just {gh.rate_limiting[0]} remaining requests")
        print(f"Will now sleep for {exp_backoff}s")
        time.sleep(exp_backoff)
    try:
        print(repo.full_name)
        store_repo(repo)
        print(f"Time to load and store repo {time.time() - start_repo}s")
        print(f"{gh.rate_limiting[0]} request remaining out of {gh.rate_limiting[1]}s")

    except Exception as e:
        print(f"Failed to store in {time.time() - start_repo}s")
        print(e)

print(f"Total time: {time.time() - start}s")

