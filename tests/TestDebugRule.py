# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, DebugRule.
"""
import typing

from rules import DebugRule as TT
from tests import common


class Base(common.Base):
    this_mod: common.MaybeModT = TT
    clear_fns: typing.List[typing.Callable] = [TT.is_enabled.cache_clear]


class RuleTestCase(common.RuleTestCase):
    base_cls = Base

    def test_base_get_filename(self):
        self.assertEqual(self.base.get_filename(), 'TestDebugRule.py')

    def test_base_get_rule_name(self):
        self.assertEqual(self.base.get_rule_name(), 'DebugRule')

    def test_base_get_rule_instance_by_name(self):
        rule = self.base.get_rule_instance_by_name(self.base.name)
        self.assertTrue(bool(rule))
        self.assertTrue(isinstance(rule, type(self.base.rule)))

    def test_base_is_runnable(self):
        self.assertTrue(self.base.is_runnable())

    def test_base_load_datasets(self):
        self.assertTrue(self.base.load_datasets())
        self.assertTrue(self.base.load_datasets(False))


class CliTestCase(common.CliTestCase):
    base_cls = Base
