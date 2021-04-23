# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
#
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""
Lint rule class to test if some blocked modules were used.
"""
import typing
import warnings

import ansiblelint.rules

from ansiblelint.config import options as OPTIONS


ID: str = 'blocked_modules'
C_BLOCKED_MODULES: str = 'blocked'

DESC: str = """Rule to test if some blocked modules were used in tasks.

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

BLOCKED_MODULES: typing.List[str] = """
shell
include
""".split()


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

    initialized: bool = False
    _blocked: typing.FrozenSet[str] = frozenset(BLOCKED_MODULES)

    def blocked_modules(self):
        """
        .. seealso:: rules.DebugRule.DebugRule.enabled
        """
        if self.initialized:
            return self._blocked

        config = getattr(OPTIONS, 'rules', {}).get(self.id, {})
        try:
            _blocked = config.get(C_BLOCKED_MODULES, BLOCKED_MODULES)
            self._blocked = _blocked
        except (TypeError, ValueError):
            warnings.warn(f'Invalid value for frozenset: {_blocked!r}')

        self.initialized = True

        return self._blocked

    def matchtask(self, task: typing.Dict[str, typing.Any]
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
