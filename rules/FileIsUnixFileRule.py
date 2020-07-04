# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>
#
# SPDX-License-Identifier: MIT
#
"""
Lint rule class to test if files are UNIX files of which lines end with CR+LF.
"""
import ansiblelint


_RULE_ID = "Custom_2020_70"


def is_not_unix_file(filepath):
    """Test if given file does not end with CR+LF.

    .. seealso:: https://docs.python.org/3/library/functions.html#open
    """
    return any(line for line in open(filepath, newline='')
               if line.endswith("\r\n") or line.endswith("\r"))


def _matchplay(_self, file_, _play):
    """Test playbook is Unix file.
    """
    fpath = file_["path"]
    if is_not_unix_file(fpath):
        return [({"File may not be a Unix style file": fpath},
                 "Not a Unix style file: {}".format(fpath))]
    return []


def _match(_self, file_, _task):
    """Test task files.
    """
    fpath = file_["path"]
    if is_not_unix_file(fpath):
        return "Not a Unix style file: {}".format(fpath)

    return False


class FileIsUnixFileRule(ansiblelint.AnsibleLintRule):
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
