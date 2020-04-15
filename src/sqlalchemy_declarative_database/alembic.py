from alembic.operations import MigrateOperation


class GenericOp(MigrateOperation):
    forward_cls = None

    def __init__(self, instance):
        self.instance = instance

    @classmethod
    def forward(cls, operations, kwargs):
        instance = cls.forward_cls(**kwargs)
        op = cls(instance)
        return operations.invoke(op)
