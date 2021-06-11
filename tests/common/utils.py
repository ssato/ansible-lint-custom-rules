# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - utilities.
"""
import functools
import pathlib
import typing

import yaml

from .datatypes import DataT, TData
from . import constants


def strip_words(astr: str, *words: str) -> str:
    """strip given words from ``astr`` one by one.
    """
    return functools.reduce(lambda acc, word: acc.replace(word, ''),
                            words, astr)


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


def get_rule_name(test_py: str = __file__) -> str:
    """
    Resolve the name of the rule to test from the filename of the test code.
    """
    return strip_words(pathlib.Path(test_py).name, '.py', 'test_', 'Test')


def get_rule_instance_by_name(rule_module, rule_name):
    """
    Get the rule instance by rule module filename.
    """
    rule_cls = getattr(rule_module, rule_name)
    if not rule_cls:
        raise ValueError(f'No such rule class {rule_name} '
                         f'in {rule_module!r}.')
    return rule_cls()


def get_rule_instance_by_module(test_py: str, rule_module):
    """
    Get the rule instance by rule module's filename and module object.
    """
    rule_name = get_rule_name(test_py)
    return get_rule_instance_by_name(rule_module, rule_name)

# vim:sw=4:ts=4:et:
