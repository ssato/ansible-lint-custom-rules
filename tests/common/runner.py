# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,too-few-public-methods
"""Common utility test routines and classes.
"""
import pathlib
import typing

import ansiblelint.config
import ansiblelint.constants
import ansiblelint.errors
import ansiblelint.file_utils
import ansiblelint.runner

from ansiblelint.rules import AnsibleLintRule, RulesCollection

from . import constants


def list_rule_ids(*rdirs: str) -> typing.Iterator[str]:
    """List the IDs of rules in given dirs.
    """
    if not rdirs:
        rdirs = [str(constants.RULES_DIR)]

    for rule in ansiblelint.rules.RulesCollection(rdirs):
        yield rule.id


RuleOptionsT = typing.Optional[typing.Dict[str, typing.Any]]


def get_collection(rule: typing.Optional[AnsibleLintRule] = None,
                   rule_options: RuleOptionsT = None
                   ) -> RulesCollection:
    """
    Get RulesCollection instance with given rule registered.
    """
    rulesdirs = [ansiblelint.constants.DEFAULT_RULESDIR]

    options = ansiblelint.config.options
    options.enable_list = ['no-same-owner']

    try:
        collection = RulesCollection(rulesdirs=rulesdirs, options=options)
    except TypeError:
        collection = RulesCollection(rulesdirs=rulesdirs)

    if rule:
        # Hack to force setting options.
        if rule_options:
            setattr(
                ansiblelint.config.options, 'rules', {rule.id: rule_options}
            )

        collection.register(rule)

    return collection


class RunFromFile:
    """Base Class to run ansiblelint for given files.

    .. seealso:: ansiblelint.testing.RunFromText
    """
    def __init__(self, collection: RulesCollection):
        """Initialize an instance with given rules collection.
        """
        self._collection = collection

    def run_playbook(self, path: typing.Union[str, pathlib.Path]
                     ) -> typing.List[ansiblelint.errors.MatchError]:
        """Lints received playbook file.
        """
        return ansiblelint.runner.Runner(
            ansiblelint.file_utils.Lintable(path, kind='playbook'),
            rules=self._collection
        ).run()

# vim:sw=4:ts=4:et:
