#! /usr/bin/bats
#
# Requirements:
#   - bats: https://github.com/sstephenson/bats
#
cd ${BATS_TEST_DIRNAME:?}
export CUSTOM_RULES_DIR=../rules/

function _dump_output_and_exit () {
    local output=$1
    local status=$2
    cat << EOM
output:
${output}
EOM
}

function test_success () {
    [[ ${status} -eq 0 ]] || _dump_output_and_exit ${output} ${status}
}

function test_failure () {
    [[ ${status} -ne 0 ]] || _dump_output_and_exit ${output} 0
}

@test "Test lint with custom rules should not fail" {
    playbooks="$(ls -1t ./res/*_ok*.yml)"
    run ansible-lint -v --parseable-severity -r ${CUSTOM_RULES_DIR} "${playbooks}"
    test_success
}

@test "Test lint with custom rules should fail" {
    playbooks="$(ls -1t ./res/*_ng*.yml)"
    run ansible-lint -v --parseable-severity -r ${CUSTOM_RULES_DIR} "${playbooks}"
    test_failure
}

# vim:sw=4:ts=4:et:filetype=sh:
