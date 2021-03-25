# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class for debug use.
"""
import functools
import os
import typing

from ansiblelint.rules import AnsibleLintRule


_RULE_ID: str = "Custom_2020_99"
_DESC: str = "Custom rule class for debug use"

_ENVVAR_PREFIX: str = "_ANSIBLE_LINT_RULE_" + _RULE_ID.upper()
ENABLE_THIS_RULE_ENVVAR: str = _ENVVAR_PREFIX + "_DEBUG"

Matched = typing.NamedTuple("Matched",
                            (("lines", typing.Set[str]),
                             ("tasks", typing.Set[str]),
                             ("plays", typing.Set[str])))


@functools.lru_cache(maxsize=64)
def is_enabled(default: bool = False) -> bool:
    """
    :param default: default regexp object to try match with task names
    """
    return bool(os.environ.get(ENABLE_THIS_RULE_ENVVAR, default))


MResType = typing.Union[bool, str]
MPResType = typing.Union[typing.Tuple[str, str], bool]


class DebugRule(AnsibleLintRule):
    """Rule class for debug use.
    """
    id = _RULE_ID
    shortdesc = description = _DESC
    severity = "LOW"
    tags = ["debug"]
    version_added = "4.2.99"  # dummy

    matched = Matched(set(), set(), set())

    def match(self, file_: typing.Mapping, text: str) -> MResType:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchlines

        :param file_: A mapping object holding target file info
        :param text: The line to apply the rule and check

        :return: A str gives error info or False
        """
        if is_enabled():
            # Limit to return debug messages per file.
            if "path" in file_ and file_["path"] not in self.matched.lines:
                self.matched.lines.add(file_["path"])
                return "file: {!r}, text: {!r}".format(file_, text)

        return False

    def matchtask(self, file_: typing.Mapping, task: typing.Mapping
                  ) -> MResType:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchtasks

        :param file_: A mapping object holding target file info
        :param task: A mapping object holding target task info

        :return: A str gives error info or False
        """
        if is_enabled():
            # Limit to return debug messages per task.
            if "name" in task and task["name"] not in self.matched.tasks:
                self.matched.tasks.add(task["name"])
                return "file: {!r}, task: {!r}".format(file_, task)

        return False

    def matchplay(self, file_: typing.Mapping, play: typing.Mapping
                  ) -> MPResType:
        """
        .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml

        :param file_: A mapping object holding target file info
        :param play: A mapping object holding target play info

        :return: A str gives error info or False
        """
        if is_enabled():
            # Limit to return debug messages per play.
            if "name" in play and play["name"] not in self.matched.plays:
                self.matched.plays.add(play["name"])
                return (os.path.basename(file_["path"]),
                        "file: {!r}, play: {!r}".format(file_, play))

        return False
