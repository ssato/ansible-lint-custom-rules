# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.base.
"""
import  functools

import pytest

from tests.common import base as TT


class FakeBase(TT.Base):
    """Fake Base class."""
    this_mod = TT


def test_get_filename():
    assert FakeBase.get_filename() == 'test_base.py'


def test_get_rule_name():
    assert FakeBase.get_rule_name() == 'base'


@functools.lru_cache()
def error():
    raise RuntimeError('Expected RuntimeError from memoized function')


class FakeBaseWithClearFns(TT.Base):
    """Fake Base class."""
    clear_fns = [error]


def test_clear():
    base = FakeBaseWithClearFns()
    with pytest.raises(RuntimeError):
        base.clear()

# vim:sw=4:ts=4:et:
