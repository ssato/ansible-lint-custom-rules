# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Test cases for the rule, FileIsUnixFile.py.
"""
from rules import FileIsUnixFileRule as TT
from tests import common as C


class TestFileIsUnixFileRule(C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, FileIsUnixFileRule.
    """
    rule = TT.FileIsUnixFileRule()
    prefix = "FileIsUnixFileRule"


class TestCliFileIsUnixFileRule(C.CliTestCasesForAnsibleLintRule):
    """CLI Test cases for the rule class, FileIsUnixFileRule.
    """
    rule = TT.FileIsUnixFileRule()
    prefix = "FileIsUnixFileRule"
