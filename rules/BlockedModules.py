# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
#
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""
Lint rule class to test if some blocked modules were used.
"""
import functools
import typing

import ansiblelint.rules

if typing.TYPE_CHECKING:
    from typing import Optional
    from ansiblelint.file_utils import Lintable


ID: str = 'blocked_modules'
C_BLOCKED_MODULES: str = 'blocked'

DESC: str = """Rule to check if some blocked modules were used in tasks.

- Options

  - ``blocked`` lists the modules blocked to use

- Configuration

  .. code-block:: yaml

  rules:
    blocked_modules:
      blocked:
        - shell
        - include

.. seealso:: :class:`~ansiblielint.rules.DeprecatedModuleRule`
"""

BLOCKED_MODULES: typing.FrozenSet[str] = frozenset("""
shell
include
""".split())


class BlockedModules(ansiblelint.rules.AnsibleLintRule):
    """
    Lint rule class to test if variables defined by users follow the namging
    conventions and guildelines.
    """
    id: str = ID
    shortdesc: str = 'Blocked modules'
    description: str = DESC
    severity: str = 'HIGH'
    tags: typing.List[str] = [ID, 'module']

    @functools.lru_cache()
    def blocked_modules(self):
        """
        .. seealso:: rules.DebugRule.DebugRule.enabled
        """
        blocked = self.get_config(C_BLOCKED_MODULES)
        if blocked:
            return frozenset(blocked)

        return BLOCKED_MODULES

    def matchtask(self, task: typing.Dict[str, typing.Any],
                  file: 'Optional[Lintable]' = None
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        try:
            mod = task['action']['__ansible_module__']
            if mod in self.blocked_modules():
                return f'{self.shortdesc}: {mod}'
        except KeyError:
            pass

        return False

# vim:sw=4:ts=4:et:
