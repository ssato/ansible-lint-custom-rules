# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Entry point of tests.common.*.
"""
from .constants import (
    TESTS_DIR, TESTS_RES_DIR, RULES_DIR,
)
from .testcases import (
    MaybeModNameT, MaybeModT, MaybeCallableT,
    RuleTestCase, CliTestCase
)
from .utils import (
    get_rule_instance_by_module, get_rule_instance_by_name
)

__all__ = [
    'TESTS_DIR', 'TESTS_RES_DIR', 'RULES_DIR', 'DEFAULT_RULES_DIR',
    'MaybeModNameT', 'MaybeModT', 'MaybeCallableT',
    'RuleTestCase', 'CliTestCase',
    'get_rule_instance_by_module', 'get_rule_instance_by_name'
]
