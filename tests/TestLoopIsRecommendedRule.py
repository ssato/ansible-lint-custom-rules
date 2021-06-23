# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, LoopIsRecommendedRule.
"""
from rules import LoopIsRecommendedRule as TT
from tests import common


class Base:
    this_mod: common.MaybeModT = TT


class RuleTestCase(Base, common.RuleTestCase):
    pass


class CliTestCase(Base, common.CliTestCase):
    pass
