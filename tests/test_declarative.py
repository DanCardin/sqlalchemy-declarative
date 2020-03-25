from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy_declarative_database import (
    declarative_schema,
    Role,
    Roles,
    Schemas,
    Privilege,
    Privileges,
)
from pytest_mock_resources import create_postgres_fixture

pg = create_postgres_fixture()


@declarative_schema
@as_declarative()
class Base:
    schemas = Schemas.options(ignore_unspecified=True).are(
        "example", "analysis", "sandbox"
    )
    roles = Roles.options(ignore_unspecified=True).roles(
        Role(
            "app",
            privileges=Privileges.options().privileges(
                Privilege(
                    schemas=["example", "analysis", "sandbox"],
                    schema=["CREATE"],
                    tables=["ALL"],
                )
            ),
        ),
        Role(
            "analyst",
            privileges=Privileges.options().privileges(
                Privilege(schemas=["example"], select=True),
                Privilege(
                    schemas=["analysis"],
                    schema=[""],
                    select=True,
                    insert=True,
                    update=True,
                    delete=True,
                    default=True,
                ),
                Privilege(schema="sandbox", all=True, default=True),
            ),
        ),
        Role("foo", in_roles=["analyst"]),
    )


def test_generate():
    pass
