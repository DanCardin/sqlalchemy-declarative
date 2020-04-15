from sqlalchemy.schema import CreateSchema
from sqlalchemy_declarative_database.schema import Schema
from sqlalchemy.sql import text


def schema_ddl(schema: Schema):
    ddl = CreateSchema(schema.name)
    return ddl.execute_if(callable_=check_schema)


def check_schema(ddl, target, connection, **_):
    dialect = connection.dialect.name
    if dialect == "postgresql":
        schema_exists = text(
            "SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"
        )
    elif "sqlite" in dialect:
        # This is pretty jank, but it seems like there's not a way to do this with `CreateSchema`
        # without first registering it on the dialect, which we cannot do.
        schema_exists = "ATTACH DATABASE ':memory:' AS :schema"
        connection.execute(schema_exists, schema=ddl.element)
        return False
    else:
        raise NotImplementedError()

    row = connection.execute(schema_exists, schema=ddl.element).scalar()
    return not bool(row)
