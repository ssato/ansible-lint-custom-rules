# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if tasks files have valid filenames.
"""
import functools
import pathlib
import re
import typing
import warnings

import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict


ID: str = 'tasks_file_has_valid_name'
DESC: str = r"""Rule to test if file defines tasks has valid filename.

- Options

  - ``name`` gives a valid task filename pattern (regexp)
  - ``unicode`` allows unicode characters are used in filenames

- Configuration

  .. code-block:: yaml

    rules:
      tasks_file_has_valid_name:
        name: ^\w+\.ya?ml$
        unicode: false
"""
C_NAME_RE: str = 'name'
C_UNICODE: str = 'unicode'

DEFAULT_NAME_RE: typing.Pattern = re.compile(r'^\w+\.ya?ml$', re.ASCII)


class TasksFileHasValidNameRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if tasks file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = ID
    shortdesc: str = 'Tasks file must have valid filename'
    description = DESC
    severity = 'HIGH'
    tags = [ID, 'task']

    @functools.lru_cache()
    def valid_name_re(self) -> typing.Pattern:
        """A valid task name pattern.
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
    def is_valid_filename(self, path: str) -> bool:
        """
        Test if given task's filename is valid.
        """
        return self.valid_name_re().match(pathlib.Path(path).name) is not None

    def matchplay(self, file: ansiblelint.file_utils.Lintable,
                  _data: 'odict[str, typing.Any]'
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:; ansiblelint.rules.AnsibleLintRule.matchplay
        """
        if file.kind == 'tasks':
            path = str(file.path)
            if not self.is_valid_filename(path):
                return [
                    self.create_matcherror(message=f'{self.shortdesc}: {path}',
                                           filename=file.name)
                ]

        return []
