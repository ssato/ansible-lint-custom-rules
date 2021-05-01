# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
""" Lint rule class to Debug
"""
import typing

import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from typing import Optional
    from ansiblelint.constants import odict
    from ansiblelint.file_utils import Lintable


ID: str = 'debug'
C_ENABLED: str = 'enabled'

DESC: str = """Rule to debug and monitor ansible-lint behavior.

- Options

  - ``enabled`` enables this rule disabled by default.

- Configuration

  .. code-block:: yaml

  rules:
    debug:
      enabled: true
"""


class DebugRule(ansiblelint.rules.AnsibleLintRule):
    """
    Lint rule class for debug.
    """
    id = ID
    shortdesc = 'Debug ansible-lint'
    description = DESC
    severity = 'LOW'
    tags = ['debug']

    @property
    def enabled(self):
        """
        .. seealso:: ansiblelint.config.options
        .. seealso:: ansiblelint.cli.load_config
        """
        return self.get_config(C_ENABLED)

    def match(self, line: str) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
        """
        return f'match() at: {line}' if self.enabled else False

    def matchtask(self, task: typing.Dict[str, typing.Any],
                  file: 'Optional[Lintable]' = None
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        return f'matchtask(): {task!r}, {file!r}' if self.enabled else False

    def matchplay(self, file: ansiblelint.file_utils.Lintable,
                  data: 'odict[str, typing.Any]'
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        if self.enabled:
            msg = f'matchplay(): {file!r}, {data!r}'
            return [self.create_matcherror(message=msg, filename=file.name)]

        return []
