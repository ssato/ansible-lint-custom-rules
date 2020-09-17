# Copyright (C) 2020 Red Hat, Inc.
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Test cases for the rule, PlaybookFileHasValidNameRule.
"""
import os
import mock

from rules import PlaybookFileHasValidNameRule as TT
from tests import common as C


_ENV_PATCH = {TT.FILENAME_ENVVAR: "\\S+NEVER_MATCH"}


class Base(object):
    """Base Mixin class."""
    prefix = "PlaybookFileHasValidNameRule"
    rule = getattr(TT, prefix)()
    clear_fn = TT.filename_re.cache_clear


class RuleTestCase(Base, C.AnsibleLintRuleTestCase):
    """Test cases for the rule class, PlaybookFileHasValidNameRule.
    """
    @mock.patch.dict(os.environ, _ENV_PATCH)
    def test_30_playbook_file_has_valid_name__ng(self):
        self.lint(False, self.path_pattern())


class CliTestCase(Base, C.AnsibleLintRuleCliTestCase):
    """CLI Test cases for the rule class, PlaybookFileHasValidNameRule.
    """
    def test_30_ng_cases__env(self):
        self.lint(False, self.path_pattern(), _ENV_PATCH)
