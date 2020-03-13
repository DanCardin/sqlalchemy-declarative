from alembic.operations import Operations
from sqlalchemy.schema import CreateSchema, DropSchema
from sqlalchemy_declarative_metadata.alembic.operation import (
    CreateSchemaOp,
    DropSchemaOp,
)


@Operations.implementation_for(CreateSchemaOp)
def create_schema(operations, operation):
    operations.execute(CreateSchema(operation.schema))


@Operations.implementation_for(DropSchemaOp)
def drop_schema(operations, operation):
    operations.execute(DropSchema(operation.schema))
