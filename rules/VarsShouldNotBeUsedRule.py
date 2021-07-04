# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if vars and include_vars are used.
"""
import functools
import re
import typing
import warnings

import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.rules


ID: str = "vars_should_not_be_used"

VARS_DIRECTIVES: typing.FrozenSet = frozenset("""
include_vars
vars
vars_files
""".split())

VARS_RE: typing.Pattern = re.compile(
    r'^(\s+)?(-\s+)?('
    f"{'|'.join(VARS_DIRECTIVES)}"
    r'):', re.ASCII
)


KINDS: typing.FrozenSet[str] = frozenset(
    'playbook tasks role'.split()
)


@functools.lru_cache()
def contains_vars_directive(path: str) -> bool:
    """
    Test if file of given path contains vars directives in it.
    """
    try:
        with open(path) as fobj:
            for line in fobj:
                if VARS_RE.match(line):
                    return True
    except (IOError, OSError) as exc:
        warnings.warn(f'Failed to load {path}, exc={exc!r}')

    return False


class VarsShouldNotBeUsedRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if vars directives are used.
    """
    id: str = ID
    shortdesc: str = 'vars should not be used'
    description: str = ('vars and include_vars should not be used and '
                        'replaced with variables defined in inventory '
                        'and related data instead.')
    severity = 'LOW'
    tags = [ID, 'readability', 'formatting']

    def matchyaml(self, file: ansiblelint.file_utils.Lintable
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """Test playbook files.
        """
        if file.kind in KINDS:
            path = str(file.path)
            if contains_vars_directive(path):
                return [
                    self.create_matcherror(message=f'{self.shortdesc}: {path}')
                ]

        return []

# vim:sw=4:ts=4:et:
