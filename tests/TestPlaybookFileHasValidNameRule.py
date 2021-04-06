# Copyright (C) 2020,2021 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,missing-class-docstring
"""Test cases for the rule, PlaybookFileHasValidNameRule.
"""
import pytest

from rules import PlaybookFileHasValidNameRule as TT
from tests import common


_ENV_PATCH = {TT.FILENAME_ENVVAR: "\\S+NEVER_MATCH"}


class Base:
    this_py = __file__
    this_mod = TT
    clear_fn = TT.filename_re.cache_clear


class RuleTestCase(Base, common.RuleTestCase):
    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_20_ng_cases(self):
        super().test_20_ng_cases()

    @pytest.mark.skip(
        reason=('Until a solution to set os.enviorn during call'
                'runner.run_playboo().')
    )
    def test_30_playbook_file_has_valid_name__ng(self):
        self.lint(False, 'ok', env=_ENV_PATCH)


class CliTestCase(Base, common.CliTestCase):
    def test_30_ng_cases__env(self):
        self.lint(False, 'ok', env=_ENV_PATCH)
