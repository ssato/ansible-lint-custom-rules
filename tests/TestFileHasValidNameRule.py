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
    this_mod: common.MaybeModT = TT
    memoized = ['valid_name_re']


class RuleTestCase(Base, common.RuleTestCase):
    pass


class CliTestCase(Base, common.CliTestCase):
    pass


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
    rule = RuleTestCase.get_rule_instance_by_name(RuleTestCase.get_rule_name())
    ansiblelint.config.options.rules = {
        rule.id: dict(name=TT.DEFAULT_NAME_RE.pattern, unicode=False)
    }

    if name:
        monkeypatch.setitem(
            ansiblelint.config.options.rules, TT.ID,
            dict(name=name, unicode=unicode)
        )
    assert rule.is_valid_filename(path) == expected

    for fname in Base.memoized:
        getattr(getattr(rule, fname), 'cache_clear')()
