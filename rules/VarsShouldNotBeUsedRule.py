# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if vars and include_vars are used.
"""
import typing

try:
    from ansiblelint.rules import AnsibleLintRule
except ImportError:
    from ansiblelint import AnsibleLintRule


_RULE_ID: str = "Custom_2020_6"
_DESC: str = """vars and include_vars should not be used and replaced with
variables defined in inventory and related data instead."""


VARS_DIRECTIVES: typing.FrozenSet = frozenset(
    vdir + ':' for vdir in """
include_vars
vars
vars_files
""".split())


def vars_msg(line: str, directives=VARS_DIRECTIVES) -> str:
    """
    Make up the warning message.
    """
    return "{} are forbidden: {}".format(" and ".join(directives), line)


def test_vars_is_used(line: str, directives=VARS_DIRECTIVES
                      ) -> typing.Union[str, bool]:
    """
    .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
    """
    line = line.strip()

    if line and any(vdir in line for vdir in directives):
        return vars_msg(line, directives)

    return False


class VarsShouldNotBeUsedRule(AnsibleLintRule):
    """
    Rule class to test if vars directives are used.
    """
    id = _RULE_ID
    shortdesc = "vars and include_vars should not be used"
    description = _DESC
    severity = "LOW"
    tags = ["readability", "formatting"]
    version_added = "4.2.99"  # dummy

    def match(self, _file, line: str) -> typing.Union[str, bool]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
        """
        return test_vars_is_used(line)
