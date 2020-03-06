# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-module-docstring
import glob
import os.path
import unittest

import ansiblelint


CURDIR = os.path.dirname(__file__)
RULES_DIR = os.path.join(CURDIR, "..", "rules")


def list_res_files(relpath_pat):
    """
    :param relpath_pat: Glob pattern to list files, e.g. a_*_ok.yml
    :return: A list of absolute file paths in <curdir>/res/
    """
    return sorted(glob.glob(os.path.join(CURDIR, "res", relpath_pat)))


class AnsibleLintRuleTestBase(unittest.TestCase):
    """Base class to test lint rules.
    """

    rule = None

    def setUp(self):
        """Initialize lint rules collection.
        """
        try:
            # Requires: ansible-lint > 4.2.0
            # pylint: disable=too-many-function-args
            self.rules = ansiblelint.RulesCollection([RULES_DIR])
        except TypeError:
            self.rules = ansiblelint.RulesCollection()
            if self.rule:
                self.rules.register(self.rule)

    def _lint_results_for_playbooks_itr(self, playbook_fn_patterns):
        """
        :param playbook_fn_patterns: Glob filenames pattern to find playbooks
        """
        playbooks = list_res_files(playbook_fn_patterns)
        for filepath in playbooks:
            with open(filepath) as fobj:
                runner = ansiblelint.Runner(self.rules, fobj.name, [], [], [])
                yield runner.run()
