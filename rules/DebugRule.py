# Copyright (C) 2020,2021 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class for debug use.
"""
import functools
import os
import typing

# https://www.python.org/dev/peps/pep-0484/#runtime-or-type-checking
if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable

from ansiblelint.rules import AnsibleLintRule


_RULE_ID: str = 'debug-rule'
_DESC: str = 'Custom rule class for debug use'

_EVAR_PREFIX: str = '_ANSIBLE_LINT_RULE_' + _RULE_ID.upper().replace('-', '_')
ENABLE_THIS_RULE_ENVVAR: str = _EVAR_PREFIX + '_DEBUG'

Matched = typing.NamedTuple('Matched',
                            (('lines', typing.Set[str]),
                             ('tasks', typing.Set[str]),
                             ('plays', typing.Set[str])))


@functools.lru_cache(maxsize=64)
def is_enabled(default: bool = False) -> bool:
    """
    Is this rule enabled with the environment variable?
    """
    return bool(os.environ.get(ENABLE_THIS_RULE_ENVVAR, default))


class Cache(typing.NamedTuple):
    """Class that tracks cachees of tasks, plays and so on."""
    tasks: typing.Set[str]
    plays: typing.Set[str]
    yamls: typing.Set[str]


class DebugRule(AnsibleLintRule):
    """Rule class for debug use.
    """
    id: str = _RULE_ID
    tags: typing.List[str] = ['debug']
    shortdesc = description = _DESC
    severity: str = 'LOW'

    cache = Cache(tasks=set(), plays=set(), yamls=set())

    def matchtask(self, task: typing.Dict[str, typing.Any]
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtask
        """
        if is_enabled():
            name = task.get('name', str(task))
            if name not in self.cache.tasks:
                self.cache.tasks.add(name)
                return f'task: {task!r}'

        return False

    def matchplay(self, file: 'Lintable', data: 'odict[str, typing.Any]'
                  ) -> typing.List['MatchError']:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchplay
        """
        if is_enabled() and file.kind == 'playbook':
            name = data.get('name', str(data))
            if name in self.cache.plays:
                return []

            self.cache.plays.add(name)
            res = [self.create_matcherror(message=f'play #{i + 1}',
                                          filename=str(file.path))
                   for i, play in data.get('block', [data])]
            return res

        return []

    def matchyaml(self, file: 'Lintable') -> typing.List['MatchError']:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
        """
        if is_enabled():
            path = str(file.path)
            if path in self.cache.yamls:
                return []

            return [self.create_matcherror(message=f'yaml: {path}',
                                           filename=path)]

        return []
