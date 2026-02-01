#!/usr/bin/env zsh
# List all __pycache__ directories, then ask for confirmation before removal.

set -euo pipefail

pycacheDirs=()
while IFS= read -r dir; do
  pycacheDirs+=("$dir")
done < <(find . -type d -name '__pycache__' -prune -print)

if (( ${#pycacheDirs} == 0 )); then
  print "No __pycache__ directories found."
  exit 0
fi

print "The following __pycache__ directories will be removed:"
print
for dir in "${pycacheDirs[@]}"; do
  print "  $dir"
done
print

print -n "Proceed? [y/N]: "
read reply

case "$reply" in
  [yY]|[yY][eE][sS])
    print
    for dir in "${pycacheDirs[@]}"; do
      rm -rf -- "$dir"
      print "Removed: $dir"
    done
    ;;
  *)
    print
    print "Aborted."
    exit 1
    ;;
esac
