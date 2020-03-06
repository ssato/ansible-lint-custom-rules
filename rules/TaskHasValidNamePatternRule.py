# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
r"""Lint rule class to test if tasks have valid names.

.. note::
   Users can specify the task name regexp with the enviornment variable,
   _ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE, for exampke,

   _ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE="\S+" ansible-lint ...
"""
import os
import re
import ansiblelint


VERBS = """\
ask be become begin call can come could do feel find ensure get give go have
hear help keep know leave let like live look make may mean might move need play
put run say see seem should show start take talk tell think try turn use want
will work would\
""".split()


# .. todo:: Allow users to customize the regexp patterns.
TASK_NAME_RE = (r"(" + '|'.join(VERBS + [v.title() for v in VERBS]) +
                r")(\s+(\S+))+$")

_NAMELESS_TASKS = ('meta', 'debug', 'include_role', 'import_role',
                   'include_tasks', 'import_tasks')


def is_named_task(task, _nameless_tasks=_NAMELESS_TASKS):
    """Test if given task should be named?
    """
    return task["action"]["__ansible_module__"] not in _nameless_tasks


def is_invalid_task_name(name):
    """
    :param name: A str

    >>> is_invalid_task_name("Run something")
    False
    >>> is_invalid_task_name("ask something")
    False
    >>> is_invalid_task_name("aaa bbb ccc")
    True
    >>> is_invalid_task_name('')
    True
    """
    if name:
        reg = os.environ.get("_ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE",
                             TASK_NAME_RE)
        return re.match(reg, name) is None

    return True


def task_has_a_invalid_name(_self, _file, task):
    """
    :param task: task object
    """
    if is_named_task(task):
        return is_invalid_task_name(task["name"])

    return False


class TaskHasValidNamePatternRule(ansiblelint.AnsibleLintRule):
    """
    Rule class to test if given task has a valid name satisfies the naming rule
    in the organization.
    """

    id = "Custom-2020-1"
    shortdesc = "All tasks should be named correctly"
    description = (
        "All tasks should have a valid name satisfies the naming rule"
    )
    severity = "MEDIUM"
    tags = ["task", "readability", "formatting"]
    version_added = "4.1.99"  # dummy

    matchtask = task_has_a_invalid_name

# vim:sw=4:ts=4:et:
