# Copyright (C) 2020,2021 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
r"""
Lint rule class to test if there are YAML files have no data.
"""
import functools
import itertools
import pathlib
import typing
import yaml
import yaml.parser

import ansiblelint.constants
import ansiblelint.rules
import ansiblelint.errors

from ansiblelint.file_utils import Lintable


RULE_ID: str = 'no-empty-data-files'
DESC = 'All YAML files should have some data'

_ENVVAR_PREFIX = '_ANSIBLE_LINT_RULE_' + RULE_ID.upper().replace('-', '_')
YML_EXT_ENVVAR = _ENVVAR_PREFIX + '_YML_EXT'


@functools.lru_cache(maxsize=32)
def is_yml_file_has_some_data(filepath: pathlib.Path) -> bool:
    """
    Is given YAML file has some data?
    """
    try:
        return bool(yaml.safe_load(filepath.open()))
    except yaml.parser.ParserError:
        pass

    return True  # Innocent until proven guilty.


def list_role_files_itr(play: ansiblelint.constants.odict[str, typing.Any]
                        ) -> typing.Iterator[pathlib.Path]:
    """
    List role files for given `play`.
    """
    for role in play.get('roles', []):
        roledir = role.get('name', None)
        if not roledir:
            continue

        roledir = pathlib.Path(play.path) / roledir
        if roledir.exists() and roledir.is_dir():
            for path in itertools.chain(roledir.glob('**/*.yml'),
                                        roledir.glob('**/*.yaml')):
                if path.is_file():
                    yield path


class NoEmptyDataFilesRule(ansiblelint.rules.AnsibleLintRule):
    """
    Lint rule class to test if roles' YAML files have some data.
    """
    id = RULE_ID
    shortdesc = description = DESC
    severity = 'MEDIUM'
    tags = ['format', 'yaml']  # temp

    def err(self, path: pathlib.Path
            ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        an wrapper method for self.create_matcherror.
        """
        return self.create_matcherror(message=f'Empty data file: {path!s}',
                                      filename=path.name)

    def matchyaml_itr(self, file: Lintable
                      ) -> typing.Iterator[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
        """
        if file.base_kind != 'text/yaml':
            return

        for match in super().matchyaml(file):
            yield match

        maybe_playbook = pathlib.Path(file.path)
        if not is_yml_file_has_some_data(maybe_playbook):
            yield self.err(maybe_playbook)

    def matchyaml(self, file: Lintable
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
        """
        return list(self.matchyaml_itr(file))

    def matchplay(self, file: Lintable,
                  data: ansiblelint.constants.odict[str, typing.Any]
                  ) -> typing.List[ansiblelint.errors.MatchError]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
        """
        raise ValueError(f'{data!r}')
        return [
            self.err(path) for path in list_role_files_itr(data)
            if not is_yml_file_has_some_data(path)
        ]

# vim:sw=4:ts=4:et:
