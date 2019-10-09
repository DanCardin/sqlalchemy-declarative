import attr


def declarative_schema(cls):
    cls.metadata.info["roles"] = cls.roles
    cls.metadata.info["schemas"] = cls.schemas
    return cls


@attr.s
class Role:
    name = attr.ib()
    in_ = attr.ib(default=None)
    privileges = attr.ib(default=None)


@attr.s
class Privileges:
    schema = attr.ib(default=None)
    select = attr.ib(default=None)
    insert = attr.ib(default=None)
    update = attr.ib(default=None)
    delete = attr.ib(default=None)
    all = attr.ib(default=None)
    default = attr.ib(default=True)
