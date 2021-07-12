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


@pytest.mark.parametrize(
    ('content', 'expected'),
    (('', False),
     ('---\n', False),
     ('---\n{}\n', False),
     ('---\na: 1\n', True),
     )
)
def test_yml_file_has_some_data(content, expected, tmp_path):
    path = tmp_path / 'test.yml'
    path.write_text(content)

    assert TT.yml_file_has_some_data(str(path)) == expected
    TT.yml_file_has_some_data.cache_clear()


class Base(common.Base):
    this_mod: common.MaybeModT = TT


class RuleTestCase(common.RuleTestCase):
    base_cls = Base


class CliTestCase(common.CliTestCase):
    base_cls = Base
