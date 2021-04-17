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


_ENV_PATCH = {TT.ENABLE_THIS_RULE_ENVVAR: '1'}


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    clear_fn: common.MaybeCallableT = TT.is_enabled.cache_clear


class RuleTestCase(Base, common.RuleTestCase):
    def test_20_ng_cases(self):
        self.lint(False, subdir='ok', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    def test_20_ng_cases(self):
        self.lint(False, subdir='ok', env=_ENV_PATCH)
