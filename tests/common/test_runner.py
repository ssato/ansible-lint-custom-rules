# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=invalid-name,missing-function-docstring
"""Test cases of tests.common.runner.
"""
import pytest

from ansiblelint.rules.DeprecatedModuleRule import DeprecatedModuleRule
from rules.BlockedModules import ID as OTHER_CUSTOM_RULE_ID_EX
from rules.DebugRule import DebugRule
from tests.common import constants, datatypes, runner as TT, utils


# ansiblelint.rules.DeprecatedModuleRule:
DEFAULT_RULE_ID_EX: str = DeprecatedModuleRule.id


@pytest.mark.parametrize(
    ('workdir', ),
    ((constants.TESTS_RES_DIR / 'DebugRule/ok/0', ),
     )
)
def test_get_lintables_success(workdir):
    with utils.chdir(workdir):
        assert TT.get_lintables(False)
        assert TT.get_lintables(True)


def test_get_lintables_failure(tmp_path):
    with utils.chdir(tmp_path):
        res = TT.get_lintables(False)
        assert not res, res

        with pytest.raises(FileNotFoundError) as exc:
            TT.get_lintables(True)

        assert 'No lintables' in str(exc)


@pytest.mark.parametrize(
    ('workdir', 'conf', 'env'),
    ((constants.TESTS_RES_DIR / 'DebugRule/ok/0', False, False),
     (constants.TESTS_RES_DIR / 'DebugRule/ng/1', True, False),
     (constants.TESTS_RES_DIR / 'DebugRule/ng/2', False, True),
     )
)
def test_make_context(workdir, conf, env):
    ctx = TT.make_context(workdir)
    assert bool(ctx)
    assert isinstance(ctx, datatypes.Context)

    assert ctx.workdir == workdir.resolve()
    assert ctx.lintables != []
    assert bool(ctx.conf) == conf, ctx.conf  # TBD
    assert bool(ctx.env) == env, ctx.env  # TBD
    assert bool(ctx.os_env) == env, ctx.os_env  # TBD


@pytest.mark.parametrize(
    ('rules_dir', 'skip_list', 'enable_default'),
    ((constants.RULES_DIR, None, False),
     (constants.RULES_DIR, [OTHER_CUSTOM_RULE_ID_EX], False),
     (constants.RULES_DIR, None, True),
     )
)
def test_RuleRunner__init__(rules_dir, skip_list, enable_default):
    runner = TT.RuleRunner(
        DebugRule(), rules_dir, skip_list=skip_list,
        enable_default=enable_default
    )
    assert runner.rule.id == DebugRule.id, runner.rule.id
    assert runner.rules

    rule_ids = [r.id for r in runner.rules]
    assert DebugRule.id in rule_ids, rule_ids

    if skip_list:
        assert runner.skip_list == skip_list, runner.skip_list

    if enable_default:
        assert DEFAULT_RULE_ID_EX in rule_ids, rule_ids


@pytest.mark.parametrize(
    ('rules_dir', 'skip_list', 'isolated'),
    ((constants.RULES_DIR, None, True),
     (constants.RULES_DIR, [OTHER_CUSTOM_RULE_ID_EX], True),
     (constants.RULES_DIR, None, True),
     (constants.RULES_DIR, None, False),
     (constants.RULES_DIR, [OTHER_CUSTOM_RULE_ID_EX], False),
     (constants.RULES_DIR, None, False),
     )
)
def test_RuleRunner_get_skip_list(rules_dir, skip_list, isolated):
    runner = TT.RuleRunner(
        DebugRule(), rules_dir, skip_list=skip_list, enable_default=True
    )
    skips = runner.get_skip_list(isolated=isolated)

    assert DebugRule.id not in skips, skips

    if skip_list:
        assert all(s in skips for s in skip_list), skips

    if isolated:
        assert DebugRule.id not in skips, skips
        assert DEFAULT_RULE_ID_EX in skips, skips


DEBUG_RES_DIR = constants.TESTS_RES_DIR / 'DebugRule'


# see tests/res/DebugRule/{ok,ng}/...
@pytest.mark.parametrize(
    ('workdir', 'isolated', 'success'),
    ((DEBUG_RES_DIR / 'ok/0', True, True),
     (DEBUG_RES_DIR / 'ok/0', False, True),
     (DEBUG_RES_DIR / 'ng/0', True, False),
     (DEBUG_RES_DIR / 'ng/0', False, False),
     )
)
def test_RuleRunner_run(workdir, isolated, success):
    runner = TT.RuleRunner(DebugRule(), constants.RULES_DIR)
    res = runner.run(workdir, isolated=isolated)
    if success:
        assert not res.result, res.result
    else:
        assert res.result


@pytest.mark.parametrize(
    ('enable_default', ),
    ((False, ),
     (True, ),
     )
)
def test_CliRunner__init__(enable_default):
    runner = TT.CliRunner(
        DebugRule(), constants.RULES_DIR, enable_default=enable_default
    )
    assert str(constants.RULES_DIR.resolve()) in runner.cmd

    if enable_default:
        assert '-R' in runner.cmd


@pytest.mark.parametrize(
    ('workdir', 'success'),
    ((DEBUG_RES_DIR / 'ok/0', True),
     (DEBUG_RES_DIR / 'ng/0', False),
     )
)
def test_CliRunner_run(workdir, success):
    runner = TT.CliRunner(DebugRule(), constants.RULES_DIR)
    res = runner.run(workdir)
    if success:
        assert res.result.returncode == 0
        assert res.result.stdout == ''
        assert res.result.stderr == ''
    else:
        assert res.result.returncode != 0
        assert bool(res.result.stdout)
        assert bool(res.result.stderr)

# vim:sw=4:ts=4:et:
