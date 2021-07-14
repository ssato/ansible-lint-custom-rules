# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if variables in vars files have valid names.
"""
import functools
import re
import typing
import warnings

import ansiblelint.rules
import ansiblelint.utils

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable


ID: str = 'vars_in_vars_files_have_valid_names'
DESC: str = r"""Rule to test if variables in vars files have valid names.

- Notes

  - Variables files = {host_vars,group_vars,vars,defaults}/**/*.ya?ml
  - .. seealso:: ansiblelint.config.DEFAULT_KINDS

- Options

  - ``name`` gives a valid task filename pattern (regexp)
  - ``unicode`` allows unicode characters are used in filenames

- Configuration

  .. code-block:: yaml

    rules:
      tasks_file_has_valid_name:
        name: ^\w+$
        unicode: false
"""
C_NAME_RE: str = 'name'
C_UNICODE: str = 'unicode'

DEFAULT_NAME_RE: typing.Pattern = re.compile(r'^\w+$', re.ASCII)


def each_keys(data: 'odict[str, typing.Any]') -> typing.Iterator[str]:
    """
    Traverse nested dict and yield keys.
    """
    for key, _val, _parent in ansiblelint.utils.nested_items(data):
        # Special case.
        # .. seealso:: ansiblelint.utils.nested_items
        if key == 'list-item':
            continue

        yield key


class VarsInVarsFilesHaveValidNamesRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if variables defined in vars files (host_vars,
    group_vars, defaults, vars) have valid names follows the naming rules.
    """
    id = ID
    shortdesc: str = 'Variable in vars files must have valid name'
    description = DESC
    severity = 'HIGH'
    tags = ['idiom']

    @functools.lru_cache(None)
    def valid_name_re(self) -> typing.Pattern:
        """A valid variable name pattern.
        """
        pattern_s = self.get_config(C_NAME_RE)
        if pattern_s:
            try:
                if self.get_config(C_UNICODE):
                    return re.compile(pattern_s)

                return re.compile(pattern_s, re.ASCII)
            except BaseException:  # pylint: disable=broad-except
                warnings.warn(f'Invalid pattern "{pattern_s}"')

        return DEFAULT_NAME_RE

    @functools.lru_cache()
    def is_invalid_name(self, var_name: str) -> bool:
        """
        True if given variable name is NOT valid.
        """
        return self.valid_name_re().match(var_name) is None

    def matchplay(self, file: 'Lintable',
                  data: 'odict[str, typing.Any]'
                  ) -> typing.List['MatchError']:
        """
        .. seealso:; ansiblelint.rules.AnsibleLintRule.matchplay
        """
        if file.kind == 'vars':
            return [
                self.create_matcherror(
                    details=f'{self.shortdesc}: {var_name}', filename=file
                )
                for var_name in each_keys(data)
                if self.is_invalid_name(var_name)
            ]

        return []
