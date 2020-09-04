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


class TestFileIsSmallEnoughRule(C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, FileIsSmallEnoughRule.
    """
    rule = TT.FileIsSmallEnoughRule()
    prefix = "FileIsSmallEnoughRule"

    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_20_ng_cases(self):
        TT.max_lines.cache_clear()  # clear the memoized results.
        self.lint(False, self.path_pattern())


class TestCliFileIsSmallEnoughRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, FileIsSmallEnoughRule.
    """
    rule = TT.FileIsSmallEnoughRule()
    prefix = "FileIsSmallEnoughRule"
    clear_fn = TT.max_lines.cache_clear

    def test_20_ng_cases(self):
        self.lint(False, "ng", _ENV_PATCH)

    def test_30_ng_cases__env(self):
        self.lint(False, "ok", _ENV_PATCH)
