from sqlalchemy_declarative_database.role import Role
from datetime import datetime
from sqlalchemy.schema import DDL
from sqlalchemy.sql import text


def role_ddl(role: Role):
    ddl = DDL(postgres_render_create_role(role))
    return ddl.execute_if(callable_=check_role, state=role)


def postgres_identify_existing_roles(conn):
    select_roles = "SELECT rolname FROM pg_roles"
    return {
        role
        for role, *_ in conn.execute(select_roles).fetchall()
        if not role.startswith("pg_")
    }


def check_role(ddl, target, connection, state, **_):
    dialect = connection.dialect.name
    if dialect == "postgresql":
        roles = postgres_identify_existing_roles(connection)

    elif "sqlite" in dialect:
        # This is pretty jank, but it seems like there's not a way to do this with `CreateSchema`
        # without first registering it on the dialect, which we cannot do.
        schema_exists = "ATTACH DATABASE ':memory:' AS :schema"
        connection.execute(schema_exists, schema=ddl.element)
        return False
    else:
        raise NotImplementedError()

    role = state
    return role.name not in roles


def conditional_option(option, condition):
    if not option:
        option = "NO{segment}"
    return option


def postgres_render_create_role(role: Role):
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
        timestamp = role.valid_until.isoformat()
        segment = f"VALID UNTIL '{timestamp}'"
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
    return command


def postgres_render_drop_role(role: Role):
    return f"DROP ROLE {role.name}"
