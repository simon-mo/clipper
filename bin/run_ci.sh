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

# Build docker images
./bin/build_docker_images.sh

echo "Pushing the following images"
cat ./bin/clipper_docker_images.txt

# Push docker images (in parallel)
# while read in; do docker push "$in"; done < ./bin/clipper_docker_images.txt
source ./bin/clipper_docker_images.txt
wait

CLIPPER_REGISTRY=$(docker info | grep Username | awk '{ print $2 }')
sha_tag=$(git rev-parse --verify --short=10 HEAD)

pip install --user click

python $DIR/run_ci_parallel.py $DIR/ci_tests.sh \
    -e CLIPPER_K8S_CERT_AUTH=$CLIPPER_K8S_CERT_AUTH \
    -e CLIPPER_K8S_CLIENT_CERT=$CLIPPER_K8S_CLIENT_CERT \
    -e CLIPPER_K8S_CLIENT_KEY=$CLIPPER_K8S_CLIENT_KEY \
    -e CLIPPER_K8S_PASSWORD=$CLIPPER_K8S_PASSWORD \
    -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    -e CLIPPER_REGISTRY=$CLIPPER_REGISTRY \
    -e CLIPPER_TESTING_DOCKERHUB_PASSWORD=$CLIPPER_TESTING_DOCKERHUB_PASSWORD \
    -e sha_tag=$sha_tag