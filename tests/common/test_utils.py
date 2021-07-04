# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.runner.
"""
import functools
import pathlib
import warnings

import pytest

from tests.common import constants, datatypes, utils as TT


def test_chdir(tmp_path):
    # todo:
    # with pytest.raises(OSError):
    #    TT.chdir(tmp_path / 'this_dir_should_not_exist')

    pwd = pathlib.Path().cwd()
    with TT.chdir(tmp_path):
        assert pathlib.Path().cwd() != pwd
        assert pathlib.Path().cwd() == tmp_path

    assert pathlib.Path().cwd() != tmp_path
    assert pathlib.Path().cwd() == pwd


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


# see: tests/res/DebugRule/ng/**/*.*
DATA_PATH_EX_0 = constants.TESTS_RES_DIR / 'DebugRule/ng/2.yml'
SUB_DATA_PATH_EX_0 = constants.TESTS_RES_DIR / 'DebugRule/ng/env/2.yml'


@pytest.mark.parametrize(
    ('path', 'exp'),
    ((SUB_DATA_PATH_EX_0, True),
     (constants.TESTS_RES_DIR / 'not_exist.yml', False),
     )
)
def test_load_data(path, exp):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")

        result = TT.load_data(path)
        assert bool(result) == exp

        if not exp:
            assert len(warns) > 0
            assert issubclass(warns[-1].category, UserWarning)
            assert 'Failed to open' in str(warns[-1].message)


@pytest.mark.parametrize(
    ('path', 'subdir', 'exp'),
    ((DATA_PATH_EX_0, 'env', SUB_DATA_PATH_EX_0),
     (SUB_DATA_PATH_EX_0, 'c', None),
     )
)
def test_find_sub_data_path(path, subdir, exp):
    assert TT.find_sub_data_path(path, subdir) == exp


def gen_ref_tdata(path):
    datadir = path.parent
    filename = path.name

    conf = dict()
    cpath = datadir / 'c' / filename
    if cpath.exists():
        conf = TT.load_data(cpath)

    env = dict()
    epath = datadir / 'env' / filename
    if epath.exists():
        env = TT.load_data(epath)

    return datatypes.TData(datadir, path, conf, env)


def each_ref_tdata(role_name, success=True,
                   root=constants.TESTS_RES_DIR):
    datadir = root / role_name / ('ok' if success else 'ng')
    for path in sorted(datadir.glob('*.yml')):
        yield gen_ref_tdata(path)


RULE_TEST_DATA_DIR = constants.TESTS_RES_DIR / 'DebugRule'


# .. seealso:: The output of ls tests/res/DebugRule/*/*.yml
@pytest.mark.parametrize(
    ('rule_datadir', 'success', 'exp'),
    ((RULE_TEST_DATA_DIR, True, list(each_ref_tdata('DebugRule', True))),
     (RULE_TEST_DATA_DIR, False, list(each_ref_tdata('DebugRule', False))),
     )
)
def test_each_test_data_for_rule(rule_datadir, success, exp):
    assert list(TT.each_test_data_for_rule(rule_datadir, success)) == exp

# vim:sw=4:ts=4:et:
