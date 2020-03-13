from alembic.operations import Operations
from datetime import datetime
from sqlalchemy_declarative_metadata.alembic.base import conditional_option
from sqlalchemy_declarative_metadata.alembic.operation import (
    CreateRoleOp,
    DropRoleOp,
)


@Operations.implementation_for(CreateRoleOp)
def create_role(operations, operation):
    role = operation

    segments = ["CREATE ROLE", role.name]
    if role.has_option:
        segments.append("WITH")

    if role.superuser is not None:
        segment = conditional_option("SUPERUSER", role.superuser)
        segments.append(segment)

    if role.createdb is not None:
        segment = conditional_option("CREATEDB", role.createdb)
        segments.append(segment)

    if role.createrole is not None:
        segment = conditional_option("CREATEROLE", role.createrole)
        segments.append(segment)

    if role.inherit is not None:
        segment = conditional_option("INHERIT", role.inherit)
        segments.append(segment)

    if role.login is not None:
        segment = conditional_option("LOGIN", role.login)
        segments.append(segment)

    if role.replication is not None:
        segment = conditional_option("REPLICATION", role.replication)
        segments.append(segment)

    if role.bypass_rls is not None:
        segment = conditional_option("BYPASSRLS", role.bypass_rls)
        segments.append(segment)

    if role.connection_limit is not None:
        segment = f"CONNECTION LIMIT {role.connection_limit}"
        segments.append(segment)

    if role.password is not None:
        segment = f"PASSWORD {role.password}"
        segments.append(segment)

    if role.password is not None:
        segment = f"PASSWORD {role.password}"
        segments.append(segment)

    if role.valid_until is not None:
        timestamp = datetime.timestamp(role.valid_until)
        segment = f"VALID UNTIL {timestamp}"
        segments.append(segment)

    if role.in_roles is not None:
        in_roles = ", ".join(role.in_roles)
        segment = f"IN ROLE {in_roles}"
        segments.append(segment)

    if role.roles is not None:
        roles = ", ".join(role.roles)
        segment = f"ROLE {roles}"
        segments.append(segment)

    if role.admins is not None:
        admins = ", ".join(role.admins)
        segment = f"ROLE {admins}"
        segments.append(segment)

    command = " ".join(segments)
    operations.execute(command)


@Operations.implementation_for(DropRoleOp)
def drop_role(operations, operation):
    role = operation

    command = f"DROP ROLE {role.name}"
    operations.execute(command)
