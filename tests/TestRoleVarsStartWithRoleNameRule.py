# Copyright (C) 2022 Guido Grazioli <guido.grazioli@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods
"""Test cases for the rule TestRoleVarsStartWithRoleNameRule.
"""
from rules import RoleVarsStartWithRoleNameRule as TT
from tests import common


class Base(common.Base):
    this_mod: common.MaybeModT = TT


class RuleTestCase(common.RuleTestCase):
    base_cls = Base


class CliTestCase(common.CliTestCase):
    base_cls = Base
