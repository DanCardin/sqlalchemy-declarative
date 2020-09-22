from dataclasses import dataclass, field, replace
from typing import List, Union
from sqlalchemy_declarative_database.functools import maybe_classmethod


@dataclass
class Schema:
    name: str


@dataclass
class Schemas:
    schemas: List[Schema] = field(default_factory=list)
    ignore_unspecified: bool = False

    @maybe_classmethod
    def options(self, ignore_unspecified=False):
        return replace(self, ignore_unspecified=ignore_unspecified)

    @maybe_classmethod()
    def are(self, *schemas: List[Union[Schema, str]]):
        return replace(
            self,
            schemas=[
                schema if isinstance(schema, Schema) else Schema(schema)
                for schema in schemas
            ],
        )

    def __iter__(self):
        for schema in self.schemas:
            yield schema
