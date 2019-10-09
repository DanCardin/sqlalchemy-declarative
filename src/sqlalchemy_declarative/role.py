import attr
import sqlalchemy
from alembic.autogenerate import comparators, renderers
from alembic.operations import MigrateOperation, Operations

from sqlalchemy_declarative.declarative import Privileges, Role


@Operations.register_operation("create_role")
class CreateRoleOp(Role, MigrateOperation):
    @classmethod
    def create_role(cls, operations, role, privileges=None, **kw):
        privileges = [Privileges(**privilege) for privilege in (privileges or [])]
        op = cls(role, privileges=privileges, **kw)
        return operations.invoke(op)

    def reverse(self):
        return DropRoleOp(**attr.asdict(self))


@Operations.register_operation("drop_role")
class DropRoleOp(Role, MigrateOperation):
    @classmethod
    def drop_role(cls, operations, role, privileges=None, **kw):
        privileges = [Privileges(**privilege) for privilege in (privileges or [])]
        op = cls(role, privileges=privileges, **kw)
        return operations.invoke(op)

    def reverse(self):
        return CreateRoleOp(**attr.asdict(self))


@renderers.dispatch_for(CreateRoleOp)
def render_create_role(autogen_context, op):
    optional_in = ""
    if op.in_:
        optional_in = "in_='{}'\n".format(op.in_)

    return (
        "op.create_role(\n"
        "    '{role}',\n"
        "    privileges={privileges},\n"
        "    " + optional_in + ")"
    ).format(role=op.name, privileges=op.privileges)


@renderers.dispatch_for(DropRoleOp)
def render_drop_role(autogen_context, op):
    return "op.drop_role('{role}'".format(role=op.name)


@comparators.dispatch_for("schema")
def compare_roles(autogen_context, upgrade_ops, schemas):
    # existing_schemas = {
    #     schema
    #     for schema, *_ in autogen_context.connection.execute(
    #         "SELECT nspname FROM pg_catalog.pg_namespace"
    #     ).fetchall()
    #     if not schema.startswith("pg_")
    #     and schema
    #     not in {"information_schema", autogen_context.dialect.default_schema_name}
    # }
    #
    # new_schemas = expected_schemas - existing_schemas
    # removed_schemas = existing_schemas - expected_schemas
    # for schema in reversed(sorted(removed_schemas)):
    #     upgrade_ops.ops.append(DropSchemaOp(schema))

    roles = autogen_context.metadata.info["roles"]
    for role in roles:
        upgrade_ops.ops.append(CreateRoleOp(**attr.asdict(role)))


@Operations.implementation_for(CreateRoleOp)
def create_role(operations, operation):
    commands = []
    for privilege in operation.privileges:
        command = "CREATE ROLE {};".format(operation.name)
        commands.append(command)

        command = (
            "ALTER DEFAULT PRIVILEGES{in_schema}\n"
            "GRANT\n"
            "{privileges}\n"
            "ON TABLES to {role};"
        ).format(
            role=operation.name,
            default=" DEFAULT" if privilege.default else "",
            privileges=(
                ", ".join(
                    [
                        "    {}\n".format(op.upper())
                        for op in ["select", "insert", "update", "delete"]
                        if getattr(privilege, op)
                    ]
                )
                if not privilege.all
                else "ALL PRIVILEGES"
            ),
            in_schema=" IN SCHEMA {}".format(privilege.schema)
            if privilege.schema
            else "",
        )
        commands.append(command)

    for command in commands:
        print(command)
        operations.execute(command)


@Operations.implementation_for(DropRoleOp)
def drop_role(operations, operation):
    import pdb

    pdb.set_trace()
