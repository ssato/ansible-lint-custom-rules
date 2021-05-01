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
import tempfile
import unittest
import unittest.mock

import yaml

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

    def clear(self):
        """Call clear function if it's callable.
        """
        if not self.initialized:
            return

        self.rule.get_config.cache_clear()
        if self.clear_fn and callable(self.clear_fn):
            self.clear_fn()  # pylint: disable=not-callable

    def init(self):
        """Initialize.
        """
        if not self.this_py or not self.this_mod:
            return

        self.name = utils.get_rule_name(self.this_py)
        self.rule = utils.get_rule_instance_by_name(self.this_mod, self.name)

        self.initialized = True

    def get_runner(self, config: runner.RuleOptionsT = None
                   ) -> runner.RunFromFile:
        """
        Make ansiblelint.RulesCollection instance registered the rule with
        given config and get runner.RunFromFile instance from it.
        """
        collection = runner.get_collection(self.rule, rule_options=config)
        return runner.RunFromFile(collection)

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
                     env: typing.Optional[typing.Dict] = None,
                     config: runner.RuleOptionsT = None):
        """Run playbook.
        """
        rnr = self.get_runner(config)
        if env:
            with unittest.mock.patch.dict(os.environ, env):
                return rnr.run_playbook(filepath)

        return rnr.run_playbook(filepath)

    def list_resources(self, success: bool = True,
                       subdir: typing.Optional[str] = None,
                       pattern: typing.Optional[str] = None):
        """
        List test resource data matches given subdir and patterns.
        """
        files = utils.list_resources(self.name, success=success,
                                     subdir=subdir, pattern=pattern)
        self.assertTrue(files,
                        'Failed to find test resource data: '
                        f'success={success}, subdir={subdir}'
                        f'pattern={pattern}')
        return files

    def lint(self, success: bool = True,
             subdir: typing.Optional[str] = None,
             pattern: typing.Optional[str] = None,
             env: typing.Optional[typing.Dict] = None,
             config: runner.RuleOptionsT = None):
        """
        Run the lint rule's check to given resource data files.
        """
        if not self.initialized:
            return

        files = self.list_resources(success=success, subdir=subdir,
                                    pattern=pattern)
        for filepath in files:
            res = self.run_playbook(filepath, env=env, config=config)
            msg = f'{filepath}, {res!r}, {env!r}, {config!r}'
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

        skip_list = [rid for rid in runner.list_rule_ids()
                     if rid != self.rule.id]
        self.config = dict(skip_list=skip_list)
        self.cmd = f'ansible-lint -r {constants.RULES_DIR!s}'.split()

    def dump_config(self, stream: typing.IO):
        """
        Generate .ansible-lint configurations as a string.
        """
        yaml.safe_dump(self.config, stream)

    def lint(self, success: bool = True,
             subdir: typing.Optional[str] = None,
             pattern: typing.Optional[str] = None,
             env: typing.Optional[typing.Dict] = None,
             config: runner.RuleOptionsT = None):
        """
        Run ansible-lint with given arguments in given env.
        """
        if not self.initialized:
            return

        oenv = os.environ.copy()
        if env:
            oenv.update(**env)

        if config:
            self.config['rules'] = {self.rule.id: config}

        files = self.list_resources(success=success, subdir=subdir,
                                    pattern=pattern)

        with tempfile.NamedTemporaryFile(mode='w') as cio:
            self.dump_config(cio)

            for filepath in files:
                res = subprocess.run(
                    self.cmd + ['-c', cio.name, filepath],
                    stdout=subprocess.PIPE, check=False, env=oenv
                )
                args = (res.returncode, 0, res.stdout.decode('utf-8'))
                if success:
                    self.assertEqual(*args)
                else:
                    self.assertNotEqual(*args)

# vim:sw=4:ts=4:et:
