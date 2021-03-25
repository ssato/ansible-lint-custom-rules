# Copyright (C) 2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases of tests.common.
"""
import pytest

from tests import common as C


@pytest.mark.parametrize(
    "astr,words,expected",
    [('', [''], ''),
     ('', ['abc'], ''),
     ('abcd', ['bc', 'd'], 'a'),
     ('test_foo.py', ['.py', 'test_'], 'foo'),
     ('TestFoo.py', ['.py', 'test_', 'Test'], 'Foo'),
     ]
)
def test_strips(astr, words, expected):
    assert C.strip_words(astr, *words) == expected


def test_get_rule_name():
    assert C.get_rule_name() == 'common'


@pytest.mark.parametrize(
    "success,search",
    [(True, None),  # Default
     (False, 'ok')  # Override the filename glob pattern.
     ]
)
def test_list_resoruces_for_ok_cases(success, search):
    name = C.get_rule_name()
    rss = C.list_resources(name, success=success,
                           search=search)
    assert rss
    assert C.pathlib.Path(rss[0]).name == 'ok_1.yml'


@pytest.mark.parametrize(
    "success,search",
    [(False, None),
     (True, 'ng')
     ]
)
def test_list_resoruces_for_ng_cases(success, search):
    name = C.get_rule_name()
    with pytest.raises(RuntimeError, match=r"No resource data files:.*"):
        C.list_resources(name, success=success, search=search)


def test_list_rule_ids_itr():
    rids = list(C.list_rule_ids_itr())
    assert rids
    assert 'Custom_2020_99' in rids  # .. seealso:: rules.DebugRule._RULE_ID
