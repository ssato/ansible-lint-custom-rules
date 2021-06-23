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


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT


class RuleTestCase(Base, common.RuleTestCase):

    def test_get_filename(self):
        self.assertEqual(self.get_filename(), 'TestDebugRule.py')

    def test_get_rule_name(self):
        self.assertEqual(self.get_rule_name(), 'DebugRule')


class CliTestCase(Base, common.CliTestCase):
    pass
