# Copyright (C) 2020, 2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
"""Common utility test routines and classes - Some constants.
"""
import pathlib

import ansiblelint.utils


TESTS_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
TESTS_RES_DIR = TESTS_DIR / 'res'

RULES_SUBDIR: str = 'rules'
RULES_DIR = TESTS_DIR.parent / RULES_SUBDIR

DEFAULT_RULES_DIR: str = str(
    pathlib.Path(ansiblelint.utils.__file__).parent / RULES_SUBDIR
)

# vim:sw=4:ts=4:et:
