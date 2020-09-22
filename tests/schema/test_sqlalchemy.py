from pytest_mock_resources import create_postgres_fixture, create_sqlite_fixture
import sqlalchemy
from sqlalchemy_declarative_database import declarative_database, Schemas
from sqlalchemy.ext.declarative import declarative_base


pg = create_postgres_fixture()
sqlite = create_sqlite_fixture()


class TestSchemas:
    @declarative_database
    class Base(declarative_base()):
        __abstract__ = True

        schemas = Schemas().are("fooschema")

    class Foo(Base):
        __tablename__ = "foo"
        __table_args__ = {"schema": "fooschema"}

        id = sqlalchemy.Column(sqlalchemy.types.Integer(), primary_key=True)

    def test_createall_schema_pg(self, pg):
        self.Base.metadata.create_all(bind=pg)
        result = pg.execute(self.Foo.__table__.select()).fetchall()
        assert result == []

    def test_createall_schema_sqlite(self, sqlite):
        self.Base.metadata.create_all(bind=sqlite, checkfirst=False)
        result = sqlite.execute(self.Foo.__table__.select()).fetchall()
        assert result == []


class TestSchemasCls:
    @declarative_database
    class Base(declarative_base()):
        __abstract__ = True

        schemas = Schemas.are("fooschema")

    class Foo(Base):
        __tablename__ = "foo"
        __table_args__ = {"schema": "fooschema"}

        id = sqlalchemy.Column(sqlalchemy.types.Integer(), primary_key=True)

    def test_createall_schema_pg(self, pg):
        self.Base.metadata.create_all(bind=pg)
        result = pg.execute(self.Foo.__table__.select()).fetchall()
        assert result == []

    def test_createall_schema_sqlite(self, sqlite):
        self.Base.metadata.create_all(bind=sqlite, checkfirst=False)
        result = sqlite.execute(self.Foo.__table__.select()).fetchall()
        assert result == []
