# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Common utility test routines and classes.
"""
import os
import pathlib
import subprocess
import unittest

import ansiblelint.utils
try:
    from ansiblelint.rules import RulesCollection
except ImportError:
    from ansiblelint import RulesCollection

try:
    from ansiblelint.runner import Runner
except ImportError:
    from ansiblelint import Runner


CURDIR = pathlib.Path(__file__).parent
RULES_DIR = str(CURDIR.parent / "rules")
DEFAULT_RULES_DIR = str(
    pathlib.Path(ansiblelint.utils.__file__).parent / "rules"
)


def list_res_files(relpath_pat):
    """
    :param relpath_pat: Glob pattern to list files, e.g. a_*_ok.yml
    :return: A list of absolute file paths in <curdir>/res/
    """
    return sorted(str(p) for p in CURDIR.glob("res/{}".format(relpath_pat)))


class AnsibleLintRuleTestCase(unittest.TestCase):
    """Base class to test ansible-lint rules.
    """

    rule = None
    prefix = None

    def setUp(self):
        """Initialize lint rules collection.
        """
        # Default rules only
        self.rules = RulesCollection()
        self.rules.register(self.rule)  # Register the rule to test explicitly.

    def _lint_results_for_playbooks_itr(self, playbook_fn_patterns):
        """
        :param playbook_fn_patterns: Glob filenames pattern to find playbooks
        """
        playbooks = list_res_files(playbook_fn_patterns)
        for filepath in playbooks:
            runner = Runner(self.rules, filepath, [], [], [])
            yield runner.run()

    def test_10_ok_cases(self):
        if self.rule is None or self.prefix is None:
            return

        pats = self.prefix + "*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)  # No errors

    def test_20_ng_cases(self):
        if self.rule is None or self.prefix is None:
            return

        pats = self.prefix + "*ng*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)  # something goes wrong


def _rule_ids_itr():
    """
    Yield custom rule IDs using ansiblelint.rules.RulesCollection.
    """
    rdirs = (DEFAULT_RULES_DIR, RULES_DIR)
    try:
        for rdir in rdirs:
            for rule in RulesCollection.create_from_directory(rdir):
                yield rule.id
    except AttributeError:  # newer ansiblelint
        for rule in RulesCollection(rdirs):
            yield rule.id


class AnsibleLintRuleCliTestCase(unittest.TestCase):
    """Run ok and ng CLI test cases automatically.
    """

    rule = None
    prefix = ''
    clear_fn = False

    def setUp(self):
        super(AnsibleLintRuleCliTestCase, self).setUp()
        if getattr(self, "clear_fn", False) and callable(self.clear_fn):
            self.clear_fn()

        excl_opt = ' '.join(("-x {!s}".format(rid)
                             for rid in _rule_ids_itr()
                             if rid != getattr(self.rule, "id", None)))
        self.cmd = "ansible-lint -r {} {}".format(RULES_DIR, excl_opt).split()

    def _run_for_playbooks(self, playbook_fn_patterns, res_ok=True, env=None):
        """
        :param playbook_fn_patterns: Glob filenames pattern to find playbooks
        """
        if env:
            os.environ.update(**env)

        playbooks = list_res_files(playbook_fn_patterns)
        for filepath in playbooks:
            res = subprocess.run(
                self.cmd + [filepath], stdout=subprocess.PIPE, check=False,
                env=os.environ
            )
            if res_ok:
                self.assertEqual(res.returncode, 0, res.stdout.decode("utf-8"))
            else:
                self.assertNotEqual(res.returncode, 0,
                                    res.stdout.decode("utf-8"))

    def test_10_ok_cases(self):
        if self.prefix:
            self._run_for_playbooks(self.prefix + "*ok*.yml")

    def test_20_ng_cases(self):
        if self.prefix:
            self._run_for_playbooks(self.prefix + "*ng*.yml", False)

# vim:sw=4:ts=4:et:
