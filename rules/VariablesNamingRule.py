# Copyright (C) 2020 Red Hat, Inc.
#
# SPDX-License-Identifier: MIT
#
r"""
Lint rule class to test if some variables follow namging conventions and
guildelines.

Users can change the behavior of this class by specifying some envrionment
variables.

- Users can switch the way to find variable names with the environment
  variable, _ANSIBLE_LINT_RULE_CUSTOM_2020_3_USE_ANSIBLE, for exampke,

  ::

      _ANSIBLE_LINT_RULE_CUSTOM_2020_3_USE_ANSIBLE=1

- Users can specify the inventory file path with the environment variable,
  _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY, for exampke,

  ::

      _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY="/tmp/hosts.ini"

- Users can specify the variable name regex pattern by the environment
  variable, _ANSIBLE_LINT_RULE_CUSTOM_2020_3_VAR_NAME_RE, for example,

  ::

    _ANSIBLE_LINT_RULE_CUSTOM_2020_3_VAR_NAME_RE="\\w+"

.. note::
   This class assume that variable names consist of only ASCII chars.
"""
import collections.abc
import configparser
import glob
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

import yaml
import yaml.parser


_RULE_ID = "Custom_2020_3"
_ENVVAR_PREFIX = "_ANSIBLE_LINT_RULE_" + _RULE_ID.upper()

USE_ANSIBLE_ENVVAR = _ENVVAR_PREFIX + "_USE_ANSIBLE"

# Ugh! there is no constant global var define this in ansible.constants...
INVENTORY_ENVVAR = _ENVVAR_PREFIX + "_INVENTORY"
INVENTORY_DEFAULT = "/etc/ansible/hosts"

NAME_RE_S = r"[a-zA-Z_]\w+"
NAME_RE_ENVVAR = _ENVVAR_PREFIX + "_VAR_NAME_RE"

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


def use_ansible():
    """
    :return: True if to use ansible internal functions to find var names
    """
    return bool(os.environ.get(USE_ANSIBLE_ENVVAR, False))


def name_re(envvar=None, name_re_s=None):
    """
    :return: compiled regex object to try match
    """
    if envvar is None:
        envvar = NAME_RE_ENVVAR
    if name_re_s is None:
        name_re_s = NAME_RE_S

    return re.compile(os.environ.get(envvar, name_re_s), re.ASCII)


def test_if_name_not_match(name=None, reg=None):
    """Test if given name does *not* match the regex pattern.

    :param name: A str tries to try matching with `reg`
    :param reg: A maybe compiled regexp str

    :return: True if `name` does *not* match with `reg`
    """
    if reg is None:
        reg = name_re()

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


def inventory_filepath():
    """
    :return: A path to inventory file
    """
    return os.environ.get(INVENTORY_ENVVAR, INVENTORY_DEFAULT)


def list_invalid_var_names_from_playbook(playbook):
    """
    :param playbook: An abosolute path of the playbook file
    :return: A list of variable names don't match with valid regexp patterns
    """
    ipath = inventory_filepath()

    loader = ansible.parsing.dataloader.DataLoader()
    inventory = ansible.inventory.manager.InventoryManager(loader, ipath)
    vmgr = ansible.vars.manager.VariableManager(loader, inventory)

    # :raises: ansible.errors.AnsibleParserError("Invalid variable name...")
    playbook = ansible.playbook.Playbook.load(playbook, vmgr, loader)

    vss = (nested_obj_keys(vs) for vs
           in (vmgr.get_vars(play) for play in playbook.get_plays()))

    return [v for v in set(itertools.chain.from_iterable(vss))
            if not is_special_var_name(v) and test_if_name_not_match(v)]


def try_load_yaml_file(filepath):
    """
    :param filepath: YAML file path
    :return: Loaded data if it suceeded to load given YAML file or None
    """
    try:
        return yaml.safe_load(open(filepath))
    except yaml.parser.ParserError:
        pass

    return None


def list_var_names_from_inventory_file_itr(inventory):
    """
    .. note:: This function only lists var names in [*:vars] sections.

    :param inventory: A inventory file path
    :return: A generator yields a variable names from the inventory file
    """
    psr = configparser.ConfigParser()
    psr.optionxform = str  # Preserve (upper) cases
    try:
        psr.read(inventory)
        for sect in psr:
            if sect.endswith(":vars"):
                for key in psr[sect]:
                    yield key

    except configparser.Error:
        raise TypeError("It does not look an inventory file: " + inventory)


def list_var_names_from_yaml_file_itr(filepath, vars_key=None):
    """
    :param files: A list of YAML file paths
    :param vars_key: A str to find variables like "vars"

    :return: A generator yields a variable names in the YAML files
    """
    obj = try_load_yaml_file(filepath)
    if not obj:
        return

    for key, val in nested_objs_items(obj):
        if vars_key is None:
            yield key
        else:
            if key == vars_key and isinstance(val, collections.abc.Mapping):
                for ckey in nested_obj_keys(val):
                    yield ckey


def list_var_names_from_yaml_files_itr(files, vars_key=None):
    """
    :param files: A list of YAML file paths
    :param vars_key: A str to find variables like "vars"

    :return: A generator yields a variable names in the YAML files
    """
    for filepath in files:
        for key in list_var_names_from_yaml_file_itr(filepath,
                                                     vars_key=vars_key):
            yield key


def find_var_names_from_inventory_var_files(inventory):
    """
    .. note:: This function does not find var names in inventory file itself.

    :param inventory: A inventory file path
    :return: A set of variable names
    """
    invdir = os.path.dirname(inventory)
    hfs = glob.glob(os.path.join(invdir, "host_vars", "*.yml"))
    gfs = glob.glob(os.path.join(invdir, "group_vars", "*.yml"))

    return set(list_var_names_from_yaml_files_itr(hfs + gfs))


def find_var_names_from_inventory():
    """
    .. note:: This function does not find var names in inventory file itself.

    :return: A set of variable names
    """
    inventory = inventory_filepath()
    if not inventory:
        return set()

    vnames = set(list_var_names_from_inventory_file_itr(inventory))

    if inventory == INVENTORY_DEFAULT:  # No {host,group}_vars/*.yml
        return vnames

    vnames.update(find_var_names_from_inventory_var_files(inventory))
    return vnames


def find_var_names_from_playbook_file(filepath):
    """
    :param filepath: A playbook file path
    :return: A set of variable names
    """
    return set(list_var_names_from_yaml_file_itr(filepath, vars_key="vars"))


def list_role_names_itr(playbook):
    """
    :param playbook: An abosolute path of the playbook file
    :return: A generator yields role names
    """
    plays = try_load_yaml_file(playbook)
    if not plays:
        return

    for play in plays:
        for role in play.get("roles", []):
            if isinstance(role, collections.abc.Mapping):
                yield role["role"]  # It should have this.
            else:
                yield role


def find_var_names_from_role_files_itr(playbook, vars_file=None):
    """
    .. note::
       This function assume that roles' variables are only defined in
       <playbook_dir>/roles/*/{defaults,vars}/`var_file`.

    :param playbook: An abosolute path of the playbook file
    :param vars_file: File glob pattern or file name which define[s] vars

    :return: A generator yields variable names from roles' var files
    """
    if vars_file is None:
        vars_file = "*.yml"

    for rname in list_role_names_itr(playbook):
        roledir = os.path.join(os.path.dirname(playbook), "roles", rname)

        dfs = glob.glob(os.path.join(roledir, "defaults", vars_file))
        vfs = glob.glob(os.path.join(roledir, "vars", vars_file))

        for vname in list_var_names_from_yaml_files_itr(dfs + vfs):
            yield vname


def list_invalid_var_names_from_playbook_natively(playbook):
    """
    :param playbook: An abosolute path of the playbook file
    :return: A list of variable names don't match with valid regexp patterns
    """
    vs_1 = find_var_names_from_inventory()
    vs_2 = find_var_names_from_playbook_file(playbook)
    vs_3 = find_var_names_from_role_files_itr(playbook)

    return [v for v in set(itertools.chain(vs_1, vs_2, vs_3))
            if not is_special_var_name(v) and test_if_name_not_match(v)]


def list_invalid_var_names_in_play(_self, file, _play):
    """
    .. seealso:: ansiblelint.AnsibleLintRule.matchyaml
    """
    if use_ansible():
        ffn = list_invalid_var_names_from_playbook
    else:
        ffn = list_invalid_var_names_from_playbook_natively

    if file["type"] == "playbook":
        playbook = file["path"]

        return [({"Playbook may have invalid var name[s]": playbook},
                 "Invalid var name: {}".format(n)) for n in ffn(playbook)]

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
