from alembic.autogenerate import comparators
from alembic.autogenerate import renderers
from sqlalchemy_declarative_database.sqlalchemy.role import (
    postgres_render_create_role,
    postgres_render_drop_role,
)
from sqlalchemy_declarative_database.alembic import GenericOp
from sqlalchemy_declarative_database.role.base import Role
from alembic.operations import Operations


@Operations.register_operation("create_role")
class CreateRoleOp(GenericOp):
    forward_cls = Role

    @classmethod
    def create_role(cls, operations, **kwargs):
        return cls.forward(operations, kwargs)

    def reverse(self):
        return DropRoleOp(self.instance)


@Operations.register_operation("drop_role")
class DropRoleOp(GenericOp):
    forward_cls = Role

    @classmethod
    def drop_role(cls, operations, **kwargs):
        return cls.forward(operations, kwargs)

    def reverse(self):
        return CreateRoleOp(self.instance)


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


@Operations.implementation_for(CreateRoleOp)
def create_role(operations, operation):
    command = postgres_render_create_role(operation)
    operations.execute(command)


@Operations.implementation_for(DropRoleOp)
def drop_role(operations, operation):
    command = postgres_render_drop_role(operation)
    operations.execute(command)
