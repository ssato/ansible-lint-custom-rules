# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, TasksFileHasValidName.
"""
from rules import TasksFileHasValidNameRule as TT
from tests import common


_ENV_PATCH = {TT.ENV_VAR: r'\S+'}


def clear_function(*_args):
    """Function to clear caches."""
    TT.filename_re.cache_clear()


class Base:
    this_py: common.MaybeModNameT = __file__
    this_mod: common.MaybeModT = TT
    clear_fn: common.MaybeCallableT = clear_function


class RuleTestCase(Base, common.RuleTestCase):
    def test_30_tasks_file_has_valid_name__ok__env(self):
        self.lint(True, search='ng', pattern='0.yml', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    def test_30_tasks_file_has_valid_name__ok__env(self):
        self.lint(True, search='ng', pattern='0.yml', env=_ENV_PATCH)
