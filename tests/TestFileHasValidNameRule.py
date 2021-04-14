# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, FileHasValidNameRule.
"""
import pytest

from rules import FileHasValidNameRule as TT
from tests import common


_ENV_PATCH = {TT.ENV_VAR: "\\S+NEVER_MATCH"}


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    clear_fn: common.MaybeCallableT = TT.filename_re.cache_clear


@pytest.mark.parametrize(
    'path,evalue,expected',
    [('main.yml', '', True),
     ('main-0.yml', '', False),
     ('main .yml', '', False),
     ('ng_１.yml', '', False),
     ('ng-２.yml', '', False),
     ('main-0.yml', r'\S+', True),
     ]
)
def test_is_valid_filename(path, evalue, expected, monkeypatch):
    if evalue:
        monkeypatch.setenv(TT.ENV_VAR, evalue)
    assert TT.is_valid_filename(path) == expected
    Base.clear_fn()


class RuleTestCase(Base, common.RuleTestCase):
    def test_30_playbook_file_has_valid_name__ng(self):
        self.lint(False, 'ok', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok', env=_ENV_PATCH)
