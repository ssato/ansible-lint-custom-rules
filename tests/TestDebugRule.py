# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, DebugRule.
"""
from rules import DebugRule as TT
from tests import common


class Base(common.Base):
    this_mod: common.MaybeModT = TT


class RuleTestCase(common.RuleTestCase):
    base_cls = Base

    def test_get_filename(self):
        self.assertEqual(self.base.get_filename(), 'TestDebugRule.py')

    def test_get_rule_name(self):
        self.assertEqual(self.base.get_rule_name(), 'DebugRule')


class CliTestCase(common.CliTestCase):
    base_cls = Base
