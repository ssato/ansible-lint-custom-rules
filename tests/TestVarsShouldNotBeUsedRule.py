# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, VarsShouldNotBeUsedRule.
"""
import typing

import pytest

from rules import VarsShouldNotBeUsedRule as TT
from tests import common


_CLEAR_FN = TT.contains_vars_directive.cache_clear


class Base(common.Base):
    this_mod: common.MaybeModT = TT
    clear_fns: typing.List[typing.Callable] = [_CLEAR_FN]


@pytest.mark.parametrize(
    'path,expected',
    [(str(common.TESTS_RES_DIR / 'VarsShouldNotBeUsedRule/ok/0.yml'), False),
     (str(common.TESTS_RES_DIR / 'VarsShouldNotBeUsedRule/ng/0.yml'), True),
     (str(common.TESTS_RES_DIR / 'VarsShouldNotBeUsedRule/ng/1.yml'), True),
     ]
)
def test_contains_vars_directive(path, expected):
    assert TT.contains_vars_directive(path) == expected
    _CLEAR_FN()


class RuleTestCase(common.RuleTestCase):
    base_cls = Base


class CliTestCase(common.CliTestCase):
    base_cls = Base
