# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Test cases for the rule, VarsShouldNotBeUsedRule.
"""
from rules import VarsShouldNotBeUsedRule as TT
from tests import common as C


class TestVarsShouldNotBeUsedRule(C.AutoTestCasesForAnsibleLintRule):
    """Test cases for the rule class, VarsShouldNotBeUsedRule.
    """

    rule = TT.VarsShouldNotBeUsedRule()
    prefix = "VarsShouldNotBeUsedRule"
