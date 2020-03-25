# flake8: noqa
from dataclasses import dataclass
from sqlalchemy_declarative_database.types import (
    Role,
    Roles,
    Schemas,
)
from sqlalchemy_declarative_database.sqlalchemy import listen


def declarative_database(cls):
    cls.metadata.info["roles"] = getattr(cls, "roles", [])
    cls.metadata.info["schemas"] = getattr(cls, "schemas", [])

    listen(cls.metadata)
    return cls
