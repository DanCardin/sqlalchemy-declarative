from alembic.operations import MigrateOperation, Operations
from sqlalchemy_declarative_metadata.types import Schema, Role


class GenericOp(MigrateOperation):
    forward_cls = None

    def __init__(self, instance):
        self.instance = instance

    @classmethod
    def forward(cls, operations, kwargs):
        instance = cls.forward_cls(**kwargs)
        op = cls(instance)
        return operations.invoke(op)


@Operations.register_operation("create_schema")
class CreateSchemaOp(GenericOp):
    """Create a SCHEMA."""

    forward_cls = Schema

    @classmethod
    def create_schema(cls, operations, **kwargs):
        return cls.forward(operations, kwargs)

    def reverse(self):
        return DropSchemaOp(self.instance)


@Operations.register_operation("drop_schema")
class DropSchemaOp(GenericOp):
    """Drop a SCHEMA."""

    forward_cls = Schema

    @classmethod
    def drop_schema(cls, operations, schema, **kwargs):
        return cls.forward(operations, kwargs)

    def reverse(self):
        return CreateSchemaOp(self.instance)


@Operations.register_operation("create_role")
class CreateRoleOp(GenericOp):
    forward_cls = Role

    @classmethod
    def create_role(cls, operations, **kwargs):
        return cls.forward(operations, kwargs)

    def reverse(self):
        return DropRoleOp(self.instance)


@Operations.register_operation("drop_role")
class DropRoleOp(GenericOp):
    forward_cls = Role

    @classmethod
    def drop_role(cls, operations, **kwargs):
        return cls.forward(operations, kwargs)

    def reverse(self):
        return CreateRoleOp(self.instance)
