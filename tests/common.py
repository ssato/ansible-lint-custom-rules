# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Common utility test routines and classes.
"""
import glob
import os.path
import re
import subprocess
import unittest

try:
    from ansiblelint.rules import RulesCollection
except ImportError:
    from ansiblelint import RulesCollection

try:
    from ansiblelint.runner import Runner
except ImportError:
    from ansiblelint import Runner


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
        # Default rules only
        self.rules = RulesCollection()
        self.rules.register(self.rule)  # Register the rule explicitly.

    def _lint_results_for_playbooks_itr(self, playbook_fn_patterns):
        """
        :param playbook_fn_patterns: Glob filenames pattern to find playbooks
        """
        playbooks = list_res_files(playbook_fn_patterns)
        for filepath in playbooks:
            with open(filepath) as fobj:
                runner = Runner(self.rules, fobj.name, [], [], [])
                yield runner.run()


class AutoTestCasesForAnsibleLintRule(AnsibleLintRuleTestBase):
    """Run ok and ng test cases automatically.
    """

    rule = None
    prefix = None

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


_LIST_RULE_ID_RE = re.compile(r"^([^: ]+): .+")


def _rule_ids_from_cli_output_itr(reg=_LIST_RULE_ID_RE):
    """
    Yield custom rule IDs extract from the output of 'ansible-lint -L'.
    """
    # Very ugly but it should work as expected.
    res = subprocess.run(
        "ansible-lint -L -r {}".format(RULES_DIR).split(),
        capture_output=True, check=True
    )
    for line in res.stdout.decode("utf-8").splitlines():
        match = reg.match(line)
        if match:
            yield match.groups()[0]


class CliTestCasesForAnsibleLintRule(unittest.TestCase):
    """Run ok and ng CLI test cases automatically.
    """

    rule = None
    prefix = ''
    clear_fn = False

    def setUp(self):
        super(CliTestCasesForAnsibleLintRule, self).setUp()
        if getattr(self, "clear_fn", False) and callable(self.clear_fn):
            self.clear_fn()

        excl_opt = ' '.join(("-x {!s}".format(rid)
                             for rid in _rule_ids_from_cli_output_itr()
                             if rid != getattr(self.rule, "id", None)))
        self.cmd = "ansible-lint -r {} {}".format(RULES_DIR, excl_opt).split()

    def _run_for_playbooks(self, playbook_fn_patterns, res_ok=True, env=None):
        """
        :param playbook_fn_patterns: Glob filenames pattern to find playbooks
        """
        playbooks = list_res_files(playbook_fn_patterns)
        for filepath in playbooks:
            res = subprocess.run(
                self.cmd + [filepath], capture_output=True, check=False,
                env=env
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
