# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
"""Common utility test routines and classes - utilities.
"""
import contextlib
import functools
import gc
import json
import os
import pathlib
import typing
import warnings

from . import constants, datatypes


@contextlib.contextmanager
def chdir(destdir: pathlib.Path):
    """Chnage dir temporary.
    """
    saved = pathlib.Path().cwd()
    try:
        os.chdir(str(destdir))
        yield
    finally:
        os.chdir(str(saved))


# pylint: disable=protected-access
def clear_all_lru_cache():
    """Clear the cache of all lru_cache-ed functions.
    """
    gc.collect()
    wrappers = (
        obj for obj in gc.get_objects()
        if callable(obj) and isinstance(obj, functools._lru_cache_wrapper)
    )
    for wrapper in wrappers:
        wrapper.cache_clear()


def get_env(env_updates: typing.Dict[str, str],
            safe_list: typing.Iterable[str] = constants.SAFE_ENV_VARS
            ) -> typing.Dict[str, str]:
    """Get os.environ subset updated with ``env_updates``.

    .. seealso:: ansiblelint.testing.run_ansible_lint
    """
    env = env_updates.copy() if env_updates else {}

    for val in safe_list:
        if val in os.environ and val not in env:
            env[val] = os.environ[val]

    return env


def load_data(path: pathlib.Path, warn: bool = False):
    """An wrapper for json.load.
    """
    if not path.exists():
        if warn:
            warnings.warn(f'Not exist: {path!s}')
        return {}

    try:
        with path.open(encoding='utf-8') as fio:
            return json.load(fio)

    except OSError as exc:
        warnings.warn(f'Failed to open {path!s}, exc={exc!r}')

    return {}


def load_sub_ctx_data_in_dir(
    workdir: typing.Optional[pathlib.Path],
    sub_ctx_names: typing.Tuple[str, str] = constants.SUB_CTX_NAMES
) -> datatypes.SubCtx:
    """Load sub context data (env and/or config) from given or current dir.
    """
    conf = load_data(workdir / sub_ctx_names[0])
    env = load_data(workdir / sub_ctx_names[1])
    os_env = get_env(env) if env else {}

    return datatypes.SubCtx(conf, env, os_env)

# vim:sw=4:ts=4:et:
