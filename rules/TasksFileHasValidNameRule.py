# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Lint rule class to test if tasks files have valid filenames.
"""
import functools
import os
import pathlib
import re
import typing

import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from ansiblelint.constants import odict


ID: str = 'tasks-file-has-valid-names'
ENV_VAR = f"_ANSIBLE_LINT_RULE_{ID.upper().replace('-', '_')}_NAME_RE"

VALID_NAME_RE: typing.Pattern = re.compile(r'^\S+$', re.ASCII)
NAME_RE_DEFAULT: str = r'^\w+\.ya?ml$'


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
def filename_re(default: typing.Optional[str] = None) -> typing.Pattern:
    """
    :return: regex object to try match with names
    """
    if default is None:
        default = NAME_RE_DEFAULT

    return re.compile(name_re(default), re.ASCII)


def is_invalid_filename(filepath: str) -> bool:
    """
    Test if given file has valid filename.
    """
    fname = pathlib.Path(filepath).name
    return filename_re().match(fname) is None


class TasksFileHasValidNameRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if tasks file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = ID
    shortdesc: str = 'Tasks file must have valid filename'
    description = (
        'Tasks files (roles/tasks/*.yml) must have valid filenames.'
    )
    severity = 'HIGH'
    tags = [ID, 'task']

    def matchplay(self, file: ansiblelint.file_utils.Lintable,
                  _data: 'odict[str, typing.Any]'
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:; ansiblelint.rules.AnsibleLintRule.matchplay
        """
        if file.kind == 'tasks':
            path = str(file.path)
            if is_invalid_filename(path):
                return [
                    self.create_matcherror(message=f'{self.shortdesc}: {path}',
                                           filename=file.name)
                ]

        return []
