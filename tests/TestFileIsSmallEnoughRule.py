# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Test cases for the rule, PlaybookFileIsNotLarge.
"""
import os
import mock

from rules import FileIsSmallEnoughRule as TT
from tests import common as C


_ENV_PATCH = {TT.MAX_LINES_ENVVAR: "3"}


class TestFileIsSmallEnoughRule(C.AutoTestCasesForAnsibleLintRule):
    """Test cases for the rule class, FileIsSmallEnoughRule.
    """
    rule = TT.FileIsSmallEnoughRule()
    prefix = "FileIsSmallEnoughRule"

    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_20_ng_cases(self):
        TT.max_lines.cache_clear()  # clear the memoized results.

        pats = self.prefix + "*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)