#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
library_dir="$(cd "$project_dir/../.." && pwd)/library-sp24"
build_dir="$(mktemp -d)"
trap 'rm -rf "$build_dir"' EXIT

# Compile only the classes used by the object-method tests.
javac --release 17 -cp "$library_dir/*" -d "$build_dir" \
    "$project_dir/src/deque/Deque61B.java" \
    "$project_dir/src/deque/ArrayDeque61B.java" \
    "$project_dir/src/deque/LinkedListDeque61B.java" \
    "$project_dir/tests/ArrayDeque61BTest.java" \
    "$project_dir/tests/LinkedListDeque61BTest.java" \
    "$project_dir/tests/Deque61BEqualityTest.java" \
    "$project_dir/tools/RunObjectMethodTests.java"

java -cp "$build_dir:$library_dir/*" RunObjectMethodTests "$@"
