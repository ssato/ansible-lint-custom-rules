# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if tasks use with_* directives.
"""
import typing

import ansiblelint.rules

if typing.TYPE_CHECKING:
    from typing import Optional
    from ansiblelint.file_utils import Lintable


ID: str = 'loop_is_recommended'
DESC: str = """loop is recommended and use of with_* may be repalced with it.
See also:
https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html
"""


class LoopIsRecommendedRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if any tasks use with_* loop directive.
    """
    id: str = ID
    shortdesc: str = 'loop is recommended and with_* may be repalced with it'
    description: str = DESC
    severity: str = 'LOW'
    tags: typing.List[str] = [ID, 'readability', 'formatting']

    def matchtask(self, task: typing.Dict[str, typing.Any],
                  file: 'Optional[Lintable]' = None
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        with_st = [key for key in task if key.startswith('with_')]
        if with_st:
            return f'Use of with_* was found: { ", ".join(with_st) }'

        return False
