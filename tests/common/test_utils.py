# Copyright (C) 2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases of tests.common.
"""
import pathlib
import typing

import pytest

from tests.common import utils as TT, constants as C


@pytest.mark.parametrize(
    "xss,expected",
    [([[]], []),
     (((), ), []),
     ([[1, 2, 3], [4, 5]], [1, 2, 3, 4, 5]),
     ([[1, 2, 3], [4, 5, [6, 7]]], [1, 2, 3, 4, 5, [6, 7]]),
     (((1, 2, 3), (4, 5, [6, 7])), [1, 2, 3, 4, 5, [6, 7]]),
     (((i, i*2) for i in range(3)), [0, 0, 1, 2, 2, 4])
     ]
)
def test_concat(xss, expected):
    assert TT.concat(xss) == expected


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
_OK_FILES: typing.List[str] = sorted(
    str(f) for f
    in pathlib.Path(C.TESTS_RES_DIR / _NAME / 'ok').glob('*.*')
    if f.is_file()
)


@pytest.mark.parametrize(
    'success,search,expected',
    [(True, None, _OK_FILES),   # Default
     (False, 'ok', _OK_FILES),  # Override the dir to search.
     (False, None, []),
     (True, 'ng', [])
     ]
)
def test_list_resoruces_for_ok_cases(success, search, expected):
    assert TT.list_resources(_NAME, success=success, search=search) == expected


@pytest.mark.parametrize(
    'filepath,expected',
    [(__file__, 'utils'),
     (str(C.RULES_DIR / f'{_NAME}.py'), _NAME)
     ]
)
def test_get_rule_name(filepath, expected):
    assert TT.get_rule_name(filepath) == expected

# vim:sw=4:ts=4:et:
