# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases for the rule, BlacklistedModuleRule.
"""
import os
import unittest.mock

from rules import BlacklistedModuleRule as TT
from tests import common as C


_BLACKLIST_PATH = str(
    C.CURDIR / "res" / "BlacklistedModuleRule" / "blacklist.txt"
)
_ENV_PATCH_0 = {TT.BLACKLIST_ENVVAR: _BLACKLIST_PATH}
_ENV_PATCH_1 = {TT.BLACKLISTED_MODULES_ENVVAR: "ping"}


class Base:
    name = C.get_rule_name(__file__)
    rule = C.get_rule_instance_by_name(TT, name)
    clear_fn = TT.blacklisted_modules.cache_clear


class Test_functions(C.unittest.TestCase):
    def setUp(self):
        TT.blacklisted_modules.cache_clear()  # clear the memoized results.

    def test_10_blacklisted_modules__env_var(self):
        self.assertEqual(TT.blacklisted_modules(), TT.BLACKLISTED_MODULES)

    @unittest.mock.patch.dict(os.environ, _ENV_PATCH_0)
    def test_20_blacklisted_modules__blacklist_file(self):
        ref = [line.strip() for line in open(_BLACKLIST_PATH)]
        self.assertEqual(TT.blacklisted_modules(), ref)

    @unittest.mock.patch.dict(os.environ, _ENV_PATCH_1)
    def test_30_blacklisted_modules__env_var(self):
        self.assertEqual(TT.blacklisted_modules(), ["ping"])


class RuleTestCase(Base, C.RuleTestCase):
    @unittest.mock.patch.dict(os.environ, _ENV_PATCH_1)
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok')


class CliTestCase(Base, C.CliTestCase):
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok', _ENV_PATCH_1)
