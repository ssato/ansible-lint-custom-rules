# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if playbook files have valid filenames.
"""
import functools
import os
import re

try:
    from ansiblelint.rules import AnsibleLintRule
except ImportError:
    from ansiblelint import AnsibleLintRule


_RULE_ID = "Custom_2020_4"
_ENVVAR_PREFIX = "_ANSIBLE_LINT_RULE_" + _RULE_ID.upper()

FILENAME_ENVVAR = _ENVVAR_PREFIX + "_PLAYBOOK_FILENAME_RE"
DEFAULT_FILENAME_RE = r"^\w+\.ya?ml$"


@functools.lru_cache(maxsize=32)
def filename_re():
    """
    :return: regexp object to try match
    """
    return re.compile(os.environ.get(FILENAME_ENVVAR, DEFAULT_FILENAME_RE),
                      re.ASCII)


def is_invalid_filename(filepath, regex=None):
    """
    :param filepath: A str represents a file path
    :return: True if given `filename` is invalid and does not satisfy the rule
    """
    if regex is None:
        regex = filename_re()

    return regex.match(os.path.basename(filepath)) is None


def check_playbook_filename(_self, file_, _play):
    """
    .. seealso:: ansiblelint.rules.AnsibleLintRule.matchyaml
    """
    if file_["type"] == "playbook":
        playbook = file_["path"]

        if is_invalid_filename(playbook):
            return [({"Playbook[s] may have invalid filename[s]": playbook},
                     "Invalid filename: {}".format(playbook))]

    return []


class PlaybookFileHasValidNameRule(AnsibleLintRule):
    """
    Rule class to test if playbook file has a valid filename satisfies the file
    naming rules in the organization.
    """
    id = _RULE_ID
    shortdesc = "Playbook files should have valid filenames"
    description = shortdesc
    severity = "MEDIUM"
    tags = ["playbook", "readability", "formatting"]
    version_added = "4.2.99"  # dummy

    matchplay = check_playbook_filename
