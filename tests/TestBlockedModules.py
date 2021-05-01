# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, BlockedModules.
"""
from rules import BlockedModules as TT
from tests import common


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    rule_memoized = ['blocked_modules']


class RuleTestCase(Base, common.RuleTestCase):
    def test_20_ng_cases(self):
        self.lint(False, 'ok', config=dict(blocked=['ping']))


class CliTestCase(Base, common.CliTestCase):
    def test_20_ng_cases__env(self):
        self.lint(False, 'ok', config=dict(blocked=['ping']))
