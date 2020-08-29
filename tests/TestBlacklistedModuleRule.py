# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Test cases for the rule, BlacklistedModuleRule.
"""
import mock
import os.path
import os

from rules import BlacklistedModuleRule as TT
from tests import common as C


_BLACKLIST_PATH = os.path.join(
    C.CURDIR, "res", "BlacklistedModuleRule_blacklist.txt"
)
_ENV_PATCH_0 = {TT.BLACKLIST_ENVVAR: _BLACKLIST_PATH}
_ENV_PATCH_1 = {TT.BLACKLISTED_MODULES_ENVVAR: "ping"}


class Test_functions(C.unittest.TestCase):
    """Test cases for functions in rules.BlacklistedModuleRule.
    """
    def setUp(self):
        TT.blacklisted_modules.cache_clear()  # clear the memoized results.

    def test_10_blacklisted_modules__env_var(self):
        self.assertEqual(TT.blacklisted_modules(), TT.BLACKLISTED_MODULES)

    @mock.patch.dict(os.environ, _ENV_PATCH_0)
    def test_20_blacklisted_modules__blacklist_file(self):
        ref = [line.strip() for line in open(_BLACKLIST_PATH)]
        self.assertEqual(TT.blacklisted_modules(), ref)

    @mock.patch.dict(os.environ, _ENV_PATCH_1)
    def test_30_blacklisted_modules__env_var(self):
        self.assertEqual(TT.blacklisted_modules(), ["ping"])


class TestBlacklistedModuleRule(C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, BlacklistedModuleRule.
    """
    rule = TT.BlacklistedModuleRule()
    prefix = "BlacklistedModuleRule"

    def setUp(self):
        super(TestBlacklistedModuleRule, self).setUp()
        TT.blacklisted_modules.cache_clear()

    @mock.patch.dict(os.environ, _ENV_PATCH_1)
    def test_30_ng_cases__env(self):
        pats = self.prefix + "*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)


class TestCliBlacklistedModuleRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, BlacklistedModuleRule.
    """
    rule = TT.BlacklistedModuleRule()
    prefix = "BlacklistedModuleRule"
    clear_fn = TT.blacklisted_modules.cache_clear

    def test_30_ng_cases__env(self):
        self._run_for_playbooks(self.prefix + "*ok*.yml", False,
                                env=_ENV_PATCH_1)
