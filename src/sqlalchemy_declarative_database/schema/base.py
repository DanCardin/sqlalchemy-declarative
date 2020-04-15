from dataclasses import dataclass, field
from typing import List, Union


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
