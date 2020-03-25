from alembic.autogenerate import renderers
from sqlalchemy_declarative_database.alembic.operation import (
    CreateSchemaOp,
    DropSchemaOp,
    CreateRoleOp,
    DropRoleOp,
)


@renderers.dispatch_for(CreateSchemaOp)
def render_create_schema(autogen_context, op):
    return "op.create_schema('{}')".format(op.schema)


@renderers.dispatch_for(DropSchemaOp)
def render_drop_schema(autogen_context, op):
    return "op.drop_schema('{}')".format(op.schema)


@renderers.dispatch_for(CreateRoleOp)
def render_create_role(autogen_context, op):
    role = op
    return (
        "op.create_role(\n"
        f"    '{role.name}',\n"
        + "".join((f"    {key}={repr(value)},\n" for key, value in role.options))
        + ")"
    )


@renderers.dispatch_for(DropRoleOp)
def render_drop_role(autogen_context, op):
    role = op
    return f"op.drop_role('{role.name}')"
