from github import Github
from dotenv import load_dotenv
import os

from orgs import orgs
from repo import store_repo

load_dotenv()

gh = Github(os.getenv("GITHUB_ACCESS_TOKEN"))

repos = [repo for org in orgs for repo in gh.get_organization(org).get_repos()]

for repo in repos:
    print(repo.full_name)
    store_repo(repo)

