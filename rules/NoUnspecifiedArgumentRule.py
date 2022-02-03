# Copyright (C) 2022 Guido Grazioli <guido.grazioli@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if all role arguments are specified in meta/argument_specs.yml
"""
import functools
import re
import typing
import warnings
import yaml

import ansiblelint.rules

from yaml.composer import Composer
from yaml.constructor import Constructor
from yaml.nodes import ScalarNode
from yaml.resolver import BaseResolver
from yaml.loader import SafeLoader

from pathlib import Path
from ansiblelint.utils import parse_yaml_linenumbers, parse_yaml_from_file, nested_items
from ansiblelint.utils import LINE_NUMBER_KEY

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable


ID: str = 'no_unspecified_argument'
SHORTDESC: str = 'All role parameters must have a specification'
DESC: str = r"""Rule to test if all role arguments are specified in meta/argument_specs.yml.

- Notes

  - Argument files = roles/**/{vars,defaults}/**/*.ya?ml
  - .. seealso:: ansiblelint.config.DEFAULT_KINDS

- Configuration

  .. code-block:: yaml

    rules:
      no_unspecified_argument:
"""

def _lookup_argument_specs(var_file: Path, var_name: str) -> bool:
    """
    Find arg specification and lookup variable name is present.
    """
    meta_data: Dict[str, Any] = {}

    if var_file.is_file():
        argument_specs_path: Path = var_file.parent / ".." / "meta" / "argument_specs.yml"
        argument_specs = str(argument_specs_path)

    if argument_specs_path.is_file() and not argument_specs in meta_data.keys():
        meta_data[argument_specs] = parse_yaml_from_file(argument_specs)

    if argument_specs in meta_data.keys():
        try:
            if meta_data[argument_specs]["argument_specs"]["main"]["options"]:
                return var_name in meta_data[argument_specs]["argument_specs"]["main"]["options"]
        except KeyError:
            return False

    return False


class LineLoader(SafeLoader):
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
            shadow_key_node = ScalarNode(tag=BaseResolver.DEFAULT_SCALAR_TAG, value='__line__' + key_node.value)
            shadow_value_node = ScalarNode(tag=BaseResolver.DEFAULT_SCALAR_TAG, value=key_node.__line__)
            node_pair_lst_for_appending.append((shadow_key_node, shadow_value_node))

        node.value = node_pair_lst + node_pair_lst_for_appending
        mapping = Constructor.construct_mapping(self, node, deep=deep)
        return mapping


class NoUnspecifiedArgumentRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if all role parameters (defaults, vars) have 
    a format specification in meta/argument_specs.yml.
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
            with open(str(file.path), 'r') as f:
                variables = yaml.load(f, Loader=LineLoader)
                for var_name in filter(lambda k: not k.startswith('__line__') and not isinstance(variables[k],dict), variables.keys()):
                    if not _lookup_argument_specs(file.path, var_name):
                        results.append(
                            self.create_matcherror(
                                details=f'{self.shortdesc}: {var_name}', filename=file, linenumber=variables["__line__"+var_name]
                            )
                        )
        else:
            results.extend(super().matchyaml(file))
        return results
