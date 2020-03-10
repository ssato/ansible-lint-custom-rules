# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-module-docstring
# pylint: disable=missing-class-docstring,missing-function-docstring
import os
import mock

from rules import VariablesNamingRule as TT
from tests import common as C


_OS_ENVIRON_PATCH = {"_ANSIBLE_LINT_RULE_CUSTOM_2020_3_VAR_NAME_RE":
                     "___x\\w+"}  # Must starts with '___x'


class TestVariablesNamingRule(C.AnsibleLintRuleTestBase):

    rule = TT.VariablesNamingRule()

    def test_playbook_refering_invalid_var_names(self):
        pats = "VariablesNamingRule*ng*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)

    def test_playbook_refering_only_valid_var_names(self):
        pats = "VariablesNamingRule*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)

    @C.unittest.skip("Not implemented correctly yet")
    @mock.patch.dict(os.environ, _OS_ENVIRON_PATCH)
    def test_playbook_refering_invalid_var_names__env(self):
        pats = "VariablesNamingRule*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)
