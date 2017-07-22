# hatch.sh

Easy deployment of static websites to [Amazon Web Services (AWS)][aws].

[![Build Status](https://travis-ci.org/hatch-sh/hatch.svg?branch=master)](https://travis-ci.org/hatch-sh/hatch)

Simple command line interface for managing your static websites on AWS — Hatch
takes cares of creating S3 buckets, configuring your custom domains, and
setting up CloudFront — All from the comforts of your command line. For more
information check out [hatch.sh][hatch.sh]

## Installing from source

If you want to install hatch from source simply follow these instructions

    git clone git@github.com:hatch-sh/hatch.git
    cd hatch
    make install

If you want to uninstall hatch again then run

    make distclean

## Working on hatch

If you want to hack around on the hatch source code then follow these
instructions

    git clone git@github.com:hatch-sh/hatch.git && cd hatch
    make setup
    source .venv/bin/activate

Now you can invoke hatch like this

    ./bin/hatch --config-file examples/website/website.yml website deploy --path examples/website
    ./bin/hatch --config-file examples/website/website.yml website start --path examples/website

## Creating a new release

    ./scripts/release <MESSAGE>

[aws]: https://aws.amazon.com/
[hatch.sh]: https://hatch.sh
[homebrew]: https://brew.sh
[oh-my-zsh]: https://github.com/robbyrussell/oh-my-zsh
