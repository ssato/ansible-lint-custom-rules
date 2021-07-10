# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - Some constants.
"""
import pathlib
import typing


TESTS_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
TESTS_RES_DIR = TESTS_DIR / 'res'

RULES_DIR = TESTS_DIR.parent / 'rules'

# .. seealso:: ansiblelint.testsing.run_ansible_lint
SAFE_ENV_VARS: typing.Iterable[str] = (
    'LANG',
    'LC_ALL',
    'LC_CTYPE',
    'NO_COLOR',
    'PATH',
    'PYTHONIOENCODING',
    'PYTHONPATH',
    'TERM',
)

# vim:sw=4:ts=4:et:
