# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`worktoy` is a Python utilities library that adds runtime type enforcement,
declarative attributes, function overloading, and custom-metaclass
infrastructure on top of stock Python. It targets Python 3.7 through
3.14 — write code accordingly (`Union[X, Y]` not `X | Y`,
`Optional[X]` not `X | None`).

Source layout: `src/worktoy/` (pyproject is `setuptools` based, but
`pytest.ini` sets `pythonpath = src`, so tests import `worktoy`
directly without `pip install -e .`).

## Common commands

```bash
# Full test suite (with coverage, term-missing report)
pytest

# Tests + HTML coverage report, opens in browser
./coverage_test.sh

# Single test file
pytest tests/test_keenum/test_hashing.py

# Single test by node id
pytest tests/test_dispatch/test_overload.py::TestClassName::test_method_name

# Run via legacy unittest discovery (used by yolo_dev.runTests)
python run_tests.py

# Profile the test suite (writes results.prof)
python profile_tests.py

# Bump version + sync pyproject.toml + tag file
python roll_version.py {major|minor|patch|dev}
```

`main.py` is the scratch entry point used during development — every
contributor keeps a `main.py` in repo root for ad-hoc work (it's
gitignored under `/main.py`). `yolo_dev.yolo(...)` is the standard
runner for that file: it calls each function passed in, prints
the version banner, traceback excerpts, and total runtime.

## Style rules (project-specific, non-negotiable)

These come from `.claude/claude.md` and `CONTRIBUTING.md`. Existing
code is consistent with them — match it.

- Max line length: **77 characters**.
- Indentation: **2 spaces** (not 4, not tabs).
- Every Python file starts with `from __future__ import annotations`.
- Type hints on all signatures including `-> None`.
- Docstrings: NumPy style, triple double quotes. Single-line if it
  fits in 77 chars including indent; multi-line otherwise.
- Naming: `camelCase` for functions/variables, `PascalCase` for
  classes. (This deviates from PEP 8 but is consistent throughout.)
- **One class per file.** Module files are named `_snake_case.py`
  and re-exported from the package `__init__.py`.
- No em-dashes anywhere — code, comments, or docstrings.
- Section banners stay in place even when the section is empty.
- `TYPE_CHECKING` imports use `# pragma: no cover` and live behind
  `if TYPE_CHECKING:` to stay 3.7-compatible.

## Architecture

The package is a layered framework. Modules import in dependency
order; the order in `src/worktoy/__init__.py` is canonical:

`utilities` → `waitaminute` → `core` → `dispatch` → `desc` → `mcls`
→ `lorem_ipsum` → `keenum` → `ezdata` → `work_io` → `work_test`

When adding to a module, only import from modules earlier in this
chain. Do not introduce backward edges.

### Layer responsibilities

- **`utilities`** — leaf-level helpers (`maybe`, `textFmt`,
  `stringList`, `wordWrap`, `typeCast`, `ExceptionInfo`,
  `bipartiteMatching`, etc.). No worktoy dependencies.
- **`waitaminute`** — every custom exception in the library lives
  here, organized into subpackages by the layer that raises them
  (`desc`, `meta`, `dispatch`, `keenum`, `ez`, plus orphans like
  `TypeException`). Philosophy is fail-fast/raise-loudly — silent
  fallbacks are bugs.
- **`core`** — most primitive runtime types: `Object`, `MetaType`,
  `ContextInstance`/`ContextOwner`, and `sentinels` (notably
  `THIS`, used by `@overload(THIS)` to refer to the enclosing
  class).
- **`dispatch`** — the `@overload(*types)` decorator and its
  supporting machinery (`Dispatcher`, `TypeSig`, `Permuter`,
  `flexCall`). This is what the README's overload examples use.
- **`desc`** — descriptor protocol: `BaseDescriptor`, `Field`
  (declarative get/set with `@field.GET` / `@field.SET`),
  `View` (read-only Field — only `@view.GET` is exposed; assigning
  to a `View` falls through to `Object`'s default and raises
  `ReadOnlyError`), `AttriBox` (runtime-typed attribute,
  `AttriBox[T](default)`), `FixBox`, `Alias`, `SymbolicName`.
  Introduces the "descriptor-context" concept (see module
  docstring).
