from dataclasses import dataclass, astuple, fields, field
from datetime import datetime
from typing import Optional, List, Union, Tuple


@dataclass
class Schema:
    name: str


@dataclass
class Schemas:
    schemas: List[Schema] = field(default_factory=list)
    ignore_unspecified: bool = False

    @classmethod
    def options(cls, ignore_unspecified=False):
        return cls(ignore_unspecified=ignore_unspecified)

    def __iter__(self):
        for schema in self.schemas:
            yield schema

    def are(self, *schemas: List[Union[Schema, str]]):
        cls = self.__class__
        return cls(
            schemas=[
                schema if isinstance(schema, Schema) else Schema(schema)
                for schema in schemas
            ],
            ignore_unspecified=self.ignore_unspecified,
        )


@dataclass
class Role:
    """
    postgres: https://www.postgresql.org/docs/current/sql-createrole.html
    """

    name: str

    superuser: Optional[bool] = None
    createdb: Optional[bool] = None
    createrole: Optional[bool] = None
    inherit: Optional[bool] = None
    login: Optional[bool] = None
    replication: Optional[bool] = None
    bypass_rls: Optional[bool] = None

    connection_limit: Optional[int] = None

    password: Optional[str] = None
    valid_until: Optional[datetime] = None

    in_roles: Optional[List[str]] = None
    roles: Optional[List[str]] = None
    admins: Optional[List[str]] = None

    @property
    def has_option(self):
        _, *options = astuple(self)
        return any(o is not None for o in options)

    @property
    def options(self):
        for f in fields(self):
            if f.name == "name":
                continue

            value = getattr(self, f.name)
            if value is None:
                continue

            yield f.name, value


@dataclass
class User(Role):
    pass


@dataclass
class Roles:
    roles: List[Role] = field(default_factory=list)
    ignore_unspecified: bool = False

    @classmethod
    def options(cls, ignore_unspecified=False):
        return cls(ignore_unspecified=ignore_unspecified)

    def roles(self, *roles: Tuple[Union[Role, str]]):
        cls = self.__class__
        return cls(
            roles=[role if isinstance(role, cls) else Role(role) for role in roles],
            ignore_unspecified=self.ignore_unspecified,
        )
