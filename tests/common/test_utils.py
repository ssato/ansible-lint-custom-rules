# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases of tests.common.
"""
import pytest

from tests.common import utils as TT, constants as C


@pytest.mark.parametrize(
    'astr,words,expected',
    [('', [''], ''),
     ('', ['abc'], ''),
     ('abcd', ['bc', 'd'], 'a'),
     ('test_foo.py', ['.py', 'test_'], 'foo'),
     ('TestFoo.py', ['.py', 'test_', 'Test'], 'Foo'),
     ]
)
def test_strips(astr, words, expected):
    assert TT.strip_words(astr, *words) == expected


_NAME = 'DebugRule'


@pytest.mark.parametrize(
    'filepath,expected',
    [(__file__, 'utils'),
     (str(C.RULES_DIR / f'{_NAME}.py'), _NAME)
     ]
)
def test_get_rule_name(filepath, expected):
    assert TT.get_rule_name(filepath) == expected

# vim:sw=4:ts=4:et:
