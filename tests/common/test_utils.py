# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.runner.
"""
import functools

import pytest

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


@pytest.mark.parametrize(
    ('path', 'exp'),
    ((constants.TESTS_RES_DIR / 'DebugRule/ng/env/2.yml', True),
     (constants.TESTS_RES_DIR / 'not_exist.yml', False),
     )
)
def test_yaml_load(path, exp):
    result = TT.yaml_load(path)
    assert bool(result) == exp


def gen_ref_tdata(path):
    datadir = path.parent
    filename = path.name

    conf = dict()
    cpath = datadir / 'c' / filename
    if cpath.exists():
        conf = TT.yaml_load(cpath)

    env = dict()
    epath = datadir / 'env' / filename
    if epath.exists():
        env = TT.yaml_load(epath)

    return datatypes.TData(datadir, path, conf, env)


def each_ref_tdata(role_name, success=True,
                   root=constants.TESTS_RES_DIR):
    datadir = root / role_name / ('ok' if success else 'ng')
    for path in sorted(datadir.glob('*.yml')):
        yield gen_ref_tdata(path)


# .. seealso:: The output of ls tests/res/DebugRule/*/*.yml
@pytest.mark.parametrize(
    ('rule_name', 'success', 'exp'),
    (('DebugRule', True, list(each_ref_tdata('DebugRule', True))),
     ('DebugRule', False, list(each_ref_tdata('DebugRule', False))),
     )
)
def test_each_test_data_for_rule(rule_name, success, exp):
    assert list(TT.each_test_data_for_rule(rule_name, success)) == exp

# vim:sw=4:ts=4:et:
