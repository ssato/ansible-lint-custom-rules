# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - utilities.
"""
import typing

import yaml

from .datatypes import DataT, TData
from . import constants


def each_test_data_for_rule(rule: str, success: bool = True,
                            root: str = constants.TESTS_RES_DIR
                            ) -> typing.Iterator[DataT]:
    """
    Yield test data files for the given rule ``rule`` (name).
    """
    datadir = root / rule / ('ok' if success else 'ng')
    for data in datadir.glob('*.yml'):
        if not data.is_file():
            continue

        conf = dict()
        cpath = datadir / 'c' / data.name
        if cpath.exists() and cpath.is_file():
            conf = yaml.load(cpath.open(), Loader=yaml.FullLoader)

        yield TData(datadir, data, conf)

# vim:sw=4:ts=4:et:
