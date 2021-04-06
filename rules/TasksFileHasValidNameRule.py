# Copyright (C) 2020,2021 Red Hat, Inc.
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

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable

from ansiblelint.rules import AnsibleLintRule


ID: str = 'tasks-file-has-valid-names'
DESC: str = 'Tasks files must have valid filenames.'

_ENVVAR_PREFIX: str = '_ANSIBLE_LINT_RULE_' + ID.upper().replace('-', '_')
NAME_RE_ENVVAR: str = _ENVVAR_PREFIX + '_TASKS_FILENAME_RE'

NAME_RE_DEFAULT: str = r'^\w+\.ya?ml$'


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
        return f'Invalid filename: {filepath}'

    return False


class TasksFileHasValidNameRule(AnsibleLintRule):
    """
    Rule class to test if tasks file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = ID
    shortdesc = DESC
    description = (
        'Tasks files (roles/tasks/*.yml) should have valid filenames.'
    )
    severity = 'HIGH'
    tags = ['task']

    def matchplay(self, file: 'Lintable', _data: 'odict[str, typing.Any]'
                  ) -> typing.List['MatchError']:
        """
        .. seealso:; ansiblelint.rules.AnsibleLintRule.matchplay
        """
        if file.kind == 'tasks' and check_filename(file.name):
            msg = f'Invalid tasks files: {file.name!s}'
            return [
                self.create_matcherror(message=msg, filename=file.name)
            ]

        return []
