# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
# pylint: disable=too-few-public-methods
"""Test cases for the rule, TaskHasValidNamePatternRule.
"""
import pytest

from rules import TaskHasValidNamePatternRule as TT
from tests import common


_ENV_PATCH = {TT.TASK_NAME_RE_ENVVAR: '\\S+'}


class Base:
    this_py = __file__
    this_mod = TT
    clear_fn = TT.task_name_re.cache_clear


class RoleTestCase(Base, common.RuleTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_10_ok_cases(self):
        super().test_10_ok_cases()

    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_20_ng_cases(self):
        super().test_20_ng_cases()

    def test_30_task_has_invalid_name_pattern__ok__setenv(self):
        self.lint(True, 'ng_1', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_10_ok_cases(self):
        super().test_10_ok_cases()

    def test_30_ok_cases__env(self):
        self.lint(True, 'ng_1', env=_ENV_PATCH)
