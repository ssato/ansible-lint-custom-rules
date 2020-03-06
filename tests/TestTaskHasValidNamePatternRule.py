# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
import os
import mock

from rules import TaskHasValidNamePatternRule as TT
from tests import common as C


_OS_ENVIRON_PATCH = {"_ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE": "\\S+"}


class TestTaskHasValidNamePattern(C.AnsibleLintRuleTestBase):

    rule = TT.TaskHasValidNamePatternRule()

    def test_task_has_valid_name_pattern__ok(self):
        pats = "TaskHasValidNamePatternRule_*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)

    def test_task_has_valid_name_pattern__ng(self):
        pats = "TaskHasValidNamePatternRule_*ng*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)  # Something goes wrong.

    @mock.patch.dict(os.environ, _OS_ENVIRON_PATCH)
    def test_task_has_invalid_name_pattern__ok__setenv(self):
        pats = "TaskHasValidNamePatternRule_ng_1.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)
