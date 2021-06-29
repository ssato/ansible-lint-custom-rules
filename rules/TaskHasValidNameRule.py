# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
r"""Lint rule class to test if tasks have valid names.
"""
import functools
import re
import typing
import warnings

import ansiblelint.utils
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from typing import Optional
    from ansiblelint.file_utils import Lintable


ID: str = 'task_has_valid_name'
C_NAME_RE: str = 'name'
DESC: str = r"""Rule to test if files are smalll enough.

- Options

  - ``name`` gives a valid task name pattern (regexp)

- Configuration

  .. code-block:: yaml

    rules:
        task_has_valid_name:
            name: ^\S+$
"""

VERBS: typing.List[str] = """\
ask be become begin call can come could do feel find ensure get give go have
hear help keep know leave let like live look make may mean might move need play
put run say see seem should show start take talk tell test think try turn use
want will work would\
""".split()

DEFAULT_NAME_RE: typing.Pattern = re.compile(
    r'(' + '|'.join(VERBS + [v.title() for v in VERBS]) + r')(\s+(\S+))+$',
    re.ASCII
)

_NAMELESS_TASKS: typing.FrozenSet[str] = frozenset("""
meta
debug
import_role
import_tasks
include_role
include_tasks
""".split())


def is_named_task(task: typing.Dict[str, typing.Any],
                  nameless_tasks: typing.FrozenSet[str] = _NAMELESS_TASKS
                  ) -> bool:
    """Test if given task should be named?
    """
    return task['action']['__ansible_module__'] not in nameless_tasks


class TaskHasValidNameRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if given task has a valid name satisfies the naming rule
    in the organization.
    """
    id = ID
    shortdesc = 'All tasks should be named correctly'
    description = DESC
    severity = 'MEDIUM'
    tags = [ID, 'task', 'readability', 'formatting']

    @functools.lru_cache()
    def valid_name_re(self) -> typing.Pattern:
        """A valid task name pattern.
        """
        pattern_s = self.get_config(C_NAME_RE)
        if pattern_s:
            try:
                return re.compile(pattern_s)
            except BaseException:  # pylint: disable=broad-except
                warnings.warn(f'Invalid pattern "{pattern_s}"')

        return DEFAULT_NAME_RE

    @functools.lru_cache()
    def is_invalid_task_name(self, name: str) -> bool:
        """
        Test if given task's name is invalid.
        """
        return self.valid_name_re().match(name) is None

    def matchtask(self, task: typing.Dict[str, typing.Any],
                  file: 'Optional[Lintable]' = None
                  ) -> typing.Union[bool, str]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtask
        """
        if is_named_task(task):
            name = task.get('name', False)
            if not name:
                return 'Task has no name: {}'.format(
                    ansiblelint.utils.task_to_str(task)
                )
            if self.is_invalid_task_name(name):
                return f"Invalid task name '{name}'"

        return False

# vim:sw=4:ts=4:et:
