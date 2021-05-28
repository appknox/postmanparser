#! /bin/bash
#
# deploy.sh
# Copyright (C) Appknox <engineering@appknox.com>
#
# Distributed under terms of the Apache 2.0 license.
#


rm -rf dist/
if [[ $(git diff --stat) != '' ]]; then
  echo "The branch is dirty, only bump version when it is clean !"
  exit 1
fi
versionold=$(poetry version | awk '{print $2}')
if [ "$1" != '' ]; then
    poetry version $1
else
    poetry version patch
fi
versionnew=$(poetry version | awk '{print $2}')
tag="v${versionnew}"
echo $tag
export CURRENT_BRANCH
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
git add .
git commit -m "v${versionold} → v${versionnew}"
git tag $tag
git push --tags
git push origin "$CURRENT_BRANCH:$CURRENT_BRANCH"
poetry build
poetry publish