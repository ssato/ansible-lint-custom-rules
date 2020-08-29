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
    def test_30_playbook_file_has_valid_name__ng_2(self):
        TT.filename_re.cache_clear()

        pats = self.prefix + "*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)


class TestCliPlaybookFileHasValidNameRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, PlaybookFileHasValidNameRule.
    """
    rule = TT.PlaybookFileHasValidNameRule()
    prefix = "PlaybookFileHasValidNameRule"
    clear_fn = TT.filename_re.cache_clear

    def test_30_ng_cases__env(self):
        self._run_for_playbooks(self.prefix + "*ok*.yml", False,
                                env=_ENV_PATCH)
