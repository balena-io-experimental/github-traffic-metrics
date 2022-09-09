from datetime import datetime
from db import Clone, Path, Referrer, View, get_engine
from sqlalchemy.orm import Session


def store_repo(repo):
    today = datetime.today()

    owner = repo.organization.login
    repo_name = repo.name

    referrers = repo.get_top_referrers()
    paths = repo.get_top_paths()
    views = repo.get_views_traffic()
    clones = repo.get_clones_traffic()

    with Session(get_engine()) as session:
        rows = []

        rows += get_db_referrels(owner, repo_name, today, referrers)
        rows += get_db_paths(owner, repo_name, today, paths)
        rows += get_db_clones(owner, repo_name, clones["clones"])
        rows += get_db_views(owner, repo_name, views["views"])

        [session.merge(row) for row in rows]
        session.commit()


def get_db_referrels(owner, repo_name, today, referrers):
    return [
        Referrer(
            owner=owner,
            repo=repo_name,
            day=today,
            rank=rank,
            referrer=ref.referrer,
            count=ref.count,
            uniques=ref.uniques,
        )
        for (rank, ref) in enumerate(referrers)
    ]


def get_db_paths(owner, repo_name, today, paths):
    return [
        Path(
            owner=owner,
            repo=repo_name,
            day=today,
            rank=rank,
            title=path.title,
            path=path.path,
            count=path.count,
            uniques=path.uniques,
        )
        for (rank, path) in enumerate(paths)
    ]


def get_db_clones(owner, repo_name, clones):
    return [
        Clone(
            owner=owner,
            repo=repo_name,
            day=clone.timestamp,
            count=clone.count,
            uniques=clone.uniques,
        )
        for clone in clones
    ]


def get_db_views(owner, repo_name, views):
    return [
        View(
            owner=owner,
            repo=repo_name,
            day=view.timestamp,
            count=view.count,
            uniques=view.uniques,
        )
        for view in views
    ]
