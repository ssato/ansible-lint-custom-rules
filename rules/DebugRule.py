# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
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
    from typing import Optional
    from ansiblelint.constants import odict
    from ansiblelint.file_utils import Lintable


ID: str = 'debug'
E_ENABLED_VAR: str = '_ANSIBLE_LINT_RULE_DEBUG'
C_ENABLED: str = 'enabled'

DESC: str = """Rule to debug and monitor ansible-lint behavior.

- Options

  - ``enabled`` enables this rule disabled by default.

- Configuration

  .. code-block:: yaml

  rules:
    debug:
      enabled: true

- Environment variables

  - Set ``_ANSIBLE_LINT_RULE_DEBUG`` to any value evaluated to true like 1,
    '0', 'foo', if you want to enable this rule. The value to enable this rule
    will be given higher priority than the above configuration value.
"""


def is_enabled(default: bool = False) -> bool:
    """
    Is this rule enabled with the environment variable?
    """
    return bool(os.environ.get(E_ENABLED_VAR, default))


class DebugRule(ansiblelint.rules.AnsibleLintRule):
    """
    Lint rule class for debug.
    """
    id = ID
    shortdesc = 'Debug ansible-lint'
    description = DESC
    severity = 'LOW'
    tags = ['debug']

    @functools.lru_cache(None)
    def enabled(self):
        """
        .. seealso:: ansiblelint.config.options
        .. seealso:: ansiblelint.cli.load_config
        """
        if is_enabled():
            return True  # Gives higher prio. to the environment variable.

        return bool(self.get_config(C_ENABLED))

    def match(self, line: str) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
        """
        return f'match() at: {line}' if self.enabled() else False

    def matchtask(self, task: typing.Dict[str, typing.Any],
                  file: 'Optional[Lintable]' = None
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        return f'matchtask(): {task!r}, {file!r}' if self.enabled() else False

    def matchplay(self, file: ansiblelint.file_utils.Lintable,
                  data: 'odict[str, typing.Any]'
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        if self.enabled():
            msg = f'matchplay(): {file!r}, {data!r}'
            return [self.create_matcherror(message=msg, filename=file.name)]

        return []
