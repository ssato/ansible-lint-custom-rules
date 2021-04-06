# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=too-few-public-methods
"""Common utility test routines and classes.
"""
import pathlib
import typing

import ansiblelint.constants
import ansiblelint.errors
import ansiblelint.rules
import ansiblelint.runner

try:
    import ansiblelint.config as AC
except ImportError:
    AC = False

from . import constants


FilepathT = typing.Union[str, pathlib.Path]
MatchResultT = typing.List[ansiblelint.errors.MatchError]


def list_rule_ids(*rdirs: str) -> typing.Iterator[str]:
    """List the IDs of rules in given dirs.
    """
    if not rdirs:
        rdirs = [constants.RULES_DIR]

    return [r.id for r in ansiblelint.rules.RulesCollection(rdirs)]


def get_collection(rule_instance: ansiblelint.rules.AnsibleLintRule = None,
                   ) -> ansiblelint.rules.RulesCollection:
    """
    Get RulesCollection instance.
    """
    if rule_instance is None:
        # .. seealso:: ansiblelint.testing.fixture.default_rules_collection
        assert pathlib.Path(ansiblelint.constants.DEFAULT_RULESDIR).is_dir()

        if AC:
            AC.options.enable_list = ['no-same-owner']
            return ansiblelint.rules.RulesCollection(
                rulesdirs=[ansiblelint.constants.DEFAULT_RULESDIR],
                options=ansiblelint.config.options
            )

        return ansiblelint.rules.RulesCollection(
            rulesdirs=[ansiblelint.constants.DEFAULT_RULESDIR]
        )

    collection = ansiblelint.rules.RulesCollection()
    collection.register(rule_instance)
    return collection


class RunFromFile:
    """Base Class to run ansiblelint for given files.

    .. seealso:: ansiblelint.testing.RunFromText
    """
    def __init__(self, collection: ansiblelint.rules.RulesCollection):
        """Initialize an instance with given rules collection.
        """
        self._collection = collection

    def run_playbook(self, path: FilepathT) -> MatchResultT:
        """Lints received playbook file.
        """
        return ansiblelint.runner.Runner(path, rules=self._collection).run()

# vim:sw=4:ts=4:et:
