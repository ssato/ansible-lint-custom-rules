# Copyright (C) 2022 Guido Grazioli <guido.grazioli@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if all role arguments are named after the role.
"""
import typing
import yaml

import ansiblelint.rules

from yaml.composer import Composer
from yaml.constructor import Constructor
from yaml.nodes import ScalarNode
from yaml.resolver import BaseResolver
from yaml.loader import SafeLoader

from pathlib import Path
from ansiblelint.utils import parse_yaml_from_file, LINE_NUMBER_KEY

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable


ID: str = 'role_vars_start_with_role_name'
SHORTDESC: str = 'All role parameters must be named ^<role_name>_.*'
DESC: str = r"""Rule to test if all role arguments have a name starting with the role name.

- Notes

  - Argument files = roles/**/{vars,defaults}/**/*.ya?ml
  - .. seealso:: ansiblelint.config.DEFAULT_KINDS

- Configuration

  .. code-block:: yaml

    rules:
      role_vars_start_with_role_name:
"""

ROLENAME_SEP: str = '_'


def _determine_role_name(var_file: Path) -> str:
    """
    Lookup role name from directory or galaxy_info.
    """
    if var_file.is_file():
        role_path: Path = var_file.parent / ".."
        name = str(role_path.resolve().name)
        meta_path: Path = role_path / 'meta' / 'main.yml'
        if (meta_path.is_file()):
            with open(str(meta_path), 'r') as f:
                meta = yaml.load(f, Loader=SafeLoader)
                try:
                    role_name = meta['galaxy_info']['role_name']
                    name = role_name
                except BaseException:
                    pass

    return name


class LineLoader(SafeLoader):
    """
    Custom LineLoader which return line number for all variables
    (not just parsed nodes).
    """
    def __init__(self, stream):
        super(LineLoader, self).__init__(stream)

    def compose_node(self, parent, index):
        # the line number where the previous token has ended (plus empty lines)
        line = self.line
        node = Composer.compose_node(self, parent, index)
        node.__line__ = line + 1
        return node

    def construct_mapping(self, node, deep=False):
        node_pair_lst = node.value
        node_pair_lst_for_appending = []

        for key_node, value_node in node_pair_lst:
            shadow_key_node = ScalarNode(tag=BaseResolver.DEFAULT_SCALAR_TAG, value=LINE_NUMBER_KEY + key_node.value)
            shadow_value_node = ScalarNode(tag=BaseResolver.DEFAULT_SCALAR_TAG, value=key_node.__line__)
            node_pair_lst_for_appending.append((shadow_key_node, shadow_value_node))

        node.value = node_pair_lst + node_pair_lst_for_appending
        mapping = Constructor.construct_mapping(self, node, deep=deep)
        return mapping


class RoleVarsStartWithRoleNameRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if all role parameters (defaults, vars) have 
    a name starting with "<role_name>_".
    """
    id = ID
    shortdesc = SHORTDESC
    description = DESC
    severity = 'HIGH'
    tags = [ID,'metadata','readability']

    def matchyaml(self, file: 'Lintable') -> typing.List['MatchError']:
        """Return matches for variables defined in vars files with no specification."""
        results: List["MatchError"] = []

        if file.kind == 'vars':
            rolename = _determine_role_name(file.path)
            with open(str(file.path), 'r') as f:
                variables = yaml.load(f, Loader=LineLoader)
                for var_name in filter(lambda k: not k.startswith(LINE_NUMBER_KEY) and not isinstance(variables[k],dict), variables.keys()):
                    if not var_name.startswith(rolename+ROLENAME_SEP):
                        results.append(
                            self.create_matcherror(
                                details=f'{self.shortdesc}: {var_name}', filename=file, linenumber=variables[LINE_NUMBER_KEY+var_name]
                            )
                        )
        else:
            results.extend(super().matchyaml(file))
        return results
