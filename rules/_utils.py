# Copyright (C) 2020,2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
"""Common utility functions.
"""
import re
import typing
import warnings

if typing.TYPE_CHECKING:
    import ansiblelint.rules


C_NAME: str = 'name'
C_UNICODE: str = 'unicode'


def make_valid_name_pattern_from_rule_config(
    rule: 'ansiblelint.rules.AnsibleLintRule',
    default: typing.Pattern,
    name_config_key: str = C_NAME,
    unicode_config_key: str = C_UNICODE
) -> typing.Pattern:
    """Make a regexp pattern object to test given name is valid or not.
    """
    pattern_s = rule.get_config(name_config_key)
    if pattern_s:
        try:
            if rule.get_config(unicode_config_key):
                return re.compile(pattern_s)

            return re.compile(pattern_s, re.ASCII)
        except BaseException:  # pylint: disable=broad-except
            warnings.warn(f'Invalid name pattern: "{pattern_s}"')

    return default


def is_valid_name(pattern: typing.Pattern, name: str) -> bool:
    """
    Test if given name is valid or not.
    """
    return pattern.match(name) is not None
