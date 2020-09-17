# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Test cases for the rule, BlacklistedModuleRule.
"""
import os

import mock

from rules import BlacklistedModuleRule as TT
from tests import common as C


_BLACKLIST_PATH = str(
    C.CURDIR / "res" / "BlacklistedModuleRule" / "blacklist.txt"
)
_ENV_PATCH_0 = {TT.BLACKLIST_ENVVAR: _BLACKLIST_PATH}
_ENV_PATCH_1 = {TT.BLACKLISTED_MODULES_ENVVAR: "ping"}


class Base(object):
    """Base Mixin class."""
    prefix = "BlacklistedModuleRule"
    rule = getattr(TT, prefix)()
    clear_fn = TT.blacklisted_modules.cache_clear


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


class RuleTestCase(Base, C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, BlacklistedModuleRule.
    """
    @mock.patch.dict(os.environ, _ENV_PATCH_1)
    def test_30_ng_cases__env(self):
        self.lint(False, self.path_pattern())


class CliTestCase(Base, C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, BlacklistedModuleRule.
    """
    def test_30_ng_cases__env(self):
        self.lint(False, self.path_pattern("ok"), _ENV_PATCH_1)
