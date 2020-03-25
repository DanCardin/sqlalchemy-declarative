from sqlalchemy import event
from sqlalchemy_declarative_database.sqlalchemy.schema import schema_ddl


def listen(metadata):
    schemas = metadata.info["schemas"]
    for schema in schemas:
        event.listen(
            metadata, "before_create", schema_ddl(schema),
        )
