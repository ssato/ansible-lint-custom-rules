#! /usr/bin/bats
#
# Requirements:
#   - bats: https://github.com/sstephenson/bats
#
cd ${BATS_TEST_DIRNAME:?}
export CUSTOM_RULES_DIR=../rules/

function test_success () {
    [[ ${status} -eq 0 ]] || {
        cat << EOM
output:
${output}
EOM
        exit ${status}
    }
}

function test_failure () {
    [[ ${status} -ne 0 ]] || {
        cat << EOM
output:
${output}
EOM
        exit 0
    }
}

@test "Test lint with custom rules should not fail" {
    ok_playbooks="$(ls -1t ./res/*_ok_*.yml)"
    run ansible-lint -v --parseable-severity -r ${CUSTOM_RULES_DIR} "${ok_playbooks}"
    test_success
}

@test "Test lint with custom rules should fail" {
    playbooks="$(ls -1t ./res/*_ng_*.yml)"
    # run ansible-lint -v --parseable-severity -r ${CUSTOM_RULES_DIR} "${playbooks}"
    # test_failure
}

# vim:sw=4:ts=4:et:filetype=sh:
