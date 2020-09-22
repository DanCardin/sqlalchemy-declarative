![CircleCI](https://img.shields.io/circleci/build/gh/schireson/sqlalchemy-declarative-database/master) [![codecov](https://codecov.io/gh/schireson/sqlalchemy-declarative-database/branch/master/graph/badge.svg)](https://codecov.io/gh/schireson/sqlalchemy-declarative-database) [![Documentation Status](https://readthedocs.org/projects/sqlalchemy-declarative-database/badge/?version=latest)](https://sqlalchemy-declarative-database.readthedocs.io/en/latest/?badge=latest)

# Introduction

Vanilla SQLAlchemy models (or table definitions) are primarily useful because they state what your
**tables** *ought* to look like. APIs like `sqlalchemy.MetaData.create_all` will only go so far
as issuing the `CREATE` statements for those tables (and related objects).

Vanilla Alembic migrations are primarily useful because they interpolate how to move from the
*current* state of your tables to the desired state. While you can execute any valid SQL in
a migration, something like the `--autogenerate` flag will only reflect against your tables.

As the name so eloquently states, `sqlalchemy-declarative-database` allows you to declaratively
specify things about your database, which would not otherwise be possible to do with vanilla
SQLAlchemy or Alembic.

# Usage

Given a declarative statement of what your database should contain:

```python
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy_declarative_database import declarative_database

@declarative_database
@as_declarative()
class Base:
    schemas = Schemas.are("example", "analysis", "sandbox")
    roles = Roles.options(ignore_unspecified=True).are(
        Role(
            "app",
            privileges=Privileges.privileges(
                Privilege(
                    schemas=["example", "analysis", "sandbox"],
                    schema=["CREATE"],
                    tables=["ALL"],
                )
            ),
        ),
        Role("foo", in_roles=["analyst"]),
    )
```

A subsequent call to `Base.metadata.create_all()` will automatically create all the specified
schemas and roles (and privileges for those roles).

When running `alembic revision --autogenerate`, alembic will automatically generate the appropriate
migrations statements to produce the desired state from the existing database.

# Why is this a good idea?

In particular, the automatic handling of schemas ought to be unambiguously a good idea, as it is
internal to the database to which your migrations are running against, and is scoped there in
much the same way as it is for tables.

Roles/Privileges/other database-wide objects may be more arguable. And to be clear, it may
**not** make sense to declaratively produce individual user roles (with passwords), as they are
subject to change, and ultimately have no bearing on the functioning of your system.

When it does make sense, is when you declare roles to describe a set of persmissions a **sort** of
user ought to have, and then (manually or otherwise) create user-roles separately.

A good set of metrics would be:

* *Will there be manual steps required before/after the running of migrations?*

  This is typical when creating new schemas or tables, and existing users may not be automatically
  granted permissions. Managing permissions (even default permissions) can be fraught with issues,
  particularly when maintaining parity between local, development, and production environments.

* *Will the migrations reference objects which were not also created in the given migration history?*

  This can happen as a result of attempting to address the above point. Suppose we don't have
  global default permissions and are creating a new schema. We want to avoid manual steps, so the
  migrations run some `ALTER DEFAULT PRIVILEGES` command against...the set of roles which need
  this new permissision.

  If your migrations didn't create the role, it's likely your migrations will now fail when
  i.e. executed locally from the beginning against an empty database.


Other concerns might be:

* *What happens if you ever add a new role?*

  This might result in a bunch of manual granting of permissions to existing objects and duplication
  of existing roles.

* *What if we change the general permissions available to some set of roles?*

  A similar scenario to the above.

All that to say, it's often the case that it makes sense to have a source of truth for the correct
set of roles and permissions to create, when instantiating an instance of a database. Encoding the
creation (and changes throughout the history of migrations) of these kinds of things makes it much
easier to reproduce the state of your database at a point in time, and (almost more importantly)
simply describe the way it **ought** to look without worrying as much about how to move from the
current state to the desired state.
