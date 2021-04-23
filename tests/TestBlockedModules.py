# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, BlockedModules.
"""
import pytest

from rules import BlockedModules as TT
from tests import common


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    clear_fn: common.MaybeCallableT = TT.blocked_modules.cache_clear


@pytest.mark.parametrize(
    'evalue,expected',
    [('', TT.BLOCKED_MODULES),
     ('ping', frozenset(('ping', ))),
     ('ping script', frozenset(('ping', 'script'))),
     ('@/dev/null', TT.BLOCKED_MODULES),
     ]
)
def test_blocked_modules(evalue, expected, monkeypatch):
    monkeypatch.setenv(TT.ENV_VAR, evalue)
    assert TT.blocked_modules() == expected
    Base.clear_fn()


@pytest.mark.parametrize(
    'content,expected',
    [('#\n\n', TT.BLOCKED_MODULES),
     ('ping\n', frozenset(('ping', ))),
     ('#\nping\nscript\n', frozenset(('ping', 'script'))),
     ]
)
def test_blocked_modules_from_file(content, expected, tmp_path, monkeypatch):
    path = tmp_path / 'blocked_modules.list'
    path.write_text(content)

    monkeypatch.setenv(TT.ENV_VAR, f'@{path!s}')
    assert TT.blocked_modules() == expected
    Base.clear_fn()


# 'ping' is listed in it.
LIST_FILE = common.TESTS_DIR / 'res' / 'BlockedModules' / 'blocked_modules.txt'


class RuleTestCase(Base, common.RuleTestCase):
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok', env={TT.ENV_VAR: 'ping'})

    def test_40_ng_cases__file(self):
        self.lint(False, 'ok', env={TT.ENV_VAR: f'@{LIST_FILE!s}'})


class CliTestCase(Base, common.CliTestCase):
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok', env={TT.ENV_VAR: 'ping'})

    def test_40_ng_cases__file(self):
        self.lint(False, 'ok', env={TT.ENV_VAR: f'@{LIST_FILE!s}'})
