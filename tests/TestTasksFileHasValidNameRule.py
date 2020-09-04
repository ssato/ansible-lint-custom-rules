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


class TestTasksFileHasValidNameRule(C.AnsibleLintRuleTestCase):
    """Test cases for the rule, TasksFileHasValidName.
    """
    rule = TT.TasksFileHasValidNameRule()
    prefix = "TasksFileHasValidNameRule"

    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_tasks_file_has_valid_name__ok__env(self):
        TT.name_re.cache_clear()
        self.lint(True, self.path_pattern("ng_1"))


class TestCliTasksFileHasValidNameRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, TasksFileHasValidNameRule.
    """
    rule = TT.TasksFileHasValidNameRule()
    prefix = "TasksFileHasValidNameRule"
    clear_fn = TT.name_re.cache_clear

    def test_30_ng_cases__env(self):
        self.lint(False, "ok", _ENV_PATCH)
