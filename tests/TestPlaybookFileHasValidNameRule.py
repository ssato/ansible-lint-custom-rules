# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
import os
import mock

from rules import PlaybookFileHasValidNameRule as TT
from tests import common as C


_ENV_PATCH_NAME_RE = {TT.FILENAME_ENVVAR: "\\S+NEVER_MATCH"}


class TestPlaybookFileHasValidNameRule(C.AnsibleLintRuleTestBase):

    rule = TT.PlaybookFileHasValidNameRule()

    def test_10_playbook_file_has_valid_name__ng(self):
        pats = "PlaybookFileHasValidNameRule_*ng*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)

    def test_20_playbook_file_has_valid_name__ok(self):
        pats = "PlaybookFileHasValidNameRule_*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)

    @mock.patch.dict(os.environ, _ENV_PATCH_NAME_RE)
    def test_30_playbook_file_has_valid_name__ng_2(self):
        TT.filename_re.cache_clear()

        pats = "PlaybookFileHasValidNameRule_*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)
