# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, LoopIsRecommendedRule.
"""
import pytest

from rules import LoopIsRecommendedRule as TT
from tests import common


class Base:
    this_py = __file__
    this_mod = TT


class RuleTestCase(Base, common.RuleTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_20_ng_cases(self):
        self.lint(success=False)


class CliTestCase(Base, common.CliTestCase):
    pass
