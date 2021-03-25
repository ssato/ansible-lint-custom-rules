# Copyright (C) 2020,2021 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
r"""
Lint rule class to test if there are YAML files have no data.

This implementation assumes target files are under <playbook_dir>/ with '.yml'
extensions by default. Users can change this with the environment variable
_ANSIBLE_LINT_RULE_CUSTOM_2020_50_YAML_EXT, for example,

::

    _ANSIBLE_LINT_RULE_CUSTOM_2020_50_YML_EXT=yaml
"""
import collections
import functools
import os
import pathlib
import typing
import yaml
import yaml.parser

from ansiblelint.rules import AnsibleLintRule


RULE_ID: str = "Custom_2020_50"
DESC = "All YAML files should have some data"

_ENVVAR_PREFIX: str = "_ANSIBLE_LINT_RULE_" + RULE_ID.upper()
YML_EXT_ENVVAR: str = _ENVVAR_PREFIX + "_YML_EXT"


def yml_extension() -> str:
    """
    Get YAML file extension maybe from the environment variable
    """
    return os.environ.get(YML_EXT_ENVVAR, "yml")


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


def role_names_itr(playbook: str) -> typing.Iterator[str]:
    """
    List role names from playbook.
    """
    try:
        plays = yaml.safe_load(open(playbook))

        for play in plays:
            for role in play.get("roles", []):
                if isinstance(role, collections.abc.Mapping):
                    yield role["role"]  # It should have this.
                else:
                    yield role

    except yaml.parser.ParserError:
        return


MatchT = typing.Tuple[typing.Union[typing.Mapping, str], str]


def no_data_yml_files_itr(playbook: str) -> typing.Iterator[MatchT]:
    """
    .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
    """
    for role in role_names_itr(playbook):
        pattern = "roles/{}/**/*.{}".format(role, yml_extension())

        for fpath in pathlib.Path(playbook).parent.glob(pattern):
            if not is_yml_file_has_some_data(fpath):
                yield ({"No data in YAML file: ": fpath},
                       "YAML file looks having no data: {}".format(fpath))


class NoEmptyDataFilesRule(AnsibleLintRule):
    """
    Lint rule class to test if roles' YAML files have some data.
    """
    id = RULE_ID
    shortdesc = description = DESC
    severity = "MEDIUM"
    tags = ["format", "yaml"]  # temp
    version_added = "4.2.99"  # dummy

    def matchplay(self, file_: typing.Mapping, _play: typing.Mapping
                  ) -> typing.Union[typing.List[MatchT], bool]:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
        """
        if file_["type"] == "playbook":
            return list(no_data_yml_files_itr(file_["path"]))

        return False

# vim:sw=4:ts=4:et:
