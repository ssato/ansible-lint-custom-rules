# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if playbook files have valid filenames.
"""
import functools
import re
import typing
import warnings

import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.rules


ID: str = 'file_has_valid_name'
DESC = r"""Rule to check if file has a valid name.

- Options

  - ``name`` lists the modules blocked to use
  - ``unicode`` allows unicode characters are used in filenames

- Configuration

  .. code-block:: yaml

  rules:
    file_has_valid_name:
        name: ^\w+\.ya?ml$
        unicode: false
"""

C_NAME_RE: str = 'name'
C_UNICODE: str = 'unicode'

DEFAULT_NAME_RE: typing.Pattern = re.compile(r'^\w+\.ya?ml$', re.ASCII)

FILE_KINDS: typing.FrozenSet[str] = frozenset((
    'playbook',
    'meta',
    'tasks',
    'handlers',
    'role',
    'yaml'
))


class FileHasValidNameRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if playbook file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = ID
    shortdesc = 'Playbook and related files should have valid filenames'
    description = DESC
    severity = 'MEDIUM'
    tags = [ID, 'playbook', 'readability', 'formatting']

    @functools.lru_cache(None)
    def valid_name_re(self) -> typing.Pattern:
        """A valid file name regex pattern.
        """
        pattern = self.get_config(C_NAME_RE)
        if pattern is not None and pattern:
            pattern = str(pattern).strip()
            if pattern:
                try:
                    if self.get_config(C_UNICODE):
                        return re.compile(pattern)

                    return re.compile(pattern, re.ASCII)
                except BaseException:  # pylint: disable=broad-except
                    warnings.warn(f'Invalid pattern? "{pattern}"')

        return DEFAULT_NAME_RE

    def is_invalid_filename(self, filename: str) -> bool:
        """
        Test if given `filename` is NOT valid and does NOT satisfy the rule.
        """
        return self.valid_name_re().match(filename) is None

    def matchyaml(self, file: ansiblelint.file_utils.Lintable
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
        """
        if file.kind in FILE_KINDS:
            if self.is_invalid_filename(file.path.name):
                return [
                    self.create_matcherror(
                        filename=file,
                        message=f'{self.shortdesc}: {file.path.name}'
                    )
                ]

        return []
