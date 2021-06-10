# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
# pylint: disable=too-few-public-methods
"""Test cases for the rule, TaskHasValidNamePatternRule.
"""
import ansiblelint.config
import pytest

from rules import TaskHasValidNameRule as TT
from tests import common


VALID_NAME_0 = 'Ensure foo is installed'
INVALID_NAME_0 = 'foo'
NAME_RE_0 = r'^\S+$'

CNF_0 = dict(name=NAME_RE_0)


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    rule_memoized = ['valid_name_re', 'is_invalid_task_name']

    use_lint_v2 = True


@pytest.mark.parametrize(
    'name,evalue,expected',
    [(VALID_NAME_0, '', False),  # default.
     (INVALID_NAME_0, '', True),
     (VALID_NAME_0, r'NEVER_MATCH', True),
     (VALID_NAME_0, NAME_RE_0, True),
     (INVALID_NAME_0, NAME_RE_0, False),
     ]
)
def test_is_invalid_task_name(name, evalue, expected, monkeypatch):
    monkeypatch.setitem(
        ansiblelint.config.options.rules, TT.ID,
        dict(name=evalue)
    )
    rule = common.get_rule_instance_by_module(Base.this_py, Base.this_mod)
    assert rule.is_invalid_task_name(name) == expected


class RoleTestCase(Base, common.RuleTestCase):
    pass


class CliTestCase(Base, common.CliTestCase):
    pass
