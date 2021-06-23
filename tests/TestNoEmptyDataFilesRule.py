# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
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


_CLEAR_FUN = TT.yml_file_has_some_data.cache_clear


@pytest.mark.parametrize(
    'content,expected',
    [('', False),
     ('---\n', False),
     ('---\n{}\n', False),
     ('---\na: 1\n', True)
     ]
)
def test_yml_file_has_some_data(content, expected, tmp_path):
    path = tmp_path / 'test.yml'
    path.write_text(content)

    assert TT.yml_file_has_some_data(str(path)) == expected
    _CLEAR_FUN()


class Base:
    this_mod: common.MaybeModT = TT
    clear_fn: common.MaybeCallableT = _CLEAR_FUN


class RuleTestCase(Base, common.RuleTestCase):
    pass


class CliTestCase(Base, common.CliTestCase):
    pass
