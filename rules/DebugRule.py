# Copyright (C) 2021 Red Hat K.K.
#
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
""" Lint rule class to Debug
"""
import functools
import os
import typing

import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict


ID: str = 'debug'

ENABLE_THIS_RULE_ENVVAR = f'_ANSIBLE_LINT_RULE_{ID.upper()}'


@functools.lru_cache(maxsize=64)
def is_enabled(default: bool = False) -> bool:
    """
    Is this rule enabled with the environment variable?
    """
    return bool(os.environ.get(ENABLE_THIS_RULE_ENVVAR, default))


class DebugRule(ansiblelint.rules.AnsibleLintRule):
    """
    Lint rule class for debug.
    """
    id = ID
    shortdesc = description = 'Debug ansible-lint objects'
    severity = 'LOW'
    tags = ['debug']

    def match(self, line: str) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
        """
        return f'match() at: {line}' if is_enabled() else False

    def matchtask(self, task: typing.Dict[str, typing.Any]
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        return f'matchtask(): {task!r}' if is_enabled() else False

    def matchplay(self, file: ansiblelint.file_utils.Lintable,
                  data: 'odict[str, typing.Any]'
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        if is_enabled():
            msg = f'matchplay(): {file!r}, {data!r}'
            return [self.create_matcherror(message=msg, filename=file.name)]

        return []
