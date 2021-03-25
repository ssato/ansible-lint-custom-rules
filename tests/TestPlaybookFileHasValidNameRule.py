# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases for the rule, PlaybookFileHasValidNameRule.
"""
import os
import unittest.mock

from rules import PlaybookFileHasValidNameRule as TT
from tests import common as C


_ENV_PATCH = {TT.FILENAME_ENVVAR: "\\S+NEVER_MATCH"}


class Base:
    name = C.get_rule_name(__file__)
    rule = C.get_rule_instance_by_name(TT, name)
    clear_fn = TT.filename_re.cache_clear


class RuleTestCase(Base, C.RuleTestCase):
    @unittest.mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_playbook_file_has_valid_name__ng(self):
        self.lint(False, 'ok')


class CliTestCase(Base, C.CliTestCase):
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok', _ENV_PATCH)
