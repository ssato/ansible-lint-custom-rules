# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if playbook files have valid filenames.
"""
import functools
import pathlib
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

FILE_KINDS: typing.FrozenSet[str] = frozenset(
    'playbook meta tasks handlers role yaml'.split()
)


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

    @functools.lru_cache()
    def valid_name_re(self) -> typing.Pattern:
        """A valid file name regex pattern.
        """
        pattern_s = self.get_config(C_NAME_RE)
        if pattern_s:
            try:
                if self.get_config(C_UNICODE):
                    return re.compile(pattern_s)
                else:
                    return re.compile(pattern_s, re.ASCII)
            except BaseException:  # pylint: disable=broad-except
                warnings.warn(f'Invalid pattern? "{pattern_s}"')

        return DEFAULT_NAME_RE

    @functools.lru_cache()
    def is_valid_filename(self, path: str) -> bool:
        """
        Test if given `filename` is valid and satisfies the rule.
        """
        return self.valid_name_re().match(pathlib.Path(path).name) is not None

    def matchyaml(self, file: ansiblelint.file_utils.Lintable
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
        """
        if file.kind in FILE_KINDS:
            path = str(file.path)
            if not self.is_valid_filename(path):
                return [
                    self.create_matcherror(message=f'{self.shortdesc}: {path}',
                                           filename=file.filename)
                ]

        return []
