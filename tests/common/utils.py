# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - utilities.
"""
import functools
import itertools
import pathlib
import typing

from . import constants


def concat(xss):
    """
    Concatenates a list of lists.
    """
    return list(itertools.chain.from_iterable(xs for xs in xss))


def strip_words(astr: str, *words: str) -> str:
    """strip given words from ``astr`` one by one.
    """
    return functools.reduce(lambda acc, word: acc.replace(word, ''),
                            words, astr)


def list_resources(name: str, success: bool = True,
                   subdir: typing.Optional[str] = None,
                   pattern: typing.Optional[str] = None
                   ) -> typing.List[str]:
    """
    List resource data files for OK or NG test cases.
    """
    if subdir is None or not subdir:
        subdir = 'ok' if success else 'ng'

    if not pattern:
        pattern = '*.*'

    root = constants.TESTS_RES_DIR / name / subdir
    return sorted(str(p) for p in root.glob(pattern) if p.is_file())


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

# vim:sw=4:ts=4:et:
