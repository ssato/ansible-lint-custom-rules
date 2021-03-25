# Copyright (C) 2020, 2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases for the rule, DebugRule.
"""
import os
import unittest.mock

from rules import DebugRule as TT
from tests import common as C


_ENV_PATCH = {TT.ENABLE_THIS_RULE_ENVVAR: "1"}


class Base:
    name = C.get_rule_name(__file__)
    rule = C.get_rule_instance_by_name(TT, name)
    clear_fn = TT.is_enabled.cache_clear


class RuleTestCase(Base, C.RuleTestCase):
    @unittest.mock.patch.dict(os.environ, _ENV_PATCH)
    def test_20_ng_cases(self):
        self.lint(False, search='ok')


class CliTestCase(Base, C.CliTestCase):
    def test_20_ng_cases(self):
        self.lint(False, search='ok', env=_ENV_PATCH)
