# Copyright (C) 2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases of tests.common.
"""
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


@pytest.mark.parametrize(
    'success,search',
    [(True, None),  # Default
     (False, 'ok')  # Override the filename glob pattern.
     ]
)
def test_list_resoruces_for_ok_cases(success, search):
    name = 'DebugRule'
    rss = TT.list_resources(name, success=success, search=search)
    assert rss
    assert TT.pathlib.Path(rss[0]).name == 'ok_1.yml'


@pytest.mark.parametrize(
    'success,search',
    [(False, None),
     (True, 'ng')
     ]
)
def test_list_resoruces_for_ng_cases(success, search):
    name = 'DebugRule'
    with pytest.raises(RuntimeError, match=r'No resource data files:.*'):
        TT.list_resources(name, success=success, search=search)


@pytest.mark.parametrize(
    'filepath,expected',
    [(__file__, 'utils'),
     (str(C.TESTS_DIR.parent / 'rules' / 'DebugRule.py'), 'DebugRule')
     ]
)
def test_get_rule_name(filepath, expected):
    assert TT.get_rule_name(filepath) == expected

# vim:sw=4:ts=4:et:
