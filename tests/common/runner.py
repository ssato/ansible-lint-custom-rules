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
import yaml

from . import utils


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

    def run(self, workdir: pathlib.Path, isolated: bool = True
            ) -> typing.List[ansiblelint.errors.MatchError]:
        """Lint in the workdir.

        :param workdir: Working dir to run runner later
        :param isolated: True if to disable other rules
        """
        workdir = workdir.resolve()
        with utils.chdir(workdir):
            lintables = ansiblelint.utils.get_lintables(
                options=ansiblelint.config.options
            )
            assert bool(
                lintables
            ), f'No lintables were found at {workdir!s}'

            ctx = utils.make_context(workdir, lintables)

            rid = self.rule.id
            # Hack to force setting options for the rule.
            setattr(
                ansiblelint.config.options, 'rules',
                {rid: ctx.conf.get('rules', {}).get(rid, {})}
            )

            runner = ansiblelint.runner.Runner(
                *lintables, rules=self.rules,
                skip_list=self.get_skip_list(isolated)
            )

            if ctx.os_env:
                with unittest.mock.patch.dict(os.environ, ctx.os_env,
                                              clear=True):
                    return runner.run()

            return runner.run()


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
        ctx = utils.make_context(workdir, ['N/A'])

        conf = ctx.conf if ctx.conf else dict()
        env = utils.get_env(ctx.env or {})

        skip_list = self.get_skip_list(isolated)
        if skip_list:
            conf['skip_list'] = skip_list

        with tempfile.NamedTemporaryFile(mode='w') as cio:
            yaml.safe_dump(conf, cio)

            opts = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        check=False, shell=False, env=env, cwd=str(workdir),
                        universal_newlines=True)

            # pylint: disable=subprocess-run-check
            res = subprocess.run(self.cmd + ['-c', cio.name], **opts)
            return (res.returncode, res.stdout, res.stderr)

# vim:sw=4:ts=4:et:
