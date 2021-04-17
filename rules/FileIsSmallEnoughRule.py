# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if playbook files are small enough.

Users can change the behavior of this class by specifying an environment
variable, _ANSIBLE_LINT_RULE_CUSTOM_2020_30_MAX_LINES.

::

    _ANSIBLE_LINT_RULE_CUSTOM_2020_30_MAX_LINES=500

"""
import functools
import os
import re
import typing

import ansiblelint.constants
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable


ID: str = 'file-is-small-enough'
ENV_VAR: str = (f"_ANSIBLE_LINT_RULE_{ID.upper().replace('-', '_')}"
                '_MAX_LINES')

MAX_LINES: int = 500
MAX_LINES_RE: typing.Pattern = re.compile(r'^[1-9]\d*$', re.ASCII)


@functools.lru_cache()
def max_lines(default: int = MAX_LINES) -> int:
    """
    :return: An int denotes the max line of playbook and related files
    """
    mlines: str = os.environ.get(ENV_VAR, '').strip()
    if mlines and MAX_LINES_RE.match(mlines):
        return int(mlines)

    return default


def exceeds_max_lines(filepath: str, mlines: int = 0) -> bool:
    """
    :param filepath: A str gives a file path
    :return: True if given file is not small and exceeds max lines

    >>> exceeds_max_lines(__file__, 1000000)
    False
    >>> exceeds_max_lines(__file__, 10)
    True
    """
    if mlines < 1:
        mlines = max_lines()

    with open(filepath) as fobj:
        # Which is better?
        # return len(fobj.readliens()) > mlines
        for idx, _line in enumerate(fobj):
            if idx + 1 > mlines:
                return True

    return False


# .. seealso:: ansiblelint.constants.FileType
FTYPES: typing.FrozenSet = frozenset(
    'playbook meta tasks handlers role yaml'.split()
)


class FileIsSmallEnoughRule(ansiblelint.rules.AnsibleLintRule):
    """
    Rule class to test if playbook and tasks files are small enough.
    """
    id = ID
    shortdesc = 'Playbook and tasks files should be small enough'
    description = shortdesc
    severity = 'MEDIUM'
    tags = [ID, 'playbook', 'tasks', 'readability']

    def __init__(self):
        """Initialize this.
        """
        super().__init__()
        self.cache: typing.Set = set()

    def matchyaml(self, file: 'Lintable') -> typing.List['MatchError']:
        """Test playbook files.
        """
        if file.kind in FTYPES:
            path = str(file.path)
            if path in self.cache:
                return []

            self.cache.add(path)

            if exceeds_max_lines(path):
                return [
                    self.create_matcherror(
                        message='File {path} may be too large',
                        filename=path
                    )
                ]

        return []

# vim:sw=4:ts=4:et:
