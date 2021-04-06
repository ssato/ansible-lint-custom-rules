# Copyright (C) 2020,2021 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if tasks use with_* directives.
"""
import typing

from ansiblelint.rules import AnsibleLintRule


_RULE_ID: str = 'loop-is-recommended'
_DESC: str = """loop is recommended and use of with_* may be repalced with it.
See also:
https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html
"""


def is_directive_used(_self, task: typing.Dict[str, typing.Any],
                      ) -> typing.Union[bool, str]:
    """
    .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
    """
    with_st = [key for key in task if key.startswith('with_')]
    if with_st:
        return f'Use of with_* was found: { ", ".join(with_st) }'

    return False


class LoopIsRecommendedRule(AnsibleLintRule):
    """
    Rule class to test if any tasks use with_* loop directive.
    """
    id: str = _RULE_ID
    shortdesc: str = 'loop is recommended and with_* may be repalced with it'
    description: str = _DESC
    severity: str = 'LOW'
    tags: typing.List[str] = ['readability', 'formatting']

    matchtask = is_directive_used
