function is_on_master {
    branch_name=$(git name-rev --name-only HEAD)

    if [ "${branch_name}" == "master" ]
    then true
    else false
    fi
}

function get_version {
    cat hatch/version.py \
    | grep VERSION \
    | cut -d "'" -f 2
}
