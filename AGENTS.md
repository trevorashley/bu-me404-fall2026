# ME404: Dynamics and Control of Mechanical Systems

This repository contains course material for Boston University's Fall 2026 offering of ME404: Dynamics and Control of Mechanical Systems.

## Audience

The students are fourth-year undergraduates in mechanical engineering with a particular interest in robotics applications. They have studied differential equations, linear algebra, mechanics, and dynamics. Their curriculum does not require coursework in signal processing (e.g., Fourier series or transforms) or complex analysis (e.g., the residue theorem or complex integration), so introduce those concepts before relying on them.

Students have prior MATLAB training; do not assume prior Python knowledge. The syllabus includes both MATLAB and Python, so explain any Python needed for student-facing examples. Python tools such as SymPy may also be used to verify course material.

## Repository Structure

- `book/` contains the mdBook project for the course website hosted on GitHub Pages. See the [mdBook guide](https://github.com/rust-lang/mdBook/tree/main/guide/src).
- `book/src/content/` contains the course website's source content.
- `book/src/content/syllabus.md` contains the course syllabus.
- `book/src/SUMMARY.md` defines the book's chapter list and navigation.
- `book/book.toml` configures mdBook and its preprocessors.
- `docs/` contains the generated HTML website. Edit the source in `book/`, then regenerate the site with `bash scripts/build_book.sh` from the repository root; do not hand-edit generated HTML.
- `references/` contains local course references and is ignored by Git, so it may be absent from a fresh checkout.
    - `references/contents/` contains Markdown tables of contents.
    - `references/documents/` contains reference PDFs grouped by book, including full books and chapter or page-range extracts.
    - `references/syllabus-topics.md` maps topics across references by chapter and section. Use it as a lookup aid; its course-format and prerequisite assumptions do not override the syllabus or the audience guidance above.

## Agent Guidelines

The course's primary reference is Franklin, Powell, and Emami-Naeini, *Feedback Control of Dynamic Systems*, 8th edition. The local 8th-edition PDF contains significant technical errors, so check relevant material against the 7th edition as well. Both editions are in `references/documents/`; the existing directory names spell the author's surname `Emami-Naeimi`.

Cross-reference other relevant references whenever possible to ensure technical accuracy and pedagogical clarity. Use `references/syllabus-topics.md` to locate relevant sections. Prefer an example from another reference when it explains a topic more clearly or adds useful insight, and identify its source and edition. If a required reference is unavailable, state that limitation rather than claiming to have checked it.

Each book-note topic in `book/src/content/book-notes/` must have an `_instructor.md` and an `_student.md` version. Keep their notation, assumptions, and examples consistent when editing either version. Some existing topics split a single instructor note across multiple student notes; preserve that correspondence unless restructuring is requested. Supporting assets and demo scripts do not need paired versions.

Publish student versions through `book/src/SUMMARY.md`; keep instructor versions out of the public chapter list. The `_instructor.md` suffix alone does not enforce hiding. The configured `scripts/hide_chapters.py` preprocessor removes chapters containing `<!--hidden-->` when hiding is enabled in `book/book.toml`. When changing publication configuration, verify that instructor content is absent from the generated site.

**Instructor versions must include complete derivations to reduce the possibility of mistakes during lecture.** State assumptions and show intermediate steps. Use symbolic tools (e.g., SymPy or MATLAB's Symbolic Math Toolbox) whenever possible to verify derivations and calculations.
