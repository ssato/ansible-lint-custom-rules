# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
#
# SPDX-License-Identifier: MIT
#
r"""
Lint rule class to test if some blocked modules were used.

Users can change the behavior of this rule by specifying a environment
variable, _ANSIBLE_LINT_RULE_BLOCKED_MODULES.

- An example to list blocked modules with the env. variable.

  ::

      _ANSIBLE_LINT_RULE_BLOCKED_MODULES="shell raw"

- An example to list blocked modules with the file given in the env. variable.

  ::

      _ANSIBLE_LINT_RULE_BLOCKED_MODULES="@/tmp/mb.list"

  The file must contain module names to be blockeded line by line, and comments
  in the file starts with '#' are ignored like this:

  ::

     # this is a comment line.
     shell
     include

.. seealso:: :class:`~ansiblielint.rules.DeprecatedModuleRule`
"""
import functools
import os
import re
import typing
import warnings

import ansiblelint.rules


ID: str = 'blockeded-modules'
ENV_VAR = '_ANSIBLE_LINT_RULE_' + ID.upper().replace('-', '_')

BLOCKED_MODULES: typing.FrozenSet[str] = frozenset("""
shell
include
""".split())

MODULES_RE = re.compile(r'^(\w+(?:\s+\w+)*)$', re.ASCII)


@functools.lru_cache()
def blocked_modules(default: typing.FrozenSet[str] = BLOCKED_MODULES
                    ) -> typing.FrozenSet[str]:
    """
    Get and return the blocked modules from the env. var, file or default.
    """
    blocked = os.environ.get(ENV_VAR, False)
    if blocked:
        if blocked.startswith('@'):  # It's a file path.
            path = blocked[1:]
            try:
                res = frozenset(line.strip() for line in open(path)
                                if line.strip() and not line.startswith('#'))
                if res:
                    return res
            except (IOError, OSError) as exc:
                warnings.warn('Failed to load blocked modules from '
                              f'{path}, exc={exc!s}')
        else:
            match = MODULES_RE.match(blocked)
            if match:
                return frozenset(match.groups()[0].split())

    return default


class BlockedModules(ansiblelint.rules.AnsibleLintRule):
    """
    Lint rule class to test if variables defined by users follow the namging
    conventions and guildelines.
    """
    id: str = ID
    shortdesc: str = 'Blocked modules'
    description: str = 'Use of the blockeded modules are prohivited.'
    severity: str = 'HIGH'
    tags: typing.List[str] = [ID, 'module']

    def matchtask(self, task: typing.Dict[str, typing.Any]
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks
        """
        try:
            mod = task['action']['__ansible_module__']
            if mod in blocked_modules():
                return f'{self.shortdesc}: {mod}'
        except KeyError:
            pass

        return False

# vim:sw=4:ts=4:et:
