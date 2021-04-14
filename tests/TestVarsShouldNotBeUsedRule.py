# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, VarsShouldNotBeUsedRule.
"""
from rules import VarsShouldNotBeUsedRule as TT
from tests import common


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT


class RuleTestCase(Base, common.RuleTestCase):
    pass


class CliTestCase(Base, common.CliTestCase):
    pass
