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


class Base(object):
    """Base Mixin class."""
    prefix = "FileIsSmallEnoughRule"
    rule = getattr(TT, prefix)()
    clear_fn = TT.max_lines.cache_clear


class RuleTestCase(Base, C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, FileIsSmallEnoughRule.
    """
    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_20_ng_cases(self):
        self.lint(False, self.path_pattern())


class CliTestCase(Base, C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, FileIsSmallEnoughRule.
    """
    def test_20_ng_cases(self):
        self.lint(False, self.path_pattern(), _ENV_PATCH)
