# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - utilities.
"""
import contextlib
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


def each_clear_fn(maybe_memoized_fns: typing.Iterable[typing.Any]
                  ) -> typing.Callable[..., None]:
    """Yield callable object from ``maybe_memoized_fns``.
    """
    for fun in maybe_memoized_fns:
        if fun and callable(fun):
            clear_fn = getattr(fun, 'cache_clear', False)
            if clear_fn and callable(clear_fn):
                yield clear_fn


def get_env(env_updates: typing.Dict[str, str],
            safe_list: typing.Iterable[str] = constants.SAFE_ENV_VARS
            ) -> typing.Dict[str, str]:
    """Get os.environ subset updated with ``env_updates``.

    .. seealso:: ansiblelint.testing.run_ansible_lint
    """
    env = env_updates.copy() if env_updates else dict()

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

    except (IOError, OSError) as exc:
        warnings.warn(f'Failed to open {path!s}, exc={exc!r}')

    return {}


def load_sub_data_in_dir(workdir: typing.Optional[pathlib.Path] = None):
    """Load data (env or config) from given dir.
    """
    if workdir and workdir.is_dir():
        with chdir(workdir):
            return load_sub_data_in_dir()

    return datatypes.SubData(
        load_data(pathlib.Path('conf.json')),
        load_data(pathlib.Path('env.json'))
    )

# vim:sw=4:ts=4:et:
