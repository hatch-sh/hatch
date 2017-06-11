is_on_master() {
    branch_name=$(git name-rev --name-only HEAD)

    if [ "${branch_name}" == "master" ]
    then return 0
    else return 1
    fi
}

get_version() {
    cat hatch/version.py \
    | grep VERSION \
    | cut -d "'" -f 2
}
