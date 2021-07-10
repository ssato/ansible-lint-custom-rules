# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.runner.
"""
import functools
import os
import pathlib
import warnings

import pytest

from tests.common import constants, datatypes, utils as TT


def test_chdir(tmp_path):
    # todo:
    # a_file_path = tmp_path / 'a_file.txt'
    # a_file_path.touch()
    # assert a_file_path.exists() and a_file_path.is_file(), a_file_path

    # with pytest.raises(NotADirectoryError):
    #     TT.chdir(a_file_path)

    # with pytest.raises(FileNotFoundError):
    #     TT.chdir(tmp_path / 'this_dir_should_not_exist')

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


@pytest.mark.parametrize(
    ('updates', 'safe_list'),
    ((dict(), constants.SAFE_ENV_VARS),
     (dict(FOO='FOO'), constants.SAFE_ENV_VARS),
     )
)
def test_get_env(updates, safe_list):
    env = TT.get_env(updates, safe_list)
    assert env
    assert all(v in env for v in safe_list if v in os.environ), env
    assert all(v not in env for v in os.environ.keys()
               if v not in safe_list and v not in updates), env
    assert all(env[v] == updates[v] for v in updates.keys()), env
    assert all(env[v] == os.environ[v] for v in safe_list
               if v in os.environ and v not in updates), env


# see: tests/res/DebugRule/ng/**/*.*
@pytest.mark.parametrize(
    ('path', 'warn', 'exp'),
    ((constants.TESTS_RES_DIR / 'DebugRule/ng/2/env.json', False, True),
     (constants.TESTS_RES_DIR / 'not_exist.json', False, False),
     (constants.TESTS_RES_DIR / 'not_exist.json', True, False),
     )
)
def test_load_data(path, warn, exp):
    with warnings.catch_warnings(record=True) as warns:
        warnings.simplefilter("always")

        result = TT.load_data(path, warn=warn)
        assert bool(result) == exp

        if not exp and warn:
            assert len(warns) > 0
            assert issubclass(warns[-1].category, UserWarning)
            assert 'Not exist' in str(warns[-1].message)


@pytest.mark.parametrize(
    ('workdir', 'conf', 'env'),
    ((constants.TESTS_RES_DIR / 'DebugRule/ok/0', False, False),
     (constants.TESTS_RES_DIR / 'DebugRule/ng/1', True, False),
     (constants.TESTS_RES_DIR / 'DebugRule/ng/2', False, True),
     )
)
def test_load_sub_data_in_dir(workdir, conf, env):
    res = TT.load_sub_data_in_dir(workdir)
    assert bool(res)
    assert isinstance(res, datatypes.SubData), res
    assert bool(res.conf) == conf, res.conf  # TBD
    assert bool(res.env) == env, res.env  # TBD

# vim:sw=4:ts=4:et:
