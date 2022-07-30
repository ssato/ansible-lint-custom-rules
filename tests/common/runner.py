# Copyright (C) 2020, 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,too-few-public-methods
"""Common utility test routines and classes.
"""
import os
import pathlib
import subprocess
import tempfile
import typing
import unittest.mock

import ansiblelint.config
import ansiblelint.constants
import ansiblelint.errors
import ansiblelint.rules
import ansiblelint.runner
import ansiblelint.utils
import yaml

from . import datatypes, utils

if typing.TYPE_CHECKING:
    from ansiblelint.file_utils import Lintable


def clear_internal_caches():
    """
    Clear the internal caches of ansible-lint by functools.lru_cache.

    Because runner will run many times for different test data, all of the
    caches must be cleared for each run.

    .. todo:: Any others?
    """
    ansiblelint.utils.parse_yaml_linenumbers.cache_clear()


def get_lintables(fail_if_no_data: bool = True) -> typing.List['Lintable']:
    """Get a list of lintables in workdir.

    note: It must change dir to the workdir to collect lintables.

    .. seealso:: ansiblelint.utils.get_lintables
    """
    lintables = ansiblelint.utils.get_lintables(
        options=ansiblelint.config.options
    )
    if not lintables:
        if fail_if_no_data:
            raise FileNotFoundError(
                f'No lintables were found: {pathlib.Path().cwd()!s}'
            )

        return []

    return lintables


def make_context(workdir: pathlib.Path,
                 fail_if_no_data: bool = True) -> datatypes.Context:
    """Make a context object from args and loaded data.
    """
    return datatypes.Context(
        workdir,
        get_lintables(fail_if_no_data=fail_if_no_data),
        *utils.load_sub_ctx_data_in_dir(workdir)
    )


class RuleRunner:
    """Base Class to run ansiblelint without a lintable in a dir.

    .. seealso:: ansiblelint.testing.RunFromText
    """
    def __init__(self, rule: ansiblelint.rules.AnsibleLintRule,
                 rules_dir: pathlib.Path,
                 skip_list: typing.Optional[typing.List[str]] = None,
                 enable_default: bool = False):
        """Initialize an instance with given rules collection.

        :param rule: An AnsibleLintRule instance to test
        :param rules_dir: The path to a dir contains custom rules
        :param skip_list: A list of rule IDs to disable (skip)
        :param enable_default:
            True if default rules will be enabled also
        """
        self.rule = rule

        self.rulesdirs = [str(rules_dir.resolve())]
        if enable_default:
            self.rulesdirs.append(ansiblelint.constants.DEFAULT_RULESDIR)

        self.skip_list = skip_list.copy() if skip_list else []

        options = ansiblelint.config.options
        # .. seealso:: ansiblelint.testing.fixtures.default_rules_collection
        options.enable_list = ['no-same-owner']
        self.rules = ansiblelint.rules.RulesCollection(
            rulesdirs=self.rulesdirs, options=options
        )

    def get_skip_list(self, isolated: bool = True) -> typing.List[str]:
        """Get a list of rule IDs to skip.

        :param isolated: True if to disable other rules
        """
        skip_list = self.skip_list.copy() if self.skip_list else []
        if isolated:
            skip_list.extend([
                r.id for r in self.rules if r.id != self.rule.id
            ])

        return skip_list

    def run_with_env(self, ctx: datatypes.Context,
                     isolated: bool = True) -> datatypes.Result:
        """
        Run runner with (os) environment variables are set as needed.
        """
        runner = ansiblelint.runner.Runner(
            *ctx.lintables, rules=self.rules,
            skip_list=self.get_skip_list(isolated)
        )
        if ctx.os_env:
            with unittest.mock.patch.dict(os.environ, ctx.os_env,
                                          clear=True):
                res = runner.run()
        else:
            res = runner.run()

        clear_internal_caches()
        return datatypes.Result(res, ctx)

    def run(self, workdir: pathlib.Path, isolated: bool = True
            ) -> typing.List[ansiblelint.errors.MatchError]:
        """Lint in the workdir.

        :param workdir: Working dir to run runner later
        :param isolated: True if to disable other rules
        """
        with utils.chdir(workdir):
            ctx = make_context(workdir.resolve())
            rule_config = ctx.conf.get('rules', {})

            if rule_config:
                # pylint: disable=no-member
                with unittest.mock.patch.dict(ansiblelint.config.options.rules,
                                              rule_config):
                    return self.run_with_env(ctx, isolated)

            return self.run_with_env(ctx, isolated)


class CliRunner(RuleRunner):
    """Base Class to run ansiblelint without a lintable in a dir.

    .. seealso:: RuleRunner
    """
    def __init__(self, rule: ansiblelint.rules.AnsibleLintRule,
                 rules_dir: pathlib.Path,
                 skip_list: typing.Optional[typing.List[str]] = None,
                 enable_default: bool = False):
        """Initialize an instance with given rules collection.

        :param rule: An AnsibleLintRule instance to test
        :param rules_dir: The path to a dir contains custom rules
        :param skip_list: A list of rule IDs to disable (skip)
        :param enable_default:
            True if default rules will be enabled also
        """
        super().__init__(rule, rules_dir, skip_list, enable_default)

        self.cmd = ['ansible-lint', '-r', f'{rules_dir.resolve()!s}']
        if enable_default:
            self.cmd.append('-R')

    def run(self, workdir: pathlib.Path, isolated: bool = True
            ) -> typing.Tuple[int, str, str]:
        """Run Ansible Lint in the workdir.

        :param workdir: Working dir to run runner later
        :param isolated: True if to disable other rules

        .. seealso:: ansiblelint.testing.run_ansible_lint
        """
        workdir = workdir.resolve()
        with utils.chdir(workdir):
            ctx = make_context(workdir, fail_if_no_data=False)

        conf = ctx.conf if ctx.conf else {}
        env = utils.get_env(ctx.env or {})

        conf['skip_list'] = self.get_skip_list(isolated)

        with tempfile.NamedTemporaryFile(mode='w') as cio:
            yaml.safe_dump(conf, cio)

            opts = {
                'stdout': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'check': False,
                'shell': False,
                'env': env,
                'cwd': str(workdir),
                'universal_newlines': True
            }

            # pylint: disable=subprocess-run-check
            res = subprocess.run(self.cmd + ['-c', cio.name], **opts)
            return datatypes.Result(res, ctx)

# vim:sw=4:ts=4:et:
