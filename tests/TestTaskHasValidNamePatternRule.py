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


_ENV_PATCH = {TT.TASK_NAME_RE_ENVVAR: "\\S+"}


class TestTaskHasValidNamePattern(C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, TaskHasValidNamePatternRule.
    """
    rule = TT.TaskHasValidNamePatternRule()
    prefix = "TaskHasValidNamePatternRule"

    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_task_has_invalid_name_pattern__ok__setenv(self):
        TT.task_name_re.cache_clear()
        self.lint(True, self.path_pattern("ng_1"))


class TestCliTaskHasValidNamePatternRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, TaskHasValidNamePatternRule.
    """
    rule = TT.TaskHasValidNamePatternRule()
    prefix = "TaskHasValidNamePatternRule"
    clear_fn = TT.task_name_re.cache_clear

    def test_30_ok_cases__env(self):
        self._run_for_playbooks(self.prefix + "*_ng_1*.yml", True,
                                env=_ENV_PATCH)
