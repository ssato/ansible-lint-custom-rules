# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if tasks files have valid filenames.
"""
import os
import re

import ansiblelint


DEFAULT_VFN_RE = re.compile(r"^\w+\.ya?ml$", re.ASCII)  # TBD


def is_invalid_filename(filename, regex=DEFAULT_VFN_RE):
    """
    :param filename: A str represents a file path
    :return: True if given `filename` is invalid and does not satisfy the rule
    """
    res = os.environ.get("_ANSIBLE_LINT_RULE_CUSTOM_2020_2_TASKS_FILENAME_RE",
                         False)
    if res:
        regex = re.compile(res)

    return regex.match(filename) is None


class TasksFileHasValidNameRule(ansiblelint.AnsibleLintRule):
    """
    Rule class to test if tasks file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = "Custom-2020-2"
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
