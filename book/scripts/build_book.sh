#!/usr/bin/env bash
cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null || exit

destdir="${DESTDIR:-../../}"
mdbook build --dest-dir "$destdir"