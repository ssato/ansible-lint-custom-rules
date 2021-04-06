# Copyright (C) 2020,2021 Red Hat, Inc.
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


_ENV_PATCH = {TT.MAX_LINES_ENVVAR: '1'}


@pytest.mark.parametrize(
    'mlines,expected',
    [(100000, False),
     (1, True)
     ]
)
def test_exceeds_max_lines(mlines, expected):
    assert TT.exceeds_max_lines(__file__, mlines=mlines) == expected


def test_exceeds_max_lines_with_env(monkeypatch):
    TT.max_lines.cache_clear()
    monkeypatch.setenv(TT.MAX_LINES_ENVVAR, '1')
    assert TT.exceeds_max_lines(__file__)
    TT.max_lines.cache_clear()


class Base:
    this_py = __file__
    this_mod = TT
    clear_fn = TT.max_lines.cache_clear


class RuleTestCase(Base, common.RuleTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_20_ng_cases(self):
        self.lint(False, 'ok', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    def test_20_ng_cases(self):
        self.lint(False, 'ok', env=_ENV_PATCH)
