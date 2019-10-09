import sqlalchemy
from alembic.autogenerate import comparators, renderers
from alembic.operations import MigrateOperation, Operations
from sqlalchemy.schema import CreateSchema, DropSchema


@comparators.dispatch_for("schema")
def compare_sequences(autogen_context, upgrade_ops, schemas):
    existing_schemas = {
        schema
        for schema, *_ in autogen_context.connection.execute(
            "SELECT nspname FROM pg_catalog.pg_namespace"
        ).fetchall()
        if not schema.startswith("pg_")
        and schema
        not in {"information_schema", autogen_context.dialect.default_schema_name}
    }

    expected_schemas = set(autogen_context.metadata.info["schemas"])
    new_schemas = expected_schemas - existing_schemas
    removed_schemas = existing_schemas - expected_schemas

    for schema in sorted(new_schemas):
        upgrade_ops.ops.insert(0, CreateSchemaOp(schema))

    for schema in reversed(sorted(removed_schemas)):
        upgrade_ops.ops.append(DropSchemaOp(schema))


@Operations.register_operation("create_schema")
class CreateSchemaOp(MigrateOperation):
    """Create a SCHEMA."""

    def __init__(self, schema):
        self.schema = schema

    @classmethod
    def create_schema(cls, operations, schema, **kw):
        """Issue a "CREATE SCHEMA" instruction."""
        op = cls(schema, **kw)
        return operations.invoke(op)

    def reverse(self):
        return DropSchemaOp(self.schema)


@Operations.register_operation("drop_schema")
class DropSchemaOp(MigrateOperation):
    """Drop a SCHEMA."""

    def __init__(self, schema):
        self.schema = schema

    @classmethod
    def drop_schema(cls, operations, schema, **kw):
        """Issue a "DROP SCHEMA" instruction."""
        operations.execute(Create)
        op = cls(schema, **kw)
        return operations.invoke(op)

    def reverse(self):
        return CreateSchemaOp(self.schema)


@renderers.dispatch_for(CreateSchemaOp)
def render_create_schema(autogen_context, op):
    return "op.create_schema('{}')".format(op.schema)


@renderers.dispatch_for(DropSchemaOp)
def render_create_schema(autogen_context, op):
    return "op.drop_schema('{}')".format(op.schema)


@Operations.implementation_for(CreateSchemaOp)
def create_schema(operations, operation):
    operations.execute(CreateSchema(operation.schema))


@Operations.implementation_for(DropSchemaOp)
def drop_schema(operations, operation):
    operations.execute(DropSchema(operation.schema))
