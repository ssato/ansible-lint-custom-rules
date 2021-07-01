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

import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.rules

# .. seealso: [options] section in setup.cfg
from ansiblelint.rules.custom.ssato import _utils


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

    @functools.lru_cache(None)
    def valid_name_re(self) -> typing.Pattern:
        """A valid file name regex pattern.
        """
        return _utils.make_valid_name_pattern_from_rule_config(
            self, DEFAULT_NAME_RE
        )

    def is_valid_filename(self, path: str) -> bool:
        """
        Test if given `filename` is valid and satisfies the rule.
        """
        return _utils.is_valid_name(
            self.valid_name_re(), pathlib.Path(path).name
        )

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
