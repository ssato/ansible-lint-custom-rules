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


class Base(common.Base):
    this_mod: common.MaybeModT = TT
    memoized = ['valid_name_re', 'is_invalid_filename']


class RuleTestCase(common.RuleTestCase):
    base_cls = Base


class CliTestCase(common.CliTestCase):
    base_cls = Base


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
    rule = Base.get_rule_instance_by_name(Base.get_rule_name())
    assert rule.is_valid_filename(path) == expected
    Base().clear()
