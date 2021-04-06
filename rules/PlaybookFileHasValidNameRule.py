# Copyright (C) 2020,2021 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if playbook files have valid filenames.
"""
import functools
import os
import re
import typing

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable

from ansiblelint.rules import AnsibleLintRule


ID: str = 'playbook-has-valid-name'
_ENVVAR_PREFIX: str = '_ANSIBLE_LINT_RULE_' + ID.upper().replace('-', '_')

FILENAME_ENVVAR: str = _ENVVAR_PREFIX + '_PLAYBOOK_FILENAME_RE'
DEFAULT_FILENAME_RE: str = r'^\w+\.ya?ml$'


@functools.lru_cache(maxsize=32)
def filename_re() -> typing.Pattern:
    """
    :return: regexp object to try match
    """
    return re.compile(os.environ.get(FILENAME_ENVVAR, DEFAULT_FILENAME_RE),
                      re.ASCII)


def is_invalid_filename(filepath: str,
                        regex: typing.Optional[typing.Pattern] = None) -> bool:
    """
    :return: True if given `filename` is invalid and does not satisfy the rule
    """
    if regex is None:
        regex = filename_re()

    return regex.match(os.path.basename(filepath)) is None


class PlaybookFileHasValidNameRule(AnsibleLintRule):
    """
    Rule class to test if playbook file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = ID
    shortdesc = 'Playbook files should have valid filenames'
    description = shortdesc
    severity = 'MEDIUM'
    tags = ['playbook', 'readability', 'formatting']

    def matchplay(self, file: 'Lintable', data: 'odict[str, typing.Any]'
                  ) -> typing.List['MatchError']:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchplay
        """
        if file.kind == 'playbook':
            playbook = file.path

            if is_invalid_filename(playbook):
                return [self.create_matcherror(
                            message=f'{playbook!s} may have invalid filename',
                            filename=file.filename
                        )]

        return []
