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

function _ansible_lint_ok () {
    local playbooks="$(echo $1)"  # expand glob pattern
    ansible-lint -v --parseable-severity -r ${CUSTOM_RULES_DIR} ${playbooks}
    test_success
}

function _ansible_lint_ng () {
    local playbooks="$(echo $1)"
    for f in ${playbooks}; do
        ansible-lint -v --parseable-severity -r ${CUSTOM_RULES_DIR} $f
        test_failure
    done
}

@test "Test lint with custom rules should succeed" {
    run _ansible_lint_ok "res/*_ok*.yml"
}

@test "Test lint with custom rules should fail" {
    run _ansible_lint_ng "res/*_ng*.yml"
}

@test "Test task name pattern with env var, should fail" {
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE="\\S+" \
        _ansible_lint_ng "res/TaskHasValidNamePatternRule_ok*.yml"
}

@test "Test task filename pattern with env var, should fail" {
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_1_NAME_RE="xxxxx\\w+.yml" \
        _ansible_lint_ng "res/TasksFileHasValidNameRule_ok*.yml"
}

@test "Test var names pattern with env var, should fail" {
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_3_VAR_NAME_RE=="xxxx\\w+" \
        _ansible_lint_ng "res/VariablesNamingRule_ok*.yml"
}

@test "Test validating var names in inventory, should succeed" {
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY="res/inventories/VariablesNamingRule/ok/1/hosts" \
        _ansible_lint_ok "res/VariablesNamingRule_ok*.yml"
}

@test "Test validating var names in inventory, should fail" {
    run _ANSIBLE_LINT_RULE_CUSTOM_2020_3_INVENTORY="res/inventories/VariablesNamingRule/ng/1/hosts" \
        _ansible_lint_ng "res/VariablesNamingRule_ok*.yml"
}

# vim:sw=4:ts=4:et:filetype=sh:
