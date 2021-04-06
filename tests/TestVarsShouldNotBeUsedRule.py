# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, VarsShouldNotBeUsedRule.
"""
import pytest

from rules import VarsShouldNotBeUsedRule as TT
from tests import common


class Base:
    this_py = __file__
    this_mod = TT


class RuleTestCase(Base, common.RuleTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_10_ok_cases(self):
        super().test_10_ok_cases()


class CliTestCase(Base, common.CliTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_10_ok_cases(self):
        super().test_10_ok_cases()
