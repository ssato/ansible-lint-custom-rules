# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Test cases for the rule, TasksFileHasValidName.
"""
import os
import mock

from rules import TasksFileHasValidNameRule as TT
from tests import common as C


_ENV_PATCH = {TT.NAME_RE_ENVVAR: "foo.+"}


class Base(object):
    """Base Mixin class."""
    prefix = "TasksFileHasValidNameRule"
    rule = getattr(TT, prefix)()
    clear_fn = TT.name_re.cache_clear


class RuleTestCase(Base, C.AnsibleLintRuleTestCase):
    """Test cases for the rule, TasksFileHasValidName.
    """
    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_tasks_file_has_valid_name__ok__env(self):
        self.lint(True, self.path_pattern("ng_1"))


class CliTestCase(Base, C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, TasksFileHasValidNameRule.
    """
    def test_30_ng_cases__env(self):
        self.lint(False, self.path_pattern(), _ENV_PATCH)
