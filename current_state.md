# Current state of worktoy, hand-off of 2026-10-19

> **Spoiler alert.** This file records findings and decisions. A session
> asked to audit or review the source must finish and write down its own
> sweep before reading past this line; a session asked for the hand-off
> reads this file and stops at the archive.

## State of the tree

- Branch `main`, nothing committed by these sessions: every change is in
  the working tree (the author's rule is no git at all from the
  assistant).
- Version still reads `1.0.1-dev1`; the release is headed for 1.1.0 and
  the version, changelog header and workflows are moved by the release
  tooling only.
- Tests, Python 3.14.5 (`worktoy_env`, pytest):
  2207 passed, 50 skipped, 10 subtests.
- Tests, Python 3.7 (`base_3_7`, `unittest discover` as the workflows
  run it): 2285 cases, OK, 68 skipped. Command:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src RUNNING_TESTS=1
  ~/miniforge3/envs/base_3_7/bin/python -B -m unittest discover -s tests`
- No bytecode is left in the tree by the sessions (always
  `PYTHONDONTWRITEBYTECODE=1`, never the `-I` flag, which ignores it).
- 192 files carry a 14:23 timestamp from a PyCharm reformat; cosmetic.

## What was done on 2026-10-19 (all test first, mutation checked)

Central packages (utilities, waitaminute, core, dispatch, desc, mcls):
every open item is fixed, closed as design, or decided. In order:

1. Review of core, dispatch, desc, mcls (58 entries), then decisions:
   C3 `StorageCollision`; C6 `ARGS` registered with `SentinelMeta`; C8
   docs; D2 `overload` refuses non-callables; D10 signature copies in
   `LoadSpaceHook`; D11 late `THIS` swap and lazy owner adoption in
   `Dispatcher.__get__`; D14 `THIS` signatures strict by default
   (`strict=False` asks for the cast); E2 `MissingInstanceDict`; E4
   `Alias` plain-value fallbacks; E7 callback `__func__` unwrap; M4
   inherited plain-base hook check; X1 `isinstance` probe in
   `TypeSig.validateTypes`; X2 `NamelessCallback`; X4 declared types and
   `restoreTHIS`; S2, S3, S6, M5, M8, X3 docstrings.
2. Reviews of keenum, ezdata, lorem_ipsum, work_test by four forks
   (archived notes, see below).
3. Cross-check against the October 16 audits; the author fixed audit
   12 (`hasattr` on values), 6 (`overload.__getattr__`), and 23 via a
   new `BlackListedType` for EZData bodies (`Dispatcher` added to the
   blacklist here).
4. `WorkToyException`: every exception in `waitaminute` (signals aside)
   lists it first before its builtin base; it captures the constructor
   call in `__new__` and rebuilds in `__reduce__`, `__copy__` and
   `__deepcopy__`; `Detached` stands in for an argument that cannot be
   pickled. Closes the exception facet of audit 11.
5. Control-flow family moved to `worktoy.core.control_flow` beside the
   sentinels; `ControlClassError` to `waitaminute.meta`;
   `waitaminute.control_flow` is a thin lazy re-export (module
   `__getattr__`) kept for 1.x, where a `FutureWarning` goes once the
   library raises warnings at all (none are raised yet; the author wants
   a consistent warnings design first).
6. `AttriBox.__reduce__`: a placed box pickles by reference to its
   owner, so tags survive a round trip (box-tag facet of audit 11).
7. `SentinelMeta` and `MetaFlow` subclass `MetaType` and derive from it
   (audit 13); `core` loads `_meta_type` first.
8. Small central batch: audit 15 (`typeCast(slice, None)` refused), 28
   (compiled dispatch carries `__doc__` and the owner's `__module__`),
   30 (`SymbolicName` refuses non-strings), 31 (`AccessError` renders
   unplaced), item 12 docstrings, two long lines, "derive" wording.
9. Audit 5 closed as design: a worktoy value in a class body is a
   shared, read-only class attribute (instances must not override class
   variables; `AttriBox` is the per-instance value); the protection is
   instance-side only, class-level writes and deletes pass. Stated in
   the `Object` docstring.
10. Audit 16: `ReservedName` is a `SyntaxError`.
11. Audit 29: `FastBox` container defaults, try the plain call and retry
    with the arguments as one iterable for the five builtin containers.
12. Keyword dispatch: a keyword call binds to each registration's
    parameter names and count; best type match wins (exact, isinstance,
    cast); `flex` binds canonical names; variadics positional only;
    `DispatchException` lists keywords and prints `(none)` (D8/M12).
13. D9 and the October 16 variadic refusal reversed: two variadics
    accepting one call are no conflict; the most recent declaration of
    the nearest class takes it; `VariadicOverlap` archived.
14. V04: keep `ClaimedName`. S1: `_AnnotationsDescriptor` wired in
    `MetaType.__new__` for metaclasses (3.10 and up only, where `type`
    has the descriptor), so `cls.__annotations__` no longer falls
    through to a base.

## Decisions and rules to carry forward

- No git, no sub-agents except forks on an explicit request, no
  em-dashes, no double backticks in docstrings (single backticks in
  Markdown are wanted), 3.7 floor (newer `typing` names only under
  `TYPE_CHECKING` or in version-gated tests), one class per test file,
  tests first, mutation-check every change, archive instead of delete.
- Values in a class body are read-only through instances, by design.
- Keyword calls dispatch by name; stray keywords raise
  `DispatchException`, not the function's own `TypeError`.
- The most recent variadic declaration wins a shared call; do not
  re-propose a refusal.
- Warnings: none yet; design them consistently before adding any.
  - Candidate (2026-10-22): warn where a box default hands a lone text
    value to a container field type, e.g. `AttriBox[list]('lol')`, which
    `list('lol')` turns into `['l', 'o', 'l']`. With the cast rule of
    2026-10-22 the boxes apply no container rules, so Python's answer
    stands; a warning is the only guard worth considering there. The
    runtime side (`obj.items = 'lol'`) is already refused, since text
    never casts to a container.

## Open items, all in the leaf packages

## Leaf: lorem_ipsum, keenum, ezdata, work_test

### keenum

- **From audit 5** (low, message): a `KeeNum` member placed in a class
  body and written through an instance raises `ReadOnlyError` naming
  `'Game.None'`, since `KeeBase.__set_name__` records no field name. The
  refusal itself is by design (audit 5 is closed); only the name is wrong.
- **K13 / audit 11, member facet** (bug): a pickled member is a phantom
  that is not the member and compares unequal; `KeeFlags` the same.
  Direction: a `__reduce__` on `KeeBase` and `KeeFlags` returning the
  member by class and name.
- **K28** (bug): `KeeBox` stores with `object.__setattr__` directly, so a
  slots-only owner fails with the bare `AttributeError` that
  `MissingInstanceDict` replaced in `AttriBox`. Direction: use `_store`.
- **Audit 14** (low): `Kee[object](None)` breaks the class statement
  with a bare `RecursionError`, `None` being the unset marker of the
  value. Direction: a built flag beside the value.
- **Audit 25** (low): a body binding `A = Kee[int](1)` and then
  `A = 'plain'` keeps the member silently. Direction: `KeeSpaceHook`
  refuses the second binding in either order.
- **Audit 26** (low): `KeeFlags` members of a subclass and its parent
  disagree on equality, membership and the operators. Direction: the
  author's choice of model, then the three views follow it.
- **K19** (bug, low): a string value of a `KeeFlags` member is
  unreachable by lookup; the docstrings mention a `fromValue` that does
  not exist on `KeeFlagsMeta`.
- **K29** (bug, low): a plain-function `__class_resolve__` inherited
  from a plain base passes validation and fails at first lookup; the M4
  check does not cover this hook.
- **K27** (bug, low): error messages that cannot name the member show
  `None` or `- N/A -`.
- **K-S1** (bug, low): `KeeFlag.valueType` has no getter.
- **K6** (hazard): `KeeBox` resolves an assigned `int` by index before
  value, so `owner.lv = 2` differs from `Level(2)`.
- **K14** (hazard): the root `KeeNum` reports `__module__` as
  `worktoy.core._meta_type`.
- **K31** (hazard): a `getKeeFlags` defined in a flags body is replaced
  silently.
- **Audit 7, V01 and V03** (waiting): a staticmethod `__class_resolve__`
  refused; `KeeBox` over an int enumeration refusing `True` with the
  enumeration's error. Both recommended keep.
- **Audit 18, keenum share** (docstrings): "derive" in `_kee_meta.py`,
  `_kee_meta_meta.py`, `_kee_box.py`, `_kee_flags.py`.

### ezdata

- **Z10 / audit 22** (bug): `@overload` on a reserved generated method
  (`__init__`, `__eq__`, ...) is accepted and silently overwritten;
  `LoadSpaceHook` claims it before `EZHook.setItemPhase` can refuse.
  Direction: `EZHook.postCompilePhase` raises `ReservedMethodError` for a
  reserved name already in the compiled dict.
- **Z2** (bug): `EZField[typing.Any](1)` is accepted and fails at the
  first instance with the interpreter's `isinstance` error; the X1 probe
  belongs in `EZField.__class_getitem__` too.
- **Audit 24** (medium): a subclass of a frozen EZData class is mutable
  and unhashable without a word. Direction: inherit the options from the
  nearest EZData base, or refuse the mix as `dataclasses` does.
- **Z13 / audit 3** (hazard, the author's open question): a misspelled
  option keyword is ignored; `frozen='no'` freezes. No guard proposed.
- **Z14** (hazard, low): a field named `instance` or `owner` gets no
  `EZStore`; since the item 12 fix a `__new__`-made instance raises a
  plain `AttributeError` for it.
- **Audit 7, V02** (waiting): a callable instance becomes a field, a
  function stays an attribute. Recommended keep.
- **Audit 18, ezdata share** (docstrings): "derive" in `_ez_meta.py`.

### lorem_ipsum

- **L5** (bug, cosmetic): `Sentence.first(15..24)` and `Paragraph(15..24)`
  render an ellipsis plus a period, four dots; counts stay exact.
- **L4** (hazard, low): `Clause(0..3)` raises `ValueError` while
  `Sentence(3)` renders `'...'`.
- **L7** (hazard, low): `del generator.charCount` is accepted; later
  reads raise `MissingVariable` while cached text still renders.
- **L13** (hazard, low): `GaussianLengths` never checks
  `minVal <= maxVal`.
- Determinism is reachable only through the global `random.seed` and is
  undocumented (note).

### work_test

- **Audit 4** (medium): `FloatSampler(0.5, minVal=0.1)` gives
  `(0.1, 1.0)`; the keyword constructor's default displaces the
  positional bound. Direction: bounds first, keywords after, as
  `IntSampler` does.
- **W4** (bug, low): an empty `with self.subTest():` records an empty
  label instead of the default.
- **W11** (bug, low): `SymbolicSampler.wordCount = '3'` raises a bare
  comparison `TypeError`; the setter compares before checking the type.
- **W9** (hazard): `rowCount` and `colCount` are refused as constructor
  keywords because subclasses replace the base key groups.
- **W10** (hazard): the `count` keyword means `wordCount` while the
  `count` attribute aliases `rowCount` on `SymbolicSampler`.
- **W8** (hazard): `BaseSampler` is instantiable; a missing hook
  surfaces as `isinstance(value, None)` on the first draw.
- **W19** (hazard): `ComplexMixin` hashes by mutable parts.
- **W6** (hazard, documented): `tearDownClass` pops the test module from
  `sys.modules`; a later import rebuilds it, and sentinels may then be
  declared twice.
- `RUNNING_TESTS` is exported by every workflow and read by nothing
  (note).
- **Audit 18, work_test share** (docstrings): "derive" in
  `work_test/__init__.py`.

## Outside both groups (project level, the author's)

- Audit 8: the changelog header and `__version__` still read 1.0.1;
  moved by the release tooling only.
- Whether 1.1.0 claims Python 3.15 (classifiers, CI matrices, the
  "3.7 to 3.14" text in four places).
- `changes.txt`, `better_testing_plan.md`, `docs/rst.txt:3`,
  `CONTRIBUTING.md:87` and `:95`, `SECURITY.md:12`, the local markwork
  version, and the lts trusted-publisher entries, all carried over from
  the morning hand-off of 2026-10-16 unverified.

## Where the records went

- `archive/review_2026_10_19/`: `research_notes.md` and
  `structure_map.html` (the structure read and interactive map of the
  non-leaf packages), `review_notes.md` (the central review, every
  decision and fix recorded), `review_notes_keenum.md`,
  `review_notes_ezdata.md`, `review_notes_lorem_ipsum.md`,
  `review_notes_work_test.md` (the four fork reviews),
  `review_decisions.md` (the author's first decision list),
  `open_issues.md` (the split list this section was taken from).
- `archive/audits/`: `audit_1_1_0.md`, `audit_1_1_0_2026_10_16.md` and
  `BUGS.md`, the October 16 audits this round cross-checked.
- `archive/variadic_overlap/`: the reversed refusal and its tests.
- `archive/no_pickle/`, `archive/init_subclass_keywords/`: older.

## Suggested next steps

1. keenum first: K13 (`__reduce__` returning `getattr(type(self),
   self.name)` on `KeeBase` and `KeeFlags`), K28 (`KeeBox` through
   `_store`), the `'Game.None'` message, then audits 14, 25, 26.
2. ezdata: Z10 and audit 24 are the two silent misbehaviours left
   anywhere; Z2 wants the X1 probe in `EZField.__class_getitem__`.
3. work_test audit 4 and the small lorem_ipsum items.
4. A `dev` workflow run before the next `rc`, and the project-level
   chores listed above.
