# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Entry point of tests.common.*.
"""
from .constants import (  # flake8: noqa
    TESTS_DIR, RULES_DIR, DEFAULT_RULES_DIR
)
from .testcases import (  # flake8: noqa
    RuleTestCase, CliTestCase
)
