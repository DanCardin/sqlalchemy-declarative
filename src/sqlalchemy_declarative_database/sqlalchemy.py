from sqlalchemy import event

from sqlalchemy_declarative_database.role.ddl import role_ddl
from sqlalchemy_declarative_database.schema.ddl import schema_ddl
from sqlalchemy_declarative_database.role.algorithms import topological_sort


def listen(metadata):
    schemas = metadata.info["schemas"]
    for schema in schemas:
        event.listen(
            metadata, "before_create", schema_ddl(schema),
        )

    roles = metadata.info["roles"]
    for role in topological_sort(roles):
        event.listen(
            metadata, "after_create", role_ddl(role),
        )
