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


@pytest.fixture(autouse=True)
def cache_clear():
    yield
    TT.max_lines.cache_clear()


@pytest.mark.parametrize(
    'evalue,expected',
    [('', TT.MAX_LINES),
     ('aaa', TT.MAX_LINES),
     ('0', TT.MAX_LINES),
     ('1', 1),
     ]
)
def test_max_lines(evalue, expected, monkeypatch):
    monkeypatch.setenv(TT.ENV_VAR, evalue)
    assert TT.max_lines() == expected


@pytest.mark.parametrize(
    'mlines,expected',
    [(100000, False),
     (1, True),
     (0, False),  # default
     ]
)
def test_exceeds_max_lines(mlines, expected):
    assert TT.exceeds_max_lines(__file__, mlines=mlines) == expected


def test_exceeds_max_lines_with_env(monkeypatch):
    monkeypatch.setenv(TT.ENV_VAR, '1')
    assert TT.exceeds_max_lines(__file__)


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    clear_fn: common.MaybeCallableT = TT.max_lines.cache_clear


_ENV_PATCH = {TT.ENV_VAR: '1'}


class RuleTestCase(Base, common.RuleTestCase):
    def test_20_ng_cases(self):
        self.lint(False, 'ok', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    def test_20_ng_cases(self):
        self.lint(False, 'ok', env=_ENV_PATCH)
