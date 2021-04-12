# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.runner.
"""
import ansiblelint.rules
import pytest

from rules.DebugRule import DebugRule
from tests.common import runner as TT


@pytest.mark.parametrize(
    'rdirs',
    [[],
     [str(TT.constants.RULES_DIR)],
     ]
)
def test_list_rule_ids(rdirs):
    res = list(TT.list_rule_ids(*rdirs))
    assert res, res
    assert 'debug' in res, f'{res!r}'


@pytest.mark.parametrize(
    'rule',
    [DebugRule(),
     None
     ]
)
def test_get_collection(rule):
    assert isinstance(TT.get_collection(rule),
                      ansiblelint.rules.RulesCollection)

# vim:sw=4:ts=4:et:
