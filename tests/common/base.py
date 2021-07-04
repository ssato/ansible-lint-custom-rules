# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""An abstract class to help to collect test data and tests for target rule.
"""
import inspect
import pathlib
import re
import types
import typing

from . import constants, runner, utils


MaybeModT = typing.Optional[types.ModuleType]

# Try to resolve the name of the rule class from the name of the test code. For
# example, name will be resolved to 'DebugRule' if the test code for the rule
# DebugRule is TestDebugRule.py.
RULE_NAME_RE: typing.Pattern = re.compile(
    r'^test_?(\w+).py$',
    re.IGNORECASE | re.ASCII
)


class Base:
    """Base class for test rule cases.
    """
    # .. todo::
    #    I don't know how to compute and set them in test case classes in
    #    modules import this module.
    this_mod: MaybeModT = None

    clear_fns: typing.List[typing.Callable] = []
    memoized: typing.List[str] = []

    use_default_rules: bool = False

    @classmethod
    def is_runnable(cls):
        """
        This class is not runnable but chidlren classes have the appropriate
        member this_mod should be runnable.
        """
        return bool(cls.this_mod)

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

    @classmethod
    def get_test_data_dir(cls,
                          root: pathlib.Path = constants.TESTS_RES_DIR
                          ) -> pathlib.Path:
        """Get the top dir to keep test data for this rule.
        """
        return root / cls.get_rule_name()

    def __init__(self):
        """Initialize."""
        if not self.is_runnable():
            return

        # .. note::
        #    The followings only happen in children classes inherits this and
        #    have appropriate self.this_mod.
        self.name = self.get_rule_name()
        self.rule = self.get_rule_instance_by_name(self.name)
        self.id = self.rule.id

        self.clear_fns.append(self.rule.get_config.cache_clear)
        self.clear_fns.extend(
            utils.each_clear_fn(
                getattr(self.rule, n, False) for n in self.memoized
            )
        )

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

    def run_playbook(self, filepath: str,
                     config: runner.RuleOptionsT = None,
                     skip_list: typing.Optional[typing.List[str]] = None):
        """Run playbook.
        """
        return self.get_runner(config).run_playbook(filepath, skip_list)

    def load_datasets(self, success: bool = True,
                      root: pathlib.Path = constants.TESTS_RES_DIR):
        """Load datasets.
        """
        datadir = self.get_test_data_dir(root)
        datasets = sorted(
            utils.each_test_data_for_rule(datadir, success=success)
        )
        if not datasets:
            raise OSError(f'{self.name}: No test data found [{success}]')

        return datasets

# vim:sw=4:ts=4:et:
