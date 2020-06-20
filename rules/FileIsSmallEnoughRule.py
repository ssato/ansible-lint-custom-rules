# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
"""Lint rule class to test if playbook files are small enough.

Users can change the behavior of this class by specifying an environment
variable, _ANSIBLE_LINT_RULE_CUSTOM_2020_30_MAX_LINES.

::

    _ANSIBLE_LINT_RULE_CUSTOM_2020_30_MAX_LINES=500


"""
import functools
import os

import ansiblelint


_RULE_ID = "Custom_2020_40"
_ENVVAR_PREFIX = "_ANSIBLE_LINT_RULE_" + _RULE_ID.upper()

MAX_LINES_ENVVAR = _ENVVAR_PREFIX + "_MAX_LINES"
MAX_LIENS = 500


@functools.lru_cache(maxsize=32)
def max_lines():
    """
    :return: A int denotes the max line of playbook and related files
    """
    return int(os.environ.get(MAX_LINES_ENVVAR, MAX_LIENS))


def exceeds_max_lines(filepath, mlines=None):
    """
    :param filepath: A str gives a file path
    :return: True if given file is not small and exceeds max lines

    >>> exceeds_max_lines(__file__, 1000000)
    False
    >>> exceeds_max_lines(__file__, 10)
    True
    """
    if not mlines:
        mlines = max_lines()

    with open(filepath) as fobj:
        # Which is better?
        # return len(fobj.readliens()) > mlines
        for idx, _line in enumerate(fobj):
            if idx + 1 > mlines:
                return True

    return False


def _matchplay(_self, file, _play):
    """Test playbook files.
    """
    if file["type"] == "playbook":
        fpath = file["path"]

        if exceeds_max_lines(fpath):
            return [({"Playbook[s] may be too large": fpath},
                     "Too large: {}".format(fpath))]
    return []


def _match(_self, file, _task):
    """Test task files.
    """
    if file["type"] == "tasks":
        fpath = file["path"]
        if exceeds_max_lines(fpath):
            return "Too large: {}".format(fpath)

    return False


class FileIsSmallEnoughRule(ansiblelint.AnsibleLintRule):
    """
    Rule class to test if playbook and tasks files are small enough.
    """
    id = _RULE_ID
    shortdesc = "Playbook and tasks files should be small enough"
    description = shortdesc
    severity = "MEDIUM"
    tags = ["playbook", "tasks", "readability"]
    version_added = "4.2.99"  # dummy

    matchplay = _matchplay
    match = _match

# vim:sw=4:ts=4:et:
