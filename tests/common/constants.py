# Copyright (C) 2020, 2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - Some constants.
"""
import pathlib


TESTS_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
TESTS_RES_DIR = TESTS_DIR / 'res'

RULES_DIR = TESTS_DIR.parent / 'rules'

# vim:sw=4:ts=4:et:
