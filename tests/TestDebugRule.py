# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Test cases for the rule, DebugRule.
"""
import os
import mock

from rules import DebugRule as TT
from tests import common as C


_ENV_PATCH = {TT.ENABLE_THIS_RULE_ENVVAR: "1"}


class Base(object):
    """Base Mixin class."""
    prefix = "DebugRule"
    rule = getattr(TT, prefix)()
    clear_fn = TT.is_enabled.cache_clear


class RuleTestCase(Base, C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, DebugRule.
    """
    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_20_ng_cases(self):
        self.lint(False, self.path_pattern())


class CliTestCase(Base, C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, DebugRule.
    """
    def test_20_ng_cases(self):
        self.lint(False, self.path_pattern(), _ENV_PATCH)
