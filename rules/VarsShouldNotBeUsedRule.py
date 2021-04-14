# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if vars and include_vars are used.
"""
import typing

import ansiblelint.errors
import ansiblelint.rules


ID: str = "vars-should-not-be-used"

VARS_DIRECTIVES: typing.FrozenSet = frozenset(
    vdir + ':' for vdir in """
include_vars
vars
vars_files
""".split())


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

    def match(self, line: str) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
        """
        directives = VARS_DIRECTIVES
        line = line.strip()

        if line and any(vdir in line for vdir in directives):
            return [
                self.create_matcherror(message=f'{self.shortdesc}: {line}')
            ]

        return []
