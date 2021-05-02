# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, FileHasValidNameRule.
"""
import pytest

import ansiblelint.config

from rules import FileHasValidNameRule as TT
from tests import common


NG_VALID_NAME_RE = r'\S+NEVER_MATCH'


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    rule_memoized = ['is_valid_filename']


@pytest.mark.parametrize(
    'path,name,unicode,expected',
    [('main.yml', '', False, True),
     ('main-0.yml', '', False, False),
     ('main .yml', '', False, False),
     ('ng_１.yml', '', False, False),
     ('ng_１.yml', r'^\w+\.ya?ml$', True, True),
     ('ng-２.yml', '', False, False),
     ('main-0.yml', r'\S+', False, True),
     ]
)
def test_is_valid_filename(path, name, unicode, expected, monkeypatch):
    if name:
        monkeypatch.setitem(
            ansiblelint.config.options.rules, TT.ID,
            dict(name=name, unicode=unicode)
        )
    rule = common.get_rule_instance_by_module(Base.this_py, Base.this_mod)
    assert rule.is_valid_filename(path) == expected


class RuleTestCase(Base, common.RuleTestCase):
    def test_30_ng_cases_by_config(self):
        self.lint(False, 'ok', config=dict(name=NG_VALID_NAME_RE))


class CliTestCase(Base, common.CliTestCase):
    def test_30_ng_cases_by_config(self):
        self.lint(False, 'ok', config=dict(name=NG_VALID_NAME_RE))
