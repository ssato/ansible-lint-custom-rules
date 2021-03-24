# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Common utility test routines and classes.
"""
import functools
import os
import pathlib
import subprocess
import typing
import unittest

import ansiblelint.utils

from ansiblelint.rules import RulesCollection
from ansiblelint.runner import Runner


CURDIR: pathlib.Path = pathlib.Path(__file__).resolve().parent

RULES_SUBDIR = 'rules'

RULES_DIR: str = str(CURDIR.parent / RULES_SUBDIR)
DEFAULT_RULES_DIR: str = str(
    pathlib.Path(ansiblelint.utils.__file__).parent / RULES_SUBDIR
)


def strip_words(astr: str, *words: str) -> str:
    """strip given words from ``astr`` one by one.
    """
    return functools.reduce(lambda acc, word: acc.replace(word, ''),
                            words, astr)


def list_resources(name: str, success: bool = True,
                   search: typing.Optional[str] = None
                   ) -> typing.List[str]:
    """
    List resource data files for OK or NG test cases.
    """
    if not search:
        search = 'ok' if success else 'ng'

    pattern = f"*{search}*.*"
    files = sorted(str(p) for p in (CURDIR / 'res' / name).glob(pattern))
    if not files:
        raise RuntimeError(f"No resource data files: { pattern }")

    return files


def get_rule_name(file_: str = __file__) -> str:
    """
    Resolve the name of the rule to test from the filename of the test code.
    """
    return strip_words(pathlib.Path(file_).name, '.py', 'test_', 'Test')


def get_rule_instance_by_name(rule_module, rule_name):
    rule_cls = getattr(rule_module, rule_name)
    if not rule_cls:
        raise ValueError(f"No such rule class {rule_name} "
                         f"in {rule_module!r}.")
    return rule_cls()


class RuleTestCase(unittest.TestCase):
    """Base class to test ansible-lint rules.
    """
    name = None
    rule = None
    clear_fn: typing.Optional[typing.Callable] = None

    def setUp(self):
        """Initialize lint rules collection.
        """
        if not self.rule or not self.name:
            return

        # Collect the default rules and add the rule to test.
        self.rules = RulesCollection()
        self.rules.register(self.rule)

        if callable(self.clear_fn):
            self.clear_fn()  # pylint: disable=not-callable

    def list_resources(self, success: bool = True,
                       search: typing.Optional[str] = None
                       ) -> typing.List[str]:
        return list_resources(self.name, success=success,
                              search=search)

    def lint(self, success: bool = True,
             search: typing.Optional[str] = None):
        """
        Run the lint rule's check to given resource data files.
        """
        if not self.rule or not self.name:
            return

        for filepath in self.list_resources(success, search=search):
            runner = Runner(self.rules, filepath, [], [], [])
            res = runner.run()
            if success:
                self.assertEqual(0, len(res), res)  # No errors
            else:
                self.assertTrue(len(res) > 0, res)  # Something went wrong

    def test_10_ok_cases(self):
        self.lint()

    def test_20_ng_cases(self):
        self.lint(False)


def list_rule_ids_itr() -> typing.Iterator[str]:
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


class CliTestCase(RuleTestCase):
    """Run ok and ng CLI test cases automatically.
    """
    def setUp(self):
        super().setUp()

        excl_opt = ' '.join(("-x {!s}".format(rid)
                             for rid in list_rule_ids_itr()
                             if rid != getattr(self.rule, "id", None)))
        self.cmd = f"ansible-lint -r { RULES_DIR } { excl_opt }".split()

    # pylint: disable=arguments-differ
    def lint(self, success: bool = True,
             search: typing.Optional[str] = None,
             env: typing.Optional[typing.Dict] = None):
        """
        Run ansible-lint with given arguments in given env.
        """
        if not self.rule or not self.name:
            return

        oenv = os.environ.copy()
        if env:
            oenv.update(**env)

        for filepath in self.list_resources(success, search=search):
            res = subprocess.run(
                self.cmd + [filepath], stdout=subprocess.PIPE, check=False,
                env=oenv
            )
            if success:
                self.assertEqual(res.returncode, 0, res.stdout.decode("utf-8"))
            else:
                self.assertNotEqual(res.returncode, 0,
                                    res.stdout.decode("utf-8"))

# vim:sw=4:ts=4:et:
