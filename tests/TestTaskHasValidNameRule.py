# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
# pylint: disable=too-few-public-methods
"""Test cases for the rule, TaskHasValidNamePatternRule.
"""
import re
import typing

import pytest

from rules import TaskHasValidNameRule as TT
from tests import common


_ENV_PATCH = {TT.ENV_VAR: r'\S+'}
_NAME_RE_DEFAULT: typing.Pattern = re.compile(TT.NAME_RE, re.ASCII)


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    clear_fn: common.MaybeCallableT = TT.task_name_pattern.cache_clear


@pytest.mark.parametrize(
    'evalue,expected',
    [('', TT.NAME_RE),
     (r'\S \S+', TT.NAME_RE),  # invalid pattern
     (r'\S+', r'\S+'),
     ]
)
def test_task_name_re(evalue, expected, monkeypatch):
    monkeypatch.setenv(TT.ENV_VAR, evalue)
    assert TT.name_re(TT.NAME_RE) == expected


class RoleTestCase(Base, common.RuleTestCase):
    def test_30_task_has_invalid_name_pattern__ok__setenv(self):
        self.lint(True, search='ng', pattern='0.yml', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    def test_30_ok_cases__env(self):
        self.lint(True, search='ng', pattern='0.yml', env=_ENV_PATCH)
