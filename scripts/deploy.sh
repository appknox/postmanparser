#! /bin/bash
#
# deploy.sh
# Copyright (C) Appknox <engineering@appknox.com>
#
# Distributed under terms of the Apache 2.0 license.
#


rm -rf dist/
if [ "$1" != '' ]; then
    poetry version $1
else
    poetry version patch
fi
version=$(poetry version | awk '{print $2}')
tag="v${version}"
echo $tag
export CURRENT_BRANCH
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
git tag $tag
git push --tags
git push origin "$CURRENT_BRANCH:$CURRENT_BRANCH"
poetry build
poetry publish