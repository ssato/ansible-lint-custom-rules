# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if tasks files have valid filenames.
"""
import functools
import os
import re

import ansiblelint


_RULE_ID = "Custom_2020_2"
_ENVVAR_PREFIX = "_ANSIBLE_LINT_RULE_" + _RULE_ID.upper()
NAME_RE_ENVVAR = _ENVVAR_PREFIX + "_TASKS_FILENAME_RE"


@functools.lru_cache(maxsize=32)
def name_re(default=None):
    """
    :return: regex object to try match with names
    """
    if default is None:
        default = r"^\w+\.ya?ml$"  # TBD

    return re.compile(os.environ.get(NAME_RE_ENVVAR, default), re.ASCII)


def is_invalid_filename(filename, reg=None):
    """
    :param filename: A str represents a file path
    :param reg: A str gives a regexp to try match with valid filenames

    :return: True if given `filename` is invalid and does not satisfy the rule
    """
    return name_re(reg).match(filename) is None


class TasksFileHasValidNameRule(ansiblelint.AnsibleLintRule):
    """
    Rule class to test if tasks file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = _RULE_ID
    shortdesc = "Tasks files should have valid filenames"
    description = (
        "Tasks files (roles/tasks/*.yml) should have valid filenames."
    )
    severity = "MEDIUM"
    tags = ["task", "readability", "formatting"]
    version_added = "4.2.99"  # dummy

    tested = set()  # acc.

    def match(self, file, _text):
        """Test tasks files.
        """
        if file["type"] != "tasks":
            return False

        filepath = file["path"]
        filename = os.path.basename(filepath)

        if filepath not in self.tested:
            self.tested.add(filepath)
            if is_invalid_filename(filename):
                return "Invalid filename: " + filename

        return False
