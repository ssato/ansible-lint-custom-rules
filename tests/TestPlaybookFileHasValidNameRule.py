# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Test cases for the rule, PlaybookFileHasValidNameRule.
"""
import os
import mock

from rules import PlaybookFileHasValidNameRule as TT
from tests import common as C


_ENV_PATCH = {TT.FILENAME_ENVVAR: "\\S+NEVER_MATCH"}


class TestPlaybookFileHasValidNameRule(C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, PlaybookFileHasValidNameRule.
    """
    rule = TT.PlaybookFileHasValidNameRule()
    prefix = "PlaybookFileHasValidNameRule"

    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_playbook_file_has_valid_name__ng(self):
        TT.filename_re.cache_clear()
        self.lint(False, self.path_pattern())


class TestCliPlaybookFileHasValidNameRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, PlaybookFileHasValidNameRule.
    """
    rule = TT.PlaybookFileHasValidNameRule()
    prefix = "PlaybookFileHasValidNameRule"
    clear_fn = TT.filename_re.cache_clear

    def test_30_ng_cases__env(self):
        self._run_for_playbooks(self.prefix + "*ok*.yml", False,
                                env=_ENV_PATCH)
