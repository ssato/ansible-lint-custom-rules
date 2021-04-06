# Copyright (C) 2020,2021 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if vars and include_vars are used.
"""
import typing

if typing.TYPE_CHECKING:
    from ansiblelint.errors import MatchError

from ansiblelint.rules import AnsibleLintRule


ID: str = "vars-is-in-use"
_DESC: str = """vars and include_vars should not be used and replaced with
variables defined in inventory and related data instead."""


VARS_DIRECTIVES: typing.FrozenSet = frozenset(
    vdir + ':' for vdir in """
include_vars
vars
vars_files
""".split())


class VarsShouldNotBeUsedRule(AnsibleLintRule):
    """
    Rule class to test if vars directives are used.
    """
    id = ID
    shortdesc = 'vars and include_vars should not be used'
    description = _DESC
    severity = 'LOW'
    tags = ['readability', 'formatting']

    def match(self, line: str) -> typing.List['MatchError']:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
        """
        directives = VARS_DIRECTIVES
        line = line.strip()

        if line and any(vdir in line for vdir in directives):
            return [self.create_matcherror(
                message='{} are forbidden: {}'.format(' and '.join(directives),
                                                      line)
            )]

        return []
