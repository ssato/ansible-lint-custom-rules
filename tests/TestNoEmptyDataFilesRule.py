# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule.
"""
import pytest

from rules import NoEmptyDataFilesRule as TT
from tests import common


_CLEAR_FUN = TT.is_yml_file_has_some_data.cache_clear


def test_is_yml_file_has_some_data(tmp_path):
    fpath = tmp_path / 'test_ng.yml'
    fpath.touch()

    assert not TT.is_yml_file_has_some_data(fpath)
    _CLEAR_FUN()

    fpath.write_text('---\n')
    assert not TT.is_yml_file_has_some_data(fpath)
    _CLEAR_FUN()

    fpath.write_text('---\n{}\n')
    assert not TT.is_yml_file_has_some_data(fpath)
    _CLEAR_FUN()

    fpath = tmp_path / 'test_ok.yml'
    fpath.write_text('---\na: 1\n')
    assert TT.is_yml_file_has_some_data(fpath)
    _CLEAR_FUN()


class Base:
    this_py = __file__
    this_mod = TT
    clear_fn = _CLEAR_FUN


class RuleTestCase(Base, common.RuleTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_20_ng_cases(self):
        super().test_20_ng_cases()


class CliTestCase(Base, common.CliTestCase):
    pass
