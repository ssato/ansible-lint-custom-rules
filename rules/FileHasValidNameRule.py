# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if playbook files have valid filenames.
"""
import functools
import os
import pathlib
import re
import typing

import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.rules


ID: str = 'file-has-valid-name'
ENV_VAR = f"_ANSIBLE_LINT_RULE_{ID.upper().replace('-', '_')}_NAME_RE"

VALID_EVALUE: typing.Pattern = re.compile(r'^\S+$', re.ASCII)
DEFAULT_NAME_RE: str = r'^\w+\.ya?ml$'


@functools.lru_cache()
def filename_re() -> typing.Pattern:
    """
    Filename Regex.
    """
    pattern = os.environ.get(ENV_VAR, False)
    if pattern and VALID_EVALUE.match(pattern):
        return re.compile(pattern, re.ASCII)

    return re.compile(DEFAULT_NAME_RE, re.ASCII)


def is_valid_filename(path: str,
                      pattern: typing.Optional[typing.Pattern] = None) -> bool:
    """
    :return: True if given `filename` is invalid and does not satisfy the rule
    """
    if pattern is None or not pattern:
        pattern = filename_re()

    return pattern.match(pathlib.Path(path).name) is not None


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
    description = shortdesc
    severity = 'MEDIUM'
    tags = [ID, 'playbook', 'readability', 'formatting']

    def __init__(self):
        """initialize this.
        """
        self.done: typing.Set[str] = set()

    def matchyaml(self, file: ansiblelint.file_utils.Lintable
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
        """
        if file.kind in FILE_KINDS:
            path = str(file.path)
            if path in self.done:
                return []

            self.done.add(path)
            if not is_valid_filename(path):
                return [
                    self.create_matcherror(message=f'{self.shortdesc}: {path}',
                                           filename=file.filename)
                ]

        return []
