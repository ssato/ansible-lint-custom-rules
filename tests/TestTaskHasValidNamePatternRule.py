# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases for the rule, TaskHasValidNamePatternRule.
"""
import os
import unittest.mock

from rules import TaskHasValidNamePatternRule as TT
from tests import common as C


_ENV_PATCH = {TT.TASK_NAME_RE_ENVVAR: "\\S+"}


class Base:
    name = C.get_rule_name(__file__)
    rule = C.get_rule_instance_by_name(TT, name)
    clear_fn = TT.task_name_re.cache_clear


class RoleTestCase(Base, C.RuleTestCase):
    @unittest.mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_task_has_invalid_name_pattern__ok__setenv(self):
        self.lint(True, 'ng_1')


class CliTestCase(Base, C.CliTestCase):
    def test_30_ok_cases__env(self):
        self.lint(True, 'ng_1', _ENV_PATCH)