- **`mcls`** — the metaclass framework. The pattern: a
  namespace class implements `compile()` returning a plain `dict`;
  the metaclass's `__prepare__` returns the namespace, and
  `__new__` calls `compile()` and forwards to `type.__new__`.
  Public exports: `AbstractMetaclass`, `AbstractNamespace`,
  `BaseMeta`, `BaseSpace`, `BaseObject`. `BaseObject` is the
  common base class users inherit from to get overload + AttriBox
  support. Note: `mcls/_nuthin.py` monkey-patches
  `builtins.__build_class__` deliberately — it provides the
  `__post_init__` hook that `AbstractMetaclass` documents (Python
  doesn't otherwise expose a "class fully built" hook for
  metaclasses), translates cryptic CPython errors (`metaclass
  conflict`, layout conflicts) to typed worktoy exceptions, and
  injects a `_InitSub` base to absorb class kwargs that
  `object.__init_subclass__` would reject. The flavor text is
  gallows humor; the patch is load-bearing. Read its docstring
  before touching it.
- **`lorem_ipsum`** — text generation (`Paragraph`, `Sentence`,
  `Clause`, `StochasticWord`).
- **`keenum`** — enum framework: `KeeNum` (recently reworked to
  remove index-based resolution and the bool/int conflation, see
  recent commits), `KeeMeta`, `KeeSpace`, `Kee` member descriptor,
  plus `KeeFlags`/`KeeFlag` for flag enums.
- **`ezdata`** — `EZData` dataclass (uses its own metaclass
  `EZMeta` and `EZSlot`/`EZDesc` descriptors, separate from `desc`
  to keep `desc` general).
- **`work_io`** — filesystem helpers (`validateExistingFile`,
  `scrapDirectory`, `newDirectory`, `yeetDirectory`, `FidGen`).
- **`work_test`** — `BaseTest` (subclass of `unittest.TestCase`)
  and `BaseContract`; tests use these rather than raw `TestCase`.
- **`termono`** — terminal pretty-printing (`LineSpec`, `Alignum`).
  Currently in active development (see uncommitted files).

### Key idioms users will see (and you should preserve)

- Inherit from `BaseObject` (from `worktoy.mcls`) to enable
  `@overload`, `AttriBox`, and `Field`.
- Class-level attribute declarations: `x = AttriBox[float](0.0)`
  enforces type at runtime and registers `x` as a class-level
  descriptor (not a per-instance dict entry).
- Multiple `__init__` signatures via `@overload(types...)`. Use
  `THIS` as a placeholder for the enclosing class type.
- Declarative computed attributes via `Field()` plus `@field.GET`
  / `@field.SET`.
- Custom exceptions in `worktoy.waitaminute` rather than raising
  built-ins where a typed one already exists.

## Tests

- All tests live under `tests/test_<module>/test_*.py`.
- Test classes typically extend `worktoy.work_test.BaseTest`, not
  `unittest.TestCase` directly.
- `pytest.ini` enforces coverage on both `worktoy` and `tests`
  (`--cov=worktoy --cov=tests --cov-branch`). New code without
  test coverage will show up in the term-missing report.
- `RUNNING_TESTS=1` is set by `run_tests.py`; `DEVELOPMENT_ENVIRONMENT=1`
  by `coverage_test.sh` and `yolo_dev.yolo`. Some code paths
  branch on these.

## Archived experiments

`archive/` at repo root holds work that isn't part of the
distribution but is kept for reference. Don't import from `archive/`
in `src/worktoy/`; it's outside the package path on purpose.

- `archive/tutorial/` — an interactive command-line tutorial
  (`python -m tutorial` from inside `archive/`, given suitable
  `PYTHONPATH`). Has two display modes: a linear "notebook" layout
  with Darcula-flavoured syntax highlighting, and a `--mode=side-
  by-side` fixed-panel TUI that draws box-character frames, places
  class source on top, `main()` and stdout in the middle with
  per-line alignment via `sys.settrace`, and pins stdin to the
  bottom. The four `archive/tutorial/examples/eNN_*.py` files
  follow an unusually narrow 50-char line limit so `main()` fits
  the side-by-side right-cell width without truncation. Archived
  because the result felt like a more ornate way to read the
  README; the user is reconsidering what shape pedagogical content
  should take. Resurrect with `git mv archive/tutorial
  src/worktoy/tutorial` if needed.

## Environment

Conda/mamba based. The dev environment is created from
`environment.yml`:

```bash
mamba env create -f environment.yml
mamba activate worktoy_env
```

Optional runtime dep: `pyperclip` (used in `main.py` and some
dev tooling — guarded with `try/except ImportError`).
