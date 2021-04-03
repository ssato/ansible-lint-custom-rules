# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.
"""
import ansiblelint.rules
import pytest

from rules.DebugRule import DebugRule
from tests.common import runner as TT


@pytest.mark.parametrize(
    'rule_instance',
    [(DebugRule(), ),
     (None, )
     ]
)
def test_get_collection(rule_instance):
    assert isinstance(TT.get_collection(rule_instance),
                      ansiblelint.rules.RulesCollection)

# vim:sw=4:ts=4:et:
