from sqlalchemy import CheckConstraint, Column, Date, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Clone(Base):
    __tablename__ = "clone"

    owner = Column(String, primary_key=True)
    repo = Column(String, primary_key=True)
    day = Column(Date, primary_key=True)
    count = Column(Integer)
    uniques = Column(Integer)

    __table_args__ = (
        CheckConstraint(count >= 0, name="check_count_non_negative"),
        CheckConstraint(uniques >= 0, name="check_uniques_non_negative"),
        {},
    )


class Path(Base):
    __tablename__ = "path"
    owner = Column(String, primary_key=True)
    repo = Column(String, primary_key=True)
    day = Column(Date, primary_key=True)
    rank = Column(Integer, primary_key=True)
    title = Column(String)
    path = Column(String)
    count = Column(Integer)
    uniques = Column(Integer)

    __table_args__ = (
        CheckConstraint(rank >= 0, name="check_rank_non_negative"),
        CheckConstraint(count >= 0, name="check_count_non_negative"),
        CheckConstraint(uniques >= 0, name="check_uniques_non_negative"),
        {},
    )


class Referrer(Base):
    __tablename__ = "referrer"
    owner = Column(String, primary_key=True)
    repo = Column(String, primary_key=True)
    day = Column(Date, primary_key=True)
    rank = Column(Integer, primary_key=True)
    referrer = Column(String)
    count = Column(Integer)
    uniques = Column(Integer)

    __table_args__ = (
        CheckConstraint(rank >= 0, name="check_rank_non_negative"),
        CheckConstraint(count >= 0, name="check_count_non_negative"),
        CheckConstraint(uniques >= 0, name="check_uniques_non_negative"),
        {},
    )


class View(Base):
    __tablename__ = "view"
    owner = Column(String, primary_key=True)
    repo = Column(String, primary_key=True)
    day = Column(Date, primary_key=True)
    count = Column(Integer)
    uniques = Column(Integer)

    __table_args__ = (
        CheckConstraint(count >= 0, name="check_count_non_negative"),
        CheckConstraint(uniques >= 0, name="check_uniques_non_negative"),
        {},
    )


engine = None


def get_engine():
    global engine
    if engine is None:
        engine = create_engine("sqlite:///db.sqlite3", echo=False, future=True)
        Base.metadata.create_all(engine)
    return engine
