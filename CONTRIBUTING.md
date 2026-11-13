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

Without 'mamba', the same development tools are declared as dependency
groups in `pyproject.toml`, which pip 25.1 or later installs into
whatever environment is active:

```terminaloutput
pip install --group dev
```

The `dev` group includes the `test` and `docs` groups.

## Version Support

Another quirk of *worktoy* is legacy support all the way back to 3.7 and
up to the latest stable Python, which as of this writing is 3.15. Extending
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

### Runtime and `if TYPE_CHECKING:  # pragma: no cover, no mutate`

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
suite. This requirement is non-negotiable. Every release workflow runs
the suite on each supported Python, from 3.7 to 3.15, and measures the
coverage on 3.15, refusing to publish below 100%. That measurement is
authoritative, but included in the repository is the
`bin/dev_tooling/coverage_test.sh` script that reliably achieves the
same results. It does rely on the previously mentioned development
dependencies. It runs all the tests in the `tests` directory and if all
pass, the script opens the HTML report in the system browser.

Running tests without measuring coverage is substantially faster and is
frequently desirable during development when designing the tests
themselves. The suite is plain `unittest`, so with `src` on the path, or
*worktoy* installed in the environment, it runs from the repository root
with:

```terminaloutput
python -m unittest discover -s tests -t .
```

Two Python functions do the same from the `bin/dev_tooling/yolo_dev.py`
file: `runTests`, which runs all the tests found and puts results in
the terminal, and `runTest`, which runs a single test by passing the
test class to it. Besides the test runners, `yolo_dev.py` also provides
the `yolo` function which runs any passed functions including relevant
information such as identifying the running Python environment.
`profile_tests.py`, beside it, runs `runTests` under `cProfile` and
saves the profile to `tmp`, with a time stamp in the name of the file.

Every test class is based on `BaseTest` from `worktoy.work_test`,
directly or through a base local to its folder. A test of a refusal
asserts the message of the exception as well as its type.

### Promises and the Manual

Beside `tests` stand two further bodies of checked text. The `promises`
directory states what the library owes the projects built upon it, one
behaviour per file, each written as a test. A change of behaviour is
held against them first: a promise is kept for every release of a major
version, and one that has to be taken back is written up in
`promises/confessions`. The `manual` directory holds one chapter per
package, and every example in it is a doctest. Both run from the
repository root:

```terminaloutput
python -m unittest discover -s promises -t . -p "promise_*.py"
python -m doctest manual/*.md
```

### Mutation Testing Before a Release

Coverage says that every line ran; it does not say that the tests would
notice a wrong line. Mutation testing does: Cosmic Ray changes one line
at a time and runs the tests against each change. The rule for releases:

> Before every release, run Cosmic Ray restricted to code changed since
> the last release tag, using `cr-filter-git`. Every surviving mutant
> must either be killed by a new test or confirmed equivalent and
> recorded as such. A release does not ship with non-equivalent
> survivors. This keeps the changelog's mutation testing claim true
> without full runs.

The run goes on a copy of `src`, `tests` and `pyproject.toml`, never on
the working tree. `cosmic-ray init` on the config, then
`cr-filter-pragma` (so that the `# pragma: no mutate` markers count)
and `cr-filter-git` (so that only the lines changed since the tag
count), then `cosmic-ray baseline` and `cosmic-ray exec`. Each
survivor is read, not trusted: an equivalent mutant is accepted only
with a written reason, as a typing stub, an `is` turned into `==` on a
class or a sentinel, or a shortcut whose removal gives the same answer.
A sweep leaves its sessions and dumps in
`bin/dev_tooling/mutation/runs/`, which is not committed. Once the
survivors and the equivalents with their reasons are written down
there, the sessions, dumps and logs are removed; the written lists
stay.

## Releases

A release is published by pressing a button, never by hand. There are
nine buttons, one GitHub workflow each, named level first and kind
second: `micro-dev`, `micro-rc` and `micro-lts`, and the same three for
`minor` and `major`. A workflow starts only when its button is pressed.
No workflow runs on a push or on a pull request.

The file `bin/release_tooling/VERSION` holds the state the buttons
read, and `release_state.py` beside it decides what a press does. A
`dev` press opens a cycle of development builds, or publishes the next
build of the open one. The `rc` press of the same level closes that
cycle with a release candidate, and the `lts` press publishes the
release, which needs at least one release candidate before it. A press
that makes no sense in the present state is refused in the first job of
its workflow.

The presses that change the kind of cycle need a safety: the press that
opens a cycle, the first release candidate, and the release. The safety
of a button is the file `<button>.safety` beside `VERSION`. It is armed
by replacing its one word `STOP` with `ALLOW` and committing, right
before the press, and every press locks all nine again.

Before it publishes, a workflow runs the suite on every supported
Python and measures the coverage. It stamps the version into
`pyproject.toml`, `src/worktoy/__init__.py` and the heading of
`README.md`, so none of the three is edited by hand, and neither is
`VERSION`.

The buttons run on `main` alone, and every press names its version from
the one `VERSION` file. The tooling therefore publishes one line of
releases: a 1.1.1 cannot be published once 1.2.0 is out. The tooling has
tests of its own:

```terminaloutput
cd bin/release_tooling
python -m unittest discover -s tests -t .
```

The changelog covers the stable releases. Development builds and
release candidates are not logged on their own; their changes are rolled
into the release they lead up to.

## Planned Work

Planned work is kept as items in
`bin/dev_tooling/planning/planned_items.md`: one item for each piece of
work, from the first idea until it is released or rejected, and one for
each release. Every item is written by the template in
`item_template.md`, beside it, so that each answers the same questions.

- The title says what is to be done, verb first, as
  `Optimize attribute access on worktoy classes`.
- The description says what the item is and why it is wanted.
- `Status` says where the item stands. An idea is at `CONCEPTION`.
  Once described it is `UNDECIDED`, `REJECTED`, or `PENDING` when
  something has to happen first. An item nothing stands in the way of
  is `READY`, then `UNDERWAY` while it is built, and `DEV`, `RC` and
  `LTS` as the release buttons publish it.
- `Level` is the kind of release the item needs: `micro` for a repair,
  a correction, speed or text, `minor` for something new, `major` when
  something promised is removed or changed.
- `Scale` says how much work it is: `small`, `medium` or `large`.
- `Release` names the release that carries the item, `Next` says what
  has to happen next and who does it, and `History` holds one dated
  line for every change of status.

A release is an item as well, and the items it carries move with it. A
rejected item stays in the file with its reason, so that it is not
proposed again.

## Reviews

`bin/dev_tooling/review` holds the prompts given to an AI session that
reads the source: `research_prompt.txt` for reading the packages until
they are understood, and `final_review_rc_prompt.txt` for the review
before a release candidate. `review_policy.md` says how the two fit
together, and the reports of earlier reviews are under `archive`.

## Other Tooling

- `bin/dev_tooling/bench.sh` runs the micro-benchmarks in
  `bin/dev_tooling/bench`, which compare *worktoy* classes with plain,
  slotted and dataclass baselines.
- `bin/dev_tooling/yeet_cache.sh` lists every `__pycache__` directory
  and removes them once confirmed.
- `tmp` at the repository root is ignored by git. Scratch output, notes
  and abandoned work go there.

## Documentation

The documentation is generated by [markwork][markwork] and published to
both [Read the Docs][rtd] and [GitHub Pages][ghpages], and it takes an
unusual approach. Rather than extracting and reformatting docstrings, the
page for a source file *is* that file, shown verbatim with syntax
highlighting. Nothing is imported and no docstrings are parsed: markwork
reads each file as text, highlights it, and wires the result into a
navigable site, so what you read on the site is exactly the code in the
repository. markwork began life in this repository as `docs/_gen.py` and
is now a package of its own on PyPI.

markwork runs as an extension of [Sphinx][sphinx], which builds the site
around its pages: the navigation, the search and the furo theme. None of
the docstring machinery of Sphinx, such as autodoc, is loaded. The
configuration is `docs/conf.py`, and the packages the build needs are
listed in `docs/requirements.txt`, which Read the Docs, the lts release
workflows and `environment.yml` all install from.

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

[markwork]: https://pypi.org/project/markwork/
