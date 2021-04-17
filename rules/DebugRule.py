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

from ansiblelint.config import options as OPTIONS

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict


ID: str = 'debug'
C_ENABLED: str = 'enabled'

DESC: str = f"""Rule to debug and monitor ansible-lint behavior.

- Options

  - ``{C_ENABLED}`` enables this rule disabled by default.

- Configuration

  .. code-block:: yaml

  rules:
    {ID}:
      {C_ENABLED}: true
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

    initialized = False
    _enabled = False

    def enabled(self):
        """
        .. seealso:: ansiblelint.config.options
        .. seealso:: ansiblelint.cli.load_config
        """
        if self.initialized:
            return self._enabled

        config = getattr(OPTIONS, 'rules', {}).get(self.id, {})
        self._enabled = config.get(C_ENABLED, False)
        self.initialized = True

        return self._enabled

    def match(self, line: str) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines
        """
        return f'match() at: {line}' if self.enabled() else False

    def matchtask(self, task: typing.Dict[str, typing.Any]
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        return f'matchtask(): {task!r}' if self.enabled() else False

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
