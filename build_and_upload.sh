#!/usr/bin/env bash
# shellcheck disable=SC2206


save_version_to_file() {
    local path="${1}"
    local content="${2}"
    echo "__version__ = '${content}'" > "${path}"
}


update_version() {
    local version_file_name='version.py'
    local data
    data=$(date '+%y.%-m.%-d')

    if [ ! -f "${version_file_name}" ]; then
        save_version_to_file "${version_file_name}" "${data}"
        poetry version "${data}"
        return
    fi
    version=$(cat "${version_file_name}" | sed -e "s#'##g" | sed -e 's/__version__ = //g')

    if [ "${version}" == "${data}" ]; then
        save_version_to_file "${version_file_name}" "${version}-1"
        poetry version "${version}-1"
    elif [[ "${version}" == *"${data}"* ]]; then
        # shellcheck disable=SC2206
        # SC2206: Quote to prevent word splitting/globbing, or split robustly with mapfile or read -a.
        # This solution is much simpler - We want to split variable value using space instead using IFS, read or mapfile
        version_elements=(${version//-/ })
        save_version_to_file "${version_file_name}" "${version_elements[0]}-$(( version_elements[1] + 1 ))"
        poetry version "${version_elements[0]}-$(( version_elements[1] + 1 ))"
    elif [[ "${version}" == *"-"* ]] && [ "${data}" != "${version}" ]; then
        save_version_to_file "${version_file_name}" "${data}"
        poetry version "${data}"
    elif [ "${version}" == "" ]; then
        save_version_to_file "${version_file_name}" "${data}"
        poetry version "${data}"
    else
        echo "Strange condition with version:"
        echo "   Date: \"${data}\""
        echo "Version: \"${version}\""
        exit 3
    fi
}


status_begin(){
    echo -en "$(printf '\033[47;30m \033[0m%.0s' $(seq 1 $(tput cols)))\r"
    echo -e "\033[44;97m (..) \033[0m\033[47;30m ${1} \033[0m"
}


status_end(){
    if [ "${1}" -gt 0 ]; then
        color="\033[41;37m"
        message="(--)"
    else
        color="\033[42;97m"
        message="(^^)"
    fi

    echo -en "$(printf '\033[47;30m \033[0m%.0s' $(seq 1 $(tput cols)))\r"
    echo -e "${color} ${message} \033[0m\033[47;30m ${2} \033[0m"
}


usage() {
    echo -e "
         \r    Usage:
         \r       ${0} build          (to build only)
         \r       ${0} build test     (to publish in TEST PYPI index)
         \r       ${0} build prod     (to publish in PRODUCTION PYPI index)
    "
    exit 1
}


BUILD="${1}"
UPLOAD="${2}"

if [ -z "${BUILD}" ] || [ "${BUILD}" != "build" ]; then
    usage
fi

if [ ! -z "${UPLOAD}" ]; then
    PIP_REPOSITORY_URL="${PIP_TEST_REPOSITORY_URL}"
    case ${UPLOAD} in
        test)
            server_info="Publishing to test PYPI Index"
            PIP_REPOSITORY_URL="${PIP_TEST_REPOSITORY_URL}"
            POETRY_PYPI="test-pypi"
            ;;
        prod)
            server_info="PUBLISHING TO PRODUCTION PYPI INDEX"
            PIP_REPOSITORY_URL="${PIP_PRODUCTION_REPOSITORY_URL}"
            POETRY_PYPI="pypi"
            ;;
        *)
            echo -e "\n    ERROR: Second parameter unknown: \"${UPLOAD}\""
            usage
            ;;
    esac
fi


echo; echo
status_begin "Poetry - lock"
poetry lock
status_end $? "Poetry - lock"

echo; echo
status_begin "Building package"
poetry build
: ' Instead poetry we can also use build:
python -m build -sw .
'
status_end $? "Building package"

if [ ! -z "${UPLOAD}" ]; then
    echo; echo
    status_begin "${server_info}"
    poetry publish -r ${POETRY_PYPI} -u ${PIP_USER_NAME} -p ${PIP_USER_PASSWORD} -vvv
    status_end $? "${server_info}"
fi

echo; echo
status_begin "Cleaning..."
rm -rf dist/
rm -rf build/
rm -rf src/*.egg-info
rm -rf __pycache__
status_end $? "Cleaning..."
