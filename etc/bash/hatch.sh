
_hatch()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $( compgen -W '-h --help -h --help --version website api' -- $cur) )
    else
        case ${COMP_WORDS[1]} in
            website)
            _hatch_website
        ;;
            api)
            _hatch_api
        ;;
        esac

    fi
}

_hatch_website()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' start deploy' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            start)
            _hatch_website_start
        ;;
            deploy)
            _hatch_website_deploy
        ;;
        esac

    fi
}

_hatch_website_start()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_hatch_website_deploy()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_hatch_api()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -eq 2 ]; then
        COMPREPLY=( $( compgen -W ' start deploy' -- $cur) )
    else
        case ${COMP_WORDS[2]} in
            start)
            _hatch_api_start
        ;;
            deploy)
            _hatch_api_deploy
        ;;
        esac

    fi
}

_hatch_api_start()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

_hatch_api_deploy()
{
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"

    if [ $COMP_CWORD -ge 3 ]; then
        COMPREPLY=( $( compgen -fW ' ' -- $cur) )
    fi
}

complete -o bashdefault -o default -o filenames -F _hatch hatch