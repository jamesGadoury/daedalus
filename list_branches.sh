#!/bin/bash

# Get the remote URL
remote_url=$(git config --get remote.origin.url)

# Extract the domain from the remote URL
domain=$(echo "$remote_url" | sed -e 's|^[^@]*@||' -e 's|:\([^/]*\)/*.*|\1|')

# Function to get the user who pushed a branch
get_pusher() {
    local branch="$1"
    local commit=$(git rev-parse --verify --quiet "$branch")
    local user=$(git log -1 --pretty=format:'%an' "$commit")
    echo "$user"
}

# Print header
echo "Remote branches and their pushers for $remote_url"
echo "---------------------------------------------------"

# Loop through remote branches
for branch in $(git branch -r | grep -v HEAD); do
    # Get the user who pushed the branch
    pusher=$(get_pusher "$branch")

    # Print branch name and pusher
    echo "$branch: $pusher"
done