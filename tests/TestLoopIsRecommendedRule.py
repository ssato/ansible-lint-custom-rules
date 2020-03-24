# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
from rules import LoopIsRecommendedRule as TT
from tests import common as C


class TestLoopIsRecommendedRule(C.AnsibleLintRuleTestBase):

    rule = TT.LoopIsRecommendedRule()

    def test_10_with_is_used_in_tasks__ng(self):
        pats = "LoopIsRecommendedRule*ng*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)

    def test_20_with_is_used_in_tasks__ok(self):
        pats = "LoopIsRecommendedRule*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)
