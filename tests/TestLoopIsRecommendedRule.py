# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Test cases for the rule, LoopIsRecommendedRule.
"""
from rules import LoopIsRecommendedRule as TT
from tests import common as C


class Base(object):
    """Base Mixin class."""
    prefix = "LoopIsRecommendedRule"
    rule = getattr(TT, prefix)()


class RuleTestCase(Base, C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, LoopIsRecommendedRule.
    """
    pass


class CliTestCase(Base, C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, LoopIsRecommendedRule.
    """
    pass
