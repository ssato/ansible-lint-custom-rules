# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.runner.
"""
import functools

import pytest
import yaml

from tests.common import constants, datatypes, utils as TT


@functools.lru_cache(None)
def mid(obj):
    return id(obj)


@pytest.mark.parametrize(
    ('fns', 'exp'),
    (([], False),
     ([id], False),
     ([mid], True),
     )
)
def test_each_clear_fn(fns, exp):
    res = list(TT.each_clear_fn(fns))
    assert bool(res) == exp
    if res:
        for fun in res:
            assert callable(fun)


def gen_ref_tdata(role_name, filename, success=True,
                  root=constants.TESTS_RES_DIR):
    datadir = root / role_name / ('ok' if success else 'ng')

    conf = dict()
    cpath = datadir / 'c' / filename
    if cpath.exists():
        conf = yaml.load(cpath.open())

    env = dict()
    epath = datadir / 'env' / filename
    if epath.exists():
        env = yaml.load(epath.open())

    return datatypes.TData(datadir, datadir / filename, conf, env)


# .. seealso:: The output of ls tests/res/DebugRule/*/*.yml
@pytest.mark.parametrize(
    ('rule_name', 'success', 'exp'),
    (('DebugRule', True, [gen_ref_tdata('DebugRule', '0.yml'),
                          gen_ref_tdata('DebugRule', '1.yml'),
                          gen_ref_tdata('DebugRule', '2.yml')]),
     ('DebugRule', False, [gen_ref_tdata('DebugRule', '0.yml', False),
                           gen_ref_tdata('DebugRule', '1.yml', False),
                           gen_ref_tdata('DebugRule', '2.yml', False)]),
     )
)
def test_each_test_data_for_rule(rule_name, success, exp):
    assert list(TT.each_test_data_for_rule(rule_name, success)) == exp

# vim:sw=4:ts=4:et:
