#!/usr/bin/env bash

#Exit on error
set -oe pipefail

# define branch names
WORK_BRANCH=$(git rev-parse --abbrev-ref HEAD) # current Git branch
BUMP="$1" # major|minor|patch
REMOTE=origin
DEV="${REMOTE}/develop"
PROD="${REMOTE}/master"
dev_head=
prod_head=


function validate() {

  if [[ -n $(git status --porcelain) ]]; then
    echo "Repo is dirty" && \
    echo "Please stash or commit your changes before releasing" && \
    exit 1;
  fi

  # validate bump string
  [ -z "$BUMP" ] && echo "Please speficy version (major|minor|patch)" && exit 1
}

function switch_to() {
    echo "Switching to $1"
    git checkout --quiet "$1"
}

function reset() {
  echo "Resetting branch $1 to commit $2"
  switch_to "$1"
  git reset --hard "$2"
}

function merge_release_to() {
   switch_to "$1"
   echo "Merging release to $1"
   git merge --quiet --no-edit --no-ff $releaseBranch
}

function fetch() {
  #Fetch remote trackers for releasing
  echo "Fetching remote branches (git fetch)"
  git fetch --quiet
}

function delete() {
  echo "Deleting branch $1"
  git branch -d "$1"
}

function rollback() {
  echo "Dropping all changes"
  git checkout -f # drop all changes
  reset "$PROD" "$prod_head"
  reset "$DEV" "$dev_head"
  delete "$releaseBranch" || true # delete release branch if exists
  switch_to "$WORK_BRANCH" # switch back
}

function on_error() {
  local line="$1"
  echo "Error on line:$line"
  rollback
}

# ------- MAIN --------#
validate
fetch
trap 'on_error $LINENO' ERR # Run on_error on any error

switch_to "$PROD"
prod_head="$(git rev-parse HEAD)"
switch_to "$DEV"
dev_head="$(git rev-parse HEAD)"

# Read current version on dev branch
version=$(<VERSION)
echo "Current version is $version"
newVersion=$(scripts/bump_version.py "$BUMP" "$version")  # Bumped version
releaseBranch="release/$newVersion"

# create the release branch from develop branch
echo "Creating release branch $releaseBranch from $DEV"
git checkout --quiet -b $releaseBranch

echo "$newVersion" > VERSION
echo "Bumped version to $newVersion"

# commit version number increment
git commit -am "version $version"

merge_release_to "$PROD"
merge_release_to "$DEV"

git branch -d $releaseBranch # Delete release branch

# create tag for new version from -master
git tag "v${newVersion}"
#Atomic ensures nothing is pushed if any of the repos fails to push
git push --atomic "$REMOTE" "$DEV" "$PROD" "v${newVersion}"

#switch back to branch started with
switch_to $WORK_BRANCH
