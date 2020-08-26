# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if tasks use with_* directives.
"""
try:
    from ansiblelint.rules import AnsibleLintRule
except ImportError:
    from ansiblelint import AnsibleLintRule


_RULE_ID = "Custom_2020_5"
_DESC = """loop is recommended and use of with_* may be repalced with it.
See also:
https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html
"""


def with_directive_is_used(_self, _file, task):
    """
    .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
    """
    with_st = [key for key in task if key.startswith("with_")]
    if with_st:
        return "Use of {} was found".format(with_st)

    return False


class LoopIsRecommendedRule(AnsibleLintRule):
    """
    Rule class to test if any tasks use with_* loop directive.
    """
    id = _RULE_ID
    shortdesc = "loop is recommended and with_* may be repalced with it"
    description = _DESC
    severity = "LOW"
    tags = ["readability", "formatting"]
    version_added = "4.2.99"  # dummy

    matchtask = with_directive_is_used
