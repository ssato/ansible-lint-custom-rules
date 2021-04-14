# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Common utility classes for test cases.
"""
import os
import subprocess
import types
import typing
import unittest
import unittest.mock

from . import constants, runner, utils


MaybeModNameT = typing.Optional[str]
MaybeModT = typing.Optional[types.ModuleType]
MaybeCallableT = typing.Optional[typing.Callable]


class BaseTestCase(unittest.TestCase):
    """Base class for test cases.
    """
    # .. todo::
    #    I don't know how to compute and set them in test case classes in
    #    modules import this module.
    this_py: MaybeModNameT = None
    this_mod: MaybeModT = None

    clear_fn: MaybeCallableT = None

    initialized: bool = False

    @classmethod
    def clear(cls):
        """Call clear function if it's callable.
        """
        if cls.clear_fn and callable(cls.clear_fn):
            cls.clear_fn()  # pylint: disable=not-callable

    def init(self):
        """Initialize.
        """
        if not self.this_py or not self.this_mod:
            return

        self.name = utils.get_rule_name(self.this_py)
        self.rule = utils.get_rule_instance_by_name(self.this_mod, self.name)

        # Collect the default rules and add the rule to test.
        collection = runner.get_collection(self.rule)
        self.runner = runner.RunFromFile(collection)

        self.initialized = True

    def setUp(self):
        """Setup
        """
        self.init()

    def tearDown(self):
        """De-initialize.
        """
        self.clear()


class RuleTestCase(BaseTestCase):
    """Base class to test rules.
    """
    def run_playbook(self, filepath: str,
                     env: typing.Optional[typing.Dict] = None):
        """Run playbook.
        """
        if env:
            # .. todo:: It does not look working in pytest env.
            # with unittest.mock.patch.dict(os.environ, env):
            saved = os.environ.copy()
            try:
                os.environ.update(**env)
                return self.runner.run_playbook(filepath)
            finally:
                os.environ = saved

        return self.runner.run_playbook(filepath)

    def list_resources(self, success: bool = True,
                       search: typing.Optional[str] = None,
                       pattern: typing.Optional[str] = None):
        """
        List test resource data (may match given search patterns).
        """
        files = utils.list_resources(self.name, success=success,
                                     search=search, pattern=pattern)
        self.assertTrue(files,
                        'Failed to find test resource data: '
                        f'success={success}, search={search}'
                        f'pattern={pattern}')
        return files

    def lint(self, success: bool = True,
             search: typing.Optional[str] = None,
             pattern: typing.Optional[str] = None,
             env: typing.Optional[typing.Dict] = None):
        """
        Run the lint rule's check to given resource data files.
        """
        if not self.initialized:
            return

        files = self.list_resources(success=success, search=search,
                                    pattern=pattern)
        for filepath in files:
            res = self.run_playbook(filepath, env=env)
            msg = f'{filepath}, {res!r}, {env!r}'
            if success:
                self.assertEqual(0, len(res), msg)  # No errors.
            else:
                self.assertTrue(len(res) > 0, msg)  # It should fail.

    def test_10_ok_cases(self):
        """10 - OK test cases"""
        self.lint()

    def test_20_ng_cases(self):
        """20 - NG test cases"""
        self.lint(success=False)


class CliTestCase(RuleTestCase):
    """Base class to test rules with CLI.
    """
    def setUp(self):
        """Set up members.
        """
        if not self.this_py or not self.this_mod:
            return

        self.init()

        excl_opt = utils.concat(('-x', rid) for rid in runner.list_rule_ids()
                                if rid != self.rule.id)
        self.cmd = (f'ansible-lint -r {constants.RULES_DIR!s}'.split()
                    + excl_opt)

    def lint(self, success: bool = True,
             search: typing.Optional[str] = None,
             pattern: typing.Optional[str] = None,
             env: typing.Optional[typing.Dict] = None):
        """
        Run ansible-lint with given arguments in given env.
        """
        if not self.initialized:
            return

        oenv = os.environ.copy()
        if env:
            oenv.update(**env)

        files = self.list_resources(success=success, search=search,
                                    pattern=pattern)
        for filepath in files:
            res = subprocess.run(
                self.cmd + [filepath], stdout=subprocess.PIPE, check=False,
                env=oenv
            )
            if success:
                self.assertEqual(res.returncode, 0, res.stdout.decode('utf-8'))
            else:
                self.assertNotEqual(res.returncode, 0,
                                    res.stdout.decode('utf-8'))

# vim:sw=4:ts=4:et:
