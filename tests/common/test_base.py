# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.base.
"""
from rules import DebugRule  # This depends on it.
from tests.common import base as TT


class FakeBase(TT.Base):
    """Fake Base class."""
    this_mod = TT


def test_get_filename():
    assert FakeBase.get_filename() == 'test_base.py'


def test_get_rule_name():
    assert FakeBase.get_rule_name() == 'base'


def test_each_lru_cache_clear_fns():
    clear_fns = list(TT.each_lru_cache_clear_fns(DebugRule))
    assert not clear_fns  # No lru_cache-ed in module level.

    clear_fns = list(TT.each_lru_cache_clear_fns(DebugRule.DebugRule))
    assert clear_fns  # lru_cache-ed are in class level.

# vim:sw=4:ts=4:et:
