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


@pytest.mark.parametrize(
    ('path', 'name', 'unicode', 'expected'),
    (('main.yml', '', False, False),
     ('main-0.yml', '', False, True),
     ('main .yml', '', False, True),
     ('ng_１.yml', '', False, True),
     ('ng_１.yml', r'^\w+\.ya?ml$', True, False),
     ('ng-２.yml', '', False, True),
     ('main-0.yml', r'\S+', False, False),
     )
)
def test_is_invalid_filename(path, name, unicode, expected, monkeypatch):
    base = Base()
    rule = base.rule
    ansiblelint.config.options.rules = {
        rule.id: dict(name=TT.DEFAULT_NAME_RE.pattern, unicode=False)
    }

    if name:
        monkeypatch.setitem(
            ansiblelint.config.options.rules, TT.ID,
            dict(name=name, unicode=unicode)
        )
    assert rule.is_invalid_filename(path) == expected
    base.clear()


class Base(common.Base):
    this_mod: common.MaybeModT = TT
    default_skip_list = ['no_unspecified_argument']


class RuleTestCase(common.RuleTestCase):
    base_cls = Base


class CliTestCase(common.CliTestCase):
    base_cls = Base
