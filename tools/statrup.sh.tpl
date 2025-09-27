#!/bin/sh

# This script is auto-generated and it is used to setup the environment and run the application.
# It is not recommended to modify this file directly.

# generated at #{GEN_TIME}

# function to join paths
join_path() {
    echo "${1%/}/$2" | sed 's#//#/#g'
}

# prepare paths
# script directory
SCRIPT_PATH=$(dirname "$(realpath "$0")")
# application path
APP_PATH=$(join_path "${SCRIPT_PATH}" "#{BIN}")
# thirdparty library path
LIBS_PATH=$(join_path "${SCRIPT_PATH}" "#{LIBS_DIRNAME}")

# add thirdparty library path to LD_LIBRARY_PATH
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${SCRIPT_PATH}:${LIBS_PATH}"

# ensure the application is executable
chmod +x ${APP_PATH}

# set the working directory to the application directory
cd #{WORK_DIR}

# run the application
${APP_PATH} "$@"

# exit with the return code of the application
exit $?