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
up to the latest stable Python which as of writing is 3.14. Extending
support to development versions of Python may come in the future. What
holds this back presently is basically just implementation of development
versions in the CI-pipeline.

The support for 3.7 limits what new features can be supported in the
*worktoy* source code. These limits fall in two categories one that is
"easy" to circumvent and one that strictly limits what syntax is allowed.

### Runtime and `from __future__ import annotations`

The *worktoy* source code files always include the following line after
the license and copyright notice:

```from __future__ import annotations```

What this line actually does is to turn type hints into strings at
runtime. Thus, any objects used only for type hinting will not actually
be needed at runtime. Meaning that it does not need to be imported at
runtime, in other words, not needed to be imported at all.

### Runtime and `if TYPE_CHECKING:  # pragma no cover`

An important companion to the stringified type annotations is the use of
the pattern of having an always `False` block containing imports that
will never see runtime. This was a common way to escape circular import
errors during runtime while still allowing static type checkers to
provide helpful guidance. *worktoy* additionally uses this block to use
more modern features from the `typing` package. This allows features
added in later version to be present in code running in older versions.

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
repository is the `coverage_test.sh` script that reliably achieves the
same results as the CI-pipeline. It does rely on the previously mentioned
devleopment dependencies. It runs all the tests in the `tests` directory
and if all pass, the script opens the HTML report in the system browser.

Running tests without measuring coverage is substantially faster and is
frequently desirable during development when designing the tests
themselves. For this purpose, two Python functions are available from the
`yolo_dev.py` module: `runTests` which runs all the tests found and puts
results in the terminal. A related function, `runTest` allows running a
single test by passing the test class to it.

Besides the test runners, the `yolo_dev.py` module also provides the
`yolo` function which runs any passed functions including relevant
information such as identifying the running Python environment.

## Documentation

Documentation is absolutely essential for any serious project, but in
particular a utilities library such as *worktoy*. Here, *all*
documentation must be in the relevant docstrings under classes and
functions. This reduces (but does not eliminate) the risk of
documentation drifting from code.

## LICENSE

worktoy is released under Apache-2.0, and contributions are accepted under
the same license.
