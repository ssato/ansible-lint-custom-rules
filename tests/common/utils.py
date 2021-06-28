# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - utilities.
"""
import typing

import yaml

from . import constants, datatypes


def each_clear_fn(maybe_memoized_fns: typing.Iterable[typing.Any]
                  ) -> typing.Callable[..., None]:
    """Yield callable object from ``maybe_memoized_fns``.
    """
    for fun in maybe_memoized_fns:
        if fun and callable(fun):
            clear_fn = getattr(fun, 'cache_clear', False)
            if clear_fn and callable(clear_fn):
                yield clear_fn


def each_test_data_for_rule(rule: str, success: bool = True,
                            root: str = constants.TESTS_RES_DIR
                            ) -> typing.Iterator[datatypes.DataT]:
    """
    Yield test data files for the given rule ``rule`` (name).
    """
    datadir = root / rule / ('ok' if success else 'ng')
    for data in sorted(datadir.glob('*.yml')):
        if not data.is_file():
            continue

        conf = dict()
        cpath = datadir / 'c' / data.name
        if cpath.exists() and cpath.is_file():
            conf = yaml.load(cpath.open(), Loader=yaml.FullLoader)

        env = dict()
        epath = datadir / 'env' / data.name
        if epath.exists() and epath.is_file():
            env = yaml.load(epath.open(), Loader=yaml.FullLoader)

        yield datatypes.TData(datadir, data, conf, env)

# vim:sw=4:ts=4:et:
