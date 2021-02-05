#!/bin/bash

set -e

SKIP_BUILD=0
DEPLOY=0

while getopts "sph" opt; do
    case $opt in
    h)
        echo "Usage:"
        echo "    -h        Display this help message."
        echo "    -p        Pushes the containers"
        echo "    -s        Skip the build"
        exit 0
        ;;
    p)
        DEPLOY=1
        ;;
    s)
        SKIP_BUILD=1
        ;;
    \?)
        echo "Invalid Option: -$OPTARG" 1>&2
        exit 1
        ;;
    esac
done
shift $((OPTIND - 1))

if ((!SKIP_BUILD)); then
    docker build . -f Dockerfile -t wbgrs/dependency-scan:7.2
    docker build . -f Dockerfile.php74 -t wbgrs/dependency-scan:7.4
fi


if ((DEPLOY)); then
    docker push wbgrs/dependency-scan:7.2
    docker push wbgrs/dependency-scan:7.4
fi

