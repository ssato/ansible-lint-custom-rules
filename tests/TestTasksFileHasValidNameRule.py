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


_OS_ENVIRON_PATCH = {"_ANSIBLE_LINT_RULE_CUSTOM_2020_2_TASKS_FILENAME_RE":
                     "\\S+"}


class TestTasksFileHasValidNameRule(C.AutoTestCasesForAnsibleLintRule):
    """Test cases for the rule, TasksFileHasValidName.
    """
    rule = TT.TasksFileHasValidNameRule()
    prefix = "TasksFileHasValidNameRule"

    @mock.patch.dict(os.environ, _OS_ENVIRON_PATCH)
    def test_tasks_file_has_valid_name__ok__env(self):
        pats = self.prefix + "_ng_1.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)
