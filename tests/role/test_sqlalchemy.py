from datetime import datetime

import psycopg2
from pytest_mock_resources import create_postgres_fixture
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_declarative_database import declarative_database, Role, Roles


@declarative_database
class Base(declarative_base()):
    __abstract__ = True

    roles = Roles().are(
        "nooptions",
        Role(
            "most_options",
            superuser=True,
            createdb=True,
            createrole=True,
            inherit=True,
            login=True,
            replication=True,
            bypass_rls=True,
            connection_limit=1,
            valid_until=datetime(2999, 1, 1),
            in_roles=["nooptions"],
        ),
    )


pg = create_postgres_fixture()


def test_createall_role(pg):
    Base.metadata.create_all(bind=pg)
    result = pg.execute(
        text(
            "SELECT rolname, rolsuper, rolinherit, rolcreaterole, rolcreatedb, rolcanlogin, rolreplication, rolconnlimit, rolvaliduntil, rolbypassrls, rolconfig FROM pg_roles WHERE rolname NOT LIKE :pg_name and rolname != :connected_name"
        ),
        pg_name="pg_%",
        connected_name=pg.pmr_credentials.username,
    ).fetchall()

    expected_result = [
        ("nooptions", False, True, False, False, False, False, -1, None, False, None),
        (
            "most_options",
            True,
            True,
            True,
            True,
            True,
            True,
            1,
            datetime(
                2999, 1, 1, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=0, name=None)
            ),
            True,
            None,
        ),
    ]
    assert expected_result == result
