# Copyright (C) Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for libs.utils.
"""
import re
import unittest.mock

import pytest

import ansiblelint.config
import ansiblelint.rules

from rules import _utils as TT


class CustomRule(ansiblelint.rules.AnsibleLintRule):
    id: str = 'custom-00'


@pytest.mark.parametrize(
    ('default', 'pattern', 'allow_unicode'),
    ((None, None, True),
     (None, None, False),
     (None, '^.+$', True),
     (None, '^.+$', False),
     (None, '^\\w+$', False),
     )
)
def test_make_valid_name_pattern_from_rule_config(
    default, pattern, allow_unicode
):
    if pattern:
        if allow_unicode:
            exp = re.compile(pattern)
        else:
            exp = re.compile(pattern, re.ASCII)
    else:
        exp = default

    with unittest.mock.patch.dict(
        ansiblelint.config.options.rules,
        {CustomRule.id: dict(name=pattern, unicode=allow_unicode)}
    ):
        res = TT.make_valid_name_pattern_from_rule_config(
            CustomRule(), default
        )
        assert res == exp


@pytest.mark.parametrize(
    ('pattern', 'name', 'exp'),
    ((re.compile('^.+$'), 'foo', True),
     (re.compile('^\\S+$'), 'foo', True),
     (re.compile('^\\S+$'), '   ', False),
     (re.compile('^\\w+$'), 'foo', True),
     )
)
def test_is_valid_name(pattern, name, exp):
    assert TT.is_valid_name(pattern, name) == exp
