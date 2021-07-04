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


def each_rule_ids(*rdirs: str, use_default: bool = False
                  ) -> typing.Iterator[str]:
    """List the IDs of rules in given dirs.
    """
    if rdirs:
        rdirs = list(rdirs)
    else:
        rdirs = [str(constants.RULES_DIR)]

    if use_default:
        rdirs.append(ansiblelint.constants.DEFAULT_RULESDIR)

    for rule in ansiblelint.rules.RulesCollection(rdirs):
        yield rule.id


RuleOptionsT = typing.Optional[typing.Dict[str, typing.Any]]


def get_collection(rule: typing.Optional[AnsibleLintRule] = None,
                   rule_options: RuleOptionsT = None,
                   use_default_rules: bool = False
                   ) -> RulesCollection:
    """
    Get RulesCollection instance with given rule registered.
    """
    if use_default_rules:
        rulesdirs = [ansiblelint.constants.DEFAULT_RULESDIR]
    else:
        rulesdirs = []

    options = ansiblelint.config.options
    options.enable_list = ['no-same-owner']

    try:
        collection = RulesCollection(rulesdirs=rulesdirs, options=options)
    except TypeError:
        collection = RulesCollection(rulesdirs=rulesdirs)

    if rule:
        # Hack to force setting options.
        setattr(
            ansiblelint.config.options, 'rules', {rule.id: rule_options or {}}
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

    def run_playbook(self, path: typing.Union[str, pathlib.Path],
                     skip_list: typing.Optional[typing.List[str]] = None
                     ) -> typing.List[ansiblelint.errors.MatchError]:
        """Lints received playbook file.
        """
        if skip_list is None:
            skip_list = []

        return ansiblelint.runner.Runner(
            ansiblelint.file_utils.Lintable(path, kind='playbook'),
            rules=self._collection,
            skip_list=skip_list
        ).run()

# vim:sw=4:ts=4:et:
