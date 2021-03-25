# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases for the rule, TasksFileHasValidName.
"""
import os
import unittest.mock

from rules import TasksFileHasValidNameRule as TT
from tests import common as C


_ENV_PATCH = {TT.NAME_RE_ENVVAR: r"\S+"}  # e.g. ng-1.yml


def clear_function(*_args):
    """Function to clear caches."""
    TT.filename_re.cache_clear()
    TT.is_invalid_filename.cache_clear()


class Base:
    name = C.get_rule_name(__file__)
    rule = C.get_rule_instance_by_name(TT, name)
    clear_fn = clear_function


class RuleTestCase(Base, C.RuleTestCase):
    @unittest.mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_tasks_file_has_valid_name__ok__env(self):
        self.lint(True, 'ng_1')


class CliTestCase(Base, C.CliTestCase):
    def test_30_tasks_file_has_valid_name__ok__env(self):
        self.lint(True, 'ng_1', _ENV_PATCH)
