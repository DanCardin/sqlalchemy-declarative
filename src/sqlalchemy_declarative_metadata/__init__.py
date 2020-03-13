# flake8: noqa
from sqlalchemy_declarative_metadata.types import (
    Role,
    Roles,
    Schemas,
    Privilege,
    Privileges,
)


def declarative_schema(cls):
    cls.metadata.info["roles"] = cls.roles
    cls.metadata.info["schemas"] = cls.schemas
    cls.metadata.info["options"] = cls.options
    return cls
