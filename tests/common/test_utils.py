# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-function-docstring
"""Test cases of tests.common.runner.
"""
import functools
import os
import pathlib
import random
import warnings

import pytest

from tests.common import constants, datatypes, utils as TT


def test_chdir(tmp_path):
    """
    .. todo::

       Add some checks to make it more robust:

       - Does the parent dir of ``tmp_path`` exists if ``tmp_path`` is a file?
       - Does the file ``tmp_path`` exists already if ``tmp_path`` is a file?
    """
    pwd = pathlib.Path().cwd()
    with TT.chdir(tmp_path):
        assert pathlib.Path().cwd() != pwd
        assert pathlib.Path().cwd() == tmp_path

    assert pathlib.Path().cwd() != tmp_path
    assert pathlib.Path().cwd() == pwd


@functools.lru_cache(None)
def randome_int(imax: int = 100000000):
    return random.randint(0, imax)


def test_clear_all_lru_cache():
    first = randome_int()
    second = randome_int()  # It should be cached one, first.
    assert first == second

    TT.clear_all_lru_cache()
    # There is an 1 / imax chance that it fails.
    assert first != randome_int()


@pytest.mark.parametrize(
    ('updates', 'safe_list'),
    (({}, constants.SAFE_ENV_VARS),
        ({'FOO': 'FOO'}, constants.SAFE_ENV_VARS),
     )
)
def test_get_env(updates, safe_list):
    env = TT.get_env(updates, safe_list)
    assert env
    assert all(v in env for v in safe_list if v in os.environ), env
    assert all(v not in env for v in os.environ
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
def test_load_sub_ctx_data_in_dir(workdir, conf, env):
    res = TT.load_sub_ctx_data_in_dir(workdir)
    assert bool(res)
    assert isinstance(res, datatypes.SubCtx)
    assert bool(res.conf) == conf, res.conf  # TBD
    assert bool(res.env) == env, res.env  # TBD
    assert bool(res.os_env) == env, res.os_env  # TBD

# vim:sw=4:ts=4:et:
