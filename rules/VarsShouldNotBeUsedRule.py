# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if vars and include_vars are used.
"""
import ansiblelint.rules


_RULE_ID = "Custom_2020_6"
_DESC = """vars and include_vars should not be used and replaced with
variables defined in inventory and related data instead."""


def vars_is_used(_self, _file, line):
    """
    .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
    """
    line_s = line.strip()
    if line_s and "vars:" in line_s or "include_vars:" in line_s:
        return "vars or include_vars was used: {}".format(line_s)

    return False


class VarsShouldNotBeUsedRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if any tasks use with_* loop directive.
    """
    id = _RULE_ID
    shortdesc = "vars and include_vars should not be used"
    description = _DESC
    severity = "LOW"
    tags = ["readability", "formatting"]
    version_added = "4.2.99"  # dummy

    match = vars_is_used
