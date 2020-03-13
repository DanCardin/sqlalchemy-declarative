from alembic.autogenerate import comparators
from sqlalchemy_declarative_metadata.alembic.operation import (
    CreateSchemaOp,
    DropSchemaOp,
    CreateRoleOp,
    DropRoleOp,
)


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


@comparators.dispatch_for("schema")
def compare_roles(autogen_context, upgrade_ops, schemas):
    roles = autogen_context.metadata.info["roles"]

    select_roles = "SELECT rolname FROM pg_roles"
    existing_roles = {
        role
        for role, *_ in autogen_context.connection.execute(select_roles).fetchall()
        if not role.startswith("pg_")
    }

    expected_roles = set(roles.roles)
    new_roles = expected_roles - existing_roles
    removed_roles = existing_roles - expected_roles

    for role in sorted(new_roles):
        upgrade_ops.ops.append(CreateRoleOp(role))

    if not roles.ignore_unspecified:
        # XXX: This probably needs to take role dependencies into account, and
        #      figure out an order which wont fail.
        for role in reversed(sorted(removed_roles)):
            upgrade_ops.ops.append(DropRoleOp(role))
