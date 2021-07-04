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


# ansiblelint.rules.IncludeMissingFileRule:
STD_RULE_EX_ID: str = 'missing-import'


@pytest.mark.parametrize(
    ('rdirs', 'use_default', 'rule_id_ex'),
    (([], False, DebugRule.id),
     ([], True, STD_RULE_EX_ID),
     ([str(TT.constants.RULES_DIR)], False, DebugRule.id),
     ([str(TT.constants.RULES_DIR)], True, STD_RULE_EX_ID),
     )
)
def test_each_rule_ids(rdirs, use_default, rule_id_ex):
    res = list(TT.each_rule_ids(*rdirs, use_default=use_default))
    assert res, res
    assert rule_id_ex in res, f'{res!r}'


@pytest.mark.parametrize(
    'rule,options',
    [(DebugRule(), None),
     (DebugRule(), dict(enabled=True)),
     (None, None),
     ]
)
def test_get_collection(rule, options):
    collection = TT.get_collection(rule, rule_options=options)
    assert isinstance(collection, ansiblelint.rules.RulesCollection)

    rules = list(collection)
    assert len(rules) > 0  # It has default rules even if `rule` is None.

    if rule:
        rules = [r for r in collection if r.id == rule.id]
        assert len(rules) == 1

        if options:
            # pylint: disable=no-member
            grops = TT.ansiblelint.config.options.rules[rule.id]
            assert sorted(grops.items()) == sorted(options.items())

# vim:sw=4:ts=4:et:
