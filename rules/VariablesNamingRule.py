# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
r"""
Lint rule class to test if some variables follow namging conventions and
guildelines.

Users can change the behavior of this class by specifying some envrionment
variables.

- Users can specify the inventory file path with the enviornment variable,
  _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY, for exampke,

  ::

      _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY="/tmp/hosts.ini"

- Users can specify the variable name regex pattern by the enviornment
  variable, _ANSIBLE_LINT_RULE_CUSTOM_2020_3_VAR_NAME_RE, for example,

  ::

    _ANSIBLE_LINT_RULE_CUSTOM_2020_3_VAR_NAME_RE="\\w+"

.. note::
   This class assume that variable names consist of only ASCII chars.
"""
import collections.abc
import itertools
import os.path
import os
import re

# .. note:: Maybe it depends on specific versions of ansible.
import ansible.errors
import ansible.inventory.manager
import ansible.parsing.dataloader
import ansible.playbook
import ansible.vars.manager
import ansiblelint


_RULE_ID = "Custom_2020_3"
_ENVVAR_PREFIX = "_ANSIBLE_LINT_RULE_" + _RULE_ID.upper()

# Ugh! there is no constant global var define this in ansible.constants...
INVENTORY_ENVVAR = _ENVVAR_PREFIX + "_INVENTORY"
INVENTORY = os.environ.get(INVENTORY_ENVVAR, "/etc/ansible/hosts")

NAME_RE_S = r"[a-zA-Z_]\w+"
NAME_RE_ENVVAR = _ENVVAR_PREFIX + "_VAR_NAME_RE"
NAME_RE = re.compile(os.environ.get(NAME_RE_ENVVAR, NAME_RE_S),
                     re.ASCII)

SPECIAL_VAR_NAMES = frozenset("""
all
ansible_dependent_role_names
ansible_play_batch
ansible_play_hosts
ansible_play_hosts_all
ansible_play_name
ansible_play_role_names
ansible_playbook_python
ansible_role_names
ansible_version
groups
host
omit
password
play_hosts
playbook_dir
role_names
server
server_port
transport
ungrouped
user
username
vars
""".split())


def test_if_name_not_match(name=None, reg=None):
    """Test if given name does *not* match the regex pattern.

    :param name: A str tries to try matching with `reg`
    :param reg: A maybe compiled regexp str

    :return: True if `name` does *not* match with `reg`
    """
    if reg is None:
        reg = NAME_RE

    if name is None:
        return False

    return reg.match(name) is None


def nested_objs_items(obj):
    """
    :param obj: A nested dict or dict-like (mapping) object or iterables
    :return: A whole list of dict key names including children's

    >>> nd0 = dict(a=1, b=dict(c=2, d=dict(e=3, f=dict(g=4))))
    >>> res = list(nested_objs_items(nd0))
    >>> res  # doctest: +NORMALIZE_WHITESPACE
    [('a', 1), ('b', {'c': 2, 'd': {'e': 3, 'f': {'g': 4}}}), ('c', 2),
     ('d', {'e': 3, 'f': {'g': 4}}), ('e', 3), ('f', {'g': 4}), ('g', 4)]

    >>> list(nested_objs_items([nd0])) == res
    True
    """
    if not obj or obj is None:
        return

    objs = [obj] if isinstance(obj, collections.abc.Mapping) else obj

    for item in objs:
        for key, val in item.items():
            yield (key, val)
            if isinstance(val, collections.abc.Mapping):
                for ckey, cval in nested_objs_items(val):
                    yield (ckey, cval)


def nested_obj_keys(obj):
    """
    :param obj: A nested dict or dict-like (mapping) object or iterables
    :return: A whole list of dict key names including children's

    >>> nd0 = dict(a=1, b=dict(c=2, d=dict(e=3, f=dict(g=4))))
    >>> list(nested_obj_keys(nd0))
    ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    """
    for key, _val in nested_objs_items(obj):
        yield key


def is_special_var_name(name):
    """
    :return: True if given `name` is a special variable name in ansible
    """
    return name in SPECIAL_VAR_NAMES or name.startswith("ansible_")


def list_invalid_var_names_from_playbook(playbook):
    """
    :param playbook: An abosolute path of the playbook file
    :return: A list of variable names don't match with valid regexp patterns
    """
    loader = ansible.parsing.dataloader.DataLoader()
    inventory = ansible.inventory.manager.InventoryManager(loader, INVENTORY)
    vmgr = ansible.vars.manager.VariableManager(loader, inventory)

    # :raises: ansible.errors.AnsibleParserError("Invalid variable name...")
    playbook = ansible.playbook.Playbook.load(playbook, vmgr, loader)

    vss = (nested_obj_keys(vs) for vs
           in (vmgr.get_vars(play) for play in playbook.get_plays()))

    return [v for v in set(itertools.chain.from_iterable(vss))
            if not is_special_var_name(v) and test_if_name_not_match(v)]


def list_invalid_var_names_in_play(_self, file, _play):
    """
    .. seealso:: ansiblelint.AnsibleLintRule.matchyaml
    """
    if file["type"] == "playbook":
        playbook = file["path"]

        return [({"Playbook may have invalid var name[s]": playbook},
                 "Invalid var name: {}".format(n))
                for n in list_invalid_var_names_from_playbook(playbook)]

    return []


class VariablesNamingRule(ansiblelint.AnsibleLintRule):
    """
    Lint rule class to test if variables defined by users follow the namging
    conventions and guildelines.
    """
    id = _RULE_ID
    shortdesc = "All variables should be named correctly"
    description = (
        "All variables should have a valid name satisfies the naming rule"
    )
    severity = "MEDIUM"
    tags = ["variables"]  # temp
    version_added = "4.2.99"  # dummy

    matchplay = list_invalid_var_names_in_play

# vim:sw=4:ts=4:et:
