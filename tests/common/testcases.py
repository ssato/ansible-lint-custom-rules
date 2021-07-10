# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Common utility classes for test cases.
"""
import pathlib
import typing
import unittest

from . import base


class RuleTestCase(unittest.TestCase):
    """Base class to test rules.
    """
    base_cls = base.Base

    def setUp(self):
        """Setup base."""
        self.base = self.base_cls()

    def tearDown(self):
        """De-initialize."""
        self.base.clear()

    def list_data_dirs(self, success: bool = True
                       ) -> typing.Iterator[pathlib.Path]:
        """Yield the test data dirs for the rule."""
        subdir = 'ok' if success else 'ng'
        for datadir in self.base.list_test_data_dirs(subdir):
            yield datadir

    def lint(self, success: bool = True, isolated: bool = True) -> None:
        """Lint the lintables found under test data dirs with the rule.
        """
        if not self.base.is_runnable():
            return

        for datadir in self.list_data_dirs(success):
            res = self.base.rule_runner.run(datadir, isolated=isolated)

            msg = f'{datadir!r}, {res!r}'
            if success:
                self.assertEqual(0, len(res), msg)  # No errors.
            else:
                self.assertTrue(len(res) > 0, msg)  # It should fail.

            self.base.clear()

    def test_success_cases_only_with_the_rule(self):
        """Run test cases only with the rule, should succeed."""
        self.lint()

    def test_success_cases_with_other_rules(self):
        """Run test cases together with other rules, should succeed."""
        self.lint(isolated=False)

    def test_failure_cases_only_with_the_rule(self):
        """Run test cases only with the rule, should fail."""
        self.lint(success=False)

    def test_failure_cases_with_other_rules(self):
        """Run test cases together with other rules, should fail."""
        self.lint(success=False, isolated=False)


class CliTestCase(RuleTestCase):
    """Base class to test rules with CLI.
    """
    def lint(self, success: bool = True, isolated: bool = True) -> None:
        """Run ansible-lint in test data dirs with the rule."""
        if not self.base.is_runnable():
            return

        for datadir in self.list_data_dirs(success):
            res = self.base.cli_runner.run(datadir, isolated=isolated)

            msg = f'{datadir!r}, {res!r}'
            args = (res[0], 0, msg)

            if success:
                self.assertEqual(*args)
            else:
                self.assertNotEqual(*args)

# vim:sw=4:ts=4:et:
