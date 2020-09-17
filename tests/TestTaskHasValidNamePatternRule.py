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


class Base(object):
    """Base Mixin class."""
    prefix = "TaskHasValidNamePatternRule"
    rule = getattr(TT, prefix)()
    clear_fn = TT.task_name_re.cache_clear


class RoleTestCase(Base, C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, TaskHasValidNamePatternRule.
    """
    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_task_has_invalid_name_pattern__ok__setenv(self):
        self.lint(True, self.path_pattern("ng_1"))


class CliTestCase(Base, C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, TaskHasValidNamePatternRule.
    """
    def test_30_ok_cases__env(self):
        self.lint(True, self.path_pattern("ng_1"), _ENV_PATCH)
