from sqlalchemy.ext.declarative import as_declarative


def declarative_schema(cls):
    cls.metadata.info["roles"] = cls.roles
    cls.metadata.info["schemas"] = cls.schemas
    return cls


@declarative_schema
@as_declarative()
class Base:
    roles = ("app", "analyst", "operator")
    schemas = {
        "example": {
            "SELECT": ("app", "analyst"),
            "INSERT": ("app",),
            "UPDATE": ("app",),
            "DELETE": ("app",),
        },
        "analysis": {
            "SELECT": ("analyst",),
            "INSERT": ("analyst",),
            "UPDATE": ("analyst",),
            "DELETE": ("analyst",),
        },
        "sandbox": {"ALL": ("analysis",)},
    }
