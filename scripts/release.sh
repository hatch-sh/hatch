#!/usr/bin/env bash

set -u
set -e

source scripts/lib.sh

function create_release {
    local version=$1
    local message=$2

    git tag "${version}" -m "${message}"
    git push --tags origin master
}

function upload_pypi_package {
    python setup.py sdist upload -r pypitest
    python setup.py sdist upload -r pypi
}

if [ -z "${1: }" ]
then
    echo 'Please provide a release message.'
    exit 1
fi

if is_on_master
then
    create_release $(get_version) $1
    upload_pypi_package
else
    echo 'We only cut release from the master branch.'
fi
