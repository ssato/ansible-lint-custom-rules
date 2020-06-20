# Copyright (C) 2020 Satoru SATOH <satoru.satoh@gmail.com>
#
# SPDX-License-Identifier: MIT
#
r"""
Lint rule class to test if some modules in the blacklist are used.

Users can change the behavior of this class by specifying some envrionment
variables.

- Users can specify the blacklisted modules with the environment variable,
  _ANSIBLE_LINT_RULE_CUSTOM_2020_20_BLACKLISTED_MODULES, for exampke,

  ::

      _ANSIBLE_LINT_RULE_CUSTOM_2020_20_BLACKLISTED_MODULES="shell raw"

- Users can specify the modules blacklist file with the environment variable,
  _ANSIBLE_LINT_RULE_CUSTOM_2020_20_MODULES_BLACKLIST, for exampke,

  ::

      _ANSIBLE_LINT_RULE_CUSTOM_2020_20_MODULES_BLACKLIST="/tmp/mb.list"

  The modules blacklist file must contain module names to be blacklisted line
  by line, and comments in the file starts with '#' are ignored like this:

  ::

     # this is a comment line.
     shell
     include

  .. note::
     modules in the blacklist will have higher prio. than modules specified in
     _ANSIBLE_LINT_RULE_CUSTOM_2020_20_BLACKLISTED_MODULES.

.. seealso:: :class:`~ansiblielint.rules.DeprecatedModuleRule`
"""
import functools
import os

# .. note:: Maybe it depends on specific versions of ansible.
import ansiblelint


_RULE_ID = "Custom_2020_20"
_ENVVAR_PREFIX = "_ANSIBLE_LINT_RULE_" + _RULE_ID.upper()

BLACKLISTED_MODULES_ENVVAR = _ENVVAR_PREFIX + "_BLACKLISTED_MODULES"
BLACKLIST_ENVVAR = _ENVVAR_PREFIX + "_MODULES_BLACKLIST"

BLACKLISTED_MODULES = frozenset("""
shell
include
""".split())


@functools.lru_cache(maxsize=32)
def blacklisted_modules(bmods=BLACKLISTED_MODULES):
    """
    :return: True if to use ansible internal functions to find var names
    """
    # Try to load blacklisted modules from the file user gave first.
    blacklist = os.environ.get(BLACKLIST_ENVVAR, False)
    if blacklist:
        try:
            return [line.strip() for line in open(blacklist)
                    if not line.startswith("#")]
        except (IOError, OSError):
            pass

    # Next, try to load them from the env. var.
    bmods_s = os.environ.get(BLACKLISTED_MODULES_ENVVAR, False)
    if bmods_s:
        return bmods_s.split()  # e.g. "shell raw ..." -> ["shell", "raw"]

    return BLACKLISTED_MODULES  # default


class BlacklistedModuleRule(ansiblelint.AnsibleLintRule):
    """
    Lint rule class to test if variables defined by users follow the namging
    conventions and guildelines.
    """
    id = _RULE_ID
    shortdesc = "Blacklisted modules"
    description = "Use of the blacklisted modules are prohivited."
    severity = "HIGH"
    tags = ["modules"]  # temp
    version_added = "4.2.99"  # dummy

    def matchtask(self, _file, task):
        """Match with lines in a task definition
        """
        module = task["action"]["__ansible_module__"]

        if module in blacklisted_modules():
            return "{0}: use of {1} is prohivited.".format(self.shortdesc,
                                                           module)
        return False

# vim:sw=4:ts=4:et:
