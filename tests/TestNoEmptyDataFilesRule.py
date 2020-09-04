# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Test cases for the rule, DebugRule.
"""
import os
import mock

from rules import NoEmptyDataFilesRule as TT
from tests import common as C


_ENV_PATCH = {TT.YML_EXT_ENVVAR: "yaml"}


def test_is_yml_file_has_some_data(tmp_path):
    fpath = tmp_path / "test_ng.yml"
    fpath.touch()

    assert not TT.is_yml_file_has_some_data(fpath)

    fpath.write_text("---\n")
    assert not TT.is_yml_file_has_some_data(fpath)

    fpath.write_text("---\n{}\n")
    assert not TT.is_yml_file_has_some_data(fpath)

    fpath = tmp_path / "test_ok.yml"
    fpath.write_text("---\na: 1\n")
    assert TT.is_yml_file_has_some_data(fpath)


class TestNoEmptyDataFilesRule(C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, DebugRule.
    """
    rule = TT.NoEmptyDataFilesRule()
    prefix = "NoEmptyDataFilesRule"

    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_ok_cases__no_data(self):
        TT.is_yml_file_has_some_data.cache_clear()
        self.lint(True, self.path_pattern("ng"))


class TestCliNoEmptyDataFilesRule(C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, DebugRule.
    """
    rule = TT.NoEmptyDataFilesRule()
    prefix = "NoEmptyDataFilesRule"
    clear_fn = TT.is_yml_file_has_some_data.cache_clear

    def test_30_ok_cases__env(self):
        self.lint(True, "ng", _ENV_PATCH)
