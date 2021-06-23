# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Entry point of tests.common.*.
"""
from .constants import (
    TESTS_DIR, TESTS_RES_DIR, RULES_DIR,
)
from .testcases import (
    MaybeModT, Base, RuleTestCase, CliTestCase
)

__all__ = [
    'TESTS_DIR', 'TESTS_RES_DIR', 'RULES_DIR', 'DEFAULT_RULES_DIR',
    'MaybeModT', 'Base', 'RuleTestCase', 'CliTestCase',
]
