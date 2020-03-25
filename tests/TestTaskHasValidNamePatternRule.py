# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Test cases for the rule, TaskHasValidNamePatternRule.
"""
import os
import mock

from rules import TaskHasValidNamePatternRule as TT
from tests import common as C


_OS_ENVIRON_PATCH = {TT.TASK_NAME_RE_ENVVAR: "\\S+"}


class TestTaskHasValidNamePattern(C.AutoTestCasesForAnsibleLintRule):
    """Test cases for the rule class, TaskHasValidNamePatternRule.
    """
    rule = TT.TaskHasValidNamePatternRule()
    prefix = "TaskHasValidNamePatternRule"

    @mock.patch.dict(os.environ, _OS_ENVIRON_PATCH)
    def test_task_has_invalid_name_pattern__ok__setenv(self):
        TT.task_name_re.cache_clear()

        pats = self.prefix + "_ng_1.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)
