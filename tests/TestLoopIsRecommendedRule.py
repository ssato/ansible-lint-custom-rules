# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-class-docstring
"""Test cases for the rule, LoopIsRecommendedRule.
"""
from rules import LoopIsRecommendedRule as TT
from tests import common as C


class Base:
    name = C.get_rule_name(__file__)
    rule = C.get_rule_instance_by_name(TT, name)


class RuleTestCase(Base, C.RuleTestCase):
    pass


class CliTestCase(Base, C.CliTestCase):
    pass
