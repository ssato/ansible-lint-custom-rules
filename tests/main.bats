#! /usr/bin/bats
#
# Requirements:
#   - bats: https://github.com/sstephenson/bats
#
cd ${BATS_TEST_DIRNAME:?}
export CUSTOM_RULES_DIR=../rules/

function _abort () {
    local output=$1
    local status=$2
    cat << EOM
output:
${output}
EOM
    exit ${status}
}

function test_success () {
    [[ ${status} -eq 0 ]] || _abort "${output}" ${status}
}

function test_failure () {
    [[ ${status} -ne 0 ]] || _abort "${output}" 1
}

function _ansible_lint () {
    local playbooks="$(echo $1)"  # expand glob pattern
    ansible-lint -v --parseable-severity -r ${CUSTOM_RULES_DIR} ${playbooks}
}

@test "Test lint with custom rules should succeed" {
    playbooks="res/*_ok*.yml"
    run _ansible_lint "${playbooks}"
    test_success
}

@test "Test lint with custom rules should fail" {
    playbooks="res/*_ng*.yml"
    run _ansible_lint "${playbooks}"
    test_failure
}

@test "Test task name pattern with env var, should fail" {
    playbooks="res/TaskHasValidNamePatternRule_ok*.yml"
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE="\\S+" _ansible_lint "${playbooks}"
    test_failure
}

@test "Test task filename pattern with env var, should fail" {
    playbooks="res/TasksFileHasValidNameRule_ok*.yml"
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE="xxxxx\\w+.yml" \
        _ansible_lint "${playbooks}"
    test_failure
}

@test "Test var names pattern with env var, should fail" {
    playbooks="res/VariablesNamingRule_ok*.yml"
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_3_VAR_NAME_RE=="xxxx\\w+" \
        _ansible_lint "${playbooks}"
    test_failure
}

# FIXME:
#   ... _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY=res/inventories/VariablesNamingRule/ok/1/hosts: No such file or directory
@test "Test validating var names in inventory, should succeed" {
    skip
    playbooks="res/VariablesNamingRule_ok*.yml"
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY="res/inventories/VariablesNamingRule/ok/1/hosts" \
        _ansible_lint "${playbooks}"
    test_success
}

@test "Test validating var names in inventory, should fail" {
    playbooks="res/VariablesNamingRule_ok*.yml"
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY="res/inventories/VariablesNamingRule/ng/1/hosts" \
        _ansible_lint "${playbooks}"
    test_failure
}

# vim:sw=4:ts=4:et:filetype=sh:
