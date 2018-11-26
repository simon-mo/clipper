#!/usr/bin/env bash

set -x
set -e
set -u
set -o pipefail

# Printout for timeout debug
date

unset CDPATH
# one-liner from http://stackoverflow.com/a/246128
# Determines absolute path of the directory containing
# the script.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


# Let the user start this script from anywhere in the filesystem.
cd $DIR/..
tag=$(<VERSION.txt)

CLIPPER_REGISTRY='clippertesting'
sha_tag=$(git rev-parse --verify --short=10 HEAD)
KAFKA_ADDRESS="ci.simon-mo.com:32775"

docker build -t shipyard ./bin/shipyard
docker run --rm shipyard \
  --sha-tag $sha_tag \
  --namespace $CLIPPER_REGISTRY \
  --clipper-root $(pwd) \
  --config clipper_docker.cfg.py \
  --kafka-address $KAFKA_ADDRESS \
  --no-push > Makefile
cat Makefile