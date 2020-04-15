from sqlalchemy_declarative_database.role.base import Role
from typing import List


def topological_sort(roles: List[Role]):
    """Sort roles in an order that guarantees success based on role dependence.

    Uses Kahn's algorithm.
    """
    role_name_map = {}
    for role in roles:
        if role.name in role_name_map:
            raise ValueError(f"Duplicate role specified: {role}")
        role_name_map[role.name] = role

    role_dep_map = {}
    valid_role_names = set(role_name_map)
    for name, role in role_name_map.items():
        roles = set((role.in_roles or []) + (role.roles or []) + (role.admins or []))

        if not roles.issubset(valid_role_names):
            missing_roles = ", ".join(sorted(roles - valid_role_names))
            raise ValueError(
                "The following roles are specified as dependencies of other top-level roles, "
                f"but are missing in the list of top-level roles: {missing_roles}."
            )
        role_dep_map[name] = roles

    fullfilled_role_names = set(role for role, deps in role_dep_map.items() if not deps)
    for role in fullfilled_role_names:
        role_dep_map.pop(role)

    result = []
    while fullfilled_role_names:
        fullfilled_role_name = fullfilled_role_names.pop()
        result.append(role_name_map[fullfilled_role_name])

        # Remove fullfilled role from deps of all other roles which might depend on it.
        for deps in role_dep_map.values():
            if fullfilled_role_name in deps:
                deps.remove(fullfilled_role_name)

        newly_fullfilled_roles = set(
            role for role, deps in role_dep_map.items() if not deps
        )

        fullfilled_role_names |= newly_fullfilled_roles
        for role in newly_fullfilled_roles:
            role_dep_map.pop(role)

    if any(role_dep_map):
        cyclical_roles = ", ".join(sorted(role_dep_map.keys()))
        raise ValueError(
            f"The following roles have cyclical dependencies: {cyclical_roles}"
        )

    return result
