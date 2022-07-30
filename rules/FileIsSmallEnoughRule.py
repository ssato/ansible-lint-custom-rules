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
import typing
import warnings

import ansiblelint.constants
import ansiblelint.rules

if typing.TYPE_CHECKING:
    from ansiblelint.errors import MatchError
    from ansiblelint.file_utils import Lintable


ID: str = 'file_is_small_enough'

C_MAX_LINES: str = 'max_lines'
DEFAULT_MAX_LINES: int = 500
DESC: str = """Rule to test if files are smalll enough.

- Options

  - ``max_lines`` limits the number of maximum lines files can have.

- Configuration

  .. code-block:: yaml

    rules:
        file_is_small_enough:
            max_lines: 500
"""


def exceeds_max_lines(filepath: str, max_lines: int) -> bool:
    """
    Test if given file in ``filepath`` has a content exceeds max lines
    ``max_lines``.

    >>> exceeds_max_lines(__file__, 1000000)
    False
    >>> exceeds_max_lines(__file__, 10)
    True
    """
    with open(filepath) as fobj:
        # Might be better to return len(fobj.readliens()) > max_lines.
        for idx, _line in enumerate(fobj):
            if idx + 1 > max_lines:
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

    @functools.lru_cache()
    def max_lines(self):
        """The limit number of lines files can have.
        """
        try:
            max_lines = int(self.get_config(C_MAX_LINES))
            assert max_lines > 0
            return max_lines

        except (ValueError, AssertionError) as exc:
            warnings.warn(f'Invalid max_lines value: {max_lines:!r}'
                          f'exc={exc!s}')

        return DEFAULT_MAX_LINES

    @functools.lru_cache()
    def exceeds_max_lines(self, path: str):
        """Test if given file is small enough.
        """
        return exceeds_max_lines(path, self.max_lines())

    def matchyaml(self, file: 'Lintable') -> typing.List['MatchError']:
        """Test playbook files.
        """
        if file.kind in FTYPES:
            path = str(file.path)
            if self.exceeds_max_lines(path):
                return [
                    self.create_matcherror(
                        message=f'File {path} may be too large',
                        filename=path
                    )
                ]

        return []

# vim:sw=4:ts=4:et:
