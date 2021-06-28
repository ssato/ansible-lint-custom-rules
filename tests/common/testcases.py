# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Common utility classes for test cases.
"""
import os
import subprocess
import tempfile
import unittest
import unittest.mock

import yaml

from . import base, constants, runner


class RuleTestCase(unittest.TestCase):
    """Base class to test rules.
    """
    base_cls = base.Base

    def setUp(self):
        """Setup
        """
        self.base = self.base_cls()

    def tearDown(self):
        """De-initialize.
        """
        self.base.clear()

    def lint(self, success: bool = True) -> None:
        """
        Run the lint rule's check to given resource data files.
        """
        if not self.base.is_ready():
            return

        for data in self.base.load_datasets(success=success):
            conf = data.conf.get('rules', {}).get(self.base.id, {})
            if data.env is None or not data.env:
                res = self.base.run_playbook(data.inpath, config=conf)
            else:
                with unittest.mock.patch.dict(os.environ, data.env):
                    res = self.base.run_playbook(data.inpath, config=conf)
                    # for debug:
                    # msg = f'{data!r}, {conf!r}, {res!r}, {os.environ!r}'

            msg = f'{data!r}, {conf!r}, {res!r}'
            if success:
                self.assertEqual(0, len(res), msg)  # No errors.
            else:
                self.assertTrue(len(res) > 0, msg)  # It should fail.

            self.base.clear()

    def test_ok_cases(self):
        """OK test cases"""
        self.lint()

    def test_ng_cases(self):
        """NG test cases"""
        self.lint(success=False)


class CliTestCase(RuleTestCase):
    """Base class to test rules with CLI.
    """
    def setUp(self):
        """Set up members."""
        super().setUp()

        if not self.base.is_ready():
            return

        skip_list = [
            rid for rid in runner.list_rule_ids() if rid != self.base.id
        ]
        self.config = dict(skip_list=skip_list)
        self.cmd = f'ansible-lint -r {constants.RULES_DIR!s}'.split()

    def lint(self, success: bool = True):
        """
        Run ansible-lint with given arguments and config files.
        """
        if not self.base.is_ready():
            return

        for data in self.base.load_datasets(success=success):
            with tempfile.NamedTemporaryFile(mode='w') as cio:
                conf = self.config.copy()
                if data.conf:
                    conf.update(data.conf)

                yaml.safe_dump(conf, cio)

                env = os.environ.copy()
                if data.env is not None and data.env:
                    env.update(data.env)

                res = subprocess.run(
                    self.cmd + ['-c', cio.name, str(data.inpath)],
                    stdout=subprocess.PIPE, check=False, env=env
                )
                args = (res.returncode, 0, res.stdout.decode('utf-8'))
                if success:
                    self.assertEqual(*args)
                else:
                    self.assertNotEqual(*args)

# vim:sw=4:ts=4:et:
