# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Test cases for the rule, BlacklistedModuleRule.
"""
from rules import BlacklistedModuleRule as TT
from tests import common as C


class TestBlacklistedModuleRule(C.AutoTestCasesForAnsibleLintRule):
    """Test cases for the rule class, BlacklistedModuleRule.
    """
    rule = TT.BlacklistedModuleRule()
    prefix = "BlacklistedModuleRule"
