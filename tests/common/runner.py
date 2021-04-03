# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=too-few-public-methods
"""Common utility test routines and classes.
"""
import pathlib
import typing

import ansiblelint.errors
import ansiblelint.rules
import ansiblelint.runner
import ansiblelint.testing.fixtures


FilepathT = typing.Union[str, pathlib.Path]
MatchResultT = typing.List[ansiblelint.errors.MatchError]


def get_collection(rule_instance: ansiblelint.rules.AnsibleLintRule = None,
                   ) -> ansiblelint.rules.RulesCollection:
    """
    Get RulesCollection instance.
    """
    if rule_instance is None:
        return ansiblelint.testing.fixtures.default_rules_collection()

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
