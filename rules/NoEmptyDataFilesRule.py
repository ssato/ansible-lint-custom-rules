# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
r"""
Lint rule class to test if there are YAML files have no data.
"""
import functools
import typing
import yaml
import yaml.parser

import ansiblelint.rules
import ansiblelint.errors

from ansiblelint.file_utils import Lintable


ID: str = 'no-empty-data-files'


@functools.lru_cache()
def yml_file_has_some_data(filepath: str) -> bool:
    """
    Is given YAML file has some data?
    """
    try:
        with open(filepath) as fio:
            return bool(yaml.safe_load(fio))
    except yaml.parser.ParserError:
        pass

    return True  # Innocent until proven guilty.


# .. seealso:: ansiblelint.constants.FileType
FTYPES: typing.FrozenSet = frozenset(
    'playbook meta tasks handlers role yaml'.split()
)


class NoEmptyDataFilesRule(ansiblelint.rules.AnsibleLintRule):
    """
    Lint rule class to test if roles' YAML files have some data.
    """
    id = ID
    shortdesc = description = 'All YAML files should have some data'
    severity = 'MEDIUM'
    tags = [ID, 'format', 'yaml']

    def matchyaml(self, file: Lintable
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """Test playbook files.
        """
        if file.kind in FTYPES:
            path = str(file.path)
            if not yml_file_has_some_data(path):
                return [
                    self.create_matcherror(
                        message=f'Empty data file: {path!s}',
                        filename=path
                    )
                ]

        return []

# vim:sw=4:ts=4:et:
