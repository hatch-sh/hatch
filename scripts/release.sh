#!/usr/bin/env bash

set -u
set -e

source scripts/lib.sh

create_release() {
    local version
    local message

    version=$1
    message=$2

    git tag "${version}" -m "${message}"
    git push --tags origin master
}

upload_pypi_package() {
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
