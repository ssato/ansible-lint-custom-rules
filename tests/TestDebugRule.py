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


class TestDebugRule(C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, DebugRule.
    """
    rule = TT.DebugRule()
    prefix = "DebugRule"

    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_ng_cases__env(self):
        TT.is_enabled.cache_clear()
        self.lint(False, self.path_pattern())


class TestCliDebugRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, DebugRule.
    """
    rule = TT.DebugRule()
    prefix = "DebugRule"
    clear_fn = TT.is_enabled.cache_clear

    def test_30_ng_cases__env(self):
        self._run_for_playbooks(self.prefix + "*ok*.yml", False,
                                env=_ENV_PATCH)
