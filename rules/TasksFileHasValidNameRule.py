# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if tasks files have valid filenames.
"""
import functools
import os
import pathlib
import re
import typing

try:
    from ansiblelint.rules import AnsibleLintRule
except ImportError:
    from ansiblelint import AnsibleLintRule


RULE_ID: str = "Custom_2020_2"
DESC: str = "Tasks files must have valid filenames."

_ENVVAR_PREFIX: str = "_ANSIBLE_LINT_RULE_" + RULE_ID.upper()
NAME_RE_ENVVAR: str = _ENVVAR_PREFIX + "_TASKS_FILENAME_RE"

NAME_RE_DEFAULT: str = r"^\w+\.ya?ml$"


@functools.lru_cache(maxsize=4)
def filename_re(default: typing.Optional[str] = None) -> typing.Pattern:
    """
    :return: regex object to try match with names
    """
    if default is None:
        default = NAME_RE_DEFAULT

    return re.compile(os.environ.get(NAME_RE_ENVVAR, default), re.ASCII)


@functools.lru_cache(maxsize=32)
def is_invalid_filename(filepath: str, name_re: typing.Optional[str] = None
                        ) -> bool:
    """
    Test if given file has valid filename.
    """
    fname = pathlib.Path(filepath).name
    return filename_re(name_re).match(fname) is None


def check_filename(filepath: str) -> typing.Union[str, bool]:
    """
    Check filename.
    """
    if is_invalid_filename(filepath):
        return "Invalid filename: " + filepath

    return False


class TasksFileHasValidNameRule(AnsibleLintRule):
    """
    Rule class to test if tasks file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = RULE_ID
    shortdesc = DESC
    description = (
        "Tasks files (roles/tasks/*.yml) should have valid filenames."
    )
    severity = "HIGH"
    tags = ["task"]

    def match(_self, file_: typing.Mapping, _text) -> typing.Union[str, bool]:
        """Test tasks files.
        """
        if file_["type"] != "tasks":
            return False

        return check_filename(file_["path"])
