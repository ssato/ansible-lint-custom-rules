# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, BlacklistedModuleRule.
"""
import os
import unittest
import unittest.mock

import pytest

from rules import BlacklistedModuleRule as TT
from tests import common


_BLACKLIST_PATH = str(
    common.TESTS_DIR / 'res' / 'BlacklistedModuleRule' / 'blacklist.txt'
)
_ENV_PATCH_0 = {TT.BLACKLIST_ENVVAR: _BLACKLIST_PATH}
_ENV_PATCH_1 = {TT.BLACKLISTED_MODULES_ENVVAR: 'ping'}


class Base:
    this_py = __file__
    this_mod = TT
    clear_fn = TT.blacklisted_modules.cache_clear


class Test_functions(unittest.TestCase):
    def setUp(self):
        TT.blacklisted_modules.cache_clear()  # clear the memoized results.

    def test_10_blacklisted_modules__env_var(self):
        self.assertTrue('shell' in TT.BLACKLISTED_MODULES)
        self.assertEqual(TT.blacklisted_modules(), TT.BLACKLISTED_MODULES)

    @unittest.mock.patch.dict(os.environ, _ENV_PATCH_0)
    def test_20_blacklisted_modules__blacklist_file(self):
        ref = [line.strip() for line in open(_BLACKLIST_PATH)]
        self.assertEqual(TT.blacklisted_modules(), ref)

    @unittest.mock.patch.dict(os.environ, _ENV_PATCH_1)
    def test_30_blacklisted_modules__env_var(self):
        self.assertEqual(TT.blacklisted_modules(), ['ping'])


class RuleTestCase(Base, common.RuleTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_20_ng_cases(self):
        self.lint(False)

    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok', env=_ENV_PATCH_1)


class CliTestCase(Base, common.CliTestCase):
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok', env=_ENV_PATCH_1)
