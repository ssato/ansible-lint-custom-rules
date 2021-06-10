# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, VarsShouldNotBeUsedRule.
"""
import pytest

from rules import VarsShouldNotBeUsedRule as TT
from tests import common


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    clear_fn: common.MaybeCallableT = TT.contains_vars_directive.cache_clear

    use_lint_v2 = True


@pytest.mark.parametrize(
    'path,expected',
    [(str(common.TESTS_RES_DIR / 'VarsShouldNotBeUsedRule/ok/0.yml'), False),
     (str(common.TESTS_RES_DIR / 'VarsShouldNotBeUsedRule/ng/0.yml'), True),
     (str(common.TESTS_RES_DIR / 'VarsShouldNotBeUsedRule/ng/1.yml'), True),
     ]
)
def test_contains_vars_directive(path, expected):
    assert TT.contains_vars_directive(path) == expected
    Base.clear_fn()


class RuleTestCase(Base, common.RuleTestCase):
    pass


class CliTestCase(Base, common.CliTestCase):
    @pytest.mark.skip(reason="until resolving unknown 'parser-error'")
    def test_10_ok_cases(self):
        pass
