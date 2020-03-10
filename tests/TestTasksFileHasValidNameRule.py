# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
import os
import mock

from rules import TasksFileHasValidNameRule as TT
from tests import common as C


_OS_ENVIRON_PATCH = {"_ANSIBLE_LINT_RULE_CUSTOM_2020_2_TASKS_FILENAME_RE":
                     "\\S+"}


class TestTasksFileHasValidNameRule(C.AnsibleLintRuleTestBase):

    rule = TT.TasksFileHasValidNameRule()

    def test_tasks_file_has_valid_name__ng(self):
        pats = "TasksFileHasValidName*ng*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)  # Something goes wrong.

    def test_tasks_file_has_valid_name__ok(self):
        pats = "TasksFileHasValidName*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)

    @mock.patch.dict(os.environ, _OS_ENVIRON_PATCH)
    def test_tasks_file_has_valid_name__ok__env(self):
        pats = "TasksFileHasValidName_ng_1.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)
