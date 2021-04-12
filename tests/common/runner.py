# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=too-few-public-methods
"""Common utility test routines and classes.
"""
import pathlib
import typing

import ansiblelint.config
import ansiblelint.constants
import ansiblelint.errors
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


def get_collection(rule: typing.Optional[AnsibleLintRule] = None
                   ) -> RulesCollection:
    """
    Get RulesCollection instance with given rule registered.
    """
    if rule is None:
        # .. seealso:: ansiblelint.testing.fixture.default_rules_collection
        assert pathlib.Path(ansiblelint.constants.DEFAULT_RULESDIR).is_dir()

        try:
            ansiblelint.config.options.enable_list = ['no-same-owner']
            return RulesCollection(
                rulesdirs=[ansiblelint.constants.DEFAULT_RULESDIR],
                options=ansiblelint.config.options
            )
        except TypeError:
            return RulesCollection(
                rulesdirs=[ansiblelint.constants.DEFAULT_RULESDIR]
            )

    collection = RulesCollection()
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
        return ansiblelint.runner.Runner(path, rules=self._collection).run()

# vim:sw=4:ts=4:et:
