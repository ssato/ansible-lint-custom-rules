# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
# pylint: disable=too-few-public-methods
"""Test cases for the rule, VarsInVarsFilesHaveValidNamesRule.
"""
from rules import VarsInVarsFilesHaveValidNamesRule as TT
from tests import common


class Base(common.Base):
    this_mod: common.MaybeModT = TT
    default_skip_list = ['no_unspecified_argument','role_vars_start_with_role_name','vars_should_not_be_used']


class RuleTestCase(common.RuleTestCase):
    base_cls = Base


class CliTestCase(common.CliTestCase):
    base_cls = Base
