# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Test cases for the rule, VarsShouldNotBeUsedRule.
"""
from rules import VarsShouldNotBeUsedRule as TT
from tests import common as C


class Base(object):
    """Base Mixin class."""
    prefix = "VarsShouldNotBeUsedRule"
    rule = getattr(TT, prefix)()


class RuleTestCase(Base, C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, VarsShouldNotBeUsedRule.
    """
    pass


class CliTestCase(Base, C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, VarsShouldNotBeUsedRule.
    """
    pass
