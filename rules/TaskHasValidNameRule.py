# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
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
ENV_VAR = f"_ANSIBLE_LINT_RULE_{ID.upper().replace('-', '_')}_NAME_RE"

VERBS: typing.List[str] = """\
ask be become begin call can come could do feel find ensure get give go have
hear help keep know leave let like live look make may mean might move need play
put run say see seem should show start take talk tell think try turn use want
will work would\
""".split()

VALID_NAME_RE: typing.Pattern = re.compile(r'^\S+$', re.ASCII)
NAME_RE: str = (r'(' + '|'.join(VERBS + [verb.title() for verb in VERBS]) +
                r')(\s+(\S+))+$')

_NAMELESS_TASKS: typing.FrozenSet[str] = frozenset("""
meta
debug
import_role
import_tasks
include_role
include_tasks
""".split())


def name_re(default: str, env_var: str = ENV_VAR,
            valid_name_re: typing.Pattern = VALID_NAME_RE) -> str:
    """
    Get a pattern to match with names as a string.
    """
    pattern_s = os.environ.get(env_var, '')
    if pattern_s and valid_name_re.match(pattern_s):
        return pattern_s

    return default


@functools.lru_cache()
def task_name_pattern(default: typing.Optional[str] = None) -> typing.Pattern:
    """
    :param default: default regexp object to try match with task names
    """
    if default is None or not default:
        default = NAME_RE

    return re.compile(name_re(default), re.ASCII)


def is_named_task(task: typing.Dict[str, typing.Any],
                  nameless_tasks: typing.FrozenSet[str] = _NAMELESS_TASKS
                  ) -> bool:
    """Test if given task should be named?
    """
    return task['action']['__ansible_module__'] not in nameless_tasks


def is_invalid_task_name(name: str, default: typing.Optional[str] = None
                         ) -> bool:
    """
    Test if given task's name is invalid.
    """
    if name:
        return task_name_pattern(default).match(name) is None

    return True


class TaskHasValidNameRule(ansiblelint.rules.AnsibleLintRule):
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
    tags = [ID, 'task', 'readability', 'formatting']

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
