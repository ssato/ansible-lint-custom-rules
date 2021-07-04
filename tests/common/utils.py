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

import yaml

from . import datatypes


@contextlib.contextmanager
def chdir(destdir: pathlib.Path):
    """Chnage dir temporary.
    """
    if not destdir.exists():
        raise OSError(f'Destination dir does NOT exist: {destdir!s}')

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


def load_data(path: pathlib.Path):
    """An wrapper for json.load and yaml.load.
    """
    try:
        with path.open(encoding='utf-8') as fio:
            if path.suffix == '.json':
                return json.load(fio)

            if path.suffix in ('.yaml', '.yml'):
                return yaml.load(fio, Loader=yaml.FullLoader)

    except (IOError, OSError) as exc:
        warnings.warn(f'Failed to open {path!s}, exc={exc!r}')

    return {}


VALID_SUFFIXES: typing.FrozenSet = frozenset(
    ('.json', '.yaml', '.yml')
)


def find_sub_data_path(data_path: pathlib.Path, subdir: str,
                       valid_suffixes=VALID_SUFFIXES
                       ) -> typing.Optional[pathlib.Path]:
    """
    Find a sub data path.
    """
    files = sorted(
        f for f in data_path.parent.glob(f'{subdir}/{data_path.stem}.*')
        if f.is_file() and f.suffix in valid_suffixes
    )
    if files:
        return files[0]

    return None


def each_test_data_for_rule(rule_datadir: pathlib.Path,
                            success: bool = True,
                            ) -> typing.Iterator[datatypes.DataT]:
    """
    Yield test data files for the given rule ``rule`` (name).
    """
    datadir = rule_datadir / ('ok' if success else 'ng')
    for data in sorted(datadir.glob('*.yml')):
        if not data.is_file():
            continue

        conf = dict()
        cpath = find_sub_data_path(data, 'c')
        if cpath:
            conf = load_data(cpath)

        env = dict()
        epath = find_sub_data_path(data, 'env')
        if epath:
            env = load_data(epath)

        yield datatypes.TData(datadir, data, conf, env)

# vim:sw=4:ts=4:et:
