"""
See https://www.postgresql.org/docs/latest/sql-grant.html.

ALTER DEFAULT PRIVILEGES
    [ FOR { ROLE | USER } target_role [, ...] ]
    [ IN SCHEMA schema_name [, ...] ]
    abbreviated_grant_or_revoke

where abbreviated_grant_or_revoke is one of:

GRANT { { SELECT | INSERT | UPDATE | DELETE | TRUNCATE | REFERENCES | TRIGGER }
    [, ...] | ALL [ PRIVILEGES ] }
    ON TABLES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { { USAGE | SELECT | UPDATE }
    [, ...] | ALL [ PRIVILEGES ] }
    ON SEQUENCES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { EXECUTE | ALL [ PRIVILEGES ] }
    ON FUNCTIONS
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]

GRANT { USAGE | ALL [ PRIVILEGES ] }
    ON TYPES
    TO { [ GROUP ] role_name | PUBLIC } [, ...] [ WITH GRANT OPTION ]
"""
from dataclasses import dataclass
import enum


class TableGrant(enum.Enum):
    select = 'SELECT'
    insert = 'INSERT'
    update = 'UPDATE'
    delete = 'DELETE'
    truncate = 'TRUNCATE'
    references = 'REFERENCES'
    trigger = 'TRIGGER'
    all = 'ALL'


class SequenceGrant(enum.Enum):
    usage = 'USAGE'
    select = 'SELECT'
    update = 'UPDATE'
    all = 'ALL'


class FunctionGrant(enum.Enum):
    execute = 'EXECUTE'
    all = 'ALL'


class TypeGrant(enum.Enum)
    usage = 'USAGE'
    all = 'ALL'


class GrantTypes(enum.Enum)
    table = 'TABLE'
    sequence = 'SEQUENCE'
    function = 'FUNCTION'
    type = 'TYPE'


@dataclass
class DefaultGrant:
