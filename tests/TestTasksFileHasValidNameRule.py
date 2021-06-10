# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, TasksFileHasValidName.
"""
import ansiblelint.config
import pytest

from rules import TasksFileHasValidNameRule as TT
from tests import common


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    rule_memoized = ['valid_name_re', 'is_invalid_filename']

    use_lint_v2 = True


@pytest.mark.parametrize(
    'path,name,unicode,expected',
    [('tasks/main.yml', '', False, True),
     ('tasks/incl/main.yml', '', False, True),
     ('tasks/main-0.yml', '', False, False),
     ('tasks/main .yml', '', False, False),
     ('tasks/ng_１.yml', '', False, False),
     ('tasks/ng_１.yml', r'^\w+\.ya?ml$', True, True),
     ('tasks/ng-２.yml', '', False, False),
     ('tasks/include/main-0.yml', r'\S+', False, True),
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


CNF_0 = dict(name=r'.+', unicode=False)


class RuleTestCase(Base, common.RuleTestCase):
    pass


class CliTestCase(Base, common.CliTestCase):
    pass
