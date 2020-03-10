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

@test "Test lint with custom rules should not fail" {
    ok_playbooks="$(ls -1t ./res/*_ok_*.yml)"
    run ansible-lint -v --parseable-severity -r ${CUSTOM_RULES_DIR} "${ok_playbooks}"
    test_success
}

# vim:sw=4:ts=4:et:filetype=sh:
