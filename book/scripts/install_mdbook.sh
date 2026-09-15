#!/usr/bin/env bash
bookpath="${BOOKPATH:-./docs/book}"  # path to the book

# install mdbook
cargo install --git https://github.com/rust-lang/mdBook.git mdbook

# install plugins...
cargo install mdbook-katex  # https://github.com/lzanini/mdbook-katex
cargo install mdbook-codeblocks  # https://github.com/Roms1383/mdbook-codeblocks
cargo install mdbook-footnote  # https://github.com/daviddrysdale/mdbook-footnote
cargo install mdbook-embedify  # https://github.com/MR-Addict/mdbook-embedify
cargo install mdbook-inline-highlighting  # https://github.com/phoenixr-codes/mdbook-inline-highlighting
cargo install mdbook-numeq  # https://github.com/yannickseurin/mdbook-numeq
cargo install mdbook-vi-mode  # https://github.com/saylesss88/mdbook-vi-mode
cargo install mdbook-mathpunc  # https://github.com/yannickseurin/mdbook-mathpunc

cargo install mdbook-mermaid  # https://github.com/badboy/mdbook-mermaid
mdbook-mermaid install "$bookpath" 2> /dev/null

# more plugins available here: https://github.com/rust-lang/mdBook/wiki/Third-party-plugins
