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

import ansiblelint.rules

from pathlib import Path
from ansiblelint.utils import parse_yaml_from_file, nested_items


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
    if var_file.is_file():
        argument_specs: Path = var_file.parent / ".." / "meta" / "argument_specs.yml"
    print('lookup var_name = %s' % var_name )
    if argument_specs.is_file():
        meta_data = parse_yaml_from_file(str(argument_specs))
        print(meta_data)
        if meta_data:
            try:
            	if meta_data["argument_specs"]["main"]["options"]:
                    return var_name in meta_data["argument_specs"]["main"]["options"]
            except KeyError:
                return False
    return False


def each_keys(data: 'odict[str, typing.Any]') -> typing.Iterator[str]:
    """
    Traverse nested dict and yield keys. 
    todo: nested_items is deprecated
    """
    for key, _val, _parent in nested_items(data):
        # Special cases.
        # .. seealso:: ansiblelint.utils.nested_items
        if key in ['list-item', '__line__', '__file__']:
            continue

        if isinstance(_val, dict) or _parent:
            continue

        print("==== key: %s  ==== val: %s  ==== par: %s" % (key, _val, _parent))
        yield key, _parent+'.' if _parent else ''


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

    def matchplay(self, file: 'Lintable',
                  data: 'odict[str, typing.Any]'
                  ) -> typing.List['MatchError']:
        """
        .. seealso:; ansiblelint.rules.AnsibleLintRule.matchplay
        """
        if file.kind == 'vars':
            print('data: %s' % data)
            return [
                self.create_matcherror(
                    details=f'{self.shortdesc}: {parent}{var_name}', filename=file
                )
                for var_name, parent in each_keys(data)
                if not _lookup_argument_specs(file.path, var_name)
            ]

        return []
