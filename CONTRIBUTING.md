# Contributing

Thank you for taking an interest in the development of *worktoy*! Since
this project is the work of a single developer, this document attempts to
provide an overview of the development process. This process does result
in a particular structure, and while this structure is quite rigid, the
process itself is not.

## Setup

*worktoy* does not actually have any required runtime dependencies, but
does have a number of development dependencies. They are entirely
optional, so feel free to replace them with other tools as you prefer.
The development process makes use of 'mamba' to provide a virtual
environment. You do not need to use 'mamba', but it is strongly
recommended that you do use some sort of virtual environment rather than
system Python. This recommendation applies generally to Python development.

The [miniforge](https://github.com/conda-forge/miniforge) distribution
provides a convenient way to get 'mamba'. Refer to the link provided for
installation instructions. For arch, the 'aur' does provide a package:

```terminaloutput
yay -S miniforge
```

Once installed, clone the repository and create the virtual environment
with:

```terminaloutput
mamba env create -f environment.yml
mamba activate worktoy_env
```

## Version Support

Another quirk of *worktoy* is legacy support all the way back to 3.7 and
up to the latest stable Python, which as of this writing is 3.14. Extending
support to development versions of Python may come in the future. What
holds this back presently is basically just the implementation of development
versions in the CI-pipeline.

The support for 3.7 limits what new features can be supported in the
*worktoy* source code. These limits fall in two categories: one that is
'easy' to circumvent and one that strictly limits what syntax is allowed.

### Runtime and `from __future__ import annotations`

The *worktoy* source code files always include the following line after
the license and copyright notice:

```from __future__ import annotations```

What this line actually does is to turn type hints into strings at
runtime. Thus, any object used only for type hinting will not actually
be needed at runtime. This means it does not need to be imported at
runtime, or in other words, not imported at all.

### Runtime and `if TYPE_CHECKING:  # pragma: no cover`

An important companion to the stringified type annotations is the use of
the pattern of having an always `False` block containing imports that
will never see runtime. This was a common way to escape circular import
errors during runtime while still allowing static type checkers to
provide helpful guidance. *worktoy* additionally uses this block to use
more modern features from the `typing` package. This allows features
added in later versions to be present in code running in older versions.

### Legacy Support and Modern Syntax

The reason the above backwards compatibility is possible is that although
`typing` only added `Never` in version 3.11, the following code:

```python
from typing import Never
```

does not use unsupported syntax. However, new syntax features added in
later versions of Python *cannot* be backported this way. This is why
*worktoy* does not make use of the under-appreciated `:=` walrus operator.

## Testing and Coverage

A point of pride for *worktoy* is the 100% branch coverage of the test
suite. This requirement is non-negotiable. The CI-pipeline contains a
measurement of the coverage that is authoritative, but included in the
repository is the `bin/dev_tooling/coverage_test.sh` script that reliably achieves the
same results as the CI-pipeline. It does rely on the previously mentioned
development dependencies. It runs all the tests in the `tests` directory
and if all pass, the script opens the HTML report in the system browser.

Running tests without measuring coverage is substantially faster and is
frequently desirable during development when designing the tests
themselves. For this purpose, two Python functions are available from the
`bin/dev_tooling/yolo_dev.py` module: `runTests`, which runs all the tests found and puts
results in the terminal. A related function, `runTest`, allows running a
single test by passing the test class to it.

Besides the test runners, the `yolo_dev.py` module also provides the
`yolo` function which runs any passed functions including relevant
information such as identifying the running Python environment.

## Documentation

The documentation is built with [Sphinx][sphinx] and published to both
[Read the Docs][rtd] and [GitHub Pages][ghpages], but it takes an unusual
approach. Rather than extracting and reformatting docstrings, the page for
a source file *is* that file, shown verbatim with syntax highlighting.
Nothing is imported and no docstrings are parsed: the generator in
`docs/_gen.py` reads each file as text, highlights it with Pygments, and
wires the result into a navigable site, so what you read on the site is
exactly the code in the repository.

Only files reachable from a package's public `__all__` get a page, which
keeps private helper modules out of view, and a mirror of the `tests`
directory is included so the tests document their own usage. Each
documented symbol gains two cross-reference sections, 'Used in' and 'Usage
in testing', that list every line in the source and the tests where the
symbol appears, each one a link to that exact line.

The rendered source is itself click-through: every name is wrapped in a
link to where it is defined. A *worktoy* symbol links to its page, a name
defined earlier in the same file links back to that line, and a
standard-library member or a builtin links out to the matching page on the
official Python documentation. These links are read from the syntax tree,
so they land exactly rather than by guesswork. To preview the whole site
locally, run `bin/dev_tooling/build_docs.sh`, which builds the same pages
into `etc/docs_build` and opens them in the browser.

## STYLE

Horizontal scrolling is the worst! No line shall exceed 77 characters
ever for any reason! Because of this limitation we cannot afford four
spaces per indentation and thus make do with two-space indentation.

Each class lives in its own file, named for it, and the same applies to
the test suite, where every test case has its own `test_*.py`. Private
dunder names carry both a leading and a trailing double underscore, for
example `__compiled_func__`, and never the single-leading `__name` form,
so that Python's name mangling never rewrites them.

Docstrings are natural prose in full sentences, declarative rather than
imperative. Since the page is the source itself, a docstring earns its
place only by adding what the code cannot show. Rather than having a
docstring tautologically explain that `getFoo` is the getter function for
`Foo`, just omit it entirely.

## LICENSE

*worktoy* is released under Apache-2.0, and contributions are accepted
under the same license. This is not a separate agreement you have to sign.
Section 5 of the license already provides that anything you intentionally
submit for inclusion is licensed under Apache-2.0 unless you state
otherwise, so the inbound and outbound terms match and no contributor
license agreement is needed.

The patent provisions live in section 3. Contributing grants a
royalty-free patent license covering your contribution, so the project and
its users are protected against a later patent claim over code you added.
The same section is the reverse card: if anyone starts patent litigation
alleging that *worktoy* infringes, their patent license under Apache-2.0
terminates on the day the suit is filed. By opening a pull request you
accept these terms for your contribution.

[rtd]: https://worktoy.readthedocs.io/stable/

[ghpages]: https://asgerjon.github.io/WorkToy/latest/

[sphinx]: https://www.sphinx-doc.org/
