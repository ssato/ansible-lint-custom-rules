# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Common utility classes for test cases.
"""
import inspect
import pathlib
import re
import subprocess
import types
import typing
import tempfile
import unittest

import yaml

from . import constants, runner, utils


MaybeModT = typing.Optional[types.ModuleType]

RULE_NAME_RE: typing.Pattern = re.compile(r'^test_?(\w+).py$',
                                          re.IGNORECASE | re.ASCII)


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
    this_mod: MaybeModT = None

    clear_fns: typing.List[typing.Callable] = []
    memoized: typing.List[str] = []

    use_default_rules: bool = False

    initialized: bool = False

    @classmethod
    def get_filename(cls) -> str:
        """Resolve and get the filename of self like __file___ dynamically.

        .. note::
           This must be a class method because inspect.getfile(self) fails.

        .. note::
           The test case of this method is implemented in tests.TestDebugRule.
        """
        return pathlib.Path(inspect.getfile(cls)).name

    @classmethod
    def get_rule_name(cls) -> str:
        """Resolve the name of the target rule by filename (__file__).

        .. note::
           The test case of this method is implemented in tests.TestDebugRule.
        """
        match = RULE_NAME_RE.match(cls.get_filename())
        if match:
            return match.groups()[0]

        return ''

    @classmethod
    def get_rule_instance_by_name(cls, rule_name):
        """Get the rule instance to test.
        """
        rule_cls = getattr(cls.this_mod, rule_name)
        if not rule_cls:
            raise ValueError(f'No such rule class {rule_name} '
                             f'in {cls.this_mod!r}.')
        return rule_cls()

    def init(self):
        """Initialize.
        """
        if self.this_mod is None or not self.this_mod:
            return

        # .. note::
        #    The followings only happen in children classes inherits this and
        #    have appropriate self.this_mod.
        self.name = self.get_rule_name()
        self.rule = self.get_rule_instance_by_name(self.name)

        self.clear_fns.append(self.rule.get_config.cache_clear)
        self.clear_fns.extend(
            cache_clear_itr(
                getattr(self.rule, n, False) for n in self.memoized
            )
        )

        self.initialized = True

    def clear(self):
        """Call clear function if it's callable.
        """
        for clear_fn in self.clear_fns:
            clear_fn()  # pylint: disable=not-callable

    def get_runner(self, config: runner.RuleOptionsT = None
                   ) -> runner.RunFromFile:
        """
        Make ansiblelint.RulesCollection instance registered the rule with
        given config and get runner.RunFromFile instance from it.
        """
        collection = runner.get_collection(
            self.rule, rule_options=config,
            use_default_rules=self.use_default_rules
        )
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
        if self.this_mod is None or not self.this_mod:
            return

        self.init()

        skip_list = [
            rid for rid in runner.list_rule_ids() if rid != self.rule.id
        ]
        self.config = dict(skip_list=skip_list)
        self.cmd = f'ansible-lint -r {constants.RULES_DIR!s}'.split()

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

                yaml.safe_dump(conf, cio)

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
