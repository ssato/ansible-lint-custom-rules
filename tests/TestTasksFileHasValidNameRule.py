# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, TasksFileHasValidName.
"""
import pytest

from rules import TasksFileHasValidNameRule as TT
from tests import common


_ENV_PATCH = {TT.NAME_RE_ENVVAR: r'\S+'}  # e.g. ng-1.yml


def clear_function(*_args):
    """Function to clear caches."""
    TT.filename_re.cache_clear()
    TT.is_invalid_filename.cache_clear()


class Base:
    this_py = __file__
    this_mod = TT
    clear_fn = clear_function


class RuleTestCase(Base, common.RuleTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_20_ng_cases(self):
        super().test_20_ng_cases()

    def test_30_tasks_file_has_valid_name__ok__env(self):
        self.lint(True, 'ng_1', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    def test_30_tasks_file_has_valid_name__ok__env(self):
        self.lint(True, 'ng_1', env=_ENV_PATCH)
