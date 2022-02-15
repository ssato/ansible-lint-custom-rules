# Copyright (C) 2022 Guido Grazioli <guido.grazioli@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods,missing-class-docstring
# pylint: disable=missing-function-docstring
"""Test cases for the rule, NoUnspecifiedArgumentRule.
"""
import pytest

from rules import NoUnspecifiedArgumentRule as TT
from tests import common


RES_DIR = common.TESTS_RES_DIR / 'NoUnspecifiedArgumentRule'


class Base(common.Base):
    this_mod: common.MaybeModT = TT


class RuleTestCase(common.RuleTestCase):
    base_cls = Base


class CliTestCase(common.CliTestCase):
    base_cls = Base


@pytest.mark.parametrize(
    ('path', 'varname', 'expected'),
    (
        (RES_DIR / 'ok/0/playbook.yml', "ping_default_var", True),
        (RES_DIR / 'ng/0/playbook.yml', "ping_default_var", False),
    )
)
def test_lookup_argument_specs(path, varname, expected):
	TT._lookup_argument_specs(path, varname)
