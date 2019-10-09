from sqlalchemy.ext.declarative import as_declarative

from sqlalchemy_declarative import role, schema  # noqa
from sqlalchemy_declarative.declarative import declarative_schema, Privileges, Role


@declarative_schema
@as_declarative()
class Base:
    schemas = ("example", "analysis", "sandbox")
    roles = (
        Role(
            "app",
            privileges=[
                Privileges(
                    schemas=["example", 'analysis', 'sandbox'],
                    schema=['CREATE'],
                    tables=['ALL'],
                )
            ],
        ),
        Role(
            "analyst",
            privileges=[
                Privileges(schemas=["example"], select=True),
                Privileges(
                    schemas=["analysis"],
                    schema=['']
                    select=True,
                    insert=True,
                    update=True,
                    delete=True,
                    default=True,
                ),
                Privileges(schema="sandbox", all=True, default=True),
            ],
        ),
        Role("foo", in_="analyst"),
    )
