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


RES_DIR = common.TESTS_RES_DIR / 'VarsShouldNotBeUsedRule'


class Base(common.Base):
    this_mod: common.MaybeModT = TT


@pytest.mark.parametrize(
    ('path', 'expected'),
    ((str(RES_DIR / 'ok/0/plays_ok_0.yml'), False),
     (str(RES_DIR / 'ng/0/playbook.yml'), True),
     (str(RES_DIR / 'ng/1/playbook.yml'), True),
     )
)
def test_contains_vars_directive(path, expected):
    assert TT.contains_vars_directive(path) == expected
    TT.contains_vars_directive.cache_clear()


class RuleTestCase(common.RuleTestCase):
    base_cls = Base


class CliTestCase(common.CliTestCase):
    base_cls = Base
