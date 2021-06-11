# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Common utility classes for test cases.
"""
import subprocess
import types
import typing
import tempfile
import unittest

import yaml

from . import constants, runner, utils


MaybeModNameT = typing.Optional[str]
MaybeModT = typing.Optional[types.ModuleType]
MaybeCallableT = typing.Optional[typing.Callable]


def cache_clear_itr(maybe_memoized_fns: typing.Iterable[typing.Any]
                    ) -> typing.Callable[..., None]:
    """Yield callable object from ``maybe_memoized_fns``.
    """
    for candidate in maybe_memoized_fns:
        if candidate and callable(candidate):
            clear_fn = getattr(candidate, 'cache_clear', False)
            if clear_fn and callable(clear_fn):
                yield clear_fn


class BaseTestCase(unittest.TestCase):
    """Base class for test cases.
    """
    # .. todo::
    #    I don't know how to compute and set them in test case classes in
    #    modules import this module.
    this_py: MaybeModNameT = None
    this_mod: MaybeModT = None

    clear_fn: MaybeCallableT = None
    memoized: typing.List[str] = []

    initialized: bool = False

    def clear(self):
        """Call clear function if it's callable.
        """
        if not self.initialized:
            return

        for clear_fn in self.clear_fns:
            if clear_fn and callable(clear_fn):
                clear_fn()  # pylint: disable=not-callable

    def init(self):
        """Initialize.
        """
        if not self.this_py or not self.this_mod:
            return

        self.name = utils.get_rule_name(self.this_py)
        self.rule = utils.get_rule_instance_by_name(self.this_mod, self.name)

        self.clear_fns = [
            self.clear_fn, self.rule.get_config.cache_clear
        ] + list(
            cache_clear_itr(
                getattr(self.rule, n, False) for n in self.memoized
            )
        )
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
                     config: runner.RuleOptionsT = None):
        """Run playbook.
        """
        return self.get_runner(config).run_playbook(filepath)

    def load_datasets(self, success: bool = True):
        """Load datasets.
        """
        datasets = sorted(
            utils.each_test_data_for_rule(self.name, success=success)
        )
        if not datasets:
            raise OSError(f'{self.name}: No test data found [{success}]')

        return datasets

    def lint(self, success: bool = True) -> None:
        """
        Run the lint rule's check to given resource data files.
        """
        if not self.initialized:
            return

        for data in self.load_datasets(success=success):
            conf = data.conf.get('rules', {}).get(self.rule.id, {})
            res = self.run_playbook(data.inpath, config=conf)
            msg = f'{data!r}, {conf!r}, {res!r}'
            if success:
                self.assertEqual(0, len(res), msg)  # No errors.
            else:
                self.assertTrue(len(res) > 0, msg)  # It should fail.

            self.clear()

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
        """Set up members.
        """
        if not self.this_py or not self.this_mod:
            return

        self.init()

        skip_list = [rid for rid in runner.list_rule_ids()
                     if rid != self.rule.id]
        self.config = dict(skip_list=skip_list)
        self.cmd = f'ansible-lint -r {constants.RULES_DIR!s}'.split()

    def dump_config(self, stream: typing.IO,
                    conf: typing.Optional[
                        typing.Dict[str, typing.Any]
                    ] = None) -> None:
        """
        Generate .ansible-lint configurations as a string.
        """
        yaml.safe_dump(conf if conf else self.config, stream)

    def lint(self, success: bool = True):
        """
        Run ansible-lint with given arguments and config files.
        """
        if not self.initialized:
            return

        for data in self.load_datasets(success=success):
            with tempfile.NamedTemporaryFile(mode='w') as cio:
                conf = self.config.copy()
                if data.conf:
                    conf.update(data.conf)

                self.dump_config(cio, conf)

                res = subprocess.run(
                    self.cmd + ['-c', cio.name, str(data.inpath)],
                    stdout=subprocess.PIPE, check=False
                )
                args = (res.returncode, 0, res.stdout.decode('utf-8'))
                if success:
                    self.assertEqual(*args)
                else:
                    self.assertNotEqual(*args)

# vim:sw=4:ts=4:et:
