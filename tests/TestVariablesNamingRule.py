# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Test cases for the rule, VariablesNamingRule.
"""
import os
import mock

from rules import VariablesNamingRule as TT
from tests import common as C


INV_1 = "inventories/VariablesNamingRule/ok/1/hosts"
HVARS_1 = "inventories/VariablesNamingRule/ok/1/host_vars/localhost_0.yml"
PLAY_1 = "VariablesNamingRule_ok_1.yml"
PLAY_2 = "VariablesNamingRule_ok_2.yml"

_ENV_PATCH_INV_1 = {"_ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY":
                    C.list_res_files(INV_1)[0]}
_ENV_PATCH_UA = {"_ANSIBLE_LINT_RULE_CUSTOM_2020_3_USE_ANSIBLE": "1"}
_ENV_PATCH_RE = {"_ANSIBLE_LINT_RULE_CUSTOM_2020_3_VAR_NAME_RE":
                 "___x\\w+"}  # Must starts with '___x'


class TestFunctions(C.unittest.TestCase):
    """test cases for some utility functions.
    """

    def test_list_var_names_from_yaml_file_itr__ok_simple_yaml_file(self):
        ypath = C.list_res_files(HVARS_1)[0]  # == HVARS_1
        ref = set(["foo_1", "BAR_baz", "bar_BAR", "__xyz"])  # see HVARS_1
        res = set(TT.list_var_names_from_yaml_file_itr(ypath))

        self.assertEqual(ref, res)

    def test_list_var_names_from_yaml_file_itr__ok_vars_name(self):
        ypath = C.list_res_files(PLAY_1)[0]
        ref = set(["foo", "BAR_1", "_foo_bar", "_baz"])  # see HVARS_1
        res = set(TT.list_var_names_from_yaml_file_itr(ypath, "vars"))
        self.assertEqual(ref, res)

    def test_list_var_names_from_yaml_files_itr__ok_simple_yaml_files(self):
        ypaths = C.list_res_files(HVARS_1)
        ref = set(["foo_1", "BAR_baz", "bar_BAR", "__xyz"])
        res = set(TT.list_var_names_from_yaml_files_itr(ypaths))
        self.assertEqual(ref, res)

    def test_list_var_names_from_inventory_file_itr(self):
        inv = C.list_res_files(INV_1)[0]
        ref = set(["BAZ_2", ])  # see INV_1
        res = set(TT.list_var_names_from_inventory_file_itr(inv))
        self.assertTrue(res)
        self.assertEqual(res, ref, res)

    @mock.patch.dict(os.environ, _ENV_PATCH_INV_1)
    def test_find_var_names_from_inventory(self):
        TT.name_re.cache_clear()

        ref = set(["foo_1", "BAR_baz", "bar_BAR",
                   "__xyz", "BAZ_2"])  # see INV_1 and HVARS_1
        res = TT.find_var_names_from_inventory()
        self.assertEqual(res, ref)

    def test_find_var_names_from_playbook_file(self):
        playbook = C.list_res_files(PLAY_1)[0]
        ref = set(["foo", "BAR_1", "_foo_bar", "_baz"])  # see PLAY_1
        res = TT.find_var_names_from_playbook_file(playbook)
        self.assertTrue(res)
        self.assertEqual(res, ref, res)

    def test_list_role_names_itr__empty(self):
        playbook = C.list_res_files(PLAY_1)[0]
        res = set(TT.list_role_names_itr(playbook))
        self.assertFalse(res)  # It should be an empty set().

    def test_list_role_names_itr__found(self):
        playbook = C.list_res_files(PLAY_2)[0]
        ref = set(("variable_naming_rule_test_ok_1", ))
        res = set(TT.list_role_names_itr(playbook))
        self.assertTrue(res)
        self.assertEqual(res, ref, res)

    def test_find_var_names_from_role_files_itr(self):
        playbook = C.list_res_files(PLAY_2)[0]
        # see defaults/main.yml and vars/main.yml
        # in tests/res/roles/variable_naming_rule_test_ok_1/
        ref = set(["foo", "BAR_1", "_foo_bar_baz"])
        res = set(TT.find_var_names_from_role_files_itr(playbook))
        self.assertTrue(res)
        self.assertEqual(res, ref, res)


class TestVariablesNamingRule(C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, VariablesNamingRule.
    """
    rule = TT.VariablesNamingRule()
    prefix = "VariablesNamingRule"

    @mock.patch.dict(os.environ, _ENV_PATCH_UA)
    def test_playbook_refering_invalid_var_names__use_ansible(self):
        TT.use_ansible.cache_clear()
        TT.name_re.cache_clear()

        pats = "VariablesNamingRule*ng*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)

    @mock.patch.dict(os.environ, _ENV_PATCH_UA)
    def test_playbook_refering_only_valid_var_names__use_ansible(self):
        TT.use_ansible.cache_clear()
        TT.name_re.cache_clear()

        pats = "VariablesNamingRule*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertEqual(0, len(res), res)

    @mock.patch.dict(os.environ, _ENV_PATCH_RE)
    def test_playbook_refering_invalid_var_names__env(self):
        TT.name_re.cache_clear()

        pats = "VariablesNamingRule*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)

    @mock.patch.dict(os.environ, _ENV_PATCH_UA)
    @mock.patch.dict(os.environ, _ENV_PATCH_RE)
    def test_playbook_refering_invalid_var_names__env__use_ansible(self):
        TT.use_ansible.cache_clear()
        TT.name_re.cache_clear()

        pats = "VariablesNamingRule*ok*.yml"
        for res in self._lint_results_for_playbooks_itr(pats):
            self.assertTrue(len(res) > 0, res)


class TestCliVariablesNamingRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, VariablesNamingRule.
    """
    rule = TT.VariablesNamingRule()
    prefix = "VariablesNamingRule"

    def setUp(self):
        super(TestCliVariablesNamingRule, self).setUp()
        TT.use_ansible.cache_clear()
        TT.name_re.cache_clear()

    def test_30_ng_cases__env(self):
        self._run_for_playbooks(self.prefix + "*ok*.yml", False,
                                env=_ENV_PATCH_RE)
