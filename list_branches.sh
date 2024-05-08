#!/bin/bash

remote_url=$(git config --get remote.origin.url)
domain=$(echo "$remote_url" | sed -e 's|^[^@]*@||' -e 's|:\([^/]*\)/*.*|\1|')

get_pusher() {
    local branch="$1"
    local commit=$(git rev-parse --verify --quiet "$branch")
    local user=$(git log -1 --pretty=format:'%an' "$commit")
    echo "$user"
}

echo "Remote branches and their pushers for $remote_url"
echo "---------------------------------------------------"

for branch in $(git branch -r | grep -v HEAD); do
    pusher=$(get_pusher "$branch")
    echo "$branch: $pusher"
done