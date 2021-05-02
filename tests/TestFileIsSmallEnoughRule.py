# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule.
"""
import pytest

from rules import FileIsSmallEnoughRule as TT
from tests import common


@pytest.mark.parametrize(
    'max_lines,expected',
    [(100000, False),
     (1, True),
     ]
)
def test_exceeds_max_lines(max_lines, expected):
    assert TT.exceeds_max_lines(__file__, max_lines) == expected


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    rule_memoized = ['max_lines', 'exceeds_max_lines']


CNF = dict(max_lines=1)


class RuleTestCase(Base, common.RuleTestCase):
    def test_20_ng_cases(self):
        self.lint(False, 'ok', config=CNF)


class CliTestCase(Base, common.CliTestCase):
    def test_20_ng_cases(self):
        self.lint(False, 'ok', config=CNF)
