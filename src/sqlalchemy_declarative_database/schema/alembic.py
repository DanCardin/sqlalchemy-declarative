from alembic.operations import Operations
from alembic.operations import Operations
from sqlalchemy.schema import CreateSchema, DropSchema


from alembic.autogenerate import comparators
from alembic.autogenerate import renderers
from sqlalchemy_declarative_database.alembic import GenericOp
from sqlalchemy_declarative_database.schema.base import Schema


@Operations.register_operation("create_schema")
class CreateSchemaOp(GenericOp):
    """Create a SCHEMA."""

    forward_cls = Schema

    @classmethod
    def create_schema(cls, operations, **kwargs):
        return cls.forward(operations, kwargs)

    def reverse(self):
        return DropSchemaOp(self.instance)


@Operations.register_operation("drop_schema")
class DropSchemaOp(GenericOp):
    """Drop a SCHEMA."""

    forward_cls = Schema

    @classmethod
    def drop_schema(cls, operations, schema, **kwargs):
        return cls.forward(operations, kwargs)

    def reverse(self):
        return CreateSchemaOp(self.instance)


@comparators.dispatch_for("schema")
def compare_schemas(autogen_context, upgrade_ops, schemas):
    schemas = autogen_context.metadata.info["schemas"]

    select_schemas = "SELECT nspname FROM pg_catalog.pg_namespace"
    existing_schemas = {
        schema
        for schema, *_ in autogen_context.connection.execute(select_schemas).fetchall()
        if not schema.startswith("pg_")
        and schema
        not in {"information_schema", autogen_context.dialect.default_schema_name}
    }

    expected_schemas = set(schemas.schemas)
    new_schemas = expected_schemas - existing_schemas
    removed_schemas = existing_schemas - expected_schemas

    for schema in sorted(new_schemas):
        upgrade_ops.ops.insert(0, CreateSchemaOp(schema))

    if not schemas.ignore_unspecified:
        for schema in reversed(sorted(removed_schemas)):
            upgrade_ops.ops.append(DropSchemaOp(schema))


@renderers.dispatch_for(CreateSchemaOp)
def render_create_schema(autogen_context, op):
    return "op.create_schema('{}')".format(op.schema)


@renderers.dispatch_for(DropSchemaOp)
def render_drop_schema(autogen_context, op):
    return "op.drop_schema('{}')".format(op.schema)


@Operations.implementation_for(CreateSchemaOp)
def create_schema(operations, operation):
    operations.execute(CreateSchema(operation.schema))


@Operations.implementation_for(DropSchemaOp)
def drop_schema(operations, operation):
    operations.execute(DropSchema(operation.schema))
