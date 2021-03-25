# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,too-few-public-methods
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases for the rule, DebugRule.
"""
import os
import unittest.mock

from rules import NoEmptyDataFilesRule as TT
from tests import common as C


_ENV_PATCH = {TT.YML_EXT_ENVVAR: "yaml"}


def test_is_yml_file_has_some_data(tmp_path):
    fpath = tmp_path / "test_ng.yml"
    fpath.touch()

    assert not TT.is_yml_file_has_some_data(fpath)
    TT.is_yml_file_has_some_data.cache_clear()

    fpath.write_text("---\n")
    assert not TT.is_yml_file_has_some_data(fpath)
    TT.is_yml_file_has_some_data.cache_clear()

    fpath.write_text("---\n{}\n")
    assert not TT.is_yml_file_has_some_data(fpath)
    TT.is_yml_file_has_some_data.cache_clear()

    fpath = tmp_path / "test_ok.yml"
    fpath.write_text("---\na: 1\n")
    assert TT.is_yml_file_has_some_data(fpath)
    TT.is_yml_file_has_some_data.cache_clear()


class Base:
    name = C.get_rule_name(__file__)
    rule = C.get_rule_instance_by_name(TT, name)
    clear_fn = TT.is_yml_file_has_some_data.cache_clear


class RuleTestCase(Base, C.RuleTestCase):
    @unittest.mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_ok_cases__no_data(self):
        self.lint(True, 'ng')


class CliTestCase(Base, C.CliTestCase):
    def test_30_ok_cases__env(self):
        self.lint(True, 'ng', _ENV_PATCH)
