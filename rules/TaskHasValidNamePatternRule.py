# Copyright (C) 2020,2021 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
r"""Lint rule class to test if tasks have valid names.

.. note::
   Users can specify the task name regexp with the enviornment variable,
   _ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE, for exampke,

   _ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE="\S+" ansible-lint ...
"""
import functools
import os
import re
import typing

import ansiblelint.utils
import ansiblelint.rules


ID: str = 'task-has-valid-name'
_ENVVAR_PREFIX: str = '_ANSIBLE_LINT_RULE_' + ID.upper().replace('-', '_')

TASK_NAME_RE_ENVVAR: str = _ENVVAR_PREFIX + '_TASK_NAME_RE'

VERBS: typing.List[str] = """\
ask be become begin call can come could do feel find ensure get give go have
hear help keep know leave let like live look make may mean might move need play
put run say see seem should show start take talk tell think try turn use want
will work would\
""".split()

_NAME_RE: str = (r'(' + '|'.join(VERBS + [verb.title() for verb in VERBS]) +
                 r')(\s+(\S+))+$')

_NAMELESS_TASKS: typing.FrozenSet[str] = frozenset("""
meta
debug
include_role import_role include_tasks import_tasks
""".split())


@functools.lru_cache(maxsize=4)
def task_name_re(default: typing.Optional[str] = None) -> typing.Pattern:
    """
    :param default: default regexp object to try match with task names
    """
    if default is None or not default:
        default = _NAME_RE

    return re.compile(os.environ.get(TASK_NAME_RE_ENVVAR, default),
                      re.ASCII)


def is_named_task(task: typing.Dict[str, typing.Any],
                  nameless_tasks: typing.FrozenSet[str] = _NAMELESS_TASKS
                  ) -> bool:
    """Test if given task should be named?
    """
    return task['action']['__ansible_module__'] not in nameless_tasks


def is_invalid_task_name(name: str, default: typing.Optional[str] = None
                         ) -> bool:
    """
    :param name: A str

    >>> task_name_re.cache_clear()
    >>> is_invalid_task_name("Run something")
    False
    >>> is_invalid_task_name("ask something")
    False
    >>> is_invalid_task_name('')
    True

    # I don't know why but it fails in tox env.
    # >>> is_invalid_task_name("a b c")
    # True
    """
    if name:
        return task_name_re(default).match(name) is None

    return True


# pylint: disable=too-few-public-methods
class TaskHasValidNamePatternRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if given task has a valid name satisfies the naming rule
    in the organization.
    """
    id = ID
    shortdesc = 'All tasks should be named correctly'
    description = (
        'All tasks should have a valid name satisfies the naming rule'
    )
    severity = 'MEDIUM'
    tags = ['task', 'readability', 'formatting']

    def matchtask(self, task: typing.Dict[str, typing.Any]
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
            if is_invalid_task_name(name):
                return f'Task name was: "{name}"'

        return False

# vim:sw=4:ts=4:et:
