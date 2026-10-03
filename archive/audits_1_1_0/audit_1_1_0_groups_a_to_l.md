# worktoy 1.1.0 audit and work list

Last updated 2026-09-29.

This file tracks the 1.1.0 update of worktoy: what the full reads of the
code found, what has been fixed so far, and what is left. The first three
sections, Status, Next and Contents, say where things stand. Everything
after them is the record behind that.

## Status

**Groups A to F are done, and so are items L1 and L11 of group G. The
rest of group G is open, and so are group H, found in a second full read
of the source on 2026-09-26, group I, found in a third on 2026-09-28,
group J, found in a fourth read the same day, group K, found in a
fifth on 2026-09-29, and group L, found in a sixth the same day. Of
group H, items 16 to 25 and 27 are done, item 26
is done for EZData, and items 28 and 29 wait for a decision. Of group I,
items 31, 32, 35, 36, 38, 44, 45 and 46 are done, the rest of items 33
to 43 are proposed for 1.1.0, and items 47 to 49 wait for a decision. Of
group
J, items 50 and 51 are done, items 52 and 53 are proposed for 1.1.0, and
items 54 and 55 wait for a decision. Of group K, items 62 to 65 are
done and items 57 to 61 are proposed for 1.1.0. Of group L, items 71
and 72 are done, and items 67 to 70 and L50 to L54 are proposed for
1.1.0. L2 of group G was settled with item 50.**

The suite gives 1707 passed on Python 3.14 with 100% line and branch
coverage, and passes on every version from 3.7 to 3.13. Of those passes,
50 run `ComplexTest` against no targets (L38). Before running 3.7, check
that `base_3_7` still runs Python 3.7: on 2026-09-29 PyCharm applied the
project's `environment.yml` to it (`conda env update --file
environment.yml --prune -p .../base_3_7`), turning it into Python 3.14,
and the author rebuilt it.

| Group | Items | Status |
|---|---|---|
| [A. Dispatch cache and ordering](#group-a-done) | 1, 2, 7, 13, L3 | done |
| [B. EZHook capturing too much](#group-b-done) | 4, 8, 9 | done |
| [C. KeeBox and KeeFlags resolution](#group-c-done) | 3, 6, 14 | done |
| [D. KeeMeta](#group-d-done) | 10, 11 | done |
| [E. flexCall](#group-e-done) | 5 | done |
| [F. Test support](#group-f-done) | 12, L5, T1 to T5 | done |
| [G. Small fixes and docs](#group-g-small-fixes-and-docs-open) | L1, L2, L4, L6 to L11, D1 to D7 | **open**, L1 and L11 done |
| [H. Source read before 1.1.0](#group-h-source-read-before-110-open) | 16 to 30, L12 to L19, D8 to D14 | **open**, 16 to 25 and 27 done, 26 done for EZData, 28 and 29 need a decision, 30 planned for 1.2 |
| [I. Third source read before 1.1.0](#group-i-third-source-read-before-110-open) | 31 to 49, L20 to L30, D15 to D24 | **open**, 31, 32, 35, 36, 38, 44, 45 and 46 done, the rest of 33 to 43 proposed for 1.1.0, 47 to 49 need a decision |
| [J. Fourth source read before 1.1.0](#group-j-fourth-source-read-before-110-open) | 50 to 55, L31 to L37 | **open**, 50 and 51 done, 52 and 53 proposed for 1.1.0, 54 and 55 need a decision |
| [K. Fifth source read before 1.1.0](#group-k-fifth-source-read-before-110-open) | 57 to 66, L38 to L49, D25 to D28 | **open**, 62 to 65 done, 57 to 61 proposed for 1.1.0, 66 planned for 1.2 |
| [L. Sixth source read before 1.1.0](#group-l-sixth-source-read-before-110-open) | 67 to 72, L50 to L54 | **open**, 71 and 72 done, the rest proposed for 1.1.0 |
| [Out of scope](#out-of-scope) | 15 | not scheduled |

## Handover (2026-09-29)

The session of 2026-09-29 made the fifth full read (group K), finished
item 27, and settled and finished items 63 and 64; item 66 was split off
item 64 for 1.2. A later session the same day made the sixth full read
(group L) and recorded it, with additions at items 53 and 58; it changed
no code and wrote no tests. The same session then settled and finished
items 45, 46, 62 and 65; at the author's request it also expanded the
docstring of `NoPickle` on its empty `__slots__`. Taking up item 46, the
author set a principle for EZData (see [Decisions](#decisions)) and
limited the work to what happens to an implementation in the class body
of an EZData subclass, which found and finished item 71. The author
asked for "decisions first", so the next session resumes with the open
decisions below before more fixes.

### Where to pick up

1. Confirm the baseline: the suite as given under
   [How to work](#how-to-work) gives 1707 passed on 3.14 with 100% line
   and branch coverage.
2. Put item 49, the first row of the table of open decisions below, to
   the author with its proposal, and go down the table one item at a
   time. Keep to one question at a time: during item 46 the author
   stopped a proposal that took on several of its parts together.
3. When the author turns to fixes, take the items under "Ready to fix
   without a decision" group by group, each by the method under
   [How to work](#how-to-work): tests that fail first, then the fix,
   then a mutation check, then the item recorded as done.

Nothing is half done: every item marked "to do" has neither tests nor a
fix yet.

### How the author works through decisions

- Put one decision at a time, with a proposal and the reason for it. The
  author rejected every batch of several questions in order to discuss a
  single item, and asked "what would you propose" rather than choosing
  from a list.
- Prefer the fix that changes the least behaviour. For item 63 a first
  version that stopped all class keywords from reaching
  `__init_subclass__` and removed `Object.__init_subclass__` was called
  too drastic; the accepted fix steps in only where
  `object.__init_subclass__` alone would receive the keywords.
- Check a proposed design against the interpreter before building it: a
  probe showed that `type.__new__` calls `__init_subclass__` before it
  returns, which ruled out patching the finished class.
- Vocabulary: a class derives from its metaclass, and subclasses, or is
  based on, its bases (`object` derives from `type`; `bool` is based on
  `int`). Older text in this file uses "derive" for inheritance; fix it
  only where a passage is being edited anyway.
- Names say what the thing does. For item 62 the author turned down
  `__unique_instances__` for `__no_box_tag__`, since the marker exists to
  refuse the tags, and `_tagCreated` for `_applyTags`.
- Explain a mechanism before building on it. A passing mention that
  every worktoy class "has `__slots__`" through `NoPickle` read as if
  slots were forced everywhere, and nearly led to rolling `NoPickle`
  back; its docstring now explains the empty `__slots__`.

### Open decisions with the proposals made so far

Each still reproduces as recorded (probed on 2026-09-29).

| Item | Proposal | Reason |
|---|---|---|
| 49 | Compare and hash `SymbolicName` by its words (a case-insensitive variant is possible, since every rendering normalises case) | the class is otherwise a value |
| 54 | Settle with item 30 in 1.2, but apply item 17's text refusal to `EZField` container defaults in 1.1.0 | `EZField[list]('abc')` splits the text while `AttriBox[list]('abc')` refuses it |
| 28 | Refuse a flag named `NULL` in the class body, together with L7 | the name collides with the empty member |
| 48 | Refuse, in an enumeration body, the `__class_*__` hooks its metaclass overrides | today they are accepted and ignored, and `__class_call__` breaks the class statement |
| 47 | Key the sentinel registry by module and qualified name | two libraries should not share a sentinel by accident |
| 29 | Refuse stacking `@overload(...)` with `flex` or `fallback`, in either order, naming both decorators | no such combination works today |
| 55 | Redesign the variadic expansions in 1.2 | already recommended there |
| 31 review | Decide whether every `KeeFlags` lookup miss raises `KeeResolveError`, as a `KeeNum` miss does | today a name miss raises `KeyError`, an index miss `KeeResolveError` and a value miss `ValueError` |

### Ready to fix without a decision

L7 and L10 (group G), 33, 34, 37 and 39 to 43 (group I), 52 and 53 (group
J), 57 to 61 (group K), 67 to 70 (group L), and the low-severity and
docstring items.

## Next: groups G, H, I, J, K and L

Every item left in group G is small, and none waits for a decision: L7
and L10 are decided and only their code is missing.

| Item | What | State |
|---|---|---|
| L1 | Two `AttriBox` fields such as `fooBar` and `foo_bar` share one storage name; a class attribute at the storage name hides the default | done: the first documented as undefined, the second fixed |
| L2 | worktoy exceptions cannot be unpickled, including `ClassFieldError`, `ReservedMethodError` and `KeeFlagNameError` from groups B and C | done with item 50: pickling refused (DECIDED) |
| L4 | A `MissingVariable` raised on a class names the metaclass instead | to do |
| L6 | `Field(other)` drops the `setName` callbacks | to do |
| L7 | A `KeeFlags` body accepts flag names that are not upper case | decided, to do |
| L8 | Deriving from the wrong `KeeNum` root gives an unhelpful message | to do |
| L9 | Errors from generated EZData methods name the factory's local function | to do |
| L10 | `onSet` receives the value as assigned instead of as stored | decided, to do |
| L11 | A field always holds an instance of its field type | done |
| D1 to D7 | Out-of-date docstrings | to do |

Each item is described in full under
[Group G](#group-g-small-fixes-and-docs-open).

Group H comes from a second full read of `src/worktoy` on 2026-09-26.
Items 16 to 24 are bugs with a clear fix, proposed for 1.1.0. Items 25
to 29 are behaviour the author may want to keep, so each needs a KEEP or
CHANGE before its tests are written.

| Item | What | State |
|---|---|---|
| 16 | A frozen `EZData` instance in any class body breaks class creation | done, in `Object` |
| 17 | Container field types (`list`, `tuple`, `set`, `frozenset`, `dict`) wrap a single argument instead of converting it | done; text refused (DECIDED) |
| 18 | `AttriBox[list[int]]` is not refused on 3.9 and 3.10, contrary to the 1.1.0 changelog | done, for `AttriBox`, `FixBox`, `KeeBox` and `FastBox` |
| 19 | `typeCast` to `set` or `frozenset` lets a raw `TypeError` escape | done |
| 20 | `KeeMeta.valueType` is the type of the first member's value, not the declared type | done |
| 21 | `@overload(ARGS[THIS])` stops matching past five arguments | done |
| 22 | A subclass of `EZSpace` drops the fields of bases built with `EZSpace` | done |
| 23 | An owner's `__getattr__` hijacks the `AttriBox` and `KeeBox` defaults | done |
| 24 | `KeeFlags` recognises its root by name | done |
| 25 | EZData replaces a class-body `__init__`, `__eq__` and others without a word | DECIDED and done: refused |
| 26 | Worktoy values as class attributes are read-only descriptors, and are not EZData fields | EZData half DECIDED and done; the read-only half moved to item 56 (1.2) |
| 27 | The lorem generators ignore keyword arguments | DECIDED and done: honour `charCount=`, refuse others with Python's `TypeError` |
| 28 | A flag named `NULL` collides with the empty member | DECISION |
| 29 | `@overload` stacked on `@overload.flex` or `@overload.fallback` fails late | DECISION |
| 30 | `AttriBox` converts through its own constructor fallback instead of `typeCast` | DECIDED, planned for 1.2 |
| L12 to L19 | Low severity | to do |
| D8 to D14 | Out-of-date docstrings | to do |

Each item is described in full under
[Group H](#group-h-source-read-before-110-open).

Group I comes from a third full read of `src/worktoy` on 2026-09-28.
Items 31 to 44 are bugs with a clear fix, proposed for 1.1.0. Items 45
to 49 are behaviour the author may want to keep, so each needs a KEEP or
CHANGE before its tests are written. The read also added to items 18,
29, 30, L2 and L19; each addition is marked at its item.

| Item | What | State |
|---|---|---|
| 31 | `KeeMeta.__instancecheck__` lets a foreign `__eq__` decide membership | done, with its `KeeFlags` counterpart |
| 32 | `DelException`, `QuestionableSyntax` and `UnboundClassHook` render as `<no detail available>` | done |
| 33 | `EZField[list[int]]` is not refused on 3.9 and 3.10 (item 18 for `EZField`) | to do, 1.1.0 |
| 34 | `FastBox` defaults skip the instance rule and the text refusal | to do, 1.1.0 |
| 35 | Copies of a frozen EZData instance keep only the fields | done |
| 36 | A refused deletion uses up the single write of a `FixBox` | done |
| 37 | `typeCast(bool, x)` lets `x.__eq__` decide | to do, 1.1.0 |
| 38 | `str()` of a `DispatchException` can raise | done; the variadic listing moved to item 55 |
| 39 | `KeeFlagsMeta.__eq__` raises when the other operand's hash fails | to do, 1.1.0 |
| 40 | A second fallback or finalizer replaces the first without a word | to do, 1.1.0 |
| 41 | The stacking order decides whether a duplicate signature is caught | to do, 1.1.0 |
| 42 | An EZData `__class_init__` sees fields without an owner | to do, 1.1.0 |
| 43 | Flags looked up by several members or indices raise `AttributeError` | to do, 1.1.0 |
| 44 | `KeeBox` reads a negative `int` as an index | done |
| 45 | EZData drops unknown keywords, and a keyword overrides a positional | DECIDED and done: both refused, one exception each |
| 46 | Customised helpers of an EZData base do not reach its subclasses | DECIDED and done: optional names defer to EZData and plain bases, reserved methods from plain bases ignored |
| 47 | Sentinels are unique by bare name across the process | DECISION |
| 48 | `__class_*__` hooks are ignored on KeeNum and KeeFlags classes | DECISION |
| 49 | `SymbolicName` compares by identity | DECISION |
| L20 to L30 | Low severity | to do |
| D15 to D24 | Out-of-date docstrings | to do |

Each item is described in full under
[Group I](#group-i-third-source-read-before-110-open).

Group J comes from a fourth full read of `src/worktoy`, later on
2026-09-28. Items 51 to 53 are bugs with a clear fix, proposed for
1.1.0. Item 50 was decided and done: worktoy refuses pickling
everywhere. Items 54 and 55 need a KEEP or CHANGE and a release before
their tests are written; item 55 was split off item 38 on 2026-09-29. The read also added to item 36.

| Item | What | State |
|---|---|---|
| 50 | Enumeration members do not survive `pickle` | done: pickling refused everywhere (DECIDED) |
| 51 | Boxes store their value through the owner's `__setattr__`, and so does `Object.__init__` | done |
| 52 | `Alias` breaks a staticmethod or a classmethod | to do, 1.1.0 |
| 53 | `KeeMeta` takes any attribute of the base for an inherited member | to do, 1.1.0 |
| 54 | `EZField` defaults skip `typeCast` | DECISION |
| 56 | Worktoy values are read-only descriptors as class-level defaults | planned for 1.2, split off item 26 |
| 55 | Variadic declarations are expanded into concrete signatures | DECISION (redesign, recommended for 1.2); its message symptom fixed with item 38 |
| L31 to L37 | Low severity | to do |

Each item is described in full under
[Group J](#group-j-fourth-source-read-before-110-open).

Group K comes from a fifth full read of `src/worktoy`, on 2026-09-29.
Items 57 to 61 are bugs with a clear fix, proposed for 1.1.0. Items 62
to 65 are behaviour the author may want to keep, so each needs a KEEP or
CHANGE before its tests are written. The read also added to L20 and L23.

| Item | What | State |
|---|---|---|
| 57 | `@overload` accepts anything as a type | to do, 1.1.0 |
| 58 | `typeCast` to a subclass of a builtin skips the lossless rules | to do, 1.1.0 |
| 59 | A KeeNum lookup by an unhashable value raises `TypeError` | to do, 1.1.0 |
| 60 | A `__class_resolve__` without `@classmethod` breaks the lookups past the names | to do, 1.1.0 |
| 61 | `Dispatcher.clone` shares its signatures with the original | to do, 1.1.0 |
| 62 | Every value a box builds carries the box, so user objects built by `AttriBox` or `Kee` refuse pickling | DECIDED and done: tags kept and made reliable (62a), boxes copy to themselves (62c) |
| 63 | Class keywords reach `object.__init_subclass__`, so `trustMeBro=True` fails outside `Object` | DECIDED and done: `MetaType` withholds them where only `object` would receive them |
| 64 | A misspelled class keyword is dropped without a word | DECIDED and done: EZData refuses it, `order` accepted |
| 65 | EZData replaces a class-body `__match_args__` without a word | DECIDED and done: the class body's tuple is kept |
| 66 | An EZData class refuses the class keyword of a base's own `__init_subclass__` | planned for 1.2, split off item 64 |
| L38 to L49 | Low severity | to do |
| D25 to D28 | Out-of-date docstrings and comments | to do |

Each item is described in full under
[Group K](#group-k-fifth-source-read-before-110-open).

Group L comes from a sixth full read of `src/worktoy`, later on
2026-09-29. Items 67 to 70 are bugs with a clear fix, proposed for
1.1.0, and none of them needs a decision. The read also added to items
53 and 58. Item 71 was found later the same day, while item 46 was
discussed, and is done, as is item 72, which followed from the
author's own mixin example.

| Item | What | State |
|---|---|---|
| 67 | `del` in a class body does not take effect | to do, 1.1.0 |
| 68 | `KeeBox` applies the keywords of its default to an assigned value | to do, 1.1.0 |
| 69 | The lorem generators keep their layout when `charCount` changes | to do, 1.1.0 |
| 70 | An `overload` bound in a second class under another name is dropped | to do, 1.1.0 |
| 71 | An EZData class body binding an attribute EZData sets itself makes a field of it | DECIDED and done: refused with `ReservedAttributeError` |
| 72 | EZData generates no `__len__`, so a plain base's placeholder `__len__` decides length and truth | DECIDED and done: `__len__` generated and reserved |
| L50 to L54 | Low severity | to do |

Each item is described in full under
[Group L](#group-l-sixth-source-read-before-110-open).

## Contents

- [Status](#status), [Handover](#handover-2026-09-29) and
  [Next](#next-groups-g-h-i-j-k-and-l): where things stand, and where the
  next session resumes.
- [How to work](#how-to-work): the commands, and the method every group
  follows.
- [Decisions](#decisions): what the author has settled, item by item.
- [Changelog material for 1.1.0](#changelog-material-for-110): drafts for
  `changelog.md`.
- The groups done, one section each with what was wrong, what changed,
  the tests and the verification: [A](#group-a-done), [B](#group-b-done),
  [C](#group-c-done), [D](#group-d-done), [E](#group-e-done),
  [F](#group-f-done).
- [Group G](#group-g-small-fixes-and-docs-open): the open items in full.
- [Group H](#group-h-source-read-before-110-open): the findings of the
  second full read of the source, with a repro for each.
- [Group I](#group-i-third-source-read-before-110-open): the findings of
  the third full read of the source, with a repro for each.
- [Group J](#group-j-fourth-source-read-before-110-open): the findings of
  the fourth full read of the source, with a repro for each.
- [Group K](#group-k-fifth-source-read-before-110-open): the findings of
  the fifth full read of the source, with a repro for each.
- [Group L](#group-l-sixth-source-read-before-110-open): the findings of
  the sixth full read of the source, with a repro for each.
- [Out of scope](#out-of-scope): item 15.
- [Background](#background): how the audit was made and how this file is
  organized.
- [Appendix](#appendix-original-findings-of-the-closed-items): the
  original findings of the closed items, as first recorded.

## How to work

Run the suite as:

```
PYTHONDONTWRITEBYTECODE=1 ~/miniforge3/envs/worktoy_env/bin/python -m pytest -p no:cacheprovider tests
```

It must give 100% line and branch coverage over both `src/worktoy` and
`tests`. The `base_3_7` to `base_3_13` environments in `~/miniforge3/envs`
cover the older versions. Only `base_3_7` has pytest; the others run the
suite as:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ~/miniforge3/envs/base_3_11/bin/python -m unittest discover -s tests -t . -q
```

Probes are throwaway scripts, run as:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ~/miniforge3/envs/worktoy_env/bin/python probe.py
```

Every group follows the same method:

- Probe first: confirm the audit's repro and the cases around it, which
  in groups B to D showed each item to be wider than first recorded.
- An item marked DECISION is settled with the author before its tests are
  written.
- A new exception is created first, in the style of `waitaminute`, so the
  tests can name it.
- Tests: one `TestCase` per file, subclassing the package's own base
  (`EZTest`, `KeeTest`). A class that fails to build today is built
  inside its test method, so one failure cannot break the whole file.
- Mutation check: copy `src/worktoy` into a fresh scratch directory per
  break, apply one break, and run pytest with `-o pythonpath=<copy>`,
  since the `pythonpath = ["src"]` setting in `pyproject.toml` otherwise
  wins. Run an unmodified copy as a control. Use new directory names
  rather than deleting old ones.
- A finished group is recorded here: a "Group X: done" section (the
  files changed, what was wrong, what changed with each decision marked
  DECIDED, tests added, verification, notes), its rows in Status and Next
  updated, its decisions added under Decisions, and its items moved from
  the open sections to the appendix. Its user-visible changes go into
  "Changelog material for 1.1.0", in the voice of `changelog.md`.

## Decisions

Settled by the author. The item sections refer back here.

- **Item 4:** a class object in an EZData body is refused
  (`ClassFieldError`).
- **Item 5:** ordinary methods are no longer wrapped by `flexCall`, so an
  extra positional argument raises Python's own `TypeError`.
  `FlexCallHook` is off by default and stays available to a namespace
  that declares it; the `BaseDescriptor` callbacks keep truncation.
- **Item 8:** assignment to a field casts like `__init__`; a class body
  may not define `__setattr__` (`ReservedMethodError`).
- **Item 9:** several EZData bases with fields combine; fields follow the
  reversed method resolution order over each class's own fields, and the
  nearest class decides a field.
- **Item 11:** the root of a metaclass is recognised as
  `cls is type(cls).keeNum`. Each subclass of `KeeMeta` builds its own
  root through the `keeNum` descriptor of `KeeMetaMeta`, and enumerations
  under that metaclass derive from that root.
- **Item 14:** a flag name may not contain `'_'` (`KeeFlagNameError`).
- **Item 15:** out of scope, since a real fix needs a new PEP.
- **L7:** enumeration names are upper case in the class body, for
  `KeeFlags` as for `KeeNum`, and lookups by call or subscript ignore
  case: `WeekDay('monday')` is `WeekDay.MONDAY`.
- **L10:** an assignment that needs a cast stores the cast value.
  `preSet` receives the value as assigned, `onSet` the value as stored:
  `2` and `2.0` for an `AttriBox[float]`.
- **L11:** the value an `AttriBox` or an `EZField` holds is always an
  instance of its field type, `isinstance(foo.bar, Foo.bar.fieldType)`,
  but not necessarily of exactly that type: a `bool` in an `int` field,
  or a `Child` in a `Parent` field, stays as it is. Whatever calling a
  class returns must be an instance of that class, `typeCast` included.
- **Group F choices**, open to review, since group F had no DECISION
  items: samplers are per test through `AttriBox`, a bare
  `with self.subTest:` is recorded under `'<sub test>'`, and `FullName`
  puts the family name first. See [Group F](#group-f-done).
- **Item 31:** a member is recognised by identity, and the pre-filter
  group C put in `KeeBox._isMember` goes, since it only worked around
  this item. The `KeeFlags` counterpart is folded in: its lookup by
  value compares a value only with member values of a type the value is
  an instance of. One choice there is open to review, since the author
  settled the fold-in but not the exception: an identifier matching no
  member raises `ValueError`, as a miss already did, rather than
  `KeeResolveError`, as a `KeeNum` does.
- **Item 25:** every method EZData installs after the class body,
  and so used to replace without a word, is refused in the class body
  with `ReservedMethodError`, as `__setattr__` already was: `__init__`,
  `__iter__`, `__eq__`, `__hash__`, the four ordering methods and
  `__delattr__`. The helpers installed before the class body stay open
  to redefinition.
- **Item 27:** the lorem generators honour `charCount=` as a keyword
  and refuse any other keyword, with the `TypeError` Python raises for an
  unexpected keyword argument, which is what the positional form raises
  too; no worktoy exception.
- **Item 50 and L2:** no worktoy object pickles, exceptions included.
  Pickling, or restoring state from a pickle stream, raises
  `PickleException`; copying keeps working.
- **Item 63:** every class deriving from a worktoy metaclass takes class
  keywords, whether or not it is based on `Object`. `MetaType.__new__`
  forwards them to `type.__new__` as before, except where only
  `object.__init_subclass__` would receive them; `BaseTest` swallows them
  as `Object` does. A first version that withheld every keyword and
  removed `Object.__init_subclass__` was rejected as too drastic.
- **Item 64:** an EZData class refuses a class keyword that is none of
  its option spellings nor `trustMeBro` or `_strictMRO`, with
  `ClassKeywordError` at the class statement. `order` is a spelling of
  `ordered`. Other worktoy classes keep accepting any class keyword.
- **Item 45:** the generated `__init__` refuses a keyword naming none of
  the fields with `ExtraKeywordException`, and a field given both by
  position and by keyword with `RepeatedFieldException`; two exceptions,
  one per case, at the author's choice over one exception for both or
  Python's plain `TypeError`. Handing the unused keywords to
  `__post_init__` was rejected, since typos would stay silent.
- **Item 62:** the box tags stay, as the way an object knows the box that
  created it, which worQt relies on. They are written by
  `AttriBox._applyTags` past the object's `__setattr__`, name the box that
  created the object and never a box it was assigned to, and are left off
  what the box did not create or cannot tag. A class opts out by
  declaring `__no_box_tag__` as true, as `KeeBase` and `KeeFlags` do.
  Tagging assigned objects (62b) was declined. A box is its own copy,
  shallow and deep (62c), so a copy of a tagged object, or of the
  instance owning the field, names the box declared on the class.
- **Item 65:** a `__match_args__` set in an EZData class body is kept as
  written, and generated only where the class body sets none, as
  `dataclasses`, `typing.NamedTuple` and `attrs` do. The rule lived in
  `EZHook.matchArgsFactory`, at the author's request, until item 46 made
  `__match_args__` one of the optional names, settled for all seven in
  `_settleOptional`; since then a subclass uses the tuple its parent set
  by hand instead of generating one.
- **EZData principle (2026-09-29, raised with item 46):** a name EZData
  generates but does not depend on for its functionality may be
  overridden by a user's implementation. Every name a user may supply is
  either allowed, and then honoured, or refused with an exception at
  once; none is replaced without a word. The author took this up first
  for implementations in the class body of an EZData subclass, which
  met it for every method and not for the five attributes of item 71.
- **Item 71:** a class body binding `__ez_fields__`, `__key_args__`,
  `__is_frozen__`, `__is_ordered__` or `__kw_only__` raises the new
  `ReservedAttributeError` at that line, pointing to the class keywords.
- **Plain bases (2026-09-29, with item 46):** an EZData class may have
  plain bases, ones not built by `EZMeta`, as well as EZData bases; an
  earlier recollection of an EZData-bases-only rule found no record, and
  the author settled it this way after the probe. A plain base may
  define the methods EZData reserves, and EZData's generated methods
  take precedence over them: they are ignored. The reason is a mixin
  such as `ComplexMixin`, written against a protocol so that several
  implementations share its arithmetic; its placeholder `__init__` and
  `__iter__` give way to the real ones. Accepted with it: an EZData
  implementation compares and hashes as EZData does, not as its plain
  base does (`EZComplex(1, 2) != 1+2j`, where a plain `ComplexMixin`
  class compares equal).
- **Item 72:** EZData generates `__len__`, the number of fields, and
  reserves it: an EZData class body may not define it, a plain base may,
  and the generated one takes precedence.
- **Item 46:** the names EZData generates are of two kinds. Reserved
  methods and attributes may not be set in an EZData class body, and a
  plain base's versions give way to the generated ones. The optional
  names, `__field_pairs__`, `asDict`, `asTuple`, `replace`, `__repr__`,
  `__str__` and `__match_args__`, defer to what the user wrote: the class
  body's own, then the first hand-written one along the bases, EZData
  and plain alike, and only then a generated one.

---

## Changelog material for 1.1.0

Drafts for the 1.1.0 section of `changelog.md`, written in its voice: one
topic per change, saying what used to go wrong and what happens now.
Each finished group adds its own topics here.

### Compatibility notes

Changes that existing code may notice:

- An enumeration member, an EZData instance or a `SymbolicName` in an
  EZData class body is now a field rather than a class attribute, and
  takes a positional argument like any other field.

- An EZData class body defining `__init__`, `__iter__`, `__eq__`,
  `__hash__`, `__lt__`, `__le__`, `__gt__`, `__ge__` or `__delattr__`
  raises `ReservedMethodError`. Such a definition never ran before, so
  only the error is new.

- `valueType` of a `KeeNum` class is the declared type `T` of its
  `Kee[T]` members rather than the type of the first value. An
  enumeration with a `bool` value among `int` values is therefore an
  `int` enumeration, and like any such enumeration it no longer resolves
  `True` or `False` by value: `Bits(True)` raises `KeeResolveError`,
  while `Bits(1)` finds the member.

- No object defined by worktoy can be pickled. `pickle.dumps` of an
  enumeration member, an EZData instance, a `BaseObject`, a descriptor
  or a worktoy exception raises `PickleException`, a `TypeError`, where
  it used to produce a stream that rebuilt the object without its
  checks. This includes the implicit pickling of `multiprocessing` and
  `concurrent.futures.ProcessPoolExecutor`. Classes still pickle by
  name, and `copy.copy` and `copy.deepcopy` work as before.

- EZData classes declare no `__slots__`. Field values live in the
  instance `__dict__`, `vars(instance)` shows them, and reading a field
  through the class (`Point2D.x`) raises `MissingVariable` instead of
  returning a slot descriptor.
- Assigning to a field of a non-frozen EZData instance casts the value
  like the constructor does, and raises `TypeException` for a value the
  cast refuses.
- An EZData class body may not define `__setattr__`
  (`ReservedMethodError`) or bind a class object (`ClassFieldError`).
- A `KeeFlags` flag name may not contain `'_'` (`KeeFlagNameError`).
- A `KeeFlags` class looks a value up only among the member values of a
  type the value is an instance of, so `FlagsExample(3.0)` raises
  `ValueError` where it found the member whose value is `3`, as a
  `KeeNum` already refuses a value of another type.
- A frozen EZData class no longer carries a generated `__copy__` and
  `__deepcopy__`. Copies go through the standard protocol and keep every
  attribute the instance holds, and a class body's own `__copy__` or
  `__deepcopy__` now takes effect instead of being replaced.
- A `KeeBox` given a negative `int` looks it up as a value, never as a
  position counted from the end, so for an enumeration whose values are
  of another type, such as `KeeBox[WeekDay](-1)`, it raises
  `KeeBoxValueError` where it gave the last member.
- A `__class_init__` hook on a KeeNum class now runs, and the bases of a
  new KeeNum class are notified through `__subclasshook__`.
- A method in the body of a worktoy class no longer drops positional
  arguments it does not declare; such a call raises `TypeError`.
  `AbstractNamespace` no longer declares `FlexCallHook`.
- The callback decorators of `BaseDescriptor` (`preGet` to `onDelete`)
  return the callback wrapped by `flexCall`, and like `setName` they
  refuse anything but a plain function (`TypeException`).
- `AttriBox`, `FixBox` and `KeeBox` store a value at the private name
  followed by the lower-case box class name and `_field_object__`, so an
  `AttriBox` named `fooBar` stores at `__foo_bar__attribox_field_object__`
  instead of `__foo_bar__`; `vars(instance)` shows the new names, and
  code reading that storage directly needs them.
- A field type whose constructor returns something other than an
  instance of that type is refused: `AttriBox` and `EZField` raise
  `TypeException` where they would have stored the value, and
  `typeCast` raises `TypeCastException` instead of returning it, so the
  cast passes of an overloaded call skip that signature.
- `BaseTest` declares its samplers and the `stochWord` and
  `loremSentence` generators with `AttriBox`, so each test builds its
  own; read through the class, they return the `AttriBox`. `BaseTest` no
  longer defines `setUpClass`. Each `LoremSampler` holds its own
  `Sentence`.
- Internal: `BaseSpace.getOverloads()` and `getVariadics()` return the
  class body's own registrations only; inherited ones come from the
  `collect*` methods. `Dispatcher.addSigFunc` and `addVariadicSigFunc`
  take an optional `distance`.
- `Clause`, `Sentence`, `Paragraph` and `BaseGenerator` take their
  character count as the `charCount` keyword and refuse any other
  keyword with `TypeError`, where every keyword used to be dropped
  without a word. The copy constructor of `Clause` refuses keywords, as
  those of `Sentence` and `Paragraph` already did.
- A class deriving from a worktoy metaclass whose bases leave only
  `object.__init_subclass__` to receive its class keywords now builds
  and drops them, where it raised `TypeError`. `BaseTest` defines an
  `__init_subclass__` accepting any keyword, as `Object` does.
- An EZData class statement with a class keyword that is none of the
  option spellings, nor `trustMeBro` or `_strictMRO`, raises
  `ClassKeywordError`, a `TypeError`, where the keyword used to be
  dropped. `order=True` makes an EZData class ordered.
- Calling an EZData class with a keyword that names none of its fields
  raises `ExtraKeywordException`, and giving a field both by position and
  by keyword raises `RepeatedFieldException`, both `TypeError`s. The
  keyword used to be dropped, and the keyword value used to replace the
  positional one.
- The tags a box writes onto an object it creates (`__field_name__`,
  `__field_owner__`, `__field_box__`) go past the object's own
  `__setattr__`, so a frozen dataclass or frozen EZData instance built by
  a box is now tagged, and a field type whose `__setattr__` refuses
  every write can now be held. An enumeration member (`Enum`, `KeeNum`,
  `KeeFlags`), a class, and an object the box handed back without
  creating it are no longer tagged.
- `copy.copy` and `copy.deepcopy` of an `AttriBox`, `FixBox`, `Kee` or
  `KeeBox` return the box itself, where they built a new one. A deep copy
  of an object a box created, or of the instance owning the field, no
  longer copies the box along with it.
- A `__match_args__` set in the body of an EZData class is kept, where
  the generated tuple of all fields used to replace it without a word.
- An EZData class uses the `__field_pairs__`, `asDict`, `asTuple`,
  `replace`, `__repr__`, `__str__` or `__match_args__` a base wrote by
  hand, an EZData base or a plain base, where it used to generate its
  own over it. A subclass of a class with a hand-written
  `__match_args__` keeps that tuple. An EZData class mixing in a class
  with its own `__repr__` or `__str__` now renders through it. The new
  class attribute `__ez_generated__` lists the names generated for a
  class, and a class body may not bind it (`ReservedAttributeError`).
- An EZData class body binding `__ez_fields__`, `__key_args__`,
  `__is_frozen__`, `__is_ordered__` or `__kw_only__` raises
  `ReservedAttributeError`, where the binding used to become a field of
  that name while the class kept the generated value.
- EZData instances have a length, the number of fields: `len(instance)`
  used to raise `TypeError`, unless a plain base supplied a `__len__`,
  which now gives way to the generated one. An instance of a class with
  no fields and no `__bool__` is falsy. An EZData class body defining
  `__len__` raises `ReservedMethodError`.

New public names: `EZStore` in `worktoy.ezdata`; `ClassFieldError`,
`ReservedMethodError`, `ClassKeywordError`, `ExtraKeywordException`,
`RepeatedFieldException` and `ReservedAttributeError` in
`worktoy.waitaminute.ezdata`; the class
attribute `__no_box_tag__`, through which a class keeps its instances
untagged by boxes;
`KeeFlagNameError` in `worktoy.waitaminute.keenum`.

### Box fields keep clear of other names

An `AttriBox`, `FixBox` or `KeeBox` stored its value at the private name
of its field, such as `__foo_bar__` for `fooBar`, which is exactly the name
a class declares for a private attribute in the `Field` pattern. A class
attribute `__value__ = None` beside `value = AttriBox[int](69)` hid the
default, a field named `init` or `dict` read the instance's own
`__init__` or `__dict__`, and a field named `posArgs` on a `BaseObject`
read the positional arguments `Object` keeps. The value is now stored at
a name that says what put it there, such as
`__foo_bar__attribox_field_object__` or `__foo_bar__fixbox_field_object__`,
which no such name can equal. Declaring the same field name twice in two
spellings, such as `fooBar` and `foo_bar`, still shares one storage, and
the `AttriBox` docstring calls that undefined behaviour.

### Fields always hold an instance of their field type

The value an `AttriBox` or an `EZData` field holds is an instance of its
field type, though not necessarily of exactly that type: a `bool` in an
`int` field stays a `bool`. A field type whose constructor returned
something else, such as a class whose `__new__` hands back an `int`,
used to leave the field holding that value, or failed with an empty
`RecursionError` on assignment. It now raises `TypeException`.
`typeCast`, which such casts go through, likewise raises
`TypeCastException` instead of returning a value that is not an
instance of its target.

### Each test gets samplers of its own

The random-data samplers of `BaseTest` (`randomInteger` and the rest) were
single objects shared by every test in the run, so a test that narrowed a
range in its `setUp` changed it for every test after it, in any class.
Every `LoremSampler` also drew from one shared `Sentence`. Each test now
builds its own samplers, and the `stochWord` and `loremSentence`
generators, on first use, and each `LoremSampler` holds its own
`Sentence`.

### SubTest blocks without a label

`with self.subTest:`, entered without calling it first, raised an empty
`RuntimeError` on leaving the block, even when the block went well, and
that error replaced whatever the block raised, a `KeyboardInterrupt`
included. Inside a labelled block it removed the outer label instead. Such
a block is now recorded under the label `'<sub test>'`, like any other.

### Methods of worktoy classes are called like any method

Every plain method in the body of a `BaseObject`, `EZData`, `KeeNum` or
`KeeFlags` class used to be wrapped so that it dropped the positional
arguments it did not declare, without a word. The wrapper also refused a
keyword argument for a positional parameter, even one with a default,
lost any attribute set on the function in the class body, and made each
call about four times slower. Methods are now kept as written: keywords
work, an extra positional argument raises Python's own `TypeError`, and
`replace(9)` on an EZData instance raises instead of returning an
unchanged copy. The notification callbacks of a descriptor (`preGet` to
`onDelete`, and `setName`) still accept fewer parameters than the
descriptor passes them. A namespace that wants the old behaviour for its
classes can declare `FlexCallHook`, which now also counts keyword
arguments.

### Overloaded methods reached through super()

An overloaded method that called the method it overrides through
`super()` recursed forever, and so did `super().__init__(...)` in an
overloaded `__init__`. Reaching the parent's version first also replaced
the override on that instance for good. The cause was the bound method a
`Dispatcher` cached on the instance, which also made a shallow copy run
its overloaded calls against the original, kept an instance whose
`__class__` changed on the old class's versions, and kept every called
instance alive through a reference cycle. A `Dispatcher` now hands out a
fresh bound method on every access and stores nothing on the instance,
just as Python does for a plain method.

### Overloads and inheritance

A subclass override now wins every call it matches. It used to lose to
the parent it overrides for long variadic calls, and for `THIS`
arguments that are instances of a further subclass. Overloads inherited
from several bases now follow the method resolution order: the nearest
class wins an equal signature, whatever the length of a variadic call,
and a plain method in a nearer base is no longer shadowed. A call that
matches only through a type cast still reaches the parent's signature
first, so a signature added in a subclass never takes over a call its
parent already handled.

### Variadic signatures render

`str()` and `repr()` of a `TypeSig` ending in `ARGS` no longer raise; it
renders as it is written, for example `ARGS[int]`.

### EZData classes may use super(), __class__ and generic bases

An EZData class body turned every plain value into a field, including
the values the interpreter writes into a class body itself. A method
using `super()` or `__class__` made the class fail to build, as did a
`Generic[T]` base or the `class Box[S]` syntax of Python 3.12, and on
Python 3.14 an annotated body gained a field named `__classdictcell__`.
These names now pass through. A class object in the body, such as a
nested class or `kind = int`, used to become a field defaulting to
`type`; it now raises `ClassFieldError` at the offending line.

### EZData assignment keeps the field type

Assigning to a field of a non-frozen EZData instance stored any value,
breaking the guarantee that every field holds a value of its declared
type. Assignment now casts exactly as the constructor does, `p.x = 2`
storing `2.0` in a `float` field, and refuses what the constructor
refuses with `TypeException`, leaving the field as it was. A class body
defining its own `__setattr__` now raises `ReservedMethodError`, since
the generated one is what keeps the guarantee.

### EZData classes with several field-carrying bases

Combining two EZData classes that both declare fields raised Python's
"multiple bases have instance lay-out conflict", because every class
declared all its fields as `__slots__`. Field values now live in the
instance `__dict__`, which lets any EZData classes combine, at the cost
of nothing measurable on reads. Fields follow the order `dataclasses`
uses, from the most general class to the most specific, and the nearest
class in the method resolution order decides a field declared more than
once. A field whose name a data descriptor further along the method
resolution order would take over, such as `directory` from `Object` or a
property on a mixin, keeps its storage through the new `EZStore`.

### KeeBox resolves members and combined flags

A member given as a `KeeBox` default never came back as itself: an
`int` enumeration landed on another member, and other enumerations
raised. A box over `KeeFlags` refused combined members such as
`'READ_WRITE'`, `3` or `Perm.READ_WRITE`. A member now resolves to
itself, and a flags box resolves each argument exactly as subscripting
the flags class does. Assigning a value that is not a member no longer
hands the decision to that value's own `__eq__`, which made an `RGB`
value assigned to a `KeeBox[ColorNum]` raise.

### KeeFlags names

A flag name containing `'_'` made member names ambiguous, since `'_'`
also joins the flag names of a combined member: the flags `READ`, `ONLY`
and `READ_ONLY` gave two members the name `READ_ONLY`. Such a flag name
now raises `KeeFlagNameError` in the class body. `'null'` and `'Null'`
now find `NULL`, as the documented case-insensitive lookup promised.

### KeeNum classes run __class_init__

A `__class_init__` hook on a KeeNum class never ran, and the bases of a
new KeeNum class were never notified through `__subclasshook__`, unlike
every other worktoy class. Both now happen once the class is complete,
so the hook sees the finished members.

### Enumerations of a custom KeeMeta

Each subclass of `KeeMeta` builds a root of its own through `keeNum`,
and enumerations under it derive from that root. The root was recognised
by the name `'KeeNum'`, so under a custom metaclass `base` pointed at
the root and every `mroNum` raised `ValueError`, while an unrelated
enumeration named `KeeNum` was taken for a root. The root is now
recognised as the class `keeNum` built.

### Enumerations recognise their members by identity

A KeeNum class decided whether an object was one of its members by
comparing it with each member through `==`, which hands the decision to
the object's own `__eq__`. A value class whose `__eq__` reads the other
operand made a lookup fail at its very first step: the example
enumeration `ColorNum` raised `AttributeError` for
`ColorNum(RGB(255, 0, 0))`, and so did `isinstance`, `in`, `typeCast` and
assigning such a value to an `AttriBox[ColorNum]`. An object equal to
everything, such as `unittest.mock.ANY`, counted as a member, and
`WeekDay(ANY)` handed it back as one. Members are now recognised by
identity, and the object's `__eq__` is never asked. The lookup by value
of a `KeeFlags` class had the same flaw, returning `NULL` for `ANY` and
raising for an `RGB`; it now compares a value only with member values of
a type the value is an instance of.

### Copies of frozen EZData instances keep their state

A frozen EZData class came with a generated `__copy__` and `__deepcopy__`
that rebuilt the fields alone, so anything else the instance held was
lost in the copy, such as a value `__post_init__` derives and stores past
the frozen `__setattr__`. That also reached a frozen default in an
`AttriBox`, which gives every owner a deep copy of its default: reading
the derived value from it raised `AttributeError`. A class body's own
`__copy__` or `__deepcopy__` was replaced by the generated one as well.
The generated methods are gone. A frozen instance now copies through the
standard protocol, which fills the copy's `__dict__` without calling
`__setattr__`, so the copy keeps all of the instance's state, as the copy
of a non-frozen instance always did.

### KeeBox reads a negative int as a value

A `KeeBox` given a lone `int` subscripted its enumeration with it before
trying the values, and a negative `int` passed that step as a position
counted from the end: with the values `-1`, `0` and `1`, `-1` gave the
member holding `1`. An `int` names a member by index now only when it is
the index of a member, and a negative `int` is looked up as a value, as
calling the enumeration does. An `int` is compared with the member values
only when it is of their type; otherwise the value type converts it
first, so `-1` finds a member holding `-1.0`, and an `int` past the last
index on an enumeration of `RGB` values raises `KeeBoxValueError`, where
the `__eq__` of `RGB` used to raise `AttributeError`.

### Syntax errors of worktoy show their message

`DelException`, `QuestionableSyntax` and `UnboundClassHook` derive from
`SyntaxError`, for which a traceback prints the `msg` attribute rather
than the text of the exception. They never set it, so pytest showed
`<no detail available>` for each of them on every Python version, and so
did an uncaught one on Python 3.13 and later. Each now sets `msg` to its
message.

### Worktoy values in an EZData body are fields

In an EZData class body, a bare value becomes a field, but an
enumeration member, an EZData instance or a `SymbolicName` was left out
of the fields, since every worktoy object looked like a descriptor. They
now become fields like any other value, while real descriptors stay
class attributes. A default that is already of the field type is copied
for each instance rather than passed to the field type's constructor,
which failed for an EZData value on every construction.

### EZData refuses the methods it would replace

An EZData class body could define `__init__`, `__eq__`, `__hash__`,
`__iter__`, `__delattr__` or an ordering method, and EZData replaced the
definition with its generated one without a word, so the method simply
never ran. Each of them is now refused at the line that defines it with
`ReservedMethodError`, as `__setattr__` already was. Validation and
derived state belong in `__post_init__`.

### Variadic overloads over the class itself

`@overload(ARGS[THIS])` matched calls of up to five instances of the
class and nothing longer, since the class was put in place of `THIS`
everywhere except inside `ARGS`. It now matches calls of any length.

### A flags class may be named KeeFlags

The root of the flags enumerations was recognised by its name, so a
user class named `KeeFlags` built no members and took the place of the
root for every flags class defined after it. The root is now recognised
as itself.

### The value type of an enumeration is the declared type

`valueType` on a `KeeNum` class used to be the type of the value of its
first member, and every other value had to be an instance of that. An
enumeration declared `Kee[Animal]` whose first value was a `Dog`, one
mixing values under `Kee[object]`, or one with a `bool` first among `int`
values built without complaint, and then every lookup by value failed
with `TypeException`, even one that should simply miss. `valueType` is
now the declared type, and those lookups work, for `KeeBox` as well.

### Deleting a field builds nothing

Before deleting, a descriptor read the old value in order to report it,
and for a box never read that meant building and storing its default. A
`FixBox` whose deletion was refused had then used up its one write, so a
later first assignment raised `WriteOnceError` against a default nobody
asked for, far from the `del` that caused it. An `AttriBox` built a
default only to overwrite it, and one whose default could not be built
could not be deleted. The read before a deletion now looks at what is
stored and nothing else. A `Field` without deleters also no longer runs
its getter twice when it refuses a deletion.

### The message of a failed dispatch

A `DispatchException` for a method declared with `@overload.finalize`
alone could not render its message: building it raised `TypeError`, and
tracebacks showed `<exception str() failed>`. The message now renders,
with an empty list of available signatures. A variadic declaration such
as `@overload(int, ARGS[str])` used to appear in the list as six concrete
signatures for zero to five trailing arguments, and never as itself; it
now appears as written, `<TypeSig: [int, ARGS[str]]>`.

### No pickling

Pickling a worktoy object rebuilt it from the stored state without
calling its class, skipping every check the class and its metaclass
perform: an enumeration member came back as a second member that the
enumeration accepted but that equalled none of the real ones, and the
exceptions could not be unpickled at all. Every object worktoy defines
now refuses the pickle protocol with `PickleException`, when pickled and
when a stream tries to restore state into it, while copying keeps
working as before.

### Boxes and objects whose class guards its attributes

`AttriBox`, `FixBox` and `KeeBox` stored their values through the
`__setattr__` of the owning class, and `Object.__init__` stored the
constructor arguments the same way. A class whose `__setattr__` refuses
some names could therefore not hold a box, and a `BaseObject` subclass
refusing private names could not be constructed at all. A frozen EZData
class refuses every assignment, so a box declared in its body failed on
its first read. The boxes and `Object` now store their own state past
the owner's `__setattr__`, the way `functools.cached_property` does on a
frozen dataclass. Assigning to a box on a frozen class is still refused.

### The lorem generators take charCount by keyword

`Clause`, `Sentence` and `Paragraph`, and their `first` constructors,
dropped every keyword argument without a word, so `Clause(charCount=30)`
built a clause of the default 40 characters, and a misspelling such as
`Sentence(chars=30)` went unnoticed. The character count is now taken by
keyword as it is by position, cast the way an assignment to `charCount`
is, and any other keyword raises the `TypeError` Python raises for an
unexpected keyword argument, as the positional form always did. The copy
constructor of `Clause`, which also dropped its keywords, now refuses
them like those of `Sentence` and `Paragraph`.

### Class keywords on every worktoy class

A class keyword such as `trustMeBro=True` worked on a `BaseObject` or
`EZData` class, but a class built by a worktoy metaclass without being
based on `Object` failed with "takes no keyword arguments": every
`KeeFlags` class, every `BaseTest` class, and a class declaring only
`metaclass=BaseMeta`. The `DelException` raised for a `__del__` in a
`KeeFlags` body even advised the keyword that then failed. The metaclass
handed its keywords on to `type.__new__`, which passes them to
`__init_subclass__`, and only `Object` swallowed them there. The
metaclass now withholds them where only `object.__init_subclass__`
would receive them, and `BaseTest` swallows them as `Object` does, so
every such class takes them. The namespace hooks read them and
`__class_init__` receives them as before, and a base's own
`__init_subclass__` still receives them.

### Misspelled EZData options

An EZData class statement dropped any class keyword it did not know, so
`class Point(EZData, frozn=True)` built a mutable class, and
`order=True`, the spelling of `dataclasses`, left the class without
ordering, which surfaced only when two instances were compared. An
unknown class keyword now raises `ClassKeywordError` at the class
statement, listing the accepted spellings, and `order` is accepted as a
spelling of `ordered`.

### EZData constructor keywords

Calling an EZData class dropped any keyword that named none of its
fields, so `Name(givenName='Jane')`, for a field named `givenNames`,
gave the default name without a word. A keyword naming a field that a
positional argument had already filled replaced that value, so
`Point(1, x=2)` was `Point(2, 0)`. The first now raises
`ExtraKeywordException`, which lists the fields, and the second
`RepeatedFieldException`, both `TypeError`s, as `dataclasses` refuses
the same calls.

### Objects know the box that created them

An object an `AttriBox`, `FixBox` or `Kee` creates carries
`__field_box__`, `__field_name__` and `__field_owner__`, naming the box
that created it. The tags used to go through the object's own
`__setattr__`, so a frozen dataclass or frozen EZData instance went
untagged without a word, and a field type refusing every write could
not be held at all. They are now written past `__setattr__`. They are
left off what the box did not create or cannot tag: an object assigned
to the field, a default handed back as it was, a class, an object
without an instance dict, and an enumeration member, whose tags would
otherwise have landed on a shared singleton. A class keeps its instances
untagged by declaring `__no_box_tag__ = True`. A box is now its own copy,
shallow and deep, so a copy of a tagged object, or of the instance
owning the field, still names the box declared on the class, where a
deep copy used to carry a detached copy of the box.

### A class-body __match_args__ is kept

An EZData class generates `__match_args__`, the field names a positional
`case` pattern binds, from its fields in declaration order. A class
body setting its own, such as `__match_args__ = ('y', 'x')`, used to be
overwritten by the generated tuple without a word. It is now kept as
written.

### Hand-written helpers reach subclasses

The helpers `asDict`, `asTuple`, `replace`, `__field_pairs__`,
`__repr__` and `__str__`, and `__match_args__`, may be written by hand
in any EZData class. A subclass used to replace them with generated
ones, so a customised `__field_pairs__` shaped the output of one class
only. Now every EZData class uses the nearest hand-written one along
its bases, and a plain base counts as well: a mixin providing
`__repr__` to several implementations renders the EZData one too.
EZData generates a helper only where none is written.

### EZData bookkeeping attributes are refused in the class body

EZData sets `__ez_fields__`, `__key_args__`, `__is_frozen__`,
`__is_ordered__` and `__kw_only__` on every class itself. A class body
binding one, such as `__kw_only__ = True`, used to get a field of that
name, while the class kept the generated value and stayed positional.
Such a binding now raises `ReservedAttributeError` at its line, whose
message shows the class keyword that sets the option, as in
`class C(EZData, kwOnly=True)`.

### EZData instances have a length, and mixins may supply the protocol

An EZData class may mix in plain classes, such as a mixin providing
arithmetic to several implementations of the same idea. Such a mixin may
declare `__init__`, `__iter__`, `__len__` and the other methods EZData
generates, as placeholders for the protocol it is written against; the
generated methods take precedence, and the mixin's methods work on the
fields. EZData now generates `__len__`, the number of fields, so an
instance's length agrees with its iteration, where a mixin's placeholder
`__len__` used to decide the length and truth of every instance.

---

## Group A: done

Files changed (under `src/worktoy`): `dispatch/_dispatcher.py`,
`dispatch/_type_sig.py`, `mcls/_base_space.py`,
`mcls/space_hooks/_load_space_hook.py`, `core/sentinels/_args.py`.

### What was wrong

- **1.** `super()` inside an overloaded override recursed forever,
  including `super().__init__(...)` in an overloaded `__init__`.
  Reaching the parent first through `super()` silently replaced the
  override on that instance.
- **2.** A shallow copy ran its overloaded calls against the original,
  and an instance given a new `__class__` kept running the old class's
  versions. Both came from the bound method cached on the instance, which
  also kept every called instance alive through a reference cycle.
- **7.** A subclass override lost to the parent it overrides for long
  variadic calls, and for `THIS` arguments that are further subclasses.
- **13.** Overloads from several bases ignored the method resolution
  order: the last base won collisions, the winner changed with the length
  of a variadic call, and plain methods in earlier bases were shadowed.
- **L3.** `str()` and `repr()` of a variadic `TypeSig` raised.

### What changed

- **Bound methods (items 1, 2):** `Dispatcher.__get__` builds a fresh
  `MethodType` on every access and stores nothing on the instance, just
  as Python does for plain methods. The cost is about 0.25 microseconds
  per call. `_getCachedKey` is gone.
- **Own and inherited registrations (items 7, 13):** `BaseSpace` records
  only the registrations its own class body makes, in lists of
  `(TypeSig, function)` pairs rather than dicts keyed by signature (a
  signature holding `THIS` hashes differently before and after its class
  exists). When the class compiles, `collectOverloads`,
  `collectVariadics`, `collectFallback` and `collectFinalizer` walk the
  method resolution order:
  - the class body's own registrations come first;
  - each class in the order then contributes its own, and a signature
    equal to one already collected is skipped, so the nearest class wins;
  - the walk stops at the first plain definition of the name
    (`_definesPlainly`). A `Dispatcher` written in a class body, or held
    by a class not built by `BaseSpace`, counts as a plain definition;
    only a `Dispatcher` that `BaseSpace` built from registrations lets the
    walk continue.
- **Cast order (DECIDED: inherited first):** every registration reaches
  the `Dispatcher` with its distance from the class, 0 for its own. The
  exact-type and `isinstance` passes try the nearest first, so an
  override wins wherever it matches. The cast passes try the farthest
  first (`Dispatcher._getCastOrder`), so a signature a subclass adds
  never takes a call its parent already handled through a cast. This is
  what keeps `Complex(69, 420)` in `tests/test_dispatch/test_dispatcher.py`
  at `69+420j`.
- **ARGS (L3, and needed for item 7):** `ARGS` instances compare and hash
  by their inner type and render as `ARGS[int]`. `TypeSig` compares an
  `ARGS` entry structurally and renders it the same way.

### Tests added

- `tests/test_overload/`: `test_super_overload.py`,
  `test_overload_binding.py`, `test_overload_footprint.py`,
  `test_override_precedence.py`, `test_base_precedence.py`,
  `test_fallback_precedence.py`
- `tests/test_dispatch/test_variadic_type_sig.py`
- `tests/test_core/test_args_sentinel.py`
- `tests/test_mcls/test_space/test_lookup_order.py`
- new cases in `test_variadic_prefix_overlap.py`, `test_load_args.py`
  and `tests/test_mcls/test_space/test_shadow_reads.py`

The one existing assertion removed is the cache check in `test_peek`
(`tests/test_dispatch/test_dispatcher.py`), which tested the cache that
was dropped.

### Verification

Besides the suite and coverage, a mutation check applied 28 deliberate
breaks to the changed code, one at a time on a scratch copy of `src`,
and the suite caught every one. The first round let 6 through, each
closed with a new test. To run the suite against a copy of `src`, pass
`-o pythonpath=<copy>` to pytest: `pyproject.toml` sets
`pythonpath = ["src"]`, which otherwise puts the real `src` ahead of
`PYTHONPATH` and makes every mutation look like it survived.

### Notes for later groups

- `BaseSpace.getOverloads()` and `getVariadics()` now return the class
  body's own registrations only, as `dict[str, list[tuple[TypeSig,
  function]]]`. Inherited registrations come from the `collect*` methods,
  which return `(sig, function, distance)` entries.
- `BaseSpace` no longer defines `__init__`, so the calls to
  `BaseSpace.__init__` in `KeeFlagsSpace` and `EZSpace` (and `super()`
  in `KeeSpace`) reach `AbstractNamespace.__init__`.
- `Dispatcher.addSigFunc` and `addVariadicSigFunc` take an optional
  `distance`. A hand-built `Dispatcher` leaves it at 0, which keeps
  registration order in every pass.

---

## Group B: done

Files changed (under `src/worktoy`): `ezdata/_ez_hook.py`,
`ezdata/_ez_space.py`, `ezdata/_ez_store.py`,
`mcls/space_hooks/_reserved_names.py`,
`waitaminute/ezdata/_class_field_error.py`,
`waitaminute/ezdata/_reserved_method_error.py`.

### What was wrong

- **4.** `EZHook` turned every plain class-body value into a field,
  including the names the interpreter writes into a class body itself:
  - `__classcell__` (any method using `super()` or `__class__`): class
    creation failed, with `RuntimeError` on 3.8 and later and
    `cannot create 'cell' instances` on 3.7.
  - `__orig_bases__` and `__type_params__`: `Generic[T]` bases and the
    3.12 `class Box[S](EZData)` syntax failed.
  - `__classdictcell__`: on 3.14 an annotated body compiled without the
    future import gained a field of that name.

  A class object (a nested class, or `kind = int`) became a field whose
  default was `type`.
- **8.** Assigning to a field of a non-frozen instance stored any value
  unchecked.
- **9.** Two EZData bases with fields raised `multiple bases have
  instance lay-out conflict`, because every class declared all its
  fields, inherited ones included, as `__slots__`.

### What changed

- **Interpreter names (item 4):** `ReservedNames` lists
  `__classcell__`, `__classdictcell__`, `__orig_bases__` and
  `__type_params__`, which `EZHook.setItemPhase` passes through.
  `__annotate_func__` (3.14) is left out on purpose: it holds a
  function, and functions already pass through.
- **Class objects (item 4, DECIDED: reject):** `setItemPhase` raises the
  new `ClassFieldError` (a `TypeError`, with `clsName`, `fieldName` and
  `classObject`).
- **Assignment (item 8, DECIDED: cast like `__init__`):** the new
  `EZHook.castField` is the one cast that the generated `__init__` and
  the new `setAttrFactory` share, so assignment accepts and refuses
  exactly what construction does. Non-frozen classes get the casting
  `__setattr__`; a name that is not a field is stored as given.
- **Class-body `__setattr__` (DECIDED: forbidden):** binding
  `__setattr__` in an EZData body raises the new `ReservedMethodError`
  (an `AttributeError`, like `ReservedFieldError`), whatever the value.
  The list is `EZSpace.__reserved_ez_methods__`.
- **Storage (item 9, DECIDED: support several bases):** EZData classes
  declare no `__slots__`. Field values live in the instance `__dict__`,
  which every EZData instance had already, since `Object` declares no
  slots. On 3.14 a read measured 14.5 ns against 13.7 ns for a slot. The
  old layout also carried a second slot for every inherited field
  (`Sub(1)` took 32 bytes where `Base(1)` took 24).
  - A data descriptor anywhere in the method resolution order beats the
    instance `__dict__`, so a field sharing its name with one gets an
    `EZStore` (new, `ezdata/_ez_store.py`) through
    `EZHook.storeFactory`. Cases in the library: `Object.directory`, and
    `REAL`/`IMAG` of `ComplexMixin` under `EZComplex`.
  - `_applyDefaults` checks the instance `__dict__` rather than
    `getattr`, so a mixin attribute of the same name no longer
    suppresses the default.
- **Field order (DECIDED: the `dataclasses` order):** `EZSpace.__init__`
  walks the reversed method resolution order and registers each EZData
  class's own fields. The farthest class decides a field's position, the
  nearest class decides the field itself, as with attribute lookup and
  the group A overload merge. The old merge (bases right to left, each
  base's merged fields) disagreed with this in 185 of 2110 small
  hierarchies: `class E(D, A)` reordered the fields `E` inherits from
  `class D(A, B)`. It differs from `dataclasses` in one case: in a
  diamond whose right-hand side redeclares a shared field,
  `dataclasses` keeps the shared base's version, since it also copies
  the fields the left-hand side inherited.

### Tests added

- `tests/test_ezdata/`: `test_interpreter_names.py`,
  `test_class_object_rejected.py`, `test_field_assignment.py`,
  `test_multiple_bases.py`, `test_reserved_method.py`,
  `test_field_storage.py`

The one existing assertion changed is in `test_field_owner_name`
(`tests/test_ezdata/test_ez_data.py`), which checked field names against
`__slots__` and now checks them against `__ez_fields__`.

### Verification

The suite passes on every version from 3.7 to 3.14; the skips are the
tests gated on 3.12 and 3.14. A mutation check applied 22 deliberate
breaks, each on its own copy of `src`, and the suite caught every one;
an unmodified copy passed as a control. Two tests (the diamond
redeclaration and the descriptor defining only `__delete__`) were
written specifically to catch breaks that would otherwise have passed.

### Notes for later groups

- `vars(instance)` now shows the fields. Reading a field without a
  store through the class (`Point2D.x`) raises `MissingVariable` through
  `AbstractMetaclass.__getattr__`, whose message names the metaclass
  (L4), where it used to return the slot descriptor.
- `EZHook.postCompilePhase` uses `BaseSpace._getLookupOrder` through
  `self.space`.
- The names added to `ReservedNames` also reach `ReservedNamespaceHook`
  in every namespace, which raises only when such a name is assigned a
  second time.
- Cost: assigning to a field of a non-frozen instance takes about
  305 ns against 14 ns for a plain attribute on 3.14, almost all of it
  the Python-level `__setattr__`. Checking `isinstance(value,
  fieldType)` before calling `castField` measured 291 ns down to 205 ns;
  it matches `typeCast` except for `slice` fields, which `typeCast`
  always revalidates. Not applied.
- `ClassFieldError` and `ReservedMethodError` call the base `__init__`
  with no arguments like the other exceptions, so L2 applies to them.

---

## Group C: done

Files changed (under `src/worktoy`): `keenum/_kee_box.py`,
`keenum/_kee_flags_meta.py`, `keenum/_kee_flags_space.py`,
`waitaminute/keenum/_kee_flag_name_error.py`.

### What was wrong

- **3.** A member given as a `KeeBox` default never came back as itself.
  An `int` enumeration read the member as its index and matched that
  against the values, landing on another member (`Slot.LEFT` gave
  `Slot.CENTER`). A `str` enumeration raised `KeeBoxValueError`, and a
  box over `KeeFlags` raised `KeeBoxTypeError` for every member, `NULL`
  included, and for members mixed with names.
- **6.** A box over `KeeFlags` built its lookup key from the plain names
  of the resolved members, so a combined member contributed
  `'READ_WRITE'` and nothing matched: `'READ_WRITE'`, `3` and a combined
  member plus a further flag all raised `KeyError`, by default and by
  assignment.
- **14.** A flag name containing `'_'` could not be told apart from a
  combination: the flags `READ`, `ONLY` and `READ_ONLY` gave two members
  named `READ_ONLY`, with `Clash.READ_ONLY` and `Clash['READ_ONLY']`
  returning different ones. Also `Perm['null']` raised where
  `Perm['NULL']` worked.
- **Found on the way.** Assigning a value that is not a member, such as an
  `RGB` to a `KeeBox[ColorNum]`, raised `AttributeError`.
  `KeeMeta.__instancecheck__` compares the value with every member
  through `==`, which hands the decision to the value's own `__eq__`, and
  `RGB.__eq__` reads `other.r` from a member.

### What changed

- **Member recognition (item 3 and the `RGB` case):** the new
  `KeeBox._isMember` refuses any value whose type is not built by
  `KeeMeta` or `KeeFlagsMeta` before running `isinstance`, so a value's
  own `__eq__` is never asked about a member. Members of subclass
  enumerations are still accepted, as before. Both `_resolveNum` and
  `__instance_set__` use it; `_resolveNum` returns a member as it is.
- **Flags (items 3 and 6):** `_resolveFlags` resolves each argument by
  subscripting the flags class, so the box accepts per argument exactly
  what the class does: members, names in any case and order, indices.
  The result is built from the union of the members' `names`.
- **Flag names (item 14, DECIDED: refuse `'_'`):**
  `KeeFlagsSpace.addKeeFlag` raises the new `KeeFlagNameError` (a
  `ValueError` with `clsName` and `name`, like `KeeCaseException`) in the
  class body. `KeeFlagsMeta._resolveName` compares canonical names
  ignoring case before splitting, which fixes `'null'`.

### Tests added

- `tests/test_keenum/`: `test_kee_box_member_default.py`,
  `test_kee_box_combined_flags.py`, `test_kee_flag_names.py`

No existing assertion changed.

### Verification

The suite passes on every version from 3.7 to 3.14. A mutation check
applied 11 deliberate breaks, each on its own copy of `src`, and the
suite caught 10; an unmodified copy passed as a control. The survivor
drops the upper-casing of the member name in `_resolveName`, which only
matters for lower-case flag names; see L7.

### Notes for later groups

- `cls['READ_WRITE', 'EXECUTE']` on a flags class still raises
  `KeyError`: several names at once must each be a single flag name.
  `KeeBox` resolves each argument separately, so it accepts that
  combination. Nothing documents the subscript form, so it is left as is.
- The `RGB` fixture (`tests/test_keenum/examples/_rgb.py`) raises from
  `__eq__` on a foreign type instead of returning `NotImplemented`. It is
  left as it is, since it is exactly what exposed the `KeeBox` issue.
- `KeeFlagNameError` calls the base `__init__` with no arguments, so L2
  applies to it.

---

## Group D: done

Files changed (under `src/worktoy`): `keenum/_kee_meta.py`,
`keenum/_kee_meta_meta.py`.

### What was wrong

- **10.** `KeeMeta.__init__` never called the inherited `__init__`, so a
  `KeeNum` class's `__class_init__` never ran, and its bases never
  heard of it through `__subclasshook__`, both of which
  `AbstractMetaclass.__init__` provides for every other worktoy class.
- **11.** `_createBase` recognised the root by the name `'KeeNum'`. Each
  subclass of `KeeMeta` builds a root of its own through `keeNum`, named
  after the metaclass (`FontMetaNum` for `FontMeta`), which is the class
  enumerations under that metaclass derive from. That root failed the
  name check: `FontMeta.keeNum.base` and every `mroNum` below it raised
  `ValueError`, and `FontNum.base` was the root instead of `FontNum`.
- **Found on the way (same cause).** An ordinary enumeration that
  happens to be named `KeeNum` passed the name check: a subclass of it
  took itself as its base, with an empty `mroNum`.

### What changed

- **`__class_init__` (item 10):** `KeeMeta.__init__` takes the bases,
  namespace and keyword arguments instead of discarding them, builds the
  members, and ends by calling the inherited `__init__`. Coming last, a
  `__class_init__` hook sees the finished members.
- **Root (item 11, DECIDED: identity with `keeNum`):** `_createBase`
  compares with `type(cls).keeNum`, the root the class's own metaclass
  builds and caches, instead of comparing names. The root is its own
  base, and so is every enumeration derived directly from it. The
  `__root_class__` marker that `_getKeeNum` wrote into the root
  namespace was never read, so it is gone. The comparison must not run
  while a root is still being built, or `keeNum` would build a second
  one; it cannot today, since `_getKeeNum` builds the root with
  `__new__` alone and `base` is computed on first read.

### Tests added

- `tests/test_keenum/`: `test_kee_num_class_init.py`,
  `test_custom_kee_meta_base.py`

No existing assertion changed.

### Verification

The suite passes on every version from 3.7 to 3.14. A mutation check
applied 6 deliberate breaks, each on its own copy of `src`, and the suite
caught every one; an unmodified copy passed as a control.

### Notes for later groups

- Deriving an enumeration under a custom metaclass from the wrong root,
  as in `class Bad(KeeNum, metaclass=FontMeta)`, is refused at class
  creation, but the message ("must have exactly one base, but received
  none!") does not name the root to derive from; see L8.

---

## Group E: done

Files changed (under `src/worktoy`): `dispatch/_flex_call.py`,
`mcls/space_hooks/_flex_call_hook.py`, `mcls/_abstract_namespace.py`,
`mcls/_base_meta.py`, `desc/_base_descriptor.py`.

### What was wrong

- **5.** `FlexCallHook` sat on `AbstractNamespace`, so `flexCall`
  wrapped every plain method in the body of a BaseObject, EZData, KeeNum
  or KeeFlags class. The wrapper counted only positional arguments
  against the required parameters. A keyword argument for a positional
  parameter therefore raised, even for a parameter with a default, and
  the error listed every parameter from the first one not given by
  position, the ones given by keyword included. Extra positional
  arguments were dropped without a word.
- **Found on the way:**
  - The wrapper did not copy the function's `__dict__`, so an attribute
    set on a method in the class body was gone from the class.
  - The generated `replace`, `asDict` and `asTuple` of EZData were
    wrapped too, so `pt.replace(9)` returned an unchanged copy.
  - Every method call went through the wrapper: 184 ns against 42 ns
    for a method of a plain class on 3.14.

### What changed

- **Ordinary methods (item 5, DECIDED: stop wrapping):**
  `AbstractNamespace` no longer declares `FlexCallHook`, so a method in
  a worktoy class body is kept as written and called as Python calls any
  method. The hook stays exported for a namespace that declares it
  (`flexCallHook = FlexCallHook()` in the namespace body). A probe that
  disabled the hook failed only the two tests checking its marker on
  `BaseObject`; nothing in the library relied on it.
- **Callbacks keep truncation:** truncation exists for the notification
  callbacks of `BaseDescriptor`, which never depended on the hook, since
  `hookPreGet` and the rest call `flexCall` on the callback at every
  access. Without the hook that call built a fresh wrapper each time,
  and an access with a callback measured 2.4 microseconds against 1.5.
  The six decorators (`preGet` to `onDelete`) therefore return the
  callback wrapped by `flexCall`, as `setName` already did, so the
  wrapping happens once in the class body. An override that was never
  decorated is still wrapped as it is called.
- **Keywords (item 5):** the wrapper counts a required parameter named
  in the keyword arguments as supplied (`_missingNames`) and names only
  the ones still missing. A positional-only parameter named by keyword is
  left for the wrapped function to refuse with its own `TypeError`,
  which says what went wrong; a first version refused it in the wrapper,
  and no test could tell the two apart.
- **Attributes:** the wrapper copies the wrapped function's `__dict__`
  before setting its own attributes, so its `__wrapped__` and marker
  still win.

### Tests added

- `tests/test_mcls/test_hooks/test_plain_method_calls.py`
- `tests/test_dispatch/test_flex_call_keywords.py`
- `tests/test_desc/test_callback_wrapping.py`
- `tests/test_ezdata/test_generated_method_calls.py`
- `tests/test_keenum/test_member_method_calls.py`

`tests/test_mcls/test_hooks/test_flex_call_hook.py` was rewritten, as
the decision requires: its tests build their classes on a namespace that
declares the hook instead of on `BaseObject`, and two new tests there
check that an opted-in method drops extra positionals and takes keywords.
Its assertions are otherwise unchanged. No other existing assertion
changed.

### Verification

The suite gives 1424 passed on 3.14 with 100% line and branch coverage,
and passes on every version from 3.7 to 3.13. A mutation check applied
16 deliberate breaks, each on its own copy of `src`, and the suite
caught every one; an unmodified copy passed as a control. Afterwards a
method call on a `BaseObject` measured 41 ns, the same as on a plain
class, and an access with a callback 1.5 microseconds, as before.

### Notes for later groups

- A decorated callback is itself the `flexCall` wrapper, so calling it
  directly (`obj._onSetX(1, 2)`) still drops extra arguments; only
  undecorated methods are strict.
- The six decorators now refuse anything but a plain function with
  `TypeException`, as `setName` always did. Applying one over a
  `staticmethod` or `classmethod` object, with the decorators in that
  order, now fails at class creation. The documented order, with the
  descriptor's decorator directly on the function, is unaffected, and
  nothing in the library or the suite used the other.
- The `TypeError` from a generated EZData method names it by the
  factory's local name; see L9.

---

## Group F: done

Files changed (under `src/worktoy`):
`work_test/samplers/_lorem_sampler.py`, `work_test/_base_test.py`,
`work_test/_sub_test.py`, `ezdata/_ez_field.py` (docstring), and tests.

### What was wrong

- **12.** All six samplers of `BaseTest` were single objects shared by
  every test in the run, since a `BaseObject` placed in a class body
  returns itself on every read. A setting made in one test's `setUp`
  (`colCount = len(text)` in `test_kee_meta_resolve.py`, for one) showed
  up in the samplers of every later test, in any class. Behind them, every
  `LoremSampler`, `BaseTest.randomLorem` included, drew from the one
  class-level `Sentence` of `LoremSampler`, and `setUpClass` attached a
  `loremSentence` shared by every test of a class.
- **L5.** A bare `with self.subTest:` raised an empty `RuntimeError` on
  leaving even a block that went well. Raised from a `finally`, it
  replaced whatever the block raised, a `KeyboardInterrupt` included.
  Inside a called block it removed the outer label, so both blocks were
  recorded under the wrong labels.
- **T1 to T5** as recorded; in T3, four of the five behaviours the empty
  tests were meant to check were already pinned by other tests
  (`test_basic.test_hash`, `test_abstract_namespace.test_duplicate_hook`,
  `test_overload_flex.test_str`, and the sampler tests for the order of
  `onSet`). Only the bases in `str()` of a namespace went unchecked: a
  break dropping them got through the suite.

### What changed

- **Samplers (item 12, chosen: per test through `AttriBox`):** `BaseTest`
  declares `randomInteger` to `randomLorem`, `stochWord` and
  `loremSentence` as `AttriBox` fields, so each test instance builds its
  own on first read, and `unittest` builds one instance per test method.
  `setUpClass` is gone. The other direction the audit gave, a reset in
  `setUp`, would need a list of every setting to restore. `LoremSampler`
  holds its `Sentence` as `AttriBox[Sentence]()`. The `stochWord` of
  `WordSampler` and `SymbolicSampler` stays a class-level
  `StochasticWord`, which keeps no state per instance.
- **Bare sub-tests (L5, chosen: record under the fallback label):**
  `__call__` raises the new `__label_pending__` flag, and `__enter__`
  lowers it, or pushes `'<sub test>'` when no call came first. The
  fallback label and its getter already existed; nothing ever pushed it.
  The other direction, a typed exception demanding the call, would refuse
  a form that reads naturally. Leaving a block that was never entered
  still raises `RuntimeError`, now with a message saying so.
- **Fixtures and tests (T1 to T5):**
  - T1: `nextPrime` loops `while not cls.isPrime(p)`, and
    `testPrimeValued` checks the prime sequence and the member values its
    docstring lists.
  - T2: `givenNames=` in `test_ez_field.py`, which now checks the fields
    of the default value; the same misspelling in the `EZField` class
    docstring is corrected.
  - T4 (chosen: family name first): `FullName` declares `familyName`
    first, as its docstring, its `__str__`, the squad data and the T2
    call all assumed; only the field order and `test_init` said
    otherwise.
  - T3: the empty tests check what the covering tests do not: a
    duplicate hook declared in a namespace body (the real path, wrapped in
    `RuntimeError` before 3.12), `hash(cls)` and the default class hash,
    the exact `str()` and `repr()` of a namespace, the `str()` of an
    unowned and an owned `Dispatcher`, the signatures of `SpacePoint`,
    and in `test_notification.py` what each notification callback sees of
    the value.
  - T5: the duplicated block and the no-op line in `test_field.py` are
    gone, and `test_word_sampler.py` checks that each draw is one word of
    the collections.

### Tests added

- `tests/test_work_test/`: `test_base_test_samplers.py`,
  `test_lorem_sampler_sentence.py`, `test_sub_test_bare.py`

Existing tests changed, as the items require: `testPrimeValued`
(`test_kee_flags_meta.py`), `test_default_value` and `test_str_repr`
(`test_ez_field.py`), `test_init`, `test_alphabetical_order` and
`test_str` (`test_full_name.py`, for the field order),
`test_match_args_ordered_class`, `test_field` (`test_field.py`),
`test_get_item` (`test_word_sampler.py`), the T3 files, and two
docstrings in `test_base_test.py` that credited `setUpClass`. The one
existing assertion whose expectation changed is the `__match_args__` of
`FullName`; `test_init` was rewritten for the field order.

### Verification

Before the fix, the regression tests failed for the reasons above, 20 in
all, and the guards passed. The suite gives 1446 passed on 3.14 with
100% line and branch coverage, and passes on every version from 3.7 to
3.13. A mutation check applied 15 deliberate breaks to the changed code,
each on its own copy of `src`, and the suite caught 14; an unmodified copy
passed as a control. The survivor drops the `SkipSet` in
`LoremSampler._preSetCharCount`, which only spares a redundant set and
leaves nothing to observe. The five T3 breaks, run before and after, went
from one getting through to all caught by the filled tests.

### Notes for later groups

- The redundant-set branch of `LoremSampler._preSetCharCount` was only
  ever reached through the leak: tests kept setting the shared sampler to
  the same length. `test_char_count_set_again` reaches it now.
- `onSet` receives the value as passed, not as stored; see L10.

---

## Group G: Small fixes and docs (open)

Files: various

### Low severity

- **L1. AttriBox storage name collisions (verified, DONE by
  documentation).**
  `src/worktoy/core/_object.py:384`, `src/worktoy/desc/_attri_box.py:389`.
  The storage name comes from the field name alone:
  - `fooBar` and `foo_bar` both map to `__foo_bar__`; an `AttriBox[int]`
    returned the `str` stored by the other field.
  - A class attribute `__value__` hides the default of an AttriBox named
    `value` (the read returns `None`), which collides with the codebase's
    own `__x__` plus `Field` convention.

  A fix through `Object.getPrivateName`, a new naming rule plus a set of
  reserved names gathered by `MetaType`, was implemented on 2026-09-25
  and rolled back the same day as disproportionate to the problem. Any
  fix should stay as small as the problem.

  **DONE (documented):** the notes of the `AttriBox` class docstring now
  say that fields whose names differ only in how their words are joined
  or capitalised, such as `fooBar` and `foo_bar`, or `X` and `x`, share
  one storage when declared on one class, and that the behaviour is then
  undefined.

  **DONE (storage name):** the box family (`AttriBox`, `FixBox`,
  `KeeBox`) stores at the private name followed by the lower-case name
  of the box class and `_field_object__`, through the new
  `AttriBox._getStorageName`: an `AttriBox` named `fooBar` stores at
  `__foo_bar__attribox_field_object__`, a `FixBox` at
  `__foo_bar__fixbox_field_object__`, so anyone meeting the name can tell
  what put it there. A first version used the suffix `value__`
  (`__foo_bar__value__`); the author chose the self-explaining form.
  `getPrivateName` itself is unchanged. The double
  underscore inside keeps the storage apart from every name written in
  the `__snake_case__` style, which fixes the second bullet (`__value__ =
  None` beside `value = AttriBox[int](69)` now reads `69`) and keeps
  fields named `init`, `dict` or `posArgs` (on a `BaseObject`) off
  `__init__`, `__dict__` and the `__pos_args__` of `Object`. The first
  bullet stays documented as undefined behaviour. Test:
  `tests/test_desc/test_attri_box_storage_name.py`, whose five tests
  failed before the change for these reasons. The suite gives 1467 passed
  on 3.14 with 100% line and branch coverage and passes on 3.7 to 3.13,
  and a mutation check caught all seven breaks (the suffix dropped, and
  each of the six call sites back on the old name).
- **L2. worktoy exceptions cannot be unpickled (verified).** They call the
  base `__init__` with no arguments, so `args == ()` and unpickling calls
  the constructor with nothing
  (`pickle.loads(pickle.dumps(TypeException('x', 1, str)))` raises).
  Matters for multiprocessing and xdist. `KeeResolveError` and
  `KeeWriteOnceError` are the exceptions that happen to work, since they
  skip the base `__init__`. **Addition (2026-09-28, third read):**
  `ReservedName` fails differently: it passes its message to
  `Exception.__init__`, so it unpickles with the whole message as the
  name, and `str()` repeats it: "Attempted to use reserved name:
  'Attempted to use reserved name: '__doc__'!'!". Item 32 was fixed
  without touching `args`, so it leaves this item as it was.
  **DONE with item 50 (2026-09-28):** pickling is refused, so every
  worktoy exception raises `PickleException` when pickled instead of
  failing on the way back.
- **L4. Class-level `MissingVariable` names the metaclass (verified).**
  `src/worktoy/mcls/_abstract_metaclass.py:309` passes `cls` as the
  instance and `MissingVariable.__str__`
  (`src/worktoy/waitaminute/_missing_variable.py:69`) prints
  `type(instance).__name__`, giving `Missing 'BaseMeta.nope'!`.
- **L6. `Field(other)` drops the `setName` hooks (verified, new).** The
  copy constructor (`src/worktoy/desc/_field.py:224`) copies every hook
  group except `__set_name_keys__`, so a callback registered with
  `@field.setName` on the prototype never fires on the copy. Every other
  group is copied, so this looks like an oversight rather than a choice.
- **L7. Lower-case `KeeFlag` names are only partly found (verified, new,
  DECIDED).** `KeeNum` refuses member names that are not upper case
  (`KeeCaseException`), but `KeeFlags` accepts any flag name. The
  canonical name of such a flag is found in any case since group C
  (`Low['READ']` and `Low['READ_WRITE']` find `Low.read` and
  `Low.read_write`), but the flag names in another order
  (`Low['write_read']`) and several names at once (`Low['read',
  'write']`) raise `KeyError`: `_resolveName` and `_resolveNames` upper-case
  the query and compare it with the flag names as declared. **DECIDED:**
  names are upper case in the class body, and lookups ignore case. A
  `KeeFlags` body declaring `read` or `Read` is refused at the offending
  line, as a `KeeNum` body declaring `monday` already is, while
  `Perm('read')`, `Perm['write_read']` and `Perm['read', 'write']` find
  their members, as `WeekDay('monday')` finds `WeekDay.MONDAY`. A probe
  in the group F session showed that only the class body needs to change:
  with upper-case flags, every call and subscript lookup already ignores
  case and order, `KeeBox` included, and `KeeNum` already matches the
  decision in full. Refusing lower-case flags also removes the partly
  working lookups above, since such flags can no longer exist. Fix
  direction: check `name.isupper()` in `KeeFlagsSpace.addKeeFlag` next to
  the `'_'` check, raising `KeeCaseException` (whose message says
  "KeeNum members" and needs to cover flags) or `KeeFlagNameError`
  (which names the class); choose while probing. Note: attribute access
  differs between the two, since `WeekDay.monday` finds `WeekDay.MONDAY`
  while `Perm.read` raises `MissingVariable`, as the `KeeFlags`
  docstring promises; the decision is about calls and subscripts, so
  attribute access stays as it is.
- **L8. Deriving from the wrong root gives an unhelpful message (verified,
  new).** An enumeration under a custom metaclass that derives from
  another metaclass's root, as in `class Bad(KeeNum,
  metaclass=FontMeta)`, is refused at class creation by
  `KeeMeta._createBase` with "Enumerating classes derived from
  'FontMeta', must have exactly one base, but received none!". The
  message should say that the base must be `FontMeta.keeNum` or an
  enumeration derived from it.
- **L9. Generated EZData methods carry the factory's local name
  (verified, new).** The functions `EZHook` builds keep the
  `__qualname__` of the local function in their factory, so the
  `TypeError` from `pt.asDict(1)` reads
  `EZHook.asDictFactory.<locals>.asDict() takes 1 positional argument
  but 2 were given`. Only `orderingFactory` sets `__qualname__`, and to
  the bare dunder name. Became visible in group E, when the generated
  methods stopped going through `flexCall`. Fix direction: name each
  generated function after the class and the method in `EZHook`, which
  knows the class name through `self.space.getClassName()`.
- **L10. `onSet` receives the value as passed, not as stored (verified,
  new, DECIDED).** `Object.__set__` (`src/worktoy/core/_object.py`)
  hands `hookOnSet` the incoming value, while `AttriBox` casts it before
  storing. The store itself is right; only the callback sees the raw
  value:

  | Box | Assigned | Stored | `onSet` got |
  |---|---|---|---|
  | `AttriBox[float]` | `2` | `2.0` | `2` |
  | `AttriBox[complex]` | `2.0` | `(2+0j)` | `2.0` |
  | `AttriBox[float]` | `True` | `1.0` | `True` |
  | `FixBox[float]` | `3` | `3.0` | `3` |

  The `BaseDescriptor` docstring says the callback receives "the value
  that was stored", and `Object.hookOnSet` says "the value just set by
  '__set__'". Found in group F while writing `test_notification.py`,
  which uses values needing no cast so as not to pin either answer.
  **DECIDED:** `preSet` receives the value as assigned, before any cast,
  which it already does, and `onSet` receives the stored, cast value:
  assigning `2` to an `AttriBox[float]` hands `preSet` the `2` and
  `onSet` the `2.0`. The docstrings stand and the code changes, and the
  tests pin both sides. Fix direction: hand `hookOnSet` the value
  as stored instead of `newValue`. Reading it back through
  `__instance_get__` would run a `Field` getter a second time, with any
  side effects it has, so having `__instance_set__` report what it stored
  may be the cleaner route; settle that while probing.
- **L11. The value an `AttriBox` holds must be an instance of its field
  type (verified, new, DECIDED, DONE ahead of the group).** Found as a
  question about `bool`:
  `AttriBox.__instance_set__` stores a value unchanged when
  `isinstance(value, fieldType)` holds, and `bool` is a subclass of
  `int`, so `foo.bar = True` on an `AttriBox[int]` stores `True` itself,
  as does an `AttriBox[int](True)` default, an `EZField[int]` and
  `typeCast(int, True)`. The same goes for an `IntEnum` member in an `int`
  field, a `str` subclass in a `str` field, and a `Child` in an
  `AttriBox[Parent]`. **DECIDED:** the rule is `isinstance(foo.bar,
  Foo.bar.fieldType)` on every read, not an exact type, so all of these
  stay as they are. Requiring the exact type would turn a `Child` into
  `Parent(child)` and end ordinary subclass use.

  A probe showed the rule already holds on every ordinary path: defaults,
  assignments needing a cast, `FixBox`, `bool`. It fails in one case, a
  field type whose constructor returns something else (`Shifty()`
  returning `42`):

  | Path | Today |
  |---|---|
  | default of `AttriBox[Shifty]()` | stores `42`, so the rule fails without a word |
  | assignment to that field | raises a bare `RecursionError` with no message |

  Both paths build the value in `AttriBox._resolve`.

  **Done:** `_resolve` checks what the field-type constructor returned,
  and raises `TypeException` naming the field, the value and the field
  type when it is not an instance of the field type. That keeps the rule
  on the default path and replaces the `RecursionError` on the set path.
  The check covers construction only, which is where a class can hand
  back something else; the deep copy of a lone default argument is left
  alone. `tests/test_desc/test_attri_box_instance_rule.py` pins both
  cases, and guards the rule across the ordinary paths, `bool` in an
  `int` field staying a `bool`, and a constructor returning an instance
  of a subclass being accepted, so no later change can tighten or loosen
  the rule by accident. Before the fix the two regression tests failed
  for the reasons in the table and the guards passed. The suite gives
  1451 passed on 3.14 with 100% line and branch coverage, and passes on
  every version from 3.7 to 3.13. A mutation check caught all three
  breaks (no check, an exact-type check, the wrong name in the
  exception) with the control passing.

  **Extended to EZField (same session, at the author's request):** a
  probe found the rule failing on all four EZData paths with such a
  field type: the default, a constructor argument, an assignment, and
  `EZField.defaultValue` all stored or returned the `42`. The root of the
  cast paths was `typeCast` itself, whose fallback returned whatever
  calling the target gave, which also sent a call through the cast pass
  of an overloaded method to the wrong overload. `typeCast` now checks
  that result and raises `TypeCastException`, which the EZData cast turns
  into `TypeException`, and the cast pass of a `Dispatcher` treats as no
  match. The EZData default recipes and `defaultValue` build their values
  through the new `EZField._construct`, which applies the same check.
  Tests: `tests/test_ezdata/test_field_instance_rule.py`,
  `tests/test_utilities/test_type_cast_instance_rule.py` and
  `tests/test_dispatch/test_cast_instance_rule.py`; the six regression
  tests failed before the change for the reasons above and the guards
  passed. The suite gives 1462 passed on 3.14 with 100% line and branch
  coverage and passes on 3.7 to 3.13, and a mutation check caught all
  seven breaks (each check removed or made exact, the wrong name in the
  exception, each call site going around `_construct`).

### Out-of-date docstrings

- **D1.** `src/worktoy/waitaminute/desc/_descriptor_exception.py`: the
  file docstring and the class docstring both list three subclasses;
  `PhantomBoxError` is a fourth, as the `waitaminute.desc` package
  docstring already says.
- **D2.** `src/worktoy/waitaminute/meta/_illegal_instantiation.py`: says
  `ValidSlice` raises it; `ValidSlice` raises plain `TypeError`.
- **D3.** `src/worktoy/mcls/_abstract_metaclass.py` (`__class_hash__`
  note): says the overload protocol expects the default hash; the
  `TypeSig` docstring says nothing depends on it.
- **D4.** `tests/test_keenum/examples/_prime_num.py` and
  `tests/test_keenum/test_http_status.py`: say `cls(2)` resolves by index;
  only `cls[2]` does.
- **D5.** Test docstrings naming things that no longer exist:
  `worktoy.markwork` (`test_base_sampler.py`), `worktoy.work_test.mixins`
  (`test_complex_mixin.py`), `Ugedag` (`test_kee.py`), `WORKTOY_DATA_DIR`
  (`test_stochastic_word.py`), `strict=True` (`test_int_sampler.py`), RGB
  as an "EZData class" (`examples/_rgb.py`, `_rgb_num.py`), and the
  "Falsy because of name" comments in `examples/_compass.py`.
- **D6 (new).** `src/worktoy/keenum/_kee_flags_space.py`: the class
  docstring says `KeeFlagsSpace` subclasses `KeeSpace`; it subclasses
  `BaseSpace`.
- **D7 (new).** `src/worktoy/mcls/__init__.py`: the package docstring
  breaks a sentence across a stray line end ("Before returning the
  created class, the" / "metaclass calls ..."), left over from an edit.

---

## Group H: Source read before 1.1.0 (open)

Files: various

On 2026-09-26 a Claude session read every file in `src/worktoy` again, in
the layer order from `src/worktoy/__init__.py`, looking for what should
be settled before 1.1.0. Each item below was reproduced with a throwaway
script on 3.14, and the repros as written here were run again on 3.9 and
3.7. The open items of group G are not repeated; the read ran into L2,
L4, L6, L7, L9, L10, D1, D2, D3, D6 and D7 independently.

The repros assume these imports:

```python
from worktoy.core.sentinels import ARGS, THIS
from worktoy.desc import AttriBox, FastBox
from worktoy.dispatch import overload, Dispatcher
from worktoy.ezdata import EZData, EZField, EZMeta, EZSpace
from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag
from worktoy.lorem_ipsum import Clause, Sentence
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast, replaceFlex
```

### Fix before 1.1.0

#### 16. A frozen EZData instance in any class body breaks class creation (high, verified)

- **Where:** `src/worktoy/core/_object.py:239-245`
  (`Object.__set_name__`), `src/worktoy/ezdata/_ez_hook.py:882-885` (the
  frozen `__setattr__`).
- **Cause:** `EZData` subclasses `Object`, so its instances define
  `__set_name__`, which Python calls on every class-body value whose type
  has one. `Object.__set_name__` assigns `__field_owner__` on the
  instance, and the frozen `__setattr__` refuses. `KeeBase.__set_name__`
  (`src/worktoy/keenum/_kee_num.py:140-144`) overrides the hook for this
  exact reason; `EZData` has no such override.
- **Repro:**
  ```python
  class RGB(EZData, frozen=True):
    r = EZField[int](0)
    g = EZField[int](0)
    b = EZField[int](0)

  class Palette:  # the same in a BaseObject or EZData body
    RED = RGB(255, 0, 0)
  # AttributeError: 'RGB' is frozen; cannot assign to attribute
  # '__field_owner__'! (wrapped in RuntimeError on 3.7 to 3.11)
  ```
- **Fix direction:** an `EZData` counterpart of `KeeBase.__set_name__`
  is the proportionate fix. Why an EZData instance is a descriptor at
  all is item 26.
- **DONE (2026-09-26), by a different route, chosen by the author.**
  Rather than an `EZData` override, `Object` now keeps its own
  bookkeeping out of reach of a subclass's `__setattr__`:
  `__set_name__`, `createContext`, `exitContext` and `getPrivateName`
  write through `object.__setattr__`. Probing showed that fixing
  `__set_name__` alone moved the crash rather than removing it: every
  read through an instance (`Palette().RED`, or `self.RED` in a method)
  runs `Object.__get__`, whose `createContext` assigned `__call_chain__`
  through the frozen guard. The rule is general, so any `Object`
  subclass with a restrictive `__setattr__` benefits, not only `EZData`.
  `exitContext` also changed from popping the stack in place to
  rebinding a shortened copy, which is equivalent here and no longer
  shortens a stack that a shallow copy of the descriptor shares. The
  cost, left for item 26: a frozen value held as a class attribute now
  carries `__field_owner__`, `__field_name__` and `__call_chain__` in its
  `__dict__`, visible in `vars()`, as non-frozen values already did.
  `Object.__init__` still assigns normally, which no frozen subclass
  reaches, since the generated `EZData.__init__` replaces it. Tests:
  `tests/test_ezdata/test_frozen_class_attribute.py`, five tests (class
  creation in a plain class, a `BaseObject` and an `EZData` body; reads
  through the class, an instance and a method; the value unchanged;
  assignment and deletion through an instance raising `ReadOnlyError`
  and `ProtectedError`, pinned until item 26 is decided). All five
  failed on the original code. The suite gives 1491 passed on 3.14 with
  100% line and branch coverage and passes on 3.7 to 3.13. Mutation
  check: reverting `__set_name__` fails all five tests and reverting
  `createContext` fails the three that read through an instance; the
  control passes. Reverting `exitContext` to `pop()` or
  `getPrivateName` to a plain assignment survives, as expected, since
  neither is reached by the frozen case: the pop never went through
  `__setattr__`, and nothing calls `getPrivateName` on an `EZData`
  value.

#### 17. Container field types wrap a single argument instead of converting it (high, verified)

- **Where:** `src/worktoy/desc/_attri_box.py:402-403` (`_resolve`).
- **Cause:** for `list`, `tuple`, `set`, `frozenset` and `dict`,
  `_resolve` calls `fieldType(args)` on the whole argument tuple. That
  is right for a tuple an assignment splatted into several arguments,
  and wrong for a single argument, which becomes the one element of the
  new container. It contradicts the class docstring, which says a
  failed cast falls back to 'T(value)' (line 167) and that
  'AttriBox[T]((a, b))' builds 'T((a, b))' (line 359). Assigning a list
  or tuple works, since `typeCast` converts containers first; only what
  `typeCast` refuses reaches `_resolve`.
- **Repro:** each row is `bar = AttriBox[T](...)` or an assignment on an
  instance of a `BaseObject` holding `bar = AttriBox[T]()`.

  | Declaration or assignment | Result | Expected |
  |---|---|---|
  | `AttriBox[list](range(3))` | `[range(0, 3)]` | `[0, 1, 2]` |
  | `AttriBox[list]((1, 2))` | `[(1, 2)]` | `[1, 2]` |
  | `AttriBox[tuple]([1, 2])` | `([1, 2],)` | `(1, 2)` |
  | `AttriBox[set]([1, 2])` | `TypeException` on the first read | `{1, 2}` |
  | `AttriBox[dict]([('a', 1)])` | `TypeException` on the first read | `{'a': 1}` |
  | `foo.bar = range(3)` on `AttriBox[list]()` | `[range(0, 3)]` | `[0, 1, 2]` |
  | `foo.bar = 'abc'` on `AttriBox[list]()` | `['abc']` | `list('abc')`, per the docstring |

- **Fix direction:** `_resolve` has to know whether its arguments came
  from a splatted tuple; a single argument that did not should go to
  `fieldType(args[0])`. Pin the one-element tuple, `foo.bar = ((1, 2),)`,
  either way in the tests.
- **DECIDED (2026-09-26):** a `str`, `bytes` or `bytearray` given to a
  container field is refused with `TypeException`, as the default or by
  assignment, rather than split into characters or integers; iterating
  text is rarely what was meant, `unpack` already treats text as atomic
  and `typeCast` already refuses it for containers. The last row of the
  table therefore expects a refusal, not `list('abc')`. The fix stays
  minimal for 1.1.0; routing single values through `typeCast` instead is
  item 30, planned for 1.2.
- **DONE (2026-09-26).** In `_resolve`, a container field type given a
  single argument converts it as a whole, `fieldType(args[0])`, and
  refuses text first; several arguments remain the elements,
  `fieldType(args)`, as `test_default_uniqueness.py` and
  `test_attri_box.py` pin. The one-element tuple question turned out to
  have an answer already: a tuple assigned to a `list`, `tuple`, `set`
  or `frozenset` field is converted by `typeCast` before `_resolve`
  runs, so `((1, 2),)` stays `[(1, 2)]`. Only a `dict` field sends an
  assigned tuple to `_resolve`, and `__instance_set__` now hands it over
  whole, as the dict's one iterable, instead of splatting it, so
  `(('c', 3),)` stays `{'c': 3}`. The containers and the text types are
  module constants in `_attri_box.py`, and the class and `_resolve`
  docstrings state the rule. `FixBox` shares the fix through
  `_resolve`; `KeeBox` has its own `_resolve`, and `FastBox` builds its
  default with `fieldType(*args)`, so neither had the bug. A side effect
  worth knowing: a non-iterable single value such as `5` for a `list`
  field is now refused, where it used to become `[5]`. Tests:
  `tests/test_desc/test_attri_box_container_argument.py`, eight tests;
  before the fix the six regression tests failed for the reasons in the
  table and the two guards (several arguments, an assigned tuple for a
  `dict`) passed. The suite gives 1486 passed on 3.14 with 100% line and
  branch coverage and passes on 3.7 to 3.13. A mutation check caught all
  four breaks, with the control passing: the single argument wrapped
  again, no text refusal, text limited to `str`, and the setter
  splatting a container tuple.

#### 18. `AttriBox[list[int]]` is not refused on 3.9 and 3.10 (medium, verified)

- **Where:** `src/worktoy/desc/_attri_box.py:543`
  (`__class_getitem__`), `src/worktoy/desc/_fast_box.py:83`.
- **Cause:** `isinstance(list[int], type)` is `True` on 3.9 and 3.10
  only, so `__class_getitem__` takes the builtin generic for a plain type.
  The class builds, and the first read raises a raw `TypeError` from
  `isinstance`. The 1.1.0 section of `changelog.md` names
  `AttriBox[list[int]]` as raising `PhantomBoxError` at class creation.
  `tests/test_desc/test_attri_box.py:217-221` spells the subscript
  `List[int]` to stay off this path, so the spelling the changelog names
  is the untested one. `PhantomBoxError._renderArg` already sorts with
  `__origin__`, which is right on every version. `FastBox` claims any
  subscript that is not a `TypeVar`, on every version.
- **Repro (3.9 or 3.10):**
  ```python
  class Foo(BaseObject):
    bar = AttriBox[list[int]]  # also with the trailing call

  Foo().bar
  # TypeError: isinstance() argument 2 cannot be a parameterized generic
  ```
- **Fix direction:** claim the subscript only for a `type` without an
  `__origin__`, and send everything else to the generic machinery as
  now. Test with `list[int]`, skipped below 3.9.
- **DONE for `AttriBox` (2026-09-26).**
  `AttriBox.__class_getitem__` now claims the subscript when
  `issubclass(type(fieldType), type)` holds, that is, when the type of
  the subscript itself is a metaclass. The `__origin__` test proposed
  above was dropped while probing: on a worktoy class, `getattr(cls,
  '__origin__', None)` goes through `AbstractMetaclass.__getattr__`, so a
  `__class_getattr__` hook answering every name makes a plain class look
  like a generic. Across 3.7 to 3.14 the new check answers exactly as
  `isinstance` did for `int`, `list`, a `BaseObject` class with such a
  hook, a `KeeNum` class, `List[int]` and a `TypeVar`, and differs only
  for `list[int]` on 3.9 and 3.10. The docstring of the method now says a
  parametrized generic goes to the generic machinery. `changelog.md:17`
  and the `PhantomBoxError` docstring now hold on every version without a
  change of text. Tests: `tests/test_desc/test_attri_box_builtin_generic.py`,
  with `list[int]` written without and with the trailing call
  (`PhantomBoxError` and `MissingVariable` at class creation, skipped
  below 3.9), and a guard for a class whose `__class_getattr__` answers
  `__origin__`. Before the fix the two regression tests failed on 3.9
  and 3.10 for the reason above, and all three passed on 3.14. The suite
  gives 1470 passed on 3.14 with 100% line and branch coverage and passes
  on 3.7 to 3.13. A mutation check on 3.10 and 3.14 caught all three
  breaks, with the control passing: back to `isinstance` (both
  regression tests, on 3.10), the `__origin__` test (the guard, on both)
  and claiming every subscript (the package fails to import).
- **DONE for the whole box family (2026-09-26, same session, at the
  author's request).** `FixBox` takes its subscript through `AttriBox`
  and needed no change. `KeeBox` accepts only an enumeration in its
  subscript and refuses a generic with `TypeException` on every version;
  even without that check the generic would reach `AttriBox`, whose
  generic machinery refuses it, since `KeeBox` is not generic itself.
  `FastBox` now settles its declaration like `AttriBox`:
  `__class_getitem__` claims only a plain class through the same check,
  sends everything else to the generic machinery wrapped in
  `_RootAlias`, and raises `TypeException` when that machinery refuses
  the subscript; `__set_name__` refuses a box without a field type with
  `MissingVariable`. Before, `FastBox[list[int]]` read back a plain `[]`
  on every version, `FastBox[List[int]]` failed on its first read, and
  `FastBox()` in a class body failed on its first read. To share
  `_RootAlias`, it moved from `_attri_box.py` to its own file,
  `src/worktoy/desc/_root_alias.py`. The `worktoy.desc` package imports
  it first, ahead of `FastBox`, keeps it out of `__all__` as a private
  name, and lists it in the package docstring under "Private, importable
  but not intended for public use", so `_fast_box.py` and
  `_attri_box.py` both take it with
  `from . import _RootAlias`, like every other sibling import in the
  package; `worktoy.desc._attri_box._RootAlias` still resolves for the
  existing tests. Tests: `FixBox` and `KeeBox`
  cases added to `tests/test_desc/test_attri_box_builtin_generic.py`,
  and `tests/test_desc/test_fast_box_builtin_generic.py` (six tests:
  `list[int]` with and without the call, `List[int]`, a bare `FastBox()`,
  two types in the subscript, and the guard). The helper that unwraps
  the `RuntimeError` of `__set_name__` moved to `DescTest`. Before the
  change the five `FastBox` refusals failed on every version and the
  guard passed. The suite gives 1478 passed on 3.14 with 100% line and
  branch coverage and passes on 3.7 to 3.13. A mutation check on 3.10
  and 3.14 caught every break of the new code, with the control
  passing: `FastBox` back to `isinstance` (on 3.10), the `__origin__`
  test (the guard), no `_RootAlias` wrapping, no `__set_name__` guard,
  no `TypeException` wrapping, and `AttriBox` back to `isinstance` (the
  `FixBox` test fails with the `AttriBox` ones, on 3.10). A break
  letting `KeeBox` accept any subscript passes these tests, for the
  reason above, and is caught by `test_bad_box` in
  `tests/test_keenum/test_kee_box.py`.
- **Addition (2026-09-28, third read):** `EZField` has the same gap, and
  accepts `EZField[list[int]]` on 3.9 and 3.10; see item 33.

#### 19. `typeCast` to `set` or `frozenset` lets a raw `TypeError` escape (medium, verified)

- **Where:** `src/worktoy/utilities/_type_cast.py:125-136`
  (`_castContainer`).
- **Cause:** the construction is not guarded, so an unhashable element
  raises Python's own `TypeError` where `typeCast` promises
  `TypeCastException`. It surfaces through an `AttriBox[set]` assignment,
  whose `__instance_set__` catches only `TypeCastException`, and through
  `EZHook.castField` (`src/worktoy/ezdata/_ez_hook.py:442-445`). The cast
  passes of a `Dispatcher` catch any `TypeError`, so dispatch is not
  affected.
- **Repro:**
  ```python
  typeCast(set, [[1], [2]])        # TypeError: unhashable type: 'list'
  typeCast(frozenset, {'a': [1]})  # the same, through the dict branch
  ```
- **Fix direction:** guard both constructions in `_castContainer` and
  raise `_exc(target, arg)` from the error.
- **DONE (2026-09-26), by the author.** `_castContainer` first refuses
  anything but a built-in container or a `dict`, then runs both
  constructions in one guarded block that raises `TypeCastException`
  from the `TypeError`. The first check is what keeps `typeCast(list,
  'abc')` refused, and with it the text refusal of item 17 on the
  assignment path: a version of the edit without it split text again,
  which the item 17 test caught at once. Tests:
  `tests/test_utilities/test_type_cast_unhashable.py`,
  `tests/test_desc/test_attri_box_unhashable_set.py` and
  `tests/test_ezdata/test_field_unhashable_set.py`. A `dict` refused by
  the cast for an `AttriBox[frozenset]` falls back to the constructor,
  which builds a set of the keys; that lenient fallback is item 30, so
  the `AttriBox` test uses an unhashable tuple instead. The suite gives
  1499 passed on 3.14 with 100% line and branch coverage and passes on
  3.7 to 3.13. A mutation check caught all four breaks, with the control
  passing: no guard, the `dict` branch unguarded, no container check
  (the item 17 test), and `dict` left out of the check (the existing
  `test_extra_type_cast.py` cases).

#### 20. `KeeMeta.valueType` is the type of the first member's value (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:204-219`.
- **Cause:** the getter returns `type(member.value)` of the first member
  and requires every other value to be an instance of it. `KeeSpace`
  pins the declared `Kee[T]` type instead, which `member.valueType`
  (`src/worktoy/keenum/_kee_num.py:99-101`) still holds. Values that are
  instances of different subclasses of `T`, mixed values under
  `Kee[object]`, and a `bool` first in an `int` enumeration (L11 keeps a
  `bool` a `bool`) all pass class creation, then break every lookup that
  reaches the value step, even one that should simply miss.
  `KeeBox._resolveNum` reads the same getter.
- **Repro:**
  ```python
  class Animal: pass
  class Dog(Animal): pass

  class Pets(KeeNum):
    DOG = Kee[Animal](Dog())
    GENERIC = Kee[Animal](Animal())

  Pets(Pets.GENERIC.value)  # TypeException: ... instance of 'Dog'

  class Mixed(KeeNum):
    ONE = Kee[object](1)
    TWO = Kee[object]('two')

  Mixed(1)  # TypeException: ... instance of 'int', received 'two'

  class Bits(KeeNum):
    ON = Kee[int](True)
    TWO = Kee[int](2)

  Bits(2)  # TypeException: ... instance of 'bool'
  ```
- **Fix direction:** return the declared type of the members.
- **DONE (2026-09-29).** The getter returns the declared type, the
  `__member_type__` that `KeeSpace` pins for every member, and still
  confirms that each value is an instance of it, raising
  `TypeException` otherwise, which keeps the two tests that tamper with a
  member value after class creation meaningful. An enumeration without
  members raises `TypeError` as before, now before the members are
  looked at. `KeeBox` reads the same getter, so it resolves a value of
  the declared type too. One consequence, pinned: an enumeration with a
  `bool` value among `int` values is an `int` enumeration, so the rule
  that no `bool` resolves an `int` enumeration by value now applies to
  it: `Bits(True)` raises `KeeResolveError` where it used to find the
  member whose value is `True`, while `Bits(1)`, `Bits('on')` and
  `Bits[0]` find it. Test: `tests/test_keenum/test_kee_value_type_declared.py`
  (seven tests); the six repro tests failed before the change. The suite
  gives 1603 passed on 3.14 with 100% line and branch coverage and passes
  on 3.7 to 3.13. A mutation check caught all four breaks (the type of
  the first value, no instance check, an exact-type check, no check for
  an empty enumeration) with the control passing.

#### 21. `@overload(ARGS[THIS])` stops matching past five arguments (medium, verified)

- **Where:** `src/worktoy/dispatch/_type_sig.py:279-296` (`swapTHIS`),
  `src/worktoy/dispatch/_overload.py:180-198` (`_addSigFunc`).
- **Cause:** `_addSigFunc` expands a variadic declaration into concrete
  signatures for zero to five trailing arguments and keeps the variadic
  entry for longer calls. `swapTHIS` replaces raw types that are `THIS`,
  which reaches the expansions, but the raw type of the variadic entry is
  the `ARGS` instance, whose `__inner_type__` stays the sentinel.
- **Repro:**
  ```python
  class Node(BaseObject):
    @overload(ARGS[THIS])
    def link(self, *others):
      return len(others)

  n = Node()
  n.link(*[Node() for _ in range(5)])  # 5
  n.link(*[Node() for _ in range(7)])  # DispatchException
  ```
- **Fix direction:** let `swapTHIS` rebuild a trailing `ARGS[THIS]` as
  `ARGS[thisType]`. `ARGS` compares by inner type, so the rebuilt entry
  still equals the one an override declares.
- **See also item 55 (2026-09-29):** the expansion this item runs into
  is the subject of item 55, whose redesign would fix this item on the
  way.
- **DONE (2026-09-29).** `TypeSig.swapTHIS` rebuilds a raw type
  `ARGS[THIS]` as `ARGS` of the class and leaves an `ARGS` of any other
  type as it was, so the variadic entry names the class and matches
  calls of any length, before or after a fixed prefix, instances of
  subclasses included. With the class as its inner type, a long call now
  also goes through the cast pass as a short call already did, which
  builds the class from an argument when its constructor accepts one.
  Test: `tests/test_overload/test_args_this_variadic.py` (seven tests,
  its fixture taking no constructor arguments so that no foreign value
  casts); five failed before the change and the two guards passed. The
  suite gives 1614 passed on 3.14 with 100% line and branch coverage and
  passes on 3.7 to 3.13. A mutation check caught both breaks (no
  rebuild, every `ARGS` rebuilt) with the control passing.

#### 22. A subclass of `EZSpace` drops the fields of bases built with `EZSpace` (medium, verified)

- **Where:** `src/worktoy/ezdata/_ez_space.py:236-240`.
- **Cause:** a base's namespace counts only when
  `isinstance(space, cls)` holds with `cls = type(self)`, so a namespace
  subclass sees only bases built with that same subclass. The
  `worktoy.ezdata` package docstring exposes `EZMeta`, `EZSpace` and
  `EZHook` "for users building their own auto-generating bases".
- **Repro:**
  ```python
  class Point(EZData):
    x = EZField[int](0)
    y = EZField[int](0)

  class MySpace(EZSpace):
    pass

  class MyMeta(EZMeta):
    @classmethod
    def __prepare__(mcls, name, bases, **kw):
      return MySpace(mcls, name, bases, **kw)

  class Point3(Point, metaclass=MyMeta):
    z = EZField[int](0)

  [f.fieldName for f in Point3.fields]  # ['z'], not ['x', 'y', 'z']
  ```
- **Fix direction:** test against `EZSpace`.
- **DONE (2026-09-26), by the author:** `EZSpace.__init__` tests
  `isinstance(space, EZSpace)`. Testing against `BaseSpace` was
  considered and refused: every worktoy class has a `BaseSpace`, so an
  `EZData` class mixing in a plain `BaseObject` class then failed at
  creation with `'BaseSpace' object has no attribute 'getEZFields'`.
  `AbstractMetaclass.getNamespaceClass` does not help either, since it
  answers which namespace a metaclass uses, not whether a base is an
  `EZData` class. Tests: `tests/test_ezdata/test_space_subclass_fields.py`;
  the old `type(self)` check fails the inheritance test and the
  `BaseSpace` check fails the mixin guard. The suite gives 1493 passed
  on 3.14 with 100% line and branch coverage and passes on 3.7 to 3.13.
  The same session's type-hint edits across `mcls` change no behaviour.

#### 23. An owner's `__getattr__` hijacks the `AttriBox` and `KeeBox` defaults (medium, verified)

- **Where:** `src/worktoy/desc/_attri_box.py:430-442`,
  `src/worktoy/keenum/_kee_box.py:83-95`.
- **Cause:** both read the storage with `getattr(instance, pvtName)` and
  take an `AttributeError` to mean the default is not built yet. An owner
  whose `__getattr__` answers every name never raises, so the default is
  never built and the read returns whatever `__getattr__` gave.
  `FixBox.__instance_set__` already reads with `object.__getattribute__`
  (`src/worktoy/desc/_fix_box.py:47`).
- **Repro:**
  ```python
  class Foo(BaseObject):
    bar = AttriBox[int](7)

    def __getattr__(self, key):
      return 'junk'

  Foo().bar  # 'junk'
  ```
- **Fix direction:** read with `object.__getattribute__`, as `FixBox`
  does.
- **DONE (2026-09-26).** `AttriBox.__instance_get__` and
  `KeeBox.__instance_get__` read their storage with
  `object.__getattribute__`, each with a one-line comment saying why.
  `FixBox` inherits the read from `AttriBox`, and `FastBox` reads
  `instance.__dict__` directly, so neither needed a change. Tests:
  `tests/test_desc/test_box_owner_getattr.py`, with an owner whose
  `__getattr__` answers every name holding an `AttriBox`, a `FixBox`
  and a `KeeBox`; the three box tests read back `'junk'` before the fix.
  The suite gives 1503 passed on 3.14 with 100% line and branch coverage
  and passes on 3.7 to 3.13. A mutation check caught both breaks, with
  the control passing: `AttriBox` back to `getattr` fails the `AttriBox`
  and `FixBox` tests, `KeeBox` back to `getattr` fails the `KeeBox` test.

#### 24. `KeeFlags` recognises its root by name (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_flags_meta.py:110-113`,
  `src/worktoy/keenum/_kee_flags_space.py:100` and `:141`.
- **Cause:** the root is the class named `'KeeFlags'`. A user class of
  that name is taken for the root: it builds no members, and
  `setattr(mcls, '__kee_class__', cls)` replaces the real root for every
  flag class built afterwards, which drives the write guard on members,
  `__subclasscheck__` and the choice of `_getValue`. Item 11 settled
  root by identity for `KeeNum`.
- **Repro:**
  ```python
  import worktoy.keenum as kn

  class KeeFlags(kn.KeeFlags):
    READ = KeeFlag()
    WRITE = KeeFlag()

  type(KeeFlags).__kee_class__ is kn.KeeFlags  # False from here on
  len(KeeFlags)  # MissingVariable: Missing 'KeeFlagsMeta.memberList'!
  ```
- **Fix direction:** recognise the root by identity, for instance as the
  class built while `__kee_class__` is still unset, or through a `_root`
  class keyword as `KeeMetaMeta` passes for `KeeNum`.
- **DONE (2026-09-29).** The root is declared
  `class KeeFlags(NoPickle, metaclass=KeeFlagsMeta, _root=True)`, and the
  three places that compared the name ask for the keyword instead:
  `KeeFlagsMeta.__new__`, which pops it so it goes no further,
  `KeeFlagsSpace.__init__` and `KeeFlagsSpace.postCompile`. A user class
  named `KeeFlags` is an ordinary flags class: it builds its members,
  inherits the flags of its parent, and leaves the real root in place for
  every class built after it. Test:
  `tests/test_keenum/test_kee_flags_root_identity.py` (four tests,
  building their classes inside the test methods, since a failure used
  to replace the root for the whole process). The suite gives 1607
  passed on 3.14 with 100% line and branch coverage and passes on 3.7 to
  3.13. A mutation check caught all three breaks, each name comparison
  put back, with the control passing; the first run let the one in
  `KeeFlagsSpace.__init__` survive, since no test derived a class named
  `KeeFlags` from a parent with flags, and the fourth test covers that.

### Decisions needed

#### 25. EZData replaces a class-body `__init__`, `__eq__` and others without a word (verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:327-353`,
  `src/worktoy/ezdata/_ez_space.py:67-69`.
- **Cause:** `postCompilePhase` sets `__init__`, `__iter__`, `__eq__`,
  `__delattr__`, `__hash__`, `__lt__`, `__le__`, `__gt__` and `__ge__`
  after the class body is merged, so a definition of the same name in the
  body is dropped. Only `__setattr__` is refused (`ReservedMethodError`,
  item 8). `dataclasses` keeps a method the class defines itself.
- **Repro:**
  ```python
  class Tagged(EZData):
    x = EZField[int](0)

    def __init__(self, *args, **kwargs):
      raise RuntimeError('never runs')

    def __eq__(self, other):
      return 'never runs'

  t = Tagged(1)  # no error
  t == t         # True
  ```
- **Options:** refuse each of them with `ReservedMethodError`, as
  `__setattr__` is, or keep a class-body definition in place of the
  generated one.
- **DECIDED (2026-09-29):** refuse every method EZData silently
  replaced. A split was proposed, refusing the three that carry the
  guarantees and letting the body win for equality, hashing and
  ordering; the author chose to refuse all of them.
- **DONE (2026-09-29).** `EZSpace.__reserved_ez_methods__` now lists
  `__init__`, `__iter__`, `__eq__`, `__hash__`, `__lt__`, `__le__`,
  `__gt__`, `__ge__`, `__setattr__` and `__delattr__`, which
  `EZHook.setItemPhase` refuses at the offending line with
  `ReservedMethodError`, naming the method and pointing to
  `__post_init__`. The docstrings of `EZSpace`, `EZData` and
  `ReservedMethodError` list them. `__repr__`, `__str__`,
  `__field_pairs__`, `asDict`, `asTuple` and `replace` may still be
  defined in the class body. No existing EZData class defined any of the
  refused names. Test:
  `tests/test_ezdata/test_reserved_generated_methods.py` (three tests:
  each name refused, a class statement refused, the open helpers kept);
  the first two failed before the change. The suite gives 1617 passed on
  3.14 with 100% line and branch coverage and passes on 3.7 to 3.13. A
  mutation check removed each of the nine new names in turn, and the
  tests caught all nine, with the control passing.

#### 26. Worktoy values as class attributes are read-only descriptors, and are not EZData fields (verified, DECISION)

- **Where:** `src/worktoy/core/_object.py:326-334`
  (`Object.__instance_set__`), `src/worktoy/keenum/_kee_num.py:151-153`
  (`KeeBase.__set__`), `src/worktoy/ezdata/_ez_hook.py:164-171` (the
  descriptor test in `EZHook.setItemPhase`).
- **Cause:** `BaseObject`, `EZData` and `KeeBase` derive from `Object`,
  so every instance, enumeration members included, defines `__get__`,
  `__set__`, `__delete__` and `__set_name__`. Placed in a class body as
  a default, such a value is a data descriptor there: assigning the
  attribute on an instance raises `ReadOnlyError` instead of shadowing
  the default, and `__set_name__` writes the owner onto the shared value.
  The message names the field `None` for a member, since
  `KeeBase.__set_name__` records nothing. The same descriptor test makes
  `EZHook` leave such a value in an EZData body as a class attribute
  rather than a field. Item 16 is the frozen case of the same root.
- **Repro:**
  ```python
  class Color(KeeNum):
    RED = Kee[str]('red')
    BLUE = Kee[str]('blue')

  class Point(EZData):
    x = EZField[int](0)
    y = EZField[int](0)

  class Car:
    color = Color.RED

  Car().color = Color.BLUE
  # ReadOnlyError: ... read-only attribute 'Car.None' ...

  class Holder:
    origin = Point(0, 0)  # any EZData or BaseObject instance

  Holder().origin = Point(1, 1)  # ReadOnlyError

  class CarData(EZData):
    color = Color.RED  # not a field
    wheels = 4         # a field

  CarData(Color.BLUE, 3)  # ExtraPositionalException: 1 fields, 2 given
  ```
- **Options:** likely 1.2 scope. Keep it and document that worktoy
  values are descriptors; or stop deriving the value classes (`EZData`,
  `KeeBase`, perhaps `BaseObject`) from the descriptor base; or at least
  have `EZHook` take instances of those classes as field values.
- **Split (2026-09-29):** the item has two halves. The EZData half, a
  worktoy value in an EZData body left out of the fields, is decided and
  done below. The other half, a worktoy value as a class-level default
  in any class being a read-only descriptor, moved to item 56, planned
  for 1.2.
- **DECIDED (2026-09-29):** EZData does not require `EZField`: a bare
  value becomes a field. The author set the rule for telling a
  descriptor from a value: a value not deriving from `Object` is a
  descriptor when its type implements `__get__` or `__set__`; an
  `Object` is one when its type overrides `__instance_get__` or
  `__instance_set__`. Everything else becomes a field.
- **DONE (2026-09-29).** `EZHook._isDescriptor` implements the rule and
  replaced the old test for `__get__`, `__set__`, `__delete__` or
  `__set_name__`. Members, EZData instances and `SymbolicName` in a
  class body now become fields, while `Field`, the boxes, `property` and
  plain descriptors stay class attributes. Such a field was built as
  `type(value)(value)`, which is no copy for every type: an EZData value
  failed on every construction and a `SymbolicName` nested itself, also
  for an explicit `EZField[Point](Point(1, 2))`. `EZField._construct`
  therefore copies a lone argument, without keywords, that is already
  of the field type (`copy.copy`); builtins come out as before, a member
  copies to itself, and a `bool` given to an `int` field now stays a
  `bool`, as L11 decided. Known edge, recorded rather than handled:
  `Alias` and `Dispatcher` override `__get__` rather than
  `__instance_get__`, so one placed by hand in an EZData body would now
  become a field. The item 16 test pinning a frozen instance in an
  EZData body as a class attribute now pins it as a field. Test:
  `tests/test_ezdata/test_worktoy_value_fields.py` (eight tests). The
  suite gives 1625 passed on 3.14 with 100% line and branch coverage and
  passes on 3.7 to 3.13. A mutation check caught all seven breaks (every
  `Object` a descriptor, each side of either test dropped, no copy, a
  copy of any lone argument) with the control passing; the first run let
  the three one-sided breaks survive, and the last test covers them.

#### 56. Worktoy values are read-only descriptors as class-level defaults (verified, planned for 1.2)

- **Where:** `src/worktoy/core/_object.py` (`Object.__set__`,
  `__instance_set__`), `src/worktoy/keenum/_kee_num.py:151-153`
  (`KeeBase.__set__`).
- **Cause:** split off item 26 on 2026-09-29. `EZData`, `KeeBase` and
  `BaseObject` derive from `Object`, the descriptor base, so their
  instances, enumeration members included, are data descriptors. As a
  class-level default in any class they refuse assignment on the
  instances, and the message names the field `None` for a member.
- **Repro:**
  ```python
  class Car:
    color = Color.RED

  Car().color = Color.BLUE
  # ReadOnlyError: ... read-only attribute 'Car.None' ...
  ```
- **Direction:** the value classes stop deriving from the descriptor
  base, a redesign planned for 1.2.

#### 27. The lorem generators ignore keyword arguments (verified, DECISION)

- **Where:** `src/worktoy/lorem_ipsum/_base_generator.py:86-88`.
- **Cause:** the `@overload()` constructor of `BaseGenerator` accepts
  `**kwargs` and discards them, so a keyword meant for `charCount`, or a
  misspelled one, is dropped without a word.
- **Repro:**
  ```python
  Clause(charCount=30).charCount  # 40
  Sentence(chars=30).charCount    # 40
  ```
- **Options:** honour `charCount=` and refuse any other keyword, or
  refuse keywords altogether.
- **DECIDED (2026-09-29):** honour the keyword. `Clause(charCount=30)`,
  `Sentence(charCount=30)` and `Paragraph(charCount=30)` build with 30
  characters, and any other keyword, a misspelling such as `chars=`
  included, is refused rather than dropped. The positional form
  `Clause(30)` stays. Still open for the implementation: the exception
  for an unknown keyword, a plain `TypeError` as Python raises or a
  worktoy one. Proposed for 1.1.0, tests first.
- **DONE (2026-09-29).** The author chose Python's own `TypeError`. The
  keyword-free overload of `BaseGenerator` declares `charCount` as its
  only keyword, `def __init__(self, *, charCount: int = None)`, and
  assigns it when given, so Python refuses any other keyword with the
  same error the positional form already raised ("got an unexpected
  keyword argument"), and no new exception was needed. A call without
  positional arguments reaches that overload whatever keywords it
  carries, since the `Dispatcher` matches positional arguments only, so
  `Clause()` and `Clause(charCount=30)` cover both branches. A value
  given by keyword is cast the way an assignment to `charCount` is,
  `30.0` giving `30` and `2.5` raising `TypeException`, and zero is
  honoured. `first` hands its keywords on, so it follows. Found on the
  way: the copy constructor of `Clause` took `**kwargs` and dropped them,
  where those of `Sentence` and `Paragraph` refuse keywords; it now takes
  none. The `BaseGenerator` class docstring states the rule. Test:
  `tests/test_lorem_ipsum/test_generator_keywords.py` (eight tests); the
  six regression tests failed before the change and the two guards (no
  arguments, and the positional form refusing keywords) passed. The
  suite gives 1633 passed on 3.14 with 100% line and branch coverage and
  passes on 3.7 to 3.13. A mutation check caught all six breaks, each by
  the test written for it, with the control passing: the old overload
  back, `if charCount:` for the `None` test, other keywords dropped beside
  `charCount`, `**kwargs` back on the `Clause` copy constructor, `**kwargs`
  on the positional overload, and `int(charCount)` in place of the cast
  through the box.

#### 28. A flag named `NULL` collides with the empty member (verified, DECISION)

- **Where:** `src/worktoy/keenum/_kee_flags_space.py:77-78`,
  `src/worktoy/keenum/_kee_flags.py:184-186`.
- **Cause:** the member with no flag high is named `'NULL'`, and so is
  the member whose only high flag is `NULL`. `KeeFlagsMeta.__new__` binds
  both to the class attribute `NULL`, the later one winning, while name
  lookup returns the first.
- **Repro:**
  ```python
  class Odd(KeeFlags):
    NULL = KeeFlag()
    ONE = KeeFlag()

  Odd.NULL.index         # 1, the flag member
  Odd['NULL'] is Odd(0)  # True, the empty member
  bool(Odd.NULL)         # True
  ```
- **Options:** refuse `NULL` as a flag name next to the `'_'` check,
  perhaps together with L7.

#### 29. `@overload` stacked on `@overload.flex` or `@overload.fallback` fails late (verified, DECISION)

- **Where:** `src/worktoy/dispatch/_overload.py:205-217`
  (`_extendLatest`) and `:244-252`.
- **Cause:** a stacked `@overload(...)` registers its signature on the
  latest function of the overload beneath it. Under `flex` that is a
  single `PermuterMethod` whose arrangement expects the flex arity, so a
  call through the new signature fails in `restoreFrom`. Under a
  fallback-only overload there is no latest function, and the class body
  raises a bare `RuntimeError`.
- **Repro:**
  ```python
  class Foo(BaseObject):
    @overload(float)
    @overload.flex(int, str)
    def bar(self, *args):
      return args

  Foo().bar(1.0)
  # ValueError: 'restoreFrom' received '1' values but arrangement has
  # length '2'

  class Baz(BaseObject):
    @overload(int)
    @overload.fallback
    def bar(self, *args):
      return args
  # RuntimeError: no function has been registered on this 'overload' yet
  ```
- **Options:** support the stacking by registering the function the
  inner overload wraps, or refuse it at the decorator with a message
  naming both decorators.
- **Addition (2026-09-28, third read):** the other order fails too, at
  class creation, but with messages that name neither decorator.
  `@overload.fallback` or `@overload.finalize` above `@overload(int)`
  raises `TypeException` for `'__fallback_func__'` or
  `'__finalizer_func__'`, which expected a 'function' or 'method' and
  received the `overload`, and `@overload.flex(...)` above
  `@overload(...)` raises it for `'arg'`, which expected an
  'Arrangement' or 'function'. The decision should cover both orders.

### Planned for 1.2

#### 30. `AttriBox` converts through its own constructor fallback instead of `typeCast` (verified, DECIDED for 1.2)

- **Where:** `src/worktoy/desc/_attri_box.py` (`__instance_set__` and
  `_resolve`).
- **Cause:** an assignment tries `typeCast` with instantiation switched
  off and, when the cast refuses, falls back to calling the field type
  in `_resolve`; a declared default never reaches `typeCast` at all.
  `EZData` sends every assignment through `typeCast` alone, so the two
  disagree, and `AttriBox` accepts values the cast refuses:

  | Value | `typeCast` | `EZField` assigned | `AttriBox` assigned | `AttriBox` default |
  |---|---|---|---|---|
  | `5` into `str` | refuses | refuses | `'5'` | `'5'` |
  | `2.5` into `int` | refuses | refuses | refuses | `2` |

- **Decision:** found while deciding item 17, which the author chose to
  fix minimally for 1.1.0. For 1.2, `_resolve` sends a single value
  through `typeCast`, as `EZData` does, and keeps its own code only for
  what `typeCast` cannot express: several arguments, keyword arguments,
  and copying a default that is already of the field type. This is a
  compatibility change for the changelog: `foo.name = 5` on an
  `AttriBox[str]`, `AttriBox[int](2.5)` and a `range` for a `list`
  field are then refused.
- **Addition (2026-09-28, third read):** the assignment path already
  lets one value through that the cast refuses. A tuple skips the
  authoritative numeric cast and goes to the constructor, which is meant
  for several components (`foo.bar = 69, 420` on an `AttriBox[complex]`),
  but a one-element tuple then rounds without a word: on an
  `AttriBox[int]`, `foo.bar = 2.5` raises `TypeException` while
  `foo.bar = (2.5,)` stores `2` (`src/worktoy/desc/_attri_box.py:387-395`).

### Low severity

- **L12. `Dispatcher.overload` by hand ignores `ARGS` (verified).**
  `src/worktoy/dispatch/_dispatcher.py:659-661` registers every signature
  through `addSigFunc`, so `ARGS[int]` becomes one concrete entry. A call
  of the same length reaches `isinstance(arg, ARGS[int])` in the
  isinstance pass (`:248-249`) and raises a raw `TypeError`; longer calls
  raise `DispatchException`. `overload._addSigFunc` shows the variadic
  route.
  ```python
  class Hand:
    bar = Dispatcher()

    @bar.overload(int, ARGS[int])
    def bar(self, *args):
      return args

  Hand().bar(1, 2)  # TypeError: isinstance() arg 2 must be a type ...
  ```
- **L13. `_strictMRO=False` crashes (verified).**
  `src/worktoy/mcls/_abstract_namespace.py:219-228` leaves
  `__class_mro__` unset for inconsistent bases, and `getMROSpace`
  (`:163`) iterates it, so a class statement fails with `TypeError:
  'NoneType' object is not iterable` from `NamespaceHook.preCompilePhase`.
  `BaseSpace._getLookupOrder` handles `None`; `getMROSpace` does not. The
  tests build the namespace directly and never reach a class statement,
  where `type.__new__` refuses the order anyway. Either drop the keyword
  or document it as a namespace-only option. Repro: `class C(A, B,
  _strictMRO=False)` with `A(BaseObject)` and `B(A)`.
- **L14. `len` and `in` refuse an EZData class that iterates
  (verified).** `EZMeta` defines `__iter__`
  (`src/worktoy/ezdata/_ez_meta.py:161-170`), but
  `AbstractMetaclass.__len__` and `__contains__`
  (`src/worktoy/mcls/_abstract_metaclass.py:240-259`) only consult
  `__class_iter__`: `list(Point)` works, `len(Point)` raises "has no
  len()" and `Point.fields[0] in Point` raises "is not iterable".
- **L15. Tracebacks on 3.12 and later suggest a name for three
  exceptions (verified).** `DuplicateError`, `ReservedFieldError` and
  `ReservedMethodError` subclass `AttributeError` and keep a slot named
  `name`. From 3.12 the `traceback` module reads `name` off any
  `AttributeError` and appends the closest name in `dir(obj)`, with
  `obj` unset, so an EZData body defining `__setattr__` ends its
  traceback with "Did you mean: '__delattr__'?". Fix direction: rename
  the slot.
- **L16. `FastBox` resets on delete (verified).**
  `src/worktoy/desc/_fast_box.py:113-139`: after `del foo.bar` the next
  read builds a fresh default, where every other box raises
  `MissingVariable` until the next assignment. Document it, or follow
  the other boxes. Note (2026-09-26): `test_delete_resets_to_default` in
  `tests/test_desc/test_fast_box.py` pins the reset as intended, so this
  is a deliberate choice that only the `FastBox` docstring leaves
  unsaid.
- **L17. `replaceFlex` with `n` below one (verified).**
  `src/worktoy/utilities/_replace_flex.py:40-46`:
  `replaceFlex('abc', 'b', 'X', 0)` returns `'abXabc'`. Guard `n < 1`.
- **L18. `skipTest` inside a sub-test block fails the test (verified).**
  `src/worktoy/work_test/_sub_test.py:217-230` records the `SkipTest`
  that `self.skipTest()` raises inside `with self.subTest(...)` as an
  error, and `BaseTest.tearDown` then fails the test: one failure, no
  skip. Let `unittest.SkipTest` propagate.
- **L19. The root of a custom `KeeMeta` never runs its `__init__` (read,
  not verified).** `src/worktoy/keenum/_kee_meta_meta.py:104-108` builds
  the root through `mcls.__new__` alone, so the `__init__` of a `KeeMeta`
  subclass never runs for its root, although the `KeeMetaMeta` docstring
  says the root carries every customization of the subclass.
  **Addition (2026-09-28, third read, read only):** the root's namespace
  is a `KeeSpace` built directly (`:104`), not through
  `mcls.__prepare__`, so a subclass that brings its own namespace class
  does not get it for its root either.

### Out-of-date docstrings

- **D8.** `src/worktoy/core/_meta_type.py:19-22`: says every worktoy
  metaclass subclasses `MetaType` and has it as its metaclass;
  `SentinelMeta`, `MetaFlow` and `_MetaSlice` subclass `type`.
- **D9.** `src/worktoy/keenum/_kee_box.py:51-53`: says `KeeBox` never
  instantiates the value type; `_resolveNum` does (`:156`), to compare
  the result with the member values. **DONE with item 44:** the class
  docstring lists that step, which the fix of item 44 relies on.
- **D10.** `src/worktoy/keenum/_kee_member.py:30-31` and `:91`,
  `src/worktoy/keenum/_kee_flag.py:40-41`: say the member or flag name
  comes from `__set_name__`; `KeeSpace.addNum` and
  `KeeFlagsSpace.addKeeFlag` set it, and both `__set_name__` methods are
  reached only by misuse.
- **D11.** `src/worktoy/keenum/_kee_meta_meta.py:26`: calls `KeeMeta`
  "the only metaclass the library ships"; `KeeFlagsMeta` ships too.
- **D12.** `src/worktoy/waitaminute/meta/_hook_exception.py:25-28`: shows
  `raise HookException(...) from exception`;
  `AbstractNamespace.__getitem__`
  (`src/worktoy/mcls/_abstract_namespace.py:258`) raises without `from`.
- **D13.** `src/worktoy/waitaminute/ezdata/_kw_only_exception.py:29`: the
  message names `kw_only=True`; the docstrings and `EZHook` lead with
  `kwOnly`.
- **D14.** `src/worktoy/waitaminute/_missing_variable.py:37-57`: the
  example uses `typing.Callable`, which has no `__name__` on 3.7 to 3.9,
  so the example's `print(missingVariable)` raises `AttributeError`
  there.

---

## Group I: Third source read before 1.1.0 (open)

Files: various

On 2026-09-28 a Claude session read every file in `src/worktoy` a third
time, in the layer order from `src/worktoy/__init__.py`, looking for what
the earlier reads and the suite had missed. The read ran into most open
items of groups G and H independently; they are not repeated here. Each
item below was reproduced with a throwaway script on 3.14, and on the
other versions its text names. At the time the suite gave 1503 passed on
3.14 with 100% line and branch coverage, and it catches none of these
items. The read also added to items 18, 29, 30, L2 and L19; each addition
is marked at its item.

The repros assume these imports and helpers:

```python
import copy
import traceback

from worktoy.core.sentinels import ARGS, OWNER, Sentinel
from worktoy.desc import AttriBox, FastBox, FixBox, SymbolicName
from worktoy.dispatch import overload
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag, KeeBox
from worktoy.mcls import BaseObject, BaseMeta
from worktoy.utilities import typeCast


class AlwaysEqual:
  def __eq__(self, other):
    return True

  __hash__ = object.__hash__


class RaisingEqual:  # like the RGB fixture, reads the other operand
  def __eq__(self, other):
    return other.r == 1

  __hash__ = object.__hash__


class Perm(KeeFlags):
  READ = KeeFlag()
  WRITE = KeeFlag()
```

### Fix before 1.1.0

#### 31. `KeeMeta.__instancecheck__` lets the value's own `__eq__` decide membership (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:392-402`
  (`__instancecheck__`), reached from `__contains__` (`:380-390`) and
  from the first step of `_resolveMember` (`:547-548`).
- **Cause:** `__instancecheck__` compares `member == instance` for every
  member. `KeeBase.__eq__` answers `NotImplemented` for a value of
  another type, so Python asks the value's own `__eq__`, which may answer
  anything or raise. Group C met this in `KeeBox` and filtered there
  (`KeeBox._isMember`); the metaclass itself still asks. For a real
  member `==` adds nothing to `is`, since `KeeBase.__eq__` is identity.
- **Repro:**
  ```python
  class Color(KeeNum):
    RED = Kee[str]('red')
    BLUE = Kee[str]('blue')

  anyEq = AlwaysEqual()
  isinstance(anyEq, Color)  # True
  anyEq in Color            # True
  Color(anyEq) is anyEq     # True: the foreign object comes back as a
                            # member
  isinstance(RaisingEqual(), Color)
  # AttributeError: 'Color' object has no attribute 'r'
  ```
- **Fix direction:** compare with `member is instance`, and keep the
  subclass branch. The class docstring ("True when 'x' equals any
  member") and the docstring of the method say "equals" and change with
  it.
- **DONE (2026-09-28).** `KeeMeta.__instancecheck__` recognises a member
  with `is` and keeps the subclass branch; its docstring and the class
  docstring say "is one of the members" in place of "equals".
  `KeeBox._isMember` is a plain `isinstance` again, since the group C
  pre-filter only worked around this item. Folded in at the author's
  request is the `KeeFlags` counterpart, found while writing the tests:
  `KeeFlagsMeta._resolveValue` compared every member value with any
  identifier, so `FileAccess(ANY)` returned `FileAccess.NULL`,
  `ANY in FileAccess` was `True`, and `FileAccess(RGB(1, 2, 3))` raised
  `AttributeError`. It now compares a value only with member values of a
  type the value is an instance of, and otherwise raises the `ValueError`
  a miss raised before (see [Decisions](#decisions)). As a consequence
  `FlagsExample(3.0)` raises where it found the member whose value is
  `3`. Tests: `tests/test_keenum/test_kee_membership.py`, eight tests,
  and `tests/test_keenum/test_kee_flags_foreign_value.py`, seven. Before
  the fix, the five regression tests of the first file failed on 3.14,
  3.10 and 3.7 for the reasons above, and so did the four of the second,
  while the guards passed: the members, the members an enumeration
  shares with those derived from it, a foreign member, a value, and a
  lookup by a value of the right type. Two lines had kept their coverage
  only through the old comparisons, `KeeFlags.__eq__` declining a
  non-member and the `NotImplemented` branch of the `PlanetData`
  fixture; `test_member_is_not_its_value` and `test_class_resolve_miss`
  in `test_kee_meta_resolve.py` now reach them directly. The suite gives
  1519 passed on 3.14 with 100% line and branch coverage and passes on
  3.7 to 3.13. A mutation check applied seven breaks, each on its own
  copy of `src`, with an unmodified copy passing as the control, and
  caught six at once: `==` for `is`, no subclass branch, no identity
  loop, `_isMember` always false, no type guard in `_resolveValue`, and
  the guard inverted. Going back to `==` also fails the group C test
  `test_value_is_not_compared_as_member`, which now guards this item as
  well. The seventh, requiring exactly the type of the member value,
  survived until `test_value_of_subclass_resolves` pinned that a value of
  a subclass counts, as it does for a `KeeNum`.

#### 32. `DelException`, `QuestionableSyntax` and `UnboundClassHook` render without their message (medium, verified)

- **Where:** `src/worktoy/waitaminute/meta/_del_exception.py:36`,
  `_questionable_syntax.py:33`, `_unbound_class_hook.py:36`.
- **Cause:** the three subclass `SyntaxError` and call its `__init__`
  with no arguments, so `msg` stays `None`. For a `SyntaxError` the
  `traceback` module prints `msg` rather than `str()`, and falls back to
  `<no detail available>`. `traceback.format_exception_only`, which
  pytest uses, does so on every version (checked on 3.7, 3.10, 3.12 and
  3.14). The default `sys.excepthook` goes through the `traceback` module
  from 3.13 on, while the C printer of 3.12 and earlier still shows
  `str()`. Each of them explains a mistake in a class body, so losing
  the message loses the explanation.
- **Repro:**
  ```python
  exc = QuestionableSyntax('__setitem__', '__set_item__')
  str(exc)  # "Received name '__set_item__' which is similar enough ..."
  traceback.format_exception_only(type(exc), exc)[-1]
  # '...QuestionableSyntax: <no detail available>\n'

  class Bad(BaseObject):  # uncaught, in a script
    __set_item__ = 1
  # 3.12: ...QuestionableSyntax: Received name '__set_item__' ...
  # 3.13 and 3.14: ...QuestionableSyntax: <no detail available>
  ```
- **Fix direction:** hand the rendered message to `SyntaxError.__init__`,
  so that `msg` holds it. That gives the exceptions an `args`, so settle
  it together with L2.
- **DONE (2026-09-28).** Each of the three sets `msg` to its rendered
  message right after the base `__init__`, rather than handing the
  message to it: `msg` is what a traceback prints, and `args` stays `()`
  like that of every other worktoy exception, so L2 is left as it was.
  Tests: `tests/test_waitaminute/test_syntax_error_message.py`, three
  tests raising each exception from the class body it explains; all
  three failed before the fix on 3.14, 3.12 and 3.7. The functions bound
  in those bodies never run, so they are lambdas, which count as covered
  under branch coverage where a one-line `def` does not. The default
  exception hook on 3.13 and 3.14 now prints the message. The suite gives
  1535 passed on 3.14 with 100% line and branch coverage and passes on
  3.7 to 3.13. A mutation check removed the new line from each file in
  turn and set a wrong `msg` in one, each on its own copy of `src`, with
  an unmodified copy passing as the control; the suite caught all four.

#### 33. `EZField[list[int]]` is not refused on 3.9 and 3.10 (medium, verified)

- **Where:** `src/worktoy/ezdata/_ez_field.py:322-346`
  (`__class_getitem__`), `:212-217` (`_getFieldType`).
- **Cause:** item 18 for `EZField`. `__class_getitem__` stores any
  subscript, and `_getFieldType` accepts it when `isinstance(fieldType,
  type)` holds, which `list[int]` answers `True` to on 3.9 and 3.10
  only. The class builds, and the first instance fails inside
  `isinstance`. From 3.11 the class statement is refused, but by the
  general check in `_getFieldType`, whose message names
  `'__field_type__'` rather than the field.
- **Repro:**
  ```python
  class Foo(EZData):
    x = EZField[list[int]]()
  # 3.11 on: TypeException: Expected object at name '__field_type__' to
  # be an instance of 'type', but received object: 'list[int]' of type
  # 'GenericAlias'!

  Foo()  # 3.9 and 3.10: TypeError: isinstance() argument 2 cannot be a
         # parameterized generic
  ```
- **Fix direction:** judge the subscript in `__class_getitem__` with the
  test item 18 settled on, `issubclass(type(fieldType), type)`, and
  refuse anything else there with a `TypeException` naming the
  subscript.

#### 34. `FastBox` defaults skip the instance rule and the text refusal (medium, verified)

- **Where:** `src/worktoy/desc/_fast_box.py:174-192` (`_build`).
- **Cause:** `_build` returns `fieldType(*args, **kwargs)` without the
  two checks `AttriBox._resolve` makes: that the result is an instance of
  the field type (L11), and that a container field type refuses text
  (item 17). Assignment is fine, since `FastBox.__set__` accepts only an
  instance of the field type. Item 18 took its fix to the whole box
  family at the author's request, and these two rules are of the same
  kind.
- **Repro:**
  ```python
  class Shifty:
    def __new__(cls, *args):
      return 42

  class Foo:
    bar = FastBox[Shifty]()
    baz = FastBox[list]('abc')

  Foo().bar  # 42
  Foo().baz  # ['a', 'b', 'c'], where AttriBox[list]('abc') raises
             # TypeException
  ```
- **Fix direction:** make both checks in `_build`. It runs once per
  instance and field, on the first read, so a read stays one dict lookup.

#### 35. Copies of a frozen EZData instance keep only the fields (medium, verified)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:336-340` and `:913-963`
  (`copyFactory`, `deepCopyFactory`).
- **Cause:** a frozen class receives a generated `__copy__` and
  `__deepcopy__` that build a blank instance and copy the fields alone.
  Any other state of the instance is lost, such as a value
  `__post_init__` derives and stores through `object.__setattr__`, the
  usual way to cache on a frozen class. Their docstring gives the reason
  they exist: the default copy sets each slot and hits the frozen
  `__setattr__`. That stopped being true when group B removed
  `__slots__`. The default protocol now fills the new instance's
  `__dict__` directly, without calling `__setattr__`, which is how a
  non-frozen instance is copied, state and all.
- **Repro:**
  ```python
  class Frozen(EZData, frozen=True):
    x = EZField[float](3.0)

    def __post_init__(self):
      object.__setattr__(self, 'double', self.x * 2)

  Frozen().double                 # 6.0
  copy.copy(Frozen()).double      # AttributeError
  copy.deepcopy(Frozen()).double  # AttributeError
  ```
- **Fix direction:** stop generating the two methods. A probe that
  deleted both from the class copied and deep-copied frozen instances
  that compare equal to the original, with `double` intact. The existing
  copy tests of frozen classes say what must keep holding.
- **DONE (2026-09-28).** `EZHook` no longer generates `__copy__` and
  `__deepcopy__` for a frozen class: `copyFactory`, `deepCopyFactory` and
  the `deepcopy` import they needed are gone, and D16 with them. The
  default protocol copies a frozen instance by filling the `__dict__` of
  a blank instance, never calling `__setattr__`, and a deep copy threads
  its memo through that state. A copy now keeps everything the instance
  holds, fields and derived state alike, as a non-frozen copy always
  did, and a class body's own `__copy__` or `__deepcopy__` is no longer
  replaced. The module docstring of `tests/test_ezdata/test_frozen_copy.py`
  gave the old reason for the generated methods and now describes the
  protocol instead; its assertions are unchanged and pass. Tests:
  `tests/test_ezdata/test_frozen_copy_state.py`, five tests. Before the
  fix the four regression tests failed on 3.14, 3.10 and 3.7, for the
  missing state and because the class's own `__copy__` was replaced, and
  the guard for a non-frozen copy passed. The suite gives 1524 passed on
  3.14 with 100% line and branch coverage and passes on 3.7 to 3.13. A
  mutation check put generated methods back in five shapes, each on its
  own copy of `src`, with an unmodified copy passing as the control, and
  the suite caught all five: the old fields-only pair, either half of it,
  a whole-`__dict__` pair whose deep copy drops the memo, and a correct
  whole-`__dict__` pair that still replaces the class's own methods,
  which only `test_own_copy_methods_are_used` catches. The `AttriBox`
  test at first let the memo break through, since a default that cannot
  be copied is shared rather than refused; it now also checks that two
  owners receive distinct copies.

#### 36. A refused deletion uses up the single write of a `FixBox` (medium, verified)

- **Where:** `src/worktoy/core/_object.py:283-302` (`Object.__delete__`,
  the read at `:293`), `src/worktoy/desc/_fix_box.py:54-60`,
  `src/worktoy/desc/_field.py:196-213`.
- **Cause:** `Object.__delete__` reads the old value through
  `__instance_get__` before calling `__instance_delete__`, to report it.
  On a `FixBox` not read yet, that read builds the default and stores it,
  which is the one write the box allows, and then the deletion is
  refused. The same read makes an `AttriBox` build a default only to
  overwrite it with `DELETED`, and makes a `Field` without deleters run
  its getter twice, since `Field.__instance_delete__` reads the value
  again for its `ProtectedError`.
- **Repro:**
  ```python
  class Foo(BaseObject):
    bar = FixBox[int](7)

  foo = Foo()
  del foo.bar   # ProtectedError, as intended
  foo.bar = 42  # WriteOnceError: ... existing value: '7' with new
                # value: '42'!
  ```
- **Fix direction:** the old value is only reported, so the read before
  a deletion should never build one. The boxes can answer that read from
  their storage alone, with `None` when nothing is stored yet, which
  `FixBox` and `KeeBox` inherit from `AttriBox`.
- **Addition (2026-09-28, fourth read):** since the read builds the
  default, a field type whose constructor raises makes `del` raise that
  exception, although nothing was stored to delete.
- **DONE (2026-09-29).** The author chose a keyword over a storage-only
  accessor: `Object.__delete__` reads the old value with
  `_deleting=True`, and `AttriBox.__instance_get__` (so also `FixBox`)
  and `KeeBox.__instance_get__` answer such a read from their storage
  alone, raising `AttributeError` for an unset field, which
  `Object.__delete__` already reports as no old value. A refused
  deletion of a `FixBox` therefore leaves its one write available, an
  `AttriBox` no longer builds a default only to overwrite it, and a
  default that fails to build no longer stops the deletion.
  `Field.__instance_get__` calls the getter as `method(self)`, since it
  used to forward its keywords, which would have handed `_deleting` to
  every getter (getters are not flexed, and `flexCall` passes keywords
  through anyway), and `Field.__instance_delete__` reports the old value
  it receives instead of running the getter a second time. Test:
  `tests/test_desc/test_deletion_reads_storage.py` (eleven tests, the
  caught `ProtectedError` followed by the first assignment among them);
  six failed before the change and the guards passed. The suite gives
  1596 passed on 3.14 with 100% line and branch coverage and passes on
  3.7 to 3.13. A mutation check caught all five breaks (no keyword, each
  box ignoring it, `Field` forwarding its keywords, `Field` reading the
  value again) with the control passing.

#### 37. `typeCast(bool, x)` lets `x.__eq__` decide (medium, verified)

- **Where:** `src/worktoy/utilities/_type_cast.py:52-55` (`_castBool`),
  and the cast passes at `src/worktoy/dispatch/_dispatcher.py:273-324`.
- **Cause:** `_castBool` tests `arg in (True, False, 0, 1)`, which
  compares with `==` and so asks the argument's own `__eq__` whenever the
  builtins do not know its type. An `__eq__` that always answers `True`
  casts anything to `True`. An `__eq__` that raises escapes `typeCast`
  with its own exception instead of `TypeCastException`, and the cast
  passes of a `Dispatcher` catch only `ValueError` and `TypeError`, so an
  `AttributeError` ends the call before the next signature or the
  fallback is tried. It is the problem of item 31 on the value side.
- **Repro:**
  ```python
  typeCast(bool, AlwaysEqual())   # True
  typeCast(bool, RaisingEqual())  # AttributeError: 'bool' object has no
                                  # attribute 'r'

  class Foo(BaseObject):
    @overload(bool)
    def bar(self, flag):
      return 'bool overload'

    @overload.fallback
    def bar(self, *args):
      return 'fallback'

  Foo().bar(object())        # 'fallback'
  Foo().bar(RaisingEqual())  # AttributeError instead of 'fallback'
  ```
- **Fix direction:** consider only numbers, `isinstance(arg,
  numbers.Number)`, before comparing with `0` and `1`, so the `1.0` the
  docstring mentions still casts.

#### 38. `str()` of a `DispatchException` can raise (medium, verified)

- **Where:** `src/worktoy/waitaminute/dispatch/_dispatch_exception.py:51-69`
  (`__str__`, the list at `:60-62`).
- **Cause:** `__str__` iterates `self.dispatch.__sig_funcs__` rather than
  `_getSigFuncList()`. That attribute is `None` on a `Dispatcher` without
  concrete signatures, which is what `LoadSpaceHook` builds for a name
  declared with `@overload.finalize` alone: every call raises
  `DispatchException`, and rendering it raises `TypeError`. The traceback
  printers then show `DispatchException: <exception str() failed>`, so
  the exception meant to explain the failed call explains nothing.
- **Repro:**
  ```python
  class Foo(BaseObject):
    @overload.finalize
    def bar(self, *args):
      pass

  try:
    Foo().bar(1)
  except Exception as exception:
    str(exception)  # TypeError: 'NoneType' object is not iterable
  ```
- **Fix direction:** read the registrations through
  `_getSigFuncList()` and `_getVariadicFuncs()`, list the variadic
  signatures too, and say so when nothing is registered.
- **Split (2026-09-29):** this item first also covered the listing of a
  variadic declaration as its six concrete expansions. That is a symptom
  of how variadics are registered, so it moved to item 55; item 38 keeps
  the crash.
- **DONE (2026-09-29).** `DispatchException.__str__` reads the
  signatures through `Dispatcher._getSigFuncList()`, which gives an
  empty list where the raw attribute is `None`; nothing else changed.
  Test: `tests/test_dispatch/test_dispatch_exception_render.py` (three
  tests: a finalizer-only name renders, its finalizer still runs, and
  signatures are still listed); the first failed before the change. The
  suite gives 1582 passed on 3.14 with 100% line and branch coverage and
  passes on 3.7 to 3.13, and putting the raw attribute back fails the
  test.
- **Variadic listing, DONE (2026-09-29).** At the author's choice, the
  message part of item 55 was fixed ahead of its redesign: the message
  leaves out the signatures marked `__expanded_from_variadic__` and lists
  the variadic signatures from `_getVariadicFuncs()`, so
  `@overload(int, ARGS[str])` shows as `<TypeSig: [int, ARGS[str]]>` and
  an explicit declaration that took the place of an expansion still
  shows. Three more tests in the same file (the variadic listed, no
  expansion listed, the explicit declarations listed); the first two
  failed before the change. The suite gives 1585 passed on 3.14 with 100%
  line and branch coverage and passes on 3.7 to 3.13, and a mutation
  check caught all three breaks (expansions kept, variadics dropped,
  every signature filtered) with the control passing.

#### 39. `KeeFlagsMeta.__eq__` raises when the other operand's hash fails (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_flags_meta.py:198-206`.
- **Cause:** `__eq__` hashes `other` and re-raises every `TypeError`
  whose message lacks the words `'hashable type'`. A `KeeNum` member with
  an unhashable value raises its own message, so comparing a flags class
  with it raises, and so does a membership test on any list holding one.
  Judging an exception by its wording is fragile besides. The method
  returns only `NotImplemented` or `False`, which leaves equality to
  identity, the result `type` gives without it, and `AbstractMetaclass`
  documents metaclass equality as deliberately not implemented.
- **Repro:**
  ```python
  class Bag(KeeNum):
    A = Kee[list]([1, 2])

  Perm == Bag.A    # TypeError: Enumeration member 'Bag.A' is unhashable
                   # because its value of type 'list' is unhashable!
  Perm in [Bag.A]  # the same
  ```
- **Fix direction:** remove `__eq__` and keep `__hash__`.

#### 40. A second fallback or finalizer replaces the first without a word (medium, verified)

- **Where:** `src/worktoy/mcls/_base_space.py:430-466` (`addFallback`,
  `addFinalizer`).
- **Cause:** both store by name in a dict, so a second
  `@overload.fallback`, or a second `@overload.finalize`, for one name in
  one class body wins silently. Everywhere else a duplicate is refused:
  two explicit declarations of a signature raise `DuplicateSignature`
  (`addOverload`), and a second fallback on a `Dispatcher` raises
  `VariableNotNone` (`setFallbackFunction`).
- **Repro:**
  ```python
  class Foo(BaseObject):
    @overload.fallback
    def bar(self, *args):
      return 'first'

    @overload.fallback
    def bar(self, *args):
      return 'second'

  Foo().bar()  # 'second'
  ```
- **Fix direction:** refuse the second registration in the class body
  with `VariableNotNone`. A fallback inherited from a base stays
  replaceable, since `collectFallback` looks at the class body first.

#### 41. The stacking order decides whether a duplicate signature is caught (medium, verified)

- **Where:** `src/worktoy/dispatch/_overload.py:160-203` (`_addSigFunc`),
  with `src/worktoy/mcls/_base_space.py:344-402` (`_resolveCollision`).
- **Cause:** `_addSigFunc` keeps its signatures in a dict. With
  `@overload(int)` stacked above `@overload(ARGS[int])`, the explicit
  `(int,)` arrives after the expansion that produced the same signature,
  and assigning to an existing key keeps the old key object: the
  expansion's `TypeSig`, marked `__expanded_from_variadic__`. The
  namespace then ranks the explicit declaration as an expansion, and an
  explicit `@overload(int)` on a later function displaces it without a
  word. With the two decorators swapped, the explicit key comes first and
  the same body raises `DuplicateSignature`.
- **Repro:**
  ```python
  class Foo(BaseObject):
    @overload(int)
    @overload(ARGS[int])
    def bar(self, *args):
      return 'A'

    @overload(int)
    def bar(self, x):
      return 'B'

  Foo().bar(1)  # 'B'; with the first two decorators swapped, the class
                # body raises DuplicateSignature
  ```
- **Fix direction:** when an explicit signature meets an expansion in
  `_addSigFunc`, remove the old entry before storing, so the stored key
  is the unmarked one.

#### 42. An EZData `__class_init__` sees fields without an owner (medium, verified)

- **Where:** `src/worktoy/ezdata/_ez_meta.py:203-225` (`EZMeta.__init__`).
- **Cause:** `EZMeta.__init__` first calls the inherited `__init__`,
  which runs `__class_init__` and notifies the bases through
  `__subclasshook__`, and binds `__field_owner__` on the fields only
  afterwards. Item 10 settled the order for `KeeMeta`: the hook comes
  last, so it sees the finished class.
- **Repro:**
  ```python
  class Pt(EZData):
    x = EZField[int](0)

    @classmethod
    def __class_init__(cls, *args, **kwargs):
      cls.fields[0].fieldOwner
  # MissingVariable: Missing 'EZField.__field_owner__: type'!
  ```
- **Fix direction:** bind the owners before calling the inherited
  `__init__`.

#### 43. Flags looked up by several members or indices raise `AttributeError` (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_flags_meta.py:237-244`
  (`_resolveNames`), reached from `__getitem__`, `__call__` and
  `__contains__` (`:187-193`) through `_resolveMember` (`:254-268`).
- **Cause:** `_resolveNames` calls `.upper()` on every identifier, so
  anything but a string raises `AttributeError`: two members in a
  subscript, or a tuple of indices. `__contains__` catches
  `KeeResolveError`, `IndexError`, `KeyError`, `ValueError` and
  `TypeError`, but not `AttributeError`, so a membership test raises as
  well. `KeeBox` already resolves each identifier separately (group C).
- **Repro:**
  ```python
  Perm[Perm.READ, Perm.WRITE]  # AttributeError: 'Perm' object has no
                               # attribute 'upper'
  (1, 2) in Perm               # AttributeError: 'int' object has no
                               # attribute 'upper'
  Perm['READ', 'WRITE']        # Perm.READ_WRITE [3]
  ```
- **Fix direction:** resolve each identifier through `_resolveMember`
  and join the names of the results, as `KeeBox._resolveFlags` does.
  That also settles the group C note that `Perm['READ_WRITE',
  'EXECUTE']` raises `KeyError`.

#### 44. `KeeBox` reads a negative `int` as an index (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_box.py:146-151` (`_resolveNum`).
- **Cause:** the index step tests `args[0] < len(fieldNum)`, which every
  negative number passes, and subscripting the enumeration then counts
  from the end. A value such as `-1` therefore picks a member by
  position, while calling the enumeration picks it by value. The class
  docstring lists index before value for an `int`, but no member has a
  negative index.
- **Repro:**
  ```python
  class Status(KeeNum):
    ERROR = Kee[int](-1)
    OK = Kee[int](0)
    WARN = Kee[int](1)

  class Holder:
    status = KeeBox[Status](-1)

  Holder().status  # Status.WARN, the last member
  Status(-1)       # Status.ERROR
  ```
- **Fix direction:** take the index step only for `0 <= args[0] <
  len(fieldNum)`, and let a `bool` skip it, as `KeeMeta.__getitem__`
  does.
- **DONE (2026-09-28).** In `_resolveNum` a lone `int` names a member by
  index only when `0 <= i < len(fieldNum)`, and it is compared with the
  member values only when it is an instance of the value type; any other
  `int` goes on to the last step, where the value type builds a value
  from it, `float(-1)` finding `-1.0`. The second half closes a hole of
  the same kind that the new path would otherwise have widened: an `int`
  past the last index was compared with every member value, and on
  `ColorNum` that asked `RGB.__eq__`, which raised `AttributeError` for
  `KeeBox[ColorNum](99)`. The second part of the fix direction, letting
  a `bool` skip the index step, was left out on purpose: a `bool` passes
  the bounds and reaches the subscript of the enumeration, which refuses
  it as calling the enumeration does, while skipping would have sent
  `True` to the lookup by value, where it equals `1`. The class
  docstring lists the steps as they now run and no longer claims that
  `KeeBox` never builds a value of the value type, which settles D9. A
  consequence: a negative `int` for an enumeration whose values are not
  numbers, such as `KeeBox[WeekDay](-1)`, raises `KeeBoxValueError` where
  it gave the last member. Tests:
  `tests/test_keenum/test_kee_box_int_identifier.py`, eight tests.
  Before the fix the five regression tests failed on 3.14, 3.10 and 3.7
  and the two guards passed, one pinning that a real index still comes
  before a value, the other that a `bool` is refused. The suite gives
  1532 passed on 3.14 with 100% line and branch coverage and passes on
  3.7 to 3.13. A mutation check applied five breaks, each on its own copy
  of `src`, with an unmodified copy passing as the control, and caught
  four at once: the original code, no lower bound, no value-type guard,
  and a `bool` skipping the index step, which the `bool` guard catches.
  The fifth, an inclusive upper bound, survived until
  `test_member_count_is_no_index` pinned the first number past the last
  index.

### Decisions needed

#### 45. EZData drops unknown keywords, and a keyword overrides a positional (verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:569-572` (`_applyKwargs`),
  `:586-595` (the generated `__init__`). The policy is stated at
  `:673-679` and in
  `src/worktoy/waitaminute/ezdata/_extra_positional_exception.py:15-17`.
- **Cause:** the generated `__init__` applies the keywords that name a
  field and ignores the rest, "to support orthogonal kwarg injection".
  Nothing receives the ignored keywords, neither a base `__init__` nor
  `__post_init__`, so a misspelled field name is lost without a word;
  that is what hid T2 in group F. A keyword naming a field also replaces
  a positional value given for the same field.
- **Repro:**
  ```python
  class Name(EZData):
    givenNames = EZField[str]('John')
    familyName = EZField[str]('Doe')

  Name(givenName='Jane')     # Name('John', 'Doe')
  Name('A', givenNames='B')  # Name('B', 'Doe')
  ```
- **Options:** refuse an unknown keyword and a field given twice, as
  `dataclasses` does and as `replace` already refuses unknown names; or
  keep the policy and hand the unused keywords to `__post_init__`, so the
  injection the docstrings describe has somewhere to go.
- **DECIDED (2026-09-29):** refuse both, with one new exception for each
  case, at the author's choice over a single exception for both and over
  Python's plain `TypeError`. A run of the suite against a copy of `src`
  refusing both showed that nothing relied on the dropped keywords; only
  `test_kwarg_overrides_positional` pinned the override.
- **DONE (2026-09-29).** The generated `__init__` refuses, after the
  positional arguments and before any keyword is applied or
  `__post_init__` runs, a keyword naming none of the fields with the new
  `ExtraKeywordException`
  (`src/worktoy/waitaminute/ezdata/_extra_keyword_exception.py`, a
  `TypeError` with `cls`, `keyword` and `fieldNames`, whose message lists
  the fields), and a keyword for a field a positional argument already
  filled with the new `RepeatedFieldException`
  (`src/worktoy/waitaminute/ezdata/_repeated_field_exception.py`, a
  `TypeError` with `cls` and `fieldName`), through the helpers
  `_refuseUnknown` and `_refuseRepeated` in `EZHook.initFactory`. The
  docstrings of `initFactory`, `replace` and `ExtraPositionalException`
  no longer promise that keywords are ignored. Tests:
  `tests/test_ezdata/test_extra_keyword_refused.py` (six tests) and
  `tests/test_ezdata/test_repeated_field_refused.py` (four tests), and
  `test_kwarg_overrides_positional` in
  `tests/test_ezdata_examples/test_ez_complex.py` became
  `test_kwarg_repeating_positional`, expecting the refusal. The eight
  regression tests failed before the change and the three guards
  (keywords naming fields, an inherited field, a keyword for a field no
  positional reached) passed. The suite gives 1657 passed on 3.14 with
  100% line and branch coverage and passes on 3.7 to 3.13. A mutation
  check caught all eleven breaks with the control passing: either check
  removed, the repeated check off by one or limited to the first field,
  both checks moved after `__post_init__`, the checks dropped for the
  applied keywords, the wrong keyword or field named, the field list
  left out of the message, and either exception based on `ValueError`
  instead of `TypeError`.

#### 46. Customised helpers of an EZData base do not reach its subclasses (verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:215-242` (`preCompilePhase`).
- **Cause:** `preCompilePhase` installs the generated `__field_pairs__`,
  `asDict`, `asTuple`, `replace`, `__repr__` and `__str__` in every class
  it builds, before the class body is merged in. A definition in the
  class body wins, but one inherited from a base loses to the generated
  method of the subclass. `dataclasses` does the same for the dunders it
  generates, but EZData also generates plain helpers, and
  `fieldPairsFactory` says that "a subclass can customize field
  rendering by overriding '__field_pairs__' alone", which holds for one
  level only.
- **Repro:**
  ```python
  class Base(EZData):
    x = EZField[int](1)

    def asDict(self):
      return 'custom asDict'

    def __field_pairs__(self):
      return ['custom pairs']

  class Sub(Base):
    pass

  Base().asDict()  # 'custom asDict'
  Sub().asDict()   # {'x': 1}
  str(Base())      # '<Base: custom pairs>'
  str(Sub())       # '<Sub: x=1>'
  ```
- **Options:** install a generated helper only where no class further
  along the method resolution order defines one that is not generated,
  which needs a mark on the generated functions; or keep the rule and
  state it in the `EZData` and `EZHook` docstrings.
- **Addition (2026-09-29, verified):** the author set the principle
  recorded under [Decisions](#decisions): allowed and honoured, or
  refused at once, never replaced without a word. A probe supplied a
  custom version of every generated name by three routes: the class
  body, the body of an EZData base, and a plain mixin base (either base
  order gave the same result).

  | Name | Class body | EZData base | Mixin base |
  |---|---|---|---|
  | `__field_pairs__`, `asDict`, `asTuple`, `replace`, `__repr__`, `__str__` | kept | replaced | replaced |
  | `__match_args__` | kept (item 65) | regenerated | regenerated |
  | `__init__`, `__iter__`, `__eq__`, `__hash__`, ordering, `__setattr__`, `__delattr__` | refused (`ReservedMethodError`) | refused, at the base's body | replaced |

  The class-body column meets the principle; its one gap, the
  bookkeeping attributes, became item 71 and is done. The other two
  columns wait. A proposal taking them on together was stopped by the
  author as conflating several problems, so each needs its own
  question: the helpers from an EZData base (the item as first
  recorded), the helpers from a mixin, `__match_args__` from a base
  (regenerated by the rule of item 65), and the essential methods from a
  mixin, which `EZComplex(EZData, ComplexMixin)` in
  `tests/test_ezdata/examples/_ez_complex.py` relies on being replaced.
- **DECIDED in part (2026-09-29):** the essential methods from a plain
  base are ignored, the generated ones taking precedence; see "Plain
  bases" under [Decisions](#decisions). This is the behaviour the probe
  found, now a rule, pinned by
  `tests/test_ezdata/test_plain_base_reserved_ignored.py` (every reserved
  method from a plain base in either base order, and a mixin written
  against construction, iteration and length) and stated in the
  docstrings of `EZData`, `EZSpace`, `ReservedMethodError` and
  `EZHook.postCompilePhase`. Settling it on the author's own mixin
  example (`main_tester_03.py`) found item 72.
- **DECIDED (2026-09-29), the rest:** the author sorted the generated
  names into two kinds. The reserved methods and attributes may not be
  set in an EZData class body, and a plain base's methods give way (the
  part above, and items 71 and 72). The optional names,
  `__field_pairs__`, `asDict`, `asTuple`, `replace`, `__repr__`,
  `__str__` and `__match_args__`, defer: the class body's own wins, then
  the first one written by hand along the bases, an EZData base and a
  plain base alike, and EZData generates one only where there is none.
  For `__match_args__` this replaces the part of item 65 that had a
  subclass regenerate its tuple: a subclass now uses the tuple its
  parent set by hand. For `EZComplex` it means the `__repr__` and
  `__str__` of `ComplexMixin`, the same rendering as its other
  implementations (`EZComplex(3.000, 4.000)`, `3.000 + 4.000J`).
- **DONE (2026-09-29).** `EZHook.postCompilePhase` settles the seven
  optional names through the new `_settleOptional`, which takes the
  class body's entry (a `Dispatcher` from `@overload` included), then
  the first hand-written value `_findHandWritten` finds along the lookup
  order (skipping `object` and every name an EZData class lists as
  generated), then the generator from `_optionalFactories`. Each class
  records the names generated for it in a new bookkeeping attribute,
  the frozenset `__ez_generated__`, so a subclass looks past a base's
  generated helper to a hand-written one further along; it joins the
  five attributes of item 71 in `__reserved_ez_attributes__`.
  `preCompilePhase`, which installed the generated helpers before the
  class body, is gone, and `matchArgsFactory` only generates; the class
  body rule of item 65 lives in `_settleOptional` with the rest. The
  docstrings of `EZHook`, `postCompilePhase`, `matchArgsFactory`,
  `EZData` and `ReservedAttributeError` say so. Tests:
  `tests/test_ezdata/test_optional_names_deferred.py` (eleven tests);
  `test_subclass_generated` in `test_match_args_class_body.py` became
  `test_subclass_inherits`, and `test_reserved_attribute.py` lists
  `__ez_generated__`. The twelve regression tests failed before the
  change and the guards passed (the class body winning, a subclass of a
  generated base generating). The suite gives 1707 passed on 3.14 with
  100% line and branch coverage and passes on 3.7 to 3.13; the author's
  `tester04` still passes. A mutation check caught all seven breaks
  with the control passing: never deferring, generated names not
  skipped, `object` not skipped, the class body not first, nothing
  recorded, the farthest hand-written one winning, and
  `__ez_generated__` left unreserved.

#### 47. Sentinels are unique by bare name across the process (verified, DECISION)

- **Where:** `src/worktoy/core/sentinels/_sentinel.py:44-84`.
- **Cause:** `SentinelMeta` keeps one registry, which its subclasses
  share, and finds a sentinel by `__name__` alone. The first class
  statement of a name wins everywhere: a later `class MISSING(Sentinel)`
  in another package receives the first package's object, and its own
  body, docstring included, is discarded. The docstrings describe the
  reuse, but for a public base class it lets two unrelated libraries
  share one sentinel by accident, which is what a sentinel exists to
  prevent.
- **Repro:**
  ```python
  class MISSING(Sentinel):
    """First library's sentinel."""

  first = MISSING

  class MISSING(Sentinel):
    """Second library's sentinel."""

  MISSING is first  # True
  MISSING.__doc__   # "First library's sentinel."

  class THIS(Sentinel):
    pass

  from worktoy.core import sentinels
  THIS is sentinels.THIS  # True
  ```
- **Options:** key the registry by module and qualified name, so a
  reload of the same module still finds its own sentinel; or keep it and
  say in the `Sentinel` docstring that names are global.

#### 48. `__class_*__` hooks are ignored on KeeNum and KeeFlags classes (verified, DECISION)

- **Where:** `src/worktoy/keenum/_kee_meta.py:308-425`,
  `src/worktoy/keenum/_kee_flags_meta.py:78-209`.
- **Cause:** `AbstractMetaclass` hands `str`, `repr`, `len`, `iter`,
  `bool`, `in`, `isinstance`, `issubclass`, attribute misses, calls and
  hashing to a `__class_*__` hook when a class defines one. `KeeMeta`
  overrides `__getattr__`, `__iter__`, `__len__`, `__contains__`,
  `__instancecheck__`, `__subclasscheck__`, `__str__`, `__repr__`,
  `__bool__` and `__call__` without handing over, and `KeeFlagsMeta`
  does the same for `__len__`, `__iter__`, `__contains__`,
  `__subclasscheck__`, `__eq__`, `__hash__` and `__call__`. A hook of
  those names in an enumeration body is accepted and never called.
  `__class_call__` is worse: both metaclasses call it while they build
  the members, in place of creating them, so a hook that returns
  anything else breaks the class statement with an unrelated
  `AttributeError`.
- **Repro:**
  ```python
  class Num(KeeNum):
    A = Kee[int](1)

    @classmethod
    def __class_str__(cls):
      return 'custom str'

    @classmethod
    def __class_len__(cls):
      return 69

  str(Num)  # "<KeeNum 'Num': 1 members>"
  len(Num)  # 1

  class Called(KeeNum):
    A = Kee[int](1)

    @classmethod
    def __class_call__(cls, *args, **kwargs):
      return 'hooked'
  # AttributeError: 'str' object has no attribute 'name'
  ```
- **Options:** consult the hooks first, as `AbstractMetaclass` does; or
  refuse such hooks in an enumeration body, where `NamespaceHook` already
  screens these names; or document the limit on `KeeMeta` and
  `KeeFlagsMeta`.

#### 49. `SymbolicName` compares by identity (verified, DECISION)

- **Where:** `src/worktoy/desc/_symbolic_name.py:23-154`.
- **Cause:** `SymbolicName` defines neither `__eq__` nor `__hash__`, so
  two names made of the same words are unequal and hash apart, although
  the class behaves as a value in every other way: it renders, indexes,
  iterates and tests membership by its words.
- **Repro:**
  ```python
  SymbolicName('a', 'b') == SymbolicName('a', 'b')  # False
  ```
- **Options:** compare and hash by `words`; or keep identity and say so
  in the docstring.

### Low severity

- **L20. Calling a KeeNum class without an identifier gives a
  self-contradicting message, and extra arguments are dropped
  (verified).** `src/worktoy/keenum/_kee_meta.py:314-318`. `Day()`
  raises `TypeException('identifier', None, object)`, which reads
  "Expected object at name 'identifier' to be an instance of 'object',
  but received object: 'None' ...", a case the `TypeException` docstring
  leaves to `MissingVariable`. `Day('monday', 'junk', x=1)` returns
  `Day.MONDAY` and drops the rest without a word.
  **Addition (2026-09-29, fifth read):** `KeeFlags` drops keyword
  arguments the same way: `KeeFlagsMeta.__call__` hands them to
  `_resolveMember`, which ignores them, so `Perm(read=True)` is
  `Perm.NULL` and `Perm('READ', junk=1)` is `Perm.READ`
  (`src/worktoy/keenum/_kee_flags_meta.py:179-182`).
- **L21. Lookups on an enumeration without members raise a plain
  `TypeError` (verified).** `src/worktoy/keenum/_kee_meta.py:564` and
  `:204-219`. Every identifier that misses the earlier steps reaches
  `cls.valueType`, which raises `TypeError` ("has no members, so no
  'valueType' can be inferred") where `KeeResolveError` is documented,
  names included: `Empty('x')`, `Empty(1)`, and `KeeNum('x')` on the
  root.
- **L22. `KeeNameConflict` always names the member 'Unknown'
  (verified).** `src/worktoy/waitaminute/keenum/_kee_name_conflict.py:39`
  reads `__name__`, which a `Kee` does not have: `A = Kee[int](1)`
  followed by `B = A` in a KeeNum body gives "Name conflict for Kee
  member object 'Unknown': existing name 'A' versus new name 'B'!".
  `str(self.member)` names the member.
- **L23. `@overload(OWNER)` builds, then every call fails (verified).**
  `src/worktoy/dispatch/_type_sig.py:190-204`. By its docstring `OWNER`
  has no role in overload signatures, but `TypeSig` hashes it during the
  class body and nothing ever replaces it, so the class builds and the
  first call raises the hash `TypeError` meant for internal misuse ("...
  not hashable outside an active class-body context ... call 'swapTHIS'
  first"). Refusing `OWNER` in `overload` reports it at the declaration.
  **Addition (2026-09-29, fifth read):** `OWNER` is one case of item 57,
  since `overload` checks none of its entries. `OWNER` is a sentinel
  class, so the check item 57 proposes lets it through, and it still
  needs this refusal of its own.
- **L24. A plain mixin's class hook is hidden in a class without worktoy
  bases (verified).** `src/worktoy/mcls/space_hooks/_name_hook.py:200-228`.
  `NamespaceHook.preCompilePhase` seeds `METACALL` for every class-hook
  name that neither the class body nor a worktoy base provides, so in
  `class Foo(Mixin, metaclass=BaseMeta)` the `METACALL` in the class dict
  shadows a `__class_str__` on the plain `Mixin`, and `str(Foo)` ignores
  it. With a worktoy base the name is found in its compiled namespace and
  the mixin wins by ordinary lookup.
- **L25. A finalizer's exception is chained to one the caller is
  handling (verified).** `src/worktoy/dispatch/_dispatcher.py:329-337`.
  The `finally` asks `sys.exc_info()` for the exception in flight, which
  also reports an exception the caller's `except` block is handling when
  the dispatched call itself went well. A finalizer that raises is then
  chained `from` that unrelated exception: calling, inside
  `except KeyError:`, a method whose finalizer raises `ValueError` gives
  the `ValueError` the `KeyError` as its `__cause__`. Keeping the call's
  own exception, rather than asking `sys.exc_info()`, avoids it.
- **L26. `AttriBox[object](None)` is refused with a contradictory
  message (verified).** `src/worktoy/desc/_attri_box.py:299-314`.
  `_resolve` uses `None` to mean "not built yet", so a lone `None` that
  is an instance of the field type (only `object` and `NoneType`
  qualify) goes to the constructor, and `object(None)` fails: "Expected
  object at name 'value' to be an instance of 'object', but received
  object: 'None' of type 'NoneType'!". A separate flag in place of the
  `None` test fixes it.
- **L27. A builtin function in an EZData body becomes a field that fails
  every construction (verified).** `src/worktoy/ezdata/_ez_hook.py:160-180`.
  Only a `FunctionType` passes through as a method. `helper = len` is a
  `builtin_function_or_method`, whose type has none of the descriptor
  methods, so it becomes a field whose default is `type(len)(len)`: the
  class builds, and every `Foo()` raises "cannot create
  'builtin_function_or_method' instances". Passing any callable through,
  or refusing it as class objects are refused (`ClassFieldError`), moves
  the problem to the class body.
- **L28. `getKeyArgs()` on an EZData instance returns the class keywords
  (verified).** `src/worktoy/ezdata/_ez_hook.py:318`. `postCompilePhase`
  stores the class keyword arguments at `__key_args__`, the name under
  which `Object` keeps the keyword arguments of the constructor, and the
  generated `__init__` never sets it on the instance: on a frozen `Pt`,
  `Pt(1).getKeyArgs()` is `{'frozen': True}`. Nothing reads the class
  attribute, and the namespace records the keywords as
  `__keyword_arguments__` anyway.
- **L29. Calling a worktoy metaclass with a plain dict skips
  `newClassPhase` (read, not verified).**
  `src/worktoy/mcls/_abstract_metaclass.py:162-175`. Given a plain dict,
  as in `BaseMeta('Foo', bases, {...})`, `__new__` builds and compiles a
  namespace from it, then tests `hasattr(space, 'getHooks')` on the dict
  it was given, so no hook's `newClassPhase` runs. No hook in the library
  implements that phase yet, so only user hooks are affected. Asking the
  namespace built there for its hooks fixes it.
- **L30. Smaller points (verified unless marked read).**
  - `unpack` iterates a `bytearray`
    (`src/worktoy/utilities/_unpack.py:63`), where item 17 counts it as
    text along with `str` and `bytes` (read).
  - The lorem generators accept a negative `charCount`, and
    `str(Sentence(-5))` is `''`
    (`src/worktoy/lorem_ipsum/_base_generator.py:44`).
  - A `Sentence` shorter than `__truncate_below__` renders its
    `_shortText()`, while its iteration and `repr()` build real clauses:
    `str(Sentence(5))` is `'Lo...'`, and its one clause is 13 characters
    long (`src/worktoy/lorem_ipsum/_sentence.py:146-158`).
  - `ComplexMixin(1, 2)` equals `(1, 2)` and `'1+2j'` but hashes apart
    from them (`src/worktoy/work_test/_complex_mixin.py:197-207`).
  - The `assertIsSubclass` and `assertNotIsSubclass` stand-ins for 3.7 to
    3.13 ignore `msg` (`src/worktoy/work_test/_base_test.py:45-51`;
    read).
  - `KeeFlagsSpace.getKeeFlags()` adds the body's flags to
    `__base_flags__` in place, so after the first flag of a subclass
    `__kee_flags__` and `__base_flags__` are one dict. Nothing observable
    breaks yet, but the getter changes state
    (`src/worktoy/keenum/_kee_flags_space.py:50-55` and `:79-92`; read).
  - Every read of `flags` on a `KeeFlags` class, and so every `highs`,
    `lows`, `name`, `names` and `hash()` of a member, clones all the flags
    again (`src/worktoy/keenum/_kee_flags_space.py:122-126`; read).
  - `Field` writes `__prototype_object__`
    (`src/worktoy/desc/_field.py:222`), and nothing reads it (read).
  - `desc/_fix_box.py`, `lorem_ipsum/_clause.py`, `_sentence.py`,
    `_paragraph.py`, `work_test/_complex_mixin.py` and
    `waitaminute/keenum/_kee_resolve_error.py` import from `worktoy.` by
    absolute path at module level, where the rest of the source imports
    relatively (read).

### Out-of-date docstrings

- **D15.** `src/worktoy/core/_object.py:351-361`: `createContext` returns
  `self` "so the descriptor can be used as a context manager", but
  `Object` defines neither `__enter__` nor `__exit__`. The type aliases
  `ExcType`, `ExcVal` and `Trace` (`:23-25`) are left from such methods
  and used nowhere.
- **D16.** `src/worktoy/ezdata/_ez_hook.py:913-963`: `copyFactory` and
  `deepCopyFactory` justify themselves with a default copy that sets
  each slot, which no longer holds (item 35). **DONE with item 35:** the
  two factories are gone, docstrings included.
- **D17.** `src/worktoy/desc/_base_descriptor.py:100-102`: the accessors
  to override are shown as `__instance_set__(self, instance, value)` and
  `__instance_delete__(self, instance)`; `Object` defines them with
  `**kwargs`, and the deleter also takes `old`.
- **D18.** `src/worktoy/keenum/_kee_flags.py:70`: "Entries must be
  integer valued", while the `_getValue` docstring (`:143-153`) invites
  subclasses to return any object.
- **D19.** `src/worktoy/waitaminute/control_flow/_control_class_error.py:21-24`:
  "Any other attribute raises this exception", but
  `ControlSpace.__setitem__` (`_control_space.py:57-64`) lets through
  every name `Exception` already has with a value that is not callable,
  such as `args` or `__doc__`.
- **D20.** `src/worktoy/waitaminute/_subclass_exception.py:29-40`: the
  example writes the continuation lines of its class body with `>>>`,
  where doctest expects `...`.
- **D21.** Stray line breaks inside a sentence, as in D7:
  `src/worktoy/waitaminute/__init__.py:4-6`,
  `lorem_ipsum/_base_generator.py:63-64`,
  `lorem_ipsum/_stochastic_variable.py:114-116`, `:181-183`, `:212-214`
  and `:236-239`, `lorem_ipsum/_stochastic_word.py:112-114`,
  `lorem_ipsum/_clause.py:106-108` and `:150-152`, and
  `ezdata/_ez_data.py:33-35`.
- **D22.** `src/worktoy/mcls/__init__.py:3`: "namespace uses across the
  'worktoy' library", for "used".
- **D23.** `src/worktoy/work_test/_base_test.py:151-152`: "A
  representation longer than 48 characters is truncated", but the code
  (`:164`) keeps only lines shorter than 48 and truncates the whole
  `<type: value>` line rather than the representation.
- **D24.** `src/worktoy/waitaminute/_unpack_exception.py:34-39` puts line
  breaks into a message that `textFmt` then collapses, and
  `src/worktoy/keenum/_kee_meta.py:159` joins the bases with
  `'<tab><br>'`, the tab before the line break instead of after it.

---

## Group J: Fourth source read before 1.1.0 (open)

Files: various

Later on 2026-09-28, after items 31, 32, 35 and 44 were done and the
release was renamed 1.1.0, a Claude session read every file in
`src/worktoy` a fourth time, in the layer order from
`src/worktoy/__init__.py`, checking each candidate against the open items
of groups G, H and I so that none is repeated here. Each item below was
reproduced with a throwaway script on 3.14; items 50 and 51 also on 3.7.
Item 50 is filed under "Fix before 1.1.0" with the other bugs; it was
marked DECISION, and settled the same day.
At the time the suite gave 1535 passed on 3.14 with 100% line and branch
coverage, and it catches none of these items. The read also added to
item 36; the addition is marked there.

The repros assume these imports:

```python
import pickle

from worktoy.desc import AttriBox, FixBox, Alias
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag, KeeBox
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast


class Day(KeeNum):
  MON = Kee[str]('mon')
  TUE = Kee[str]('tue')


class Perm(KeeFlags):
  READ = KeeFlag()
  WRITE = KeeFlag()
```

### Fix before 1.1.0

#### 50. Enumeration members do not survive `pickle` (medium, verified, DECIDED)

- **Where:** `src/worktoy/keenum/_kee_num.py:159-170` (`KeeBase` defines
  `__copy__` and `__deepcopy__`, but no `__reduce__`) and
  `src/worktoy/keenum/_kee_flags.py:213-222` (the same for `KeeFlags`).
- **Cause:** the default reduce protocol rebuilds a member through
  `cls.__new__` and restores its `__dict__`, which makes a second member
  object instead of returning the canonical one. The enumeration then
  accepts that object as its own: `KeeMeta.__instancecheck__` falls back
  to `issubclass(type(instance), cls)`, so `isinstance`, `in` and the
  identity step of `_resolveMember` all take it, while `KeeBase.__eq__`,
  which is identity, matches it to nothing. This is the family of the
  rc18 copy bug: a generic operation breaking the singleton invariant.
- **Repro:**
  ```python
  mon = pickle.loads(pickle.dumps(Day.MON))
  mon is Day.MON         # False
  mon == Day.MON         # False
  isinstance(mon, Day)   # True
  mon in Day             # True
  Day(mon) is mon        # True, the copy resolves to itself
  {Day.MON: 1}[mon]      # KeyError: Day.MON

  read = pickle.loads(pickle.dumps(Perm.READ))
  read == Perm.READ      # True, 'KeeFlags.__eq__' compares indices
  read is Perm.READ      # False, so 'member is Perm.NULL' checks fail
  ```
  Same results on 3.7. Matters for `multiprocessing`, `shelve` and any
  cache that pickles.
- **Fix direction:** a `__reduce__` that rebuilds through the class:
  `(type(self), (self.name,))` on `KeeBase`, resolved by name to the
  canonical member, and `(type(self), (self.index,))` on `KeeFlags`. An
  inherited member is the parent's member object, so `type(self)` is the
  parent and the rebuild still finds it.
- **DECISION:** when the rc18 copy bugs were fixed, pickling was left out
  of scope, and the members got `__copy__` and `__deepcopy__` rather than
  a reduce method. L2, worktoy exceptions that cannot be unpickled, is
  open all the same. Fix it for 1.1.0, or record pickling of worktoy
  objects as unsupported.
- **DECIDED (2026-09-28):** no pickling, anywhere. Unpickling rebuilds an
  object without calling its class, which skips every check the class
  and its metaclass perform, so the fix direction above was rejected:
  no worktoy object pickles, not even through a sound `__reduce__`, and
  the refusal must be explicit, exceptions included. This settles L2.
- **DONE (2026-09-28).** The new mixin `NoPickle`
  (`src/worktoy/utilities/_no_pickle.py`) raises the new
  `PickleException` (`src/worktoy/waitaminute/_pickle_exception.py`, a
  `TypeError`) from four layers, each refusing on its own:
  `__reduce_ex__`, `__reduce__` and `__getstate__` when an object is
  pickled, and `__setstate__` when a stream tries to restore state into
  one. The `copy` module falls back on the same reduce protocol, so the
  mixin also brings `__copy__` and `__deepcopy__`, which do what that
  protocol did: a new instance made by the nearest `__new__` not written
  in Python, holding the arguments of an exception, the slot values, the
  instance dict and the items of a `dict`, written past `__setattr__`.
  Copies therefore behave as before, item 35 included, and the
  enumeration members keep their own copy methods returning themselves.
  `Object` mixes it in, which covers `BaseObject`, `EZData`, the
  members and the descriptors; so do the 39 exceptions with a builtin
  base, and every standalone class: `ContextInstance`, `ContextOwner`,
  `ARGS`, `QuickDesc`, `ExceptionInfo`, `Directory`, `Arrangement`,
  `Arrangements`, `TypeSig`, `overload`, `CallMeMaybe`, `FastBox`,
  `_RootAlias`, `AbstractNamespace`, `ControlSpace`, `SpaceDesc`,
  `ReservedNames`, `KeeFlag`, `KeeFlags`, `EZStore`, `ComplexMixin`,
  `SubTest` and `BaseTest`. Classes are left out, since pickle stores a
  class by name alone, rebuilds nothing and consults no hook of it, and
  so are the never-instantiated sentinels and `ValidSlice`. Tests:
  `tests/test_utilities/test_no_pickle.py` (the mixin on local classes,
  every protocol, each layer alone, the copies),
  `tests/test_utilities/test_no_pickle_classes.py` (an instance of every
  class refuses, copies shallow and deep, and every exported class mixes
  in `NoPickle`), `tests/test_waitaminute/test_no_pickle_exceptions.py`
  (all 44 exported exceptions, every protocol) and
  `tests/test_waitaminute/test_pickle_exception.py`. The suite gives 1579
  passed on 3.14 with 100% line and branch coverage and passes on 3.7 to
  3.13. A mutation check caught all eighteen breaks with the control
  passing: each layer removed, the unpickle action mislabelled, the
  shallow copy made deep, the memo, the arguments, the slots, a bare
  string slot, an unset slot, the dict items, the dict written through
  `setattr`, `__new__` taken from Python code, and `NoPickle` dropped
  from `Object`, `TypeException`, `KeeFlags` and `PickleException`. The
  first run left `__reduce_ex__` and `__reduce__` alone as survivors,
  each covered by the next layer, so a test now reopens one layer in a
  subclass and checks that the others still refuse.

#### 51. Boxes store their value through the owner's `__setattr__` (medium, verified)

- **Where:** `src/worktoy/desc/_attri_box.py:360` (the lazy default in
  `__instance_get__`), `:376` and `:414`;
  `src/worktoy/keenum/_kee_box.py:99` and `:105`; `FixBox` shares the
  `AttriBox` paths. Also `src/worktoy/core/_object.py:231-233`
  (`Object.__init__`).
- **Cause:** item 23 moved the reads of the box storage to
  `object.__getattribute__`, so an owner's `__getattr__` cannot answer
  them, but the writes still go through `setattr(instance, ...)`, and so
  through the owner's `__setattr__`. A frozen EZData class refuses every
  assignment, so a box in its body can never store its lazily built
  default, and the first read fails. Any owner whose `__setattr__`
  refuses unknown names fails the same way. `Object.__init__` has the
  same shape for its bookkeeping (`__pos_args__`, `__key_args__`,
  `__call_chain__`): item 16 moved `__set_name__` and the context stack
  to `object.__setattr__`, and left `__init__`.
- **Repro:**
  ```python
  class Pt(EZData, frozen=True):
    x = EZField[int](0)
    extra = AttriBox[list]()

  Pt().extra
  # AttributeError: 'Pt' is frozen; cannot assign to attribute
  # '__extra__attribox_field_object__'!
  # (the same for FixBox[int](7) and KeeBox[Day]('tue'))

  class Guarded(BaseObject):
    def __setattr__(self, key, value):
      if key.startswith('_'):
        raise AttributeError('private name: %s' % key)
      object.__setattr__(self, key, value)

  Guarded()  # AttributeError: private name: __pos_args__
  ```
- **Fix direction:** write the box storage and the `Object` bookkeeping
  with `object.__setattr__`, as the reads and item 16 already do. An
  explicit assignment still passes the owner's `__setattr__` first, so a
  frozen class keeps refusing `pt.extra = [...]`. Python's own
  `functools.cached_property` writes `instance.__dict__` directly for the
  same reason, and works on frozen dataclasses.
- **DONE (2026-09-28).** The storage writes of the boxes, the lazy
  default and the assignment of `AttriBox.__instance_get__` and
  `__instance_set__`, the `DELETED` marker of `__instance_delete__`, and
  the same two writes of `KeeBox`, go through `object.__setattr__`;
  `FixBox` shares the `AttriBox` paths. `Object.__init__` stores
  `__pos_args__`, `__key_args__` and `__call_chain__` the same way. An
  assignment to the field itself still passes the owner's `__setattr__`
  first, so a frozen EZData class keeps refusing it. Tests:
  `tests/test_desc/test_box_owner_setattr.py` (eight tests, an owner
  refusing private names), `tests/test_ezdata/test_frozen_box_attribute.py`
  (seven tests, boxes in a frozen EZData body) and
  `tests/test_core/test_object_init_setattr.py` (three tests). Before the
  change fifteen failed for the reasons above and the three guards
  passed: the owner does refuse private names, and a frozen class
  refuses deletion and keeps its boxes out of its fields. The suite
  gives 1553 passed on 3.14 with 100% line and branch coverage and
  passes on 3.7 to 3.13. A mutation check caught all eight breaks, each
  of the eight writes put back on `setattr` or a plain assignment, with
  the control passing.

#### 52. `Alias` breaks a staticmethod or a classmethod (medium, verified)

- **Where:** `src/worktoy/desc/_alias.py:56-67` (`__set_name__`).
- **Cause:** `__set_name__` copies `getattr(owner, realName)` onto the
  alias name. Attribute access through the class has already applied the
  descriptor protocol: it unwraps a staticmethod into a plain function,
  which then binds as an instance method, and it binds a classmethod to
  the class declaring the alias, where subclasses stay. It works for the
  boxes and `Field`, which return themselves through the class, and that
  is all the tests alias.
- **Repro:**
  ```python
  class Parent(BaseObject):
    @staticmethod
    def helper(x):
      return x * 2

    @classmethod
    def who(cls):
      return cls.__name__

  class Child(Parent):
    h = Alias('helper')
    w = Alias('who')

  class GrandChild(Child):
    pass

  Child().h(3)      # TypeError: Parent.helper() takes 1 positional
                    # argument but 2 were given
  GrandChild.who()  # 'GrandChild'
  GrandChild.w()    # 'Child'
  ```
- **Fix direction:** look the raw attribute up in the `__dict__` of each
  class along the MRO, as `inspect.getattr_static` does, and copy that.

#### 53. `KeeMeta` takes any attribute of the base for an inherited member (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:183-194`
  (`_createMembers`, the lookup at `:188`); the failure surfaces at
  `:229`.
- **Cause:** to reuse an inherited member, `_createMembers` asks
  `getattr(cls.base, key)` and takes whatever comes back. That lookup
  also finds plain class attributes: of the parent, and, for an
  enumeration whose base is itself, of the class under construction. The
  plain value then lands in the member list, and the class fails to
  build with a message that says nothing about the cause.
- **Repro:**
  ```python
  class Base(KeeNum):
    A = Kee[int](1)
    LIMIT = 10

  class Derived(Base):
    LIMIT = Kee[int](5)
  # AttributeError: 'int' object has no attribute 'name'

  class Foo(KeeNum):
    A = Kee[int](1)
    A = 5
  # AttributeError: 'int' object has no attribute 'name'
  ```
- **Fix direction:** accept only a `KeeBase` member from the lookup and
  build a new member otherwise. For a body binding a member name again
  to a plain value, raise a clear error naming the clash, such as
  `KeeDuplicate`.
- **Addition (2026-09-29, sixth read, verified):** `KeeFlags` has the
  same fault in its namespace. `KeeFlagsSpace.__init__`
  (`src/worktoy/keenum/_kee_flags_space.py:140-148`) reads `flags` off
  every base and takes each entry for an inherited flag, so a plain
  mixin carrying a `flags` attribute breaks the class with a message
  about the mixin's contents:
  ```python
  class Mixin:
    flags = ['not a flag']

  class P(KeeFlags, Mixin):
    READ = KeeFlag()
  # AttributeError: 'str' object has no attribute '__member_name__'
  ```
  Taking flags only from bases that are instances of `KeeFlagsMeta`
  fixes it.

### Decisions needed

#### 54. `EZField` defaults skip `typeCast` (verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_field.py:116` (`_construct`), used
  by the default recipes of the generated `__init__`
  (`src/worktoy/ezdata/_ez_hook.py:555-556`) and by `defaultValue`.
- **Cause:** a declared default is built by calling the field type with
  the declared arguments, while a constructor argument and an assignment
  go through `castField`, that is `typeCast`. One EZData class therefore
  accepts as a default what it refuses as an argument, and converts some
  values differently:

  | Declaration | Default | Same value as an argument |
  |---|---|---|
  | `EZField[list]('abc')` | `['a', 'b', 'c']` | `TypeException` |
  | `EZField[int](2.5)` | `2` | `TypeException` |
  | `EZField[str](5)` | `'5'` | `TypeException` |
  | `EZField[bool](2)` | `True` | `TypeException` |
  | `EZField[str](b'ab')` | `"b'ab'"` | `'ab'` |

- **Note:** the `EZField` docstring documents the default as 'T(value)',
  so this is the documented behaviour. It runs against the decision of
  item 17, a container refusing text as the default or by assignment,
  which was implemented for `AttriBox` alone, and against the EZData
  promise that every value is cast. It is the `EZField` counterpart of
  item 30, which sends `AttriBox` single values through `typeCast` in
  1.2. **DECISION:** fix it together with item 30 in 1.2, or in 1.1.0,
  and whether a single default argument goes through `typeCast` while
  several arguments and keyword arguments keep the constructor, as item
  30 plans for `AttriBox`.

#### 55. Variadic declarations are expanded into concrete signatures (verified, DECISION)

- **Where:** `src/worktoy/dispatch/_overload.py:160-203` (`_addSigFunc`)
  and `:97` (`__variadic_fastpath_limit__`);
  `src/worktoy/mcls/_base_space.py:344-416` (`_resolveCollision`,
  `_settleAmbiguity`); `src/worktoy/mcls/space_hooks/_load_space_hook.py:86-91`.
- **Cause:** `@overload(int, ARGS[str])` is not stored as one
  registration. `_addSigFunc` expands it into six concrete signatures,
  the prefix followed by zero to five copies of the inner type, so that
  short calls reach the constant-time lookup, and stores the variadic
  signature separately for longer calls. The speed-up leaks into the
  data model: the concrete registrations of a `Dispatcher` mix what the
  class body declared with copies the machinery made. Split off item 38
  on 2026-09-29. Symptoms:
  - `DispatchException` listed the six expansions under "available
    signatures" and never the declaration itself. **Fixed on its own on
    2026-09-29** (see item 38): the message now filters the expansions
    by their marker and lists the variadic signatures.
  - Item 21: `swapTHIS` reaches the expansions but not the `ARGS[THIS]`
    of the variadic entry, so `ARGS[THIS]` stops matching past five
    arguments.
  - `BaseSpace` carries collision rules for the artifacts: an explicit
    declaration displaces an expansion, and two variadics expanding to
    the same signature for different functions are recorded as ambiguous
    until an explicit declaration settles them, with the
    `__expanded_from_variadic__` marker telling the kinds apart.
  - `__variadic_fastpath_limit__ = 5` is an arbitrary cut-off in the
    speed of dispatch.
  - L12: `Dispatcher.overload` by hand has no variadic route at all.
- **Repro:**
  ```python
  class Baz(BaseObject):
    @overload(int, ARGS[str])
    def qux(self, *args):
      pass

  Baz().qux('no', 'int')
  # DispatchException: ... available signatures:
  #   <TypeSig: [int]>
  #   <TypeSig: [int, str]>
  #   ... up to <TypeSig: [int, str, str, str, str, str]>
  # and no <TypeSig: [int, ARGS[str]]>
  ```
- **Proposal:** keep a variadic declaration as exactly one registration,
  and give the `Dispatcher` an exact-type pass over the variadic
  signatures, the prefix and each tail argument compared by exact type,
  ahead of the `isinstance` passes. That costs a loop over the arguments
  of the call rather than a dict lookup. The expansions, the marker, the
  ambiguity bookkeeping and the limit go, item 21 is solved on the way,
  and the message of item 38 no longer needs its filter.
  **Note (2026-09-29):** the expansions also do real work. Two variadics
  sharing a prefix, `f(int, *ARGS[str])` and `f(int, *ARGS[int])`, both
  expand `(int,)`, which is how class creation detects that a call
  `f(5)` fits both and raises `DuplicateSignature` unless an explicit
  `@overload(int)` settles it (`tests/test_overload/test_variadic_prefix_overlap.py`).
  The redesign has to keep that rule by comparing variadic signatures
  directly, whether any call length fits both, and two tests are built
  on `__variadic_fastpath_limit__`. Item 21 has its own small fix and
  does not need to wait.
  **DECISION:** a redesign of the variadic path in `overload`, `BaseSpace`
  and the `Dispatcher`, with a new overlap check; recommended for 1.2.

### Low severity

- **L31. `typeCast(slice, ...)` reads a one-element sequence as a start
  (verified).** `src/worktoy/utilities/_type_cast.py:34-39` pads a list or
  tuple to three entries as `(start, stop, step)`, where Python's own
  `slice(*seq)` takes one argument as the stop:
  `typeCast(slice, 5)` and `slice(*[5])` give `slice(None, 5, None)`,
  but `typeCast(slice, [5])` and `typeCast(slice, (5,))` give
  `slice(5, None, None)`. Two and three entries agree with `slice(*seq)`.
- **L32. `KeeFlags` takes a bool as an index (verified).**
  `src/worktoy/keenum/_kee_flags_meta.py:275-276`. `Perm(True)` and
  `Perm[True]` are `Perm.READ`, `Perm(False)` is `Perm.NULL`, and
  `True in Perm` is `True`, where `KeeNum` refuses a bool index
  (`Day[True]` raises `KeeResolveError`) and so does `KeeBox`.
- **L33. `KeeFlagsMeta` pins `_getValue`, which breaks a diamond
  (verified).** `src/worktoy/keenum/_kee_flags_meta.py:132-145` writes the
  chosen getter into the `__dict__` of every flags class. In
  `class Both(Left, Right)`, with `Base` and `Right` both overriding
  `_getValue`, the copy of `Base`'s getter pinned on `Left` is found
  before `Right`'s override: `Both.A.value` is `'base-1'`, where Python's
  own lookup (`Both`, `Left`, `Right`, `Base`) reaches `Right` first. The
  walk already skips the pinned default of `KeeFlags` itself; the pinned
  overrides of a base need the same treatment, or the pinning can go,
  since the `value` field finds `_getValue` by name along the MRO anyway.
- **L34. A `ControlFlow` subclass cannot use `super()` in `__str__`
  (verified).** `src/worktoy/waitaminute/control_flow/_control_space.py:29-35`
  allows `__str__` and `__repr__` but not the `__classcell__` the
  interpreter adds for a method using `super()` or `__class__`, so the
  class fails with `ControlClassError: ... tried implementing attribute
  '__classcell__'!`. Adding `__classcell__` to the white list fixes it.
- **L35. `Object.directory` fails without `__file__` (verified).**
  `src/worktoy/utilities/_directory.py:29-31` reads `__file__` from the
  module of the class, and a module without one, as in the REPL or under
  `exec`, makes every `obj.directory` raise a bare `AttributeError` from
  inside the descriptor.
- **L36. `ComplexMixin` edge cases (verified).**
  `src/worktoy/work_test/_complex_mixin.py`. Division compares the squared
  magnitude of the divisor with `sys.float_info.epsilon` (`:262-264`), so
  `Z(3, 4) / 1e-8` raises `ZeroDivisionError`, where `(3+4j) / 1e-8` is
  fine. `__init__` drops components past the second (`:111-113`), so
  `Z(1, 2) == (1, 2, 99)` is `True`. `repr(Z(1e-20, 0))` is `'Z()'`.
- **L37. Smaller points (verified unless marked read).**
  - `textFmt` keeps the whitespace next to a `<br>`, so a message with
    `<br>` at the end of a source line gets a trailing space before the
    line break and a leading space after it: a line of the
    `DuplicateSignature` message reads " rejected duplicate:"
    (`src/worktoy/utilities/_text_fmt.py:68-74`).
  - `QuickDesc` refuses writes and deletions with a plain
    `AttributeError` (`src/worktoy/utilities/_quick_desc.py:72-84`),
    where `Directory` in the same package raises `ReadOnlyError` and
    `ProtectedError` (read).
  - `KeeMeta.__init__` writes `__class_name__` on every enumeration
    class, and nothing reads it (`src/worktoy/keenum/_kee_meta.py:452`;
    read).
  - `repr(Arrangement(('a', 'b'), (1, 0)))` is `Arrangement(a, b, 1, 0)`:
    items and indices in one list, through `str()`
    (`src/worktoy/utilities/combinatorics/_arrangement.py:107-112`; read).
  - `SymbolicSampler.wordCount` accepts `0` and negative counts
    (`src/worktoy/work_test/samplers/_symbolic_sampler.py:85-87`), where
    `colCount` and `rowCount` refuse them (read).
  - `KeeFlags.__iter__` is hinted `Iterator[Self]` but yields the high
    `KeeFlag` objects (`src/worktoy/keenum/_kee_flags.py:230-231`; read).
  - Messages: `ExtraPositionalException` says "has 1 fields";
    `KeeMeta.__str__` says "<KeeNum 'X': 1 members>", and says `KeeNum`
    for the enumerations of a custom metaclass too; `PhantomBoxError`
    says "rather than a 'AttriBox'"; `UnboundClassHook` says "plain
    function" for a staticmethod (read).

---

## Group K: Fifth source read before 1.1.0 (open)

Files: various

On 2026-09-29 a Claude session read every file in `src/worktoy` (164
files, 19,886 lines) a fifth time, in the layer order from
`src/worktoy/__init__.py`, checking each candidate against the open
items of groups G to J so that none is repeated here. Each item below
was reproduced with a throwaway script on 3.14 and again on 3.7, and the
text says where the two differ. At the time the suite gave 1625 passed
on 3.14 with 100% line and branch coverage, 50 of them the empty runs of
L38, and it catches none of these items. The read also added to L20 and
L23; each addition is marked at its item.

The repros assume these imports and helpers:

```python
import pickle

from worktoy.core.sentinels import ARGS, THIS
from worktoy.desc import AttriBox
from worktoy.dispatch import overload, Dispatcher
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag
from worktoy.mcls import BaseObject, BaseMeta
from worktoy.utilities import typeCast


class MyStr(str):
  pass


class MyInt(int):
  pass
```

### Fix before 1.1.0

#### 57. `@overload` accepts anything as a type (medium, verified)

- **Where:** `src/worktoy/dispatch/_overload.py:223-254`
  (`overload.__new__`), with the `isinstance` passes at
  `src/worktoy/dispatch/_dispatcher.py:244-272`.
- **Cause:** `overload` builds its `TypeSig` from whatever it receives
  and checks none of it. The class builds, and the exact-type lookup
  still serves its signatures, but a call that misses that lookup reaches
  the `isinstance` pass, where the first entry that is not a class raises
  Python's own `TypeError` before any later signature, the cast passes or
  the fallback get a turn. It is the dispatch counterpart of item 18,
  done for the boxes, and of item 33, open for `EZField`, and L23 is one
  case of it.
- **Repro:**
  ```python
  class Foo(BaseObject):
    @overload(list[int])
    def bar(self, x):
      return 'list'

    @overload(str)
    def bar(self, x):
      return 'str'

  Foo().bar('x')         # 'str', by exact type
  Foo().bar(MyStr('x'))  # TypeError: isinstance() argument 2 cannot be a
                         # parameterized generic
  ```
  `@overload(5)` and `@overload('int')` build the same way on every
  version and fail every call. `@overload(Optional[int])` works on 3.14,
  where `isinstance` takes it as a union, and fails like `list[int]` on
  3.7 ("Subscripted generics cannot be used with class and instance
  checks").
- **Fix direction:** refuse in the decorator every entry that is neither
  a class, judged as item 18 judges one (`issubclass(type(entry),
  type)`), nor an `ARGS` whose inner type is one, with `TypeException`
  naming the entry. `THIS` and `OWNER` are sentinel classes and pass that
  test, so L23 still needs its own refusal. `Dispatcher.overload` by hand
  wants the same check.

#### 58. `typeCast` to a subclass of a builtin skips the lossless rules (medium, verified)

- **Where:** `src/worktoy/utilities/_type_cast.py:226-241`.
- **Cause:** the handlers of `str`, `bool`, `int`, `float`, `complex` and
  `dict` are looked up by the exact target, so a subclass of one goes to
  the constructor fallback, which rounds or truncates without a word.
  `typeCast(int, 2.5)` refuses, while `typeCast(MyInt, 2.5)` returns `2`,
  a `MyInt`. Through `EZHook.castField` an `EZField[MyInt]` stores `2.5`
  as `2` where an `EZField[int]` refuses it, and the cast passes of an
  overloaded method take the truncated value for a `MyInt` signature. The
  same fallback serves the builtins without a handler: `typeCast(bytes,
  5)` gives five zero bytes.
- **Repro:**
  ```python
  typeCast(int, 2.5)    # TypeCastException
  typeCast(MyInt, 2.5)  # 2

  class Z(EZData):
    n = EZField[MyInt](MyInt(0))
    m = EZField[int](0)

  Z(n=2.5).n  # 2
  Z(m=2.5)    # TypeException
  ```
- **Fix direction:** find the first class along the target's method
  resolution order that has a handler, cast to that base with it (a value
  already of the base needs no cast), then build the target from the
  result and keep the instance check. How the fallback treats `bytes`
  and the other builtins without a handler belongs with item 30.
- **Addition (2026-09-29, sixth read, verified on 3.14 and 3.7):** the
  zero bytes reach dispatch as well. The cast pass tries the signatures
  in order, `typeCast(str, 3)` refuses and `typeCast(bytes, 3)` does
  not, so an integer lands in a `bytes` overload as zero bytes:
  ```python
  class Disp(BaseObject):
    @overload(bytes)
    def f(self, b):
      return ('bytes', b)

    @overload(str)
    def f(self, s):
      return ('str', s)

  Disp().f(3)  # ('bytes', b'\x00\x00\x00')
  ```
  `EZField[bytes]` and `AttriBox[bytes]` store an assigned `4` as
  `b'\x00\x00\x00\x00'` the same way.

#### 59. A KeeNum lookup by an unhashable value raises `TypeError` (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:514-517`
  (`_resolveFromValue`), reached from `_resolveMember` (`:572-575`) and
  `fromValue` (`:584-589`).
- **Cause:** the lookup by value indexes `valuedMembers` with the
  identifier, which then has to hash. An instance of the value type need
  not: a tuple holding a list, or any unhashable object under
  `Kee[object]`. Python's `TypeError` escapes where a miss raises
  `KeeResolveError`. `KeeBox` compares with `==` and is not affected.
- **Repro:**
  ```python
  class Pairs(KeeNum):
    A = Kee[tuple]((1, 2))

  Pairs((1, 2))              # Pairs.A
  Pairs((1, [2]))            # TypeError: cannot use 'tuple' as a dict key
                             # (unhashable type: 'list')
  Pairs.fromValue((1, [2]))  # the same
  ```
  On 3.7 the message reads "unhashable type: 'list'".
- **Fix direction:** hash the identifier first, and when that fails take
  the linear scan the method already uses when a member value is
  unhashable.

#### 60. A `__class_resolve__` without `@classmethod` breaks the lookups past the names (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:277-294`
  (`_validateClassResolve`) and `:561-564`; the names `UnboundClassHook`
  covers are listed in `src/worktoy/mcls/space_hooks/_name_hook.py:65-107`.
- **Cause:** `_validateClassResolve` only asks whether the hook is
  callable. A routed `__class_*__` hook bound to a plain function is
  refused in the class body with `UnboundClassHook`, but
  `__class_resolve__` belongs to `KeeMeta` and is not on that list, so a
  plain function passes, and every lookup that reaches the hook calls it
  unbound, lookups by index and by value included. Only names, resolved
  before the hook, still work.
- **Repro:**
  ```python
  class Num(KeeNum):
    A = Kee[int](1)

    def __class_resolve__(cls, identifier):
      return NotImplemented

  Num('A')  # Num.A
  Num(1)    # TypeError: Num.__class_resolve__() missing 1 required
            # positional argument: 'identifier'
  Num[0]    # the same
  ```
- **Fix direction:** refuse a plain function or a staticmethod bound to
  `__class_resolve__` at the offending line with `UnboundClassHook`, from
  `KeeSpace`. Item 48 concerns the `__class_*__` hooks on enumerations
  in general.

#### 61. `Dispatcher.clone` shares its signatures with the original (medium, verified)

- **Where:** `src/worktoy/dispatch/_dispatcher.py:606-632` (`clone`),
  `:751-769` (`swapAllTHIS`), `src/worktoy/dispatch/_type_sig.py:279-300`
  (`swapTHIS`).
- **Cause:** `clone` hands the copy the very `TypeSig` objects of the
  original, and `swapTHIS` rewrites a signature in place when its
  dispatcher is set on a class. Clones of a dispatcher whose signatures
  still hold `THIS`, placed on two classes, therefore resolve `THIS` to
  whichever class came first, for both and for the original. The
  documented use, cloning a dispatcher already on a class as in
  `tests/test_dispatch/examples/_space_point.py`, holds no `THIS` any more
  and is not affected.
- **Repro:**
  ```python
  d = Dispatcher()

  @d.overload(THIS)
  def f(self, other):
    return 'this'

  class A:
    x = d.clone()

  class B:
    y = d.clone()

  A().x(A())  # 'this'
  B().y(B())  # DispatchException; the signature of 'B.y' reads [A]
  ```
- **Fix direction:** give the clone copies of the signatures, carrying
  `__allow_flex__` and the `__expanded_from_variadic__` marker.

### Decisions needed

#### 62. Every value a box builds carries the box, so user objects built by `AttriBox` or `Kee` refuse pickling (medium, verified, DECISION)

- **Where:** `src/worktoy/desc/_attri_box.py:335-340` (the end of
  `_resolve`), reached by `Kee.getValue`
  (`src/worktoy/keenum/_kee_member.py:82`); pinned by
  `tests/test_desc/test_box.py:77`.
- **Cause:** `_resolve` writes `__field_name__`, `__field_owner__` and
  `__field_box__` onto every value it builds, through the value's own
  `__setattr__`, ignoring only `AttributeError`. Since item 50 the box
  refuses pickling, so a plain, picklable user class built as a box
  default, or as the value of an enumeration member, now refuses too,
  naming `AttriBox` or `Kee`. The three names also land in the value's
  `__dict__`: an `__eq__` or `__repr__` built on `vars()` changes, a deep
  copy of the value deep-copies the box along with it, and a field type
  whose `__setattr__` refuses with anything but `AttributeError` cannot
  be held at all. A value assigned already of the field type is stored as
  it is and gets no tags, so whether a value carries them depends on how
  it arrived. Nothing in `src` reads `__field_box__`; only the test does.
- **Repro:**
  ```python
  class Config:
    def __init__(self, x=1):
      self.x = x

    def __eq__(self, other):
      return vars(self) == vars(other)

  class App(BaseObject):
    cfg = AttriBox[Config]()

  app = App()
  sorted(vars(app.cfg))  # ['__field_box__', '__field_name__',
                         #  '__field_owner__', 'x']
  pickle.dumps(Config())  # works
  pickle.dumps(app.cfg)   # PickleException: Objects of type 'AttriBox'
                          # cannot be pickled! ...
  app.cfg == Config()     # False
  app.cfg = Config(7)
  sorted(vars(app.cfg))   # ['x']

  class RGB:
    def __init__(self, r=0, g=0, b=0):
      self.r, self.g, self.b = r, g, b

  class Color(KeeNum):
    RED = Kee[RGB](255, 0, 0)

  pickle.dumps(Color.RED.value)  # PickleException: ... 'Kee' ...

  class Strict:
    def __setattr__(self, key, value):
      raise TypeError('immutable')

  class Holder(BaseObject):
    s = AttriBox[Strict]()

  Holder().s  # TypeError: immutable
  ```
- **Options:** stop tagging, which removes the three writes and the
  assertion at `test_box.py:77` and leaves user objects as their class
  made them; or tag only values that are themselves worktoy objects,
  which carry these names already; or keep the tags and document that a
  value built by a box refers to it and cannot be pickled. Recommended:
  stop tagging.
- **Correction (2026-09-29):** the tags are a feature, not a leftover:
  they let an object know the box that made it, which worQt, a separate
  project of the author's, relies on. `tests/test_desc/test_box.py` and
  its fixture `BoxedFloat` test them as such. A suite run without the
  tags failed `testSetName` and `testBoxedFloat`. The pickling cost does
  not count under the project's policy of refusing pickling; the other
  costs do: a field type whose `__setattr__` refuses with anything but
  `AttributeError` could not be held at all; frozen dataclasses, frozen
  EZData instances and `__slots__` classes went untagged without a word;
  an assigned object went untagged; the tags go into `vars()`; and a deep
  copy of a tagged value carries a detached copy of the box.
- **DECIDED (2026-09-29):** keep the tags and make them reliable, in three
  parts. 62a: move the tagging into a method of its own, write the tags
  with `object.__setattr__`, and leave untagged what the box did not
  create or cannot tag, enumeration members and objects without an
  instance dict included. 62b, tagging assigned objects too, was
  declined: assignment falls outside the worQt use, so the tags are
  documented as naming the box that created the object rather than one
  holding it. 62c: give the boxes a `__copy__` and `__deepcopy__`
  returning the box itself, decided after a second explanation, with the
  author asking for it to be documented very precisely. `desc` loads
  before `keenum` and
  cannot name its classes, so the enumerations opt out through a class
  attribute; the author named it `__no_box_tag__`, and the method
  `_applyTags`.
- **DONE, 62a (2026-09-29).** `AttriBox._applyTags`
  (`src/worktoy/desc/_attri_box.py`), called at the end of `_resolve`,
  writes `__field_name__`, `__field_owner__` and `__field_box__` with
  `object.__setattr__`, and leaves untagged: one of the arguments the
  object was built from, handed back as it was (a default that refuses
  to be copied or copies to itself); a class; an instance of a class
  declaring `__no_box_tag__` as true; an `Enum` member; and an object
  without an instance dict. `KeeBase` and `KeeFlags` declare
  `__no_box_tag__ = True`, since a member reached through a box, as in
  `AttriBox[Day]('MON')`, would otherwise be tagged past its freeze. The
  class docstring of `AttriBox` and the docstring of `_applyTags` state
  that the tags name the box that created the object. Test:
  `tests/test_desc/test_box_tags.py` (thirteen tests). The eight
  regression tests failed before the change (a strict `__setattr__`
  held and tagged, a frozen dataclass and a frozen EZData instance
  tagged, and a `__no_box_tag__` class, an `Enum` member, an uncopyable
  default, a self-copying default and a created class left untagged) and
  the five guards passed (a plain value tagged, and a slotted value,
  KeeNum and KeeFlags members and an assigned value left untagged). The
  suite gives 1670 passed on 3.14 with 100% line and branch coverage and
  passes on 3.7 to 3.13. A mutation check caught all eleven breaks with
  the control passing: the method never called, a plain `setattr`, each
  of the five rules removed, either marker removed, and the wrong box or
  field name written.
- **DONE, 62c (2026-09-29).** `AttriBox.__copy__` and
  `AttriBox.__deepcopy__` return the box itself, in place of the copying
  `NoPickle` provides; `FixBox`, `Kee` and `KeeBox` inherit them, and
  `FastBox`, which creates no tags, keeps the copying of `NoPickle`.
  Before, a deep copy of a tagged object carried a new `AttriBox` of the
  same name and owner, installed on no class, with deep copies of the
  captured default arguments. The docstring of `__deepcopy__` states
  the behaviour, the reason (a box is part of its class, as a method is)
  and the ways to get a separate box (subscript and call again, or
  `Kee.clone`); the class docstrings of `AttriBox` and `NoPickle` point
  to it. Tests: `tests/test_desc/test_box_copy.py` (six tests), and
  `tests/test_utilities/test_no_pickle_classes.py`, whose
  `test_copy` and `test_deepcopy` pinned every object as copying to a
  new one: the four boxes moved to the new `test_boxes_copy_to_themselves`,
  beside the enumeration members. The six regression tests failed before
  the change (deep copies of objects created by an `AttriBox`, a
  `FixBox` and a `Kee`, of the owning instance and of the box defaults,
  and the boxes copying to themselves) and the shallow-copy guard
  passed. The suite gives 1677 passed on 3.14 with 100% line and branch
  coverage and passes on 3.7 to 3.13. A mutation check caught all four
  breaks with the control passing: either method removed, and either
  method falling back on the copying of `NoPickle`.

#### 63. Class keywords reach `object.__init_subclass__`, so `trustMeBro=True` fails outside `Object` (medium, verified, DECISION)

- **Where:** `src/worktoy/mcls/_abstract_metaclass.py:170` and
  `src/worktoy/core/_meta_type.py:36-39`, which hand the class keywords
  on to `type.__new__`; `src/worktoy/core/_object.py:310-314`
  (`Object.__init_subclass__`).
- **Cause:** every class keyword worktoy uses, `trustMeBro`,
  `_strictMRO` and the EZData options, goes on from the namespace to
  `type.__new__` and from there to `__init_subclass__`.
  `Object.__init_subclass__` swallows them all, which is the only reason
  they work. A worktoy class without `Object` among its bases hands them
  to `object.__init_subclass__`, which refuses any keyword: every
  `KeeFlags` class, every `BaseTest` class, and any class declaring
  `metaclass=BaseMeta` alone. For a `KeeFlags` class, `DelException`
  itself tells the user to pass `trustMeBro=True`, which then fails with
  an unrelated `TypeError`. The swallowing has a second side: a
  cooperative base that comes after `Object` in the method resolution
  order never receives its own keyword.
- **Repro:**
  ```python
  class Perm(KeeFlags, trustMeBro=True):
    READ = KeeFlag()

    def __del__(self):
      pass
  # TypeError: Perm.__init_subclass__() takes no keyword arguments

  class Plain(metaclass=BaseMeta, trustMeBro=True):  # the same
    def __del__(self):
      pass

  class Tagged:
    def __init_subclass__(cls, tag=None, **kwargs):
      super().__init_subclass__(**kwargs)
      cls.tag = tag

  class A(BaseObject, Tagged, tag='hello'):
    pass

  A.tag  # None; with the two bases swapped, 'hello'
  ```
  On 3.7 the message reads "__init_subclass__() takes no keyword
  arguments".
- **Options:** give `KeeFlags` and `BaseTest` an `__init_subclass__`
  that swallows keywords as that of `Object` does, and say in the
  `BaseMeta` docstring that a class using it without `Object` needs one
  too, which fixes the cases above and keeps today's rules; or have
  `AbstractMetaclass.__new__` pass no keywords to `type.__new__`, since
  the namespace keeps them anyway (`__keyword_arguments__`), which makes
  `Object.__init_subclass__` unnecessary but also stops the keyword of a
  plain mixin from passing through a worktoy class statement in either
  order; or settle it with item 64, each consumer declaring the keywords
  it takes and only the rest going on to `__init_subclass__`.
- **DECIDED (2026-09-29):** fix it. The author's observation: every
  class worktoy introduces with a custom metaclass without basing it on
  `Object` has this problem, not only `KeeFlags` and `BaseTest`. A first
  version kept all class keywords from `type.__new__` and removed
  `Object.__init_subclass__`; the author found that too drastic and chose
  to keep the forwarding, withholding the keywords only where
  `object.__init_subclass__` alone would receive them.
- **DONE (2026-09-29).** `MetaType.__new__` forwards the class keywords
  to `type.__new__` as before, unless no class along the method
  resolution order of the bases, `object` aside, defines
  `__init_subclass__` in its own `__dict__` (the new module function
  `_takesKeywords` in `src/worktoy/core/_meta_type.py`); then it withholds
  them. The namespace records them either way, and `__class_init__`
  receives them either way. `BaseTest` gains the same keyword-swallowing
  `__init_subclass__` as `Object`, since its base `TestCase` defines one
  that passes keywords on to `object`. `Object.__init_subclass__` and the
  forwarding to a base's own `__init_subclass__` are unchanged. The
  `MetaType` class docstring states the rule. Test:
  `tests/test_mcls/test_meta/test_class_keywords.py` (eight tests: a
  class declaring only `metaclass=BaseMeta`, `_strictMRO`, a `KeeFlags`
  class and a `BaseTest` class each taking a keyword, `__class_init__`
  receiving the keywords of a class not based on `Object`, a base's own
  `__init_subclass__` still receiving them, directly or further up the
  method resolution order, a class based on `Object` built by `MetaType`
  taking one, and the namespace recording them). Five tests failed before
  the change and the three guards passed. The suite gives 1641 passed on
  3.14 with 100% line and branch coverage and passes on 3.7 to 3.13. A
  mutation check caught all five breaks, with the control passing: no
  check at all, never forwarding, `object` counted as defining
  `__init_subclass__`, and `BaseTest` without its method; the fifth,
  looking at each base's own `__dict__` only, survived until the guard
  gained a base defining `__init_subclass__` further up.

#### 64. A misspelled class keyword is dropped without a word (medium, verified, DECISION)

- **Where:** `src/worktoy/core/_object.py` (`Object.__init_subclass__`),
  `src/worktoy/ezdata/_ez_hook.py:78-80` (the synonyms) and `:327-332`
  (`parseKwargs`).
- **Cause:** `parseKwargs` looks for the known spellings of the three
  EZData options and ignores everything else, and
  `Object.__init_subclass__` accepts any keyword, so no class keyword is
  ever refused. `class Q(EZData, frozn=True)` builds a mutable class, and
  `order=True`, the spelling of `dataclasses`, is not among the synonyms
  (`ordered`, `sortable`, `comparable`), so such a class has no ordering
  and each comparison raises far from the class statement. Item 45 is the
  same policy for the keywords of the generated `__init__`; at the class
  statement a misspelling is cheapest to catch. `BaseObject` accepts any
  keyword as well.
- **Repro:**
  ```python
  class Q(EZData, frozn=True):
    x = EZField[int](0)

  Q.isFrozen  # False

  class R(EZData, order=True):
    x = EZField[int](0)

  R(1) < R(2)  # TypeError: '<' not supported between instances of 'R'
               # and 'R'

  class S(BaseObject, anything=42):  # builds
    pass
  ```
- **Options:** refuse unknown class keywords, which needs each consumer
  (the namespace hooks, `EZHook`, the enumeration metaclasses) to declare
  the keywords it takes, and is best decided together with item 63; or
  refuse unknown keywords on EZData classes alone, where `EZHook` knows
  every option. Independently: whether `order` joins the ordered
  synonyms.
- **After item 63 (2026-09-29):** a class that no `__init_subclass__`
  but that of `object` would receive keywords for now drops them too,
  instead of failing, so no class built by a worktoy metaclass refuses an
  unknown class keyword any more: `class Q(EZData, frozn=True)` still
  builds a mutable class.
- **DECIDED (2026-09-29):** refuse unknown class keywords on EZData
  classes alone, where every option is known, and accept `order` among
  the spellings of `ordered`, so every `dataclasses` spelling (`frozen`,
  `order`, `kw_only`) works. Other worktoy classes keep accepting any
  keyword, since there a keyword may be meant for a user's own hook or a
  mixin's `__init_subclass__`, and nothing lists those.
- **DONE (2026-09-29).** `EZHook.preparePhase` refuses any class keyword
  that is none of the spellings in `__frozen_keys__`, `__ordered_keys__`
  and `__kw_only_keys__`, nor one of the new `__space_keys__`
  (`trustMeBro`, `_strictMRO`) the namespace reads, with the new
  `ClassKeywordError` (`src/worktoy/waitaminute/ezdata/_class_keyword_error.py`,
  a `TypeError` with `clsName`, `keyword` and `accepted`, whose message
  lists the accepted keywords). It runs as the namespace is created, so
  the error points at the class statement before the class body runs.
  `order` joins `__ordered_keys__`. The docstrings of `EZHook`, `EZData`
  and `EZMeta.isOrdered` say so. Known limit: an EZData class also based
  on a mixin whose `__init_subclass__` takes a keyword of its own has that
  keyword refused; item 66 takes that up for 1.2. Test:
  `tests/test_ezdata/test_class_keyword_refused.py`
  (six tests); the four regression tests failed before the change and
  the two guards (every spelling of every option, and the namespace
  keywords) passed. The suite gives 1647 passed on 3.14 with 100% line
  and branch coverage and passes on 3.7 to 3.13. A mutation check caught
  all six breaks with the control passing: no check, `order` dropped, no
  `__space_keys__`, the `kwOnly` spellings left out of the accepted list,
  the wrong keyword named, and the accepted list missing from the
  message.

#### 65. EZData replaces a class-body `__match_args__` without a word (medium, verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:146-147` (the reserved names
  pass through) and `:334-336` (the generated tuple).
- **Cause:** `__match_args__` is in `ReservedNames`, so `setItemPhase`
  lets a class-body binding through to the namespace, and
  `postCompilePhase` then writes the generated tuple over it. Item 25
  refused every method EZData replaced without a word; `__match_args__`
  is the one generated attribute left.
- **Repro:**
  ```python
  class P(EZData):
    x = EZField[int](0)
    y = EZField[int](0)
    __match_args__ = ('y',)

  P.__match_args__  # ('x', 'y')
  ```
- **Options:** refuse it in the class body as item 25 refuses the
  methods, which needs `ReservedMethodError`, or a sibling of it, to
  speak of an attribute; or keep the class body's tuple in place of the
  generated one, as `dataclasses` does.
- **DECIDED (2026-09-29):** keep the class body's tuple, generating one
  only when the class body sets none, the rule `dataclasses`,
  `typing.NamedTuple` and `attrs` share (checked against the interpreter
  and, for `attrs`, its source). A subclass whose body sets none receives
  the generated tuple of all its fields, not its parent's. The tuple is
  not checked against the field names. The author asked for the rule to
  live in `EZHook.matchArgsFactory`. A suite run against a copy of `src`
  keeping the tuple showed that nothing relied on the override.
- **DONE (2026-09-29).** `EZHook.matchArgsFactory` takes the namespace
  assembled so far as a new third argument, `classBody`, and returns
  its `__match_args__` as it is when the class body set one; nothing but
  the class body writes that name before `postCompilePhase` runs.
  Otherwise it generates as before. The docstrings of `matchArgsFactory`,
  `postCompilePhase`, `EZData` and `EZMeta.kwOnly` say so. Test:
  `tests/test_ezdata/test_match_args_class_body.py` (six tests). The
  four regression tests failed before the change (a subset, another
  order, an empty tuple, and a keyword-only class keeping its tuple) and
  the two guards passed (a class body setting none, and a subclass
  receiving the generated tuple). The suite gives 1683 passed on 3.14
  with 100% line and branch coverage and passes on 3.7 to 3.13 (3.7 once
  the author had parenthesized the annotated key tuples at
  `_ez_hook.py:84-88`, which an edit outside the audit work had left
  valid only from 3.8). A mutation check caught all five
  breaks with the control passing: the class-body rule removed, the
  keyword-only rule moved before it, the keyword-only rule removed, an
  empty class-body tuple ignored, and an empty dict passed in place of
  the namespace.

### Planned for 1.2

#### 66. An EZData class refuses the class keyword of a base's own `__init_subclass__` (verified, planned for 1.2)

- **Where:** `src/worktoy/ezdata/_ez_hook.py` (`EZHook.preparePhase`,
  from item 64).
- **Cause:** split off item 64 on 2026-09-29. `preparePhase` accepts only
  the option spellings and `__space_keys__`, so an EZData class also
  based on a class whose `__init_subclass__` takes a keyword of its own
  has that keyword refused with `ClassKeywordError`, although item 63
  forwards it to that `__init_subclass__` everywhere else.
- **Repro:**
  ```python
  class Tagged:
    def __init_subclass__(cls, tag=None, **kwargs):
      super().__init_subclass__(**kwargs)
      cls.tag = tag

  class Point(EZData, Tagged, tag='hello'):
    x = EZField[int](0)
  # ClassKeywordError: ... received the class keyword 'tag' ...
  ```
- **Direction:** accept a keyword that an `__init_subclass__` along the
  bases, other than those of `object` and `Object`, declares as a
  parameter, or let such a base declare the keywords it takes. Decide
  which in 1.2.

### Low severity

- **L38. `ComplexTest` runs as a test wherever it is imported
  (verified).** `src/worktoy/work_test/_complex_test.py:18-36`.
  `ComplexTest` is a `TestCase` with 25 test methods and `targets = ()`,
  and both pytest and `unittest` collect every `TestCase` class they find
  in a test module, imported ones included.
  `tests/test_work_test/test_complex_mixin.py:13` and
  `tests/test_ezdata_examples/test_ez_complex.py:11` import it, so 50 of
  the passes run the 25 methods against no targets; `pytest
  --collect-only -q` on the two files lists 50 ids under
  `::ComplexTest::`. Its `tearDownClass`, inherited from `BaseTest`, then
  pops `cls.__module__` from `sys.modules`, which for `ComplexTest` is
  the library module `worktoy.work_test._complex_test`, so a later import
  of it builds a second `ComplexTest` class. Fix direction: have
  `ComplexTest` skip itself from `setUpClass` when `targets` is empty,
  which both runners honour, or keep it out of the namespace of the
  importing modules.
- **L39. `str()` of a `Dispatcher` lists the variadic expansions
  (verified).** `src/worktoy/dispatch/_dispatcher.py:586-598` lists
  `_getSigFuncList()` as it stands, so a `Dispatcher` built from
  `@overload(int, ARGS[str])` shows the six concrete signatures and never
  the declaration. Item 38 fixed the same listing in `DispatchException`
  alone; its filter applies here too.
- **L40. `@overload` over `@staticmethod` or `@classmethod` fails at the
  first call (verified).** `src/worktoy/dispatch/_overload.py:244-252`
  stores the staticmethod or classmethod object as the function, and the
  `Dispatcher` calls it with the instance first: `Foo().st(1)` raises
  "Foo.st() takes 1 positional argument but 2 were given" on 3.14 and
  "'staticmethod' object is not callable" on 3.7, and `Foo().cm(1)` raises
  "'classmethod' object is not callable". Refuse both in the decorator.
- **L41. A `KeyError` bound in a class body cannot be read back there
  (verified).** `src/worktoy/mcls/_abstract_namespace.py:248-265`.
  `__getitem__` keeps the caught `KeyError` as its marker for a missing
  name and tests `isinstance(val, KeyError)` afterwards, so a stored
  `KeyError` instance reads as missing: `ERR = KeyError('x')` followed by
  `other = ERR` raises `NameError: name 'ERR' is not defined` in a
  worktoy class body, where a plain class reads it. A private marker
  object fixes it.
- **L42. `KeeMeta.keeNum` is a `Field` without a getter (verified).**
  `src/worktoy/keenum/_kee_meta.py:118`. The declaration only serves the
  type hints, and at run time `WeekDay.keeNum` raises `AccessError`
  ("The 'Field' descriptor at 'KeeMeta.keeNum' failed to retrieve a
  value!"), while `KeeMeta.keeNum` works through `KeeMetaMeta`. Move it
  under `TYPE_CHECKING` or remove it.
- **L43. `AttriBox.__instance_set__` honours an undocumented `_root`
  keyword (read).** `src/worktoy/desc/_attri_box.py:380` stores any value
  unchecked when called with `_root=True`, past the rule of L11 that a
  field holds an instance of its field type. Nothing in `src` or `tests`
  passes it. Remove it.
- **L44. `NoPickle` copies lose name-mangled slots (verified).**
  `src/worktoy/utilities/_no_pickle.py:40-49` reads each slot by the name
  it was declared with, so a slot declared `__secret`, stored as
  `_Slotted__secret`, is skipped without a word and missing from the
  copy. worktoy itself never mangles, but `NoPickle` is public and
  promises copies "the way that protocol did", and `copyreg._slotnames`
  mangles. Mangle a name that starts with two underscores and does not
  end with two.
- **L45. The refusals of `Directory` name the field `object`
  (verified).** `ReadOnlyError` and `ProtectedError` read
  `__field_name__`, which `Directory` never sets
  (`src/worktoy/utilities/_directory.py:18-41`), so `Foo().directory =
  'x'` reports "read-only attribute 'Foo.object'" and `del
  Foo().directory` reports "'Foo.object' with value: 'None'". A
  `__set_name__` on `Directory` fixes both.
- **L46. The copy constructors of the lorem generators drop `isFirst`
  and share their parts (verified).**
  `src/worktoy/lorem_ipsum/_clause.py:180-186`, `_sentence.py:103-109` and
  `_paragraph.py:109-115` copy the character count and the cached arrays
  but not `__is_first__`, so `Clause(Clause.first(40)).isFirst` is
  `False` although its words begin with 'Lorem ipsum', and a `reset()` of
  the copy then loses the lead-in. `Sentence` and `Paragraph` copy the
  list but keep its `Clause` or `Sentence` objects, so resetting a part
  through the copy changes the original.
- **L47. The float samplers refuse an `int` keyword (verified).**
  `BaseSampler.__init__`
  (`src/worktoy/work_test/samplers/_base_sampler.py:134-145`) checks each
  keyword against `__key_types__` with `isinstance`, and `FloatSampler`
  and `GaussianSampler` declare `float`, so `FloatSampler(minVal=0,
  maxVal=1)` and `GaussianSampler(mean=0)` raise `TypeException`, while
  `FloatSampler(0, 1)`, `GaussianSampler(0, 1)` and assignment accept the
  `int`.
- **L48. A `Permuter` without an arrangement fails on an internal
  attribute (verified).** `src/worktoy/dispatch/_permuter.py:192-211`:
  the docstring says the arrangement must be set before a call, and a
  call without one raises "'NoneType' object has no attribute
  'restoreFrom'". `MissingVariable(self, '__arg_arrangement__',
  Arrangement)` would name what is missing.
- **L49. Smaller points (verified unless marked read).**
  - `indexPermutations(-1)` returns a generator, and the `ValueError` its
    docstring promises comes only with the first `next`
    (`src/worktoy/utilities/combinatorics/_index_permutations.py:41-42`).
  - Calling a box through its class once the class exists, as in
    `Holder.n(99)`, captures a new default for every instance that has
    not read the field yet, since `AttriBox.__call__` accepts a second
    capture (`src/worktoy/desc/_attri_box.py:491-509`).
  - `Dispatcher.finalize` and `fallback` are annotated and documented as
    returning a `Decorator`, but return the dispatcher
    (`src/worktoy/dispatch/_dispatcher.py:665-712`; read).
  - `overload` takes a `strict=True` keyword that turns off the cast
    passes for its signature, which no docstring mentions, and accepts
    and ignores any other keyword
    (`src/worktoy/dispatch/_overload.py:246`; read).
  - `bipartiteMatching` names the slot by its position in the reduced
    list rather than the original one when no assignment exists
    (`src/worktoy/utilities/_bipartite_matching.py:76`; read).
  - `AbstractNamespace.deepGetItem` scans the namespace in a loop and
    builds the combined MRO namespace twice per call, and
    `NamespaceHook.preCompilePhase` calls it for each of its 17 names on
    every class statement
    (`src/worktoy/mcls/_abstract_namespace.py:104-115`; read).

### Out-of-date docstrings and comments

- **D25.** `src/worktoy/ezdata/_ez_field.py:28-31`, `:47-50`, `:54-58`,
  `:280-283` and `:312-315` describe the default as
  'fieldType(*posArgs, **keyArgs)', as 'T(value)' and, for `fromValue`,
  as 'type(v)(v)'. Since item 26, `_construct` copies a lone argument
  without keywords that is already of the field type, which `fromValue`
  always gives.
- **D26.** `src/worktoy/waitaminute/ezdata/_class_field_error.py:16-19`
  and `src/worktoy/ezdata/_ez_hook.py:96-97` give as the reason to refuse
  a class object that its rebuilt default would be its metaclass. Since
  item 26 it would be the class itself, copied:
  `EZField.fromValue(int).defaultValue` is `int`. The refusal stands
  (item 4); only the reason is out of date.
- **D27.** `src/worktoy/mcls/_abstract_metaclass.py:308-312`: the
  docstring of `__getattr__` forbids the dot operator inside the method,
  which itself reads `cls.__class_getattr__`. That read is safe because
  `AbstractMetaclass` defines the name, which the docstring could say
  instead.
- **D28 (comments).** `src/worktoy/utilities/__init__.py:17-39`: the
  heading "Orphans not requiring local imports" covers `_join_words`,
  which imports `unpack`, and `_directory`, which imports `NoPickle`, and
  `_quick_desc`, filed under "Requiring 'textFmt'", imports `NoPickle` as
  well. The published page is the source, so the comments are part of
  it.

---

## Group L: Sixth source read before 1.1.0 (open)

Files: various

Later on 2026-09-29 a Claude session read every file in `src/worktoy`
(165 files, 19,995 lines) a sixth time, in the layer order from
`src/worktoy/__init__.py`, checking each candidate against every item of
groups A to K so that none is repeated here. Each item below was
reproduced with a throwaway script on 3.14 and again on 3.7, and the
text says where the two differ. At the time the suite gave 1647 passed
on 3.14 with 100% line and branch coverage, and it catches none of these
items. The read also added to items 53 and 58; each addition is marked
at its item.

The repros assume these imports:

```python
from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.keenum import KeeNum, Kee, KeeBox, KeeFlags, KeeFlag
from worktoy.lorem_ipsum import Clause, Sentence, Paragraph
from worktoy.mcls import BaseObject
from worktoy.utilities import unpack, joinWords, ExceptionInfo
from worktoy.work_test.samplers import LoremSampler
```

### Fix before 1.1.0

#### 67. `del` in a class body does not take effect (medium, verified)

- **Where:** `src/worktoy/mcls/_abstract_namespace.py:240-287`
  (`AbstractNamespace.__getitem__` and `__setitem__`).
- **Cause:** `__setitem__` records every class-body binding in the
  shadow space, and `__getitem__` falls back to it when the namespace
  itself misses. `AbstractNamespace` defines no `__delitem__`, so `del
  name` removes the name from the dict but leaves it in the shadow space,
  and the next read of the name finds the deleted value. Where plain
  Python falls through to the module scope, or raises `NameError`, a
  worktoy class body reads back what it deleted. A name a hook claimed
  never reached the dict, so deleting it raises `NameError`, where plain
  Python deletes it.
- **Repro:**
  ```python
  tmp = 'GLOBAL'

  class Foo(BaseObject):
    tmp = 'LOCAL'
    del tmp
    seen = tmp

  Foo.seen  # 'LOCAL'; a plain class gives 'GLOBAL'

  class Bar(BaseObject):
    @overload(int)
    def foo(self, n):
      return n

    del foo
  # NameError: name 'foo' is not defined
  ```
- **Fix direction:** a `__delitem__` that removes the name from the
  shadow space as well as from the dict, and raises `KeyError` only when
  neither holds it. Whether deleting a hook-claimed name should also undo
  the registration the hook made (an overload, a `Kee`, an `EZField`) is
  worth settling while probing; refusing it with a clear message is the
  smaller fix.

#### 68. `KeeBox` applies the keywords of its default to an assigned value (medium, verified)

- **Where:** `src/worktoy/keenum/_kee_box.py:133-163` (`_resolveNum`, the
  keywords read at `:135` and used at `:155`).
- **Cause:** `_resolveNum` takes its positional arguments from the call
  when there are any and from the captured default otherwise, but always
  takes its keyword arguments from the captured default. An assignment
  then builds the value type from the assigned value together with the
  keywords written for the default, and can resolve to a different
  member than the value names.
- **Repro:**
  ```python
  class Num(KeeNum):
    TEN = Kee[int](10)
    SIXTEEN = Kee[int](16)

  class Holder(BaseObject):
    n = KeeBox[Num]('10', base=16)

  h = Holder()
  h.n         # Num.SIXTEEN, as declared
  h.n = '10'
  h.n         # Num.SIXTEEN; 'int('10')' is Num.TEN
  ```
- **Fix direction:** read the captured keywords only on the path that
  also reads the captured positional arguments, the build of the default.

#### 69. The lorem generators keep their layout when `charCount` changes (medium, verified)

- **Where:** `src/worktoy/lorem_ipsum/_base_generator.py:231` (the
  `charCount` box), the caches of `_clause.py:58-59`, `_sentence.py:295-296`
  and `_paragraph.py:45-46`, and
  `src/worktoy/work_test/samplers/_lorem_sampler.py:217-219`.
- **Cause:** `charCount` is a plain `AttriBox`, and nothing clears the
  cached lengths and words, clauses or sentences when it is assigned.
  Once a generator has rendered, a new `charCount` is ignored until
  `reset()` or `clear()`. `LoremSampler` renders its `Sentence` and then
  resets it after every draw, so its caches are always full, and the
  first draw after `sampler.charCount = n` still has the old length,
  where its docstring promises the configured one.
- **Repro:**
  ```python
  s = Sentence(40)
  len(str(s))    # 40
  s.charCount = 90
  len(str(s))    # 40, and s.charCount is 90

  c = Clause(40); str(c); c.charCount = 90; len(str(c))           # 40
  p = Paragraph(200); str(p); p.charCount = 400; len(str(p))      # 200

  sampler = LoremSampler()
  len(sampler())         # 40
  sampler.charCount = 100
  len(sampler())         # 40
  len(sampler())         # 100
  ```
- **Fix direction:** an `onSet` callback on `charCount` in
  `BaseGenerator` that calls `clear()`, with a `clear` on
  `BaseGenerator` for the three subclasses to extend. The copy
  constructors set `charCount` before they copy the caches, so they keep
  working.

#### 70. An `overload` bound in a second class under another name is dropped (medium, verified)

- **Where:** `src/worktoy/mcls/space_hooks/_load_space_hook.py:35-53`
  (`LoadSpaceHook.setItemPhase`).
- **Cause:** the hook marks an `overload` with the name it was first
  bound to, `__claimed_name__`, on the object itself, and reads a
  binding under a different name as an alias of that name within the
  same class body. The mark outlives the class, so an `overload` bound
  in a second class under another name is taken for an alias of a name
  the second class never bound. The alias copies nothing, the hook
  claims the binding, and the class gets no attribute, without a word.
  Under the same name the second class works.
- **Repro:**
  ```python
  ov = overload(int)(lambda self, n: ('int', n))

  class A(BaseObject):
    foo = ov

  class B(BaseObject):
    bar = ov

  A().foo(1)            # ('int', 1)
  'bar' in B.__dict__   # False
  B().bar(1)            # AttributeError: 'B' object has no attribute 'bar'
  ```
- **Fix direction:** keep the record of claimed names on the namespace,
  which lives for one class body, rather than on the `overload`.

#### 71. An EZData class body binding an attribute EZData sets itself makes a field of it (medium, verified, DECIDED, DONE)

- **Where:** `src/worktoy/ezdata/_ez_hook.py` (`EZHook.setItemPhase` and
  `postCompilePhase`).
- **Cause:** found on 2026-09-29 while applying the author's principle
  (see [Decisions](#decisions)) to the class body of an EZData
  subclass. EZData sets five attributes on every class itself:
  `__ez_fields__`, `__key_args__`, `__is_frozen__`, `__is_ordered__` and
  `__kw_only__`. None is a method, nor among the names the interpreter
  writes, so `setItemPhase` turned a class-body binding of one into a
  field of that name, and `postCompilePhase` then overwrote the class
  attribute with its own value. The binding was neither honoured nor
  refused, and the field then shadowed the class attribute on every
  instance: the generated `__repr__` reads `self.__kw_only__` and got
  the field, while `__init__` reads the class attribute before any field
  is set.
- **Repro:**
  ```python
  class C(EZData):
    x = EZField[int](1)
    __kw_only__ = True

  C.__kw_only__                    # False: the class is positional
  [f.fieldName for f in C.fields]  # ['x', '__kw_only__']
  ```
- **DECIDED (2026-09-29):** refuse the five names in the class body with a
  new `ReservedAttributeError`, the attribute counterpart of
  `ReservedMethodError`, pointing to the class keywords that set the
  options.
- **DONE (2026-09-29).** `EZSpace.__reserved_ez_attributes__` lists the
  five names, beside `__reserved_ez_methods__`, and `setItemPhase` raises
  `ReservedAttributeError`
  (`src/worktoy/waitaminute/ezdata/_reserved_attribute_error.py`, an
  `AttributeError` with `attributeName` and `space`) for any of them,
  whatever the value, at the class-body line. The slot is named
  `attributeName` rather than `name`, so the exception does not join
  the three of L15. Its message names the class and the attribute and
  shows the class-keyword form, as in `class C(EZData, kwOnly=True)`. The
  docstrings of `EZSpace`, `EZHook.setItemPhase` and `EZData` say so.
  Test: `tests/test_ezdata/test_reserved_attribute.py` (six tests). The
  five regression tests failed before the change (each name refused, the
  names listed on `EZSpace`, the keyword hint, `AttributeError`, and the
  refusal coming before the rest of the body runs) and the guard passed
  (the class keyword still sets the option). The suite gives 1689 passed
  on 3.14 with 100% line and branch coverage and passes on 3.7 to 3.13.
  A mutation check caught all ten breaks with the control passing: the
  check removed, the wrong name raised, `ReservedMethodError` raised
  instead, the keyword hint dropped, a `TypeError` base, and each of the
  five names left off the list.

#### 72. EZData generates no `__len__`, so a plain base's placeholder `__len__` decides length and truth (medium, verified, DECIDED, DONE)

- **Where:** `src/worktoy/ezdata/_ez_hook.py` (`postCompilePhase`), found
  with the author's `main_tester_03.py`.
- **Cause:** EZData generates `__iter__` over the fields but no
  `__len__`. A mixin written against the protocol, as the author's
  `GeometryMixin` is, declares placeholder `__init__`, `__iter__` and
  `__len__`; EZData's `__init__` and `__iter__` take precedence, but its
  `__len__` placeholder returning 0 was inherited. Every instance then
  had length 0 and, having no `__bool__`, was falsy.
- **Repro:**
  ```python
  class GeometryMixin:
    def __iter__(self): yield from ()
    def __len__(self): return 0
    def __init__(self, *args): pass

  class PlanePoint(EZData, GeometryMixin):
    x = EZField[float](0.)
    y = EZField[float](0.)

  p = PlanePoint(3, 4)
  list(p), len(p), bool(p)  # ([3.0, 4.0], 0, False)
  ```
- **DECIDED (2026-09-29):** EZData generates `__len__` and reserves it:
  an EZData class body may not define it (`ReservedMethodError`), a
  plain base may, and the generated one takes precedence over it, as
  for the other reserved methods.
- **DONE (2026-09-29).** `EZHook.lenFactory` builds `__len__`, returning
  the number of fields, own and inherited, which is the number of values
  `__iter__` yields; `postCompilePhase` installs it beside `__iter__`,
  and `EZSpace.__reserved_ez_methods__` lists it. A class without a
  `__bool__` of its own is then truthy exactly when it has fields. The
  docstrings of `EZData` (with a type stub), `EZSpace`,
  `ReservedMethodError`, `lenFactory` and `postCompilePhase` say so.
  Tests: `tests/test_ezdata/test_generated_len.py` (five tests) and
  `tests/test_ezdata/test_plain_base_reserved_ignored.py` (two tests);
  the six regression tests failed before the change, and the guard over
  every reserved method from a plain base passed. The suite gives 1696
  passed on 3.14 with 100% line and branch coverage and passes on 3.7 to
  3.13 (3.7 once the author had rebuilt `base_3_7`, see
  [Status](#status)). The author's
  `PlanePoint(3, 4)` now has length 2 and is truthy. A mutation check
  caught all four breaks with the control passing: the method not
  installed, off by one, always zero, and `__len__` left off the
  reserved list.

### Low severity

- **L50. `KeeFlags` operators between a flags class and a derived one
  raise a raw `KeyError` (verified).**
  `src/worktoy/keenum/_kee_flags.py:251-281`. `__or__`, `__and__` and
  `__xor__` accept `other` when `isinstance(other, type(self))`, which
  holds for a member of a derived flags class, and then look the combined
  names up in the `memberDict` of `type(self)`, which lacks the flags the
  derived class added. `Perm.READ | MorePerm.EXEC` raises `KeyError:
  frozenset({'READ', 'EXEC'})`, while `MorePerm.EXEC | Perm.READ` raises
  Python's `TypeError` for unsupported operands, with `Perm` holding
  `READ` and `WRITE` and `MorePerm(Perm)` adding `EXEC`. Returning
  `NotImplemented` unless `type(other) is type(self)` gives both orders
  the same `TypeError`; resolving a mixed operation in the derived class
  is the alternative, should mixing be wanted.
- **L51. Dispatch raises a raw `TypeError` for an argument whose class
  cannot be hashed (verified).**
  `src/worktoy/dispatch/_dispatcher.py:239-240`. The exact-type pass
  looks the `TypeSig` of the argument types up in a dict, which hashes
  each type. A class whose metaclass defines `__eq__` without `__hash__`
  is unhashable, so a call passing an instance of it raises `TypeError`
  from the lookup before the `isinstance` passes run, and even an
  `@overload(object)` never receives it:
  ```python
  class M(type):
    def __eq__(cls, other):
      return cls is other

  class Weird(metaclass=M):
    pass

  class HD(BaseObject):
    @overload(object)
    def f(self, x):
      return 'object'

  HD().f(Weird())
  # 3.14: TypeError: cannot use 'worktoy.dispatch._type_sig.TypeSig' as a
  #       dict key (unhashable type: 'M')
  # 3.7:  TypeError: unhashable type: 'M'
  ```
  Catching the `TypeError` of the lookup and going on to the `isinstance`
  pass fixes it.
- **L52. `unpack` recurses without end on an iterable that yields itself
  (verified).** `src/worktoy/utilities/_unpack.py:62-73`. `unpack`
  flattens every iterable other than `str` and `bytes` recursively, and
  `ARGS` instances are iterable and yield themselves
  (`src/worktoy/core/sentinels/_args.py:49-53`), so `unpack(ARGS[int])`
  and `joinWords(ARGS[int])` raise `RecursionError`. Nothing in `src`
  passes one today, since every caller hands `joinWords` strings, but
  both functions are public. Treating an iterable whose only item is
  itself as atomic, as a one-character `str` already is, fixes it.
- **L53. `ExceptionInfo` accepts an expected type it can never catch
  (verified).** `src/worktoy/utilities/_exception_info.py:107-117` and
  `:135-138`. The constructor accepts any subclass of `BaseException` as
  the expected type, but `__exit__` lets every `BaseException` that is
  not an `Exception` propagate, so `with ExceptionInfo(KeyboardInterrupt):
  raise KeyboardInterrupt` raises. Refusing such a type in the
  constructor, with the reason the class docstring already gives, fixes
  it.
- **L54. `DelException` quotes the bases as part of the metaclass name
  (verified).** `src/worktoy/waitaminute/meta/_del_exception.py:41-53`.
  The bases are formatted into the metaclass name before it goes between
  the quotes, so the message reads "When attempting to derive a class
  named 'Foo' from the metaclass 'BaseMeta with bases: (Base)', the
  '__del__' method was found ...". Formatting the bases after the closing
  quote fixes it.

---

## Out of scope

### 15. On 3.14, classes built by some metaclasses report the wrong `__annotations__` (medium, verified, new, OUT OF SCOPE)

- **Where:** every worktoy metaclass whose own class body holds
  annotations: `EZMeta` (`ezdata/_ez_meta.py`), `KeeMeta`
  (`keenum/_kee_meta.py`), `KeeFlagsMeta` (`keenum/_kee_flags_meta.py`),
  `KeeMetaMeta` (`keenum/_kee_meta_meta.py`), `MetaFlow`
  (`waitaminute/control_flow/_meta_flow.py`) and `_MetaARGS`
  (`core/sentinels/_args.py`).
- **Cause:** each of these metaclasses has an `__annotations__` dict of
  its own. From 3.14, a class body compiled without `from __future__
  import annotations` keeps its annotations lazily instead of as an
  `__annotations__` dict. Looking up `cls.__annotations__` then finds
  the metaclass's plain dict before the getter on `type`, which is not a
  data descriptor there, so the lookup falls through to the first class
  in the method resolution order holding such a dict: `Object` for
  EZData classes, `KeeBase` for KeeNum classes.
  `annotationlib.get_annotations(cls)` still answers correctly, 3.13 and
  earlier are unaffected, and so is `BaseMeta`, which has no annotations.
- **Repro:**
  ```python
  # A file without 'from __future__ import annotations', on 3.14
  class Pt(EZData):
    x: float = EZField[float](0.0)

  Pt.__annotations__  # the annotations of 'Object', not {'x': float}
  ```
- **DECIDED: out of scope for 1.1.0.** A proper fix needs a change to the
  language itself, through a new PEP, so the item belongs to no group.
  Code that needs the annotations of such a class should use
  `annotationlib.get_annotations(cls)`, which answers correctly.

---

## Background

### How the audit was produced

One Claude session read every file in `src/worktoy` (157 files, ~18.7k
lines) and `tests` (251 files, ~26.1k lines) in the layer order from
`src/worktoy/__init__.py`. Every item marked **verified** in this file was
reproduced with a throwaway script, run as:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ~/miniforge3/envs/worktoy_env/bin/python probe.py
```

Baseline at the time: Python 3.14.5, `pytest tests` gives 1286 passed,
100% line and branch coverage. None of the bugs it found were caught by
the suite.

Groups H, I, J, K and L come from five later reads of `src/worktoy`
alone, on 2026-09-26, twice on 2026-09-28 and twice on 2026-09-29, each
described at the head of its group.

The repro snippets are meant to become regression tests. Items marked
**DECISION** are behaviour the author may want to keep; mark them KEEP or
CHANGE before a session starts on them.

### How this file is organized

This file is both the record of the full-read audit and the current work
list for the 1.1.0 update. It merges the two files that used to hold
these, whose last versions are kept in `archive/audits_1_1_0/`. The work
was first planned as a 1.1 update, and the file was named
`audit_1_1_0.md` until 2026-09-26, when it was renamed `audit_1_0_1.md`
to match the `1.0.1` of the version and the changelog. On 2026-09-28 the
release became 1.1.0 again: its compatibility notes and new public names
are more than a patch release may carry, so the file took back its first
name. The version string, the `VERSION` file and the changelog header
still read `1.0.1` until the release tooling moves them. Items 26 and 30,
once planned for 1.1, now belong to 1.2.

Items keep their original numbers: plain numbers for the main findings,
L for low severity, T for test issues and D for docstrings. Items 13,
14, 15, L5 to L11, D6 and D7 were added after the original audit. Group
H (items 16 to 30, L12 to L19, D8 to D14) comes from a second full read
of `src/worktoy` on 2026-09-26, and group I (items 31 to 49, L20 to L30,
D15 to D24) from a third on 2026-09-28, group J (items 50 to 55, L31 to
L37) from a fourth later that day, group K (items 57 to 66, L38 to
L49, D25 to D28) from a fifth on 2026-09-29, and group L (items 67 to
70, L50 to L54) from a sixth later that day; item 56 was split off item
26 and sits in group H. Group L shares its letter with the prefix of the
low-severity items; "group L" always names the group, and "L50" an
item. A finished group takes its items
out of the open sections: its "Group X: done" section says what changed,
and the appendix keeps each finding as first recorded. An item marked
DECISION needed the author's answer before its tests were written; the
answers are under [Decisions](#decisions).

---

## Appendix: original findings of the closed items

These are the closed items exactly as the full-read audit recorded them,
before groups A to F fixed them. Line numbers refer to the code of that
time.

### 1. `super()` inside an overriding overload recurses forever (verified)

- **Where:** `src/worktoy/dispatch/_dispatcher.py:172` (`_getCachedKey`),
  `:477` (`__get__`)
- **Cause:** the bound dispatch function is cached on the instance under
  `'__bound_dispatch_%s__' % fieldName`. The key has no owner component,
  so the parent's `Dispatcher.__get__` (reached through `super()`) finds
  the child's cached bound method and calls the child again.
- **Repro:**
  ```python
  class Parent(BaseObject):
    @overload(int)
    def foo(self, x): return 'parent'

  class Child(Parent):
    @overload(int)
    def foo(self, x): return 'child+' + super().foo(x)

  Child().foo(1)  # RecursionError
  ```
- **Variants (verified, added in the group A session):**
  - `super().__init__(...)` inside an overloaded `__init__` recurses the
    same way. Python reads `__init__` through the instance during
    construction, so the subclass's bound method is always cached first.
    This is the most common way to hit the bug.
  - A chain of three overriding overloads recurses too.
  - Reaching the parent first (`super(Child, c).foo(1)` from outside)
    caches the parent's bound method, after which `c.foo(1)` silently
    runs the parent version instead of the override.
- **Fix direction:** see item 2; both come from the same cache.
- **Tests:** `tests/test_overload/test_super_overload.py`.

### 2. `copy.copy` of a BaseObject shares its overloaded methods with the original (verified)

- **Where:** same cache as item 1.
- **Cause:** the cached `MethodType` lives in the instance `__dict__`, so
  `copy.copy` copies a bound method whose `__self__` is the original.
  Overloaded calls on the copy then run against the original.
- **Repro:**
  ```python
  class Counter(BaseObject):
    def __init__(self, *args): self.n = 0
    @overload(int)
    def bump(self, k):
      self.n += k
      return self.n

  a = Counter(); a.bump(1)
  b = copy.copy(a); b.bump(10)
  (a.n, b.n)  # (11, 1): the copy's call mutated the original
  ```
- **Variants (verified, added in the group A session):**
  - After `obj.__class__ = Other`, overloaded calls keep running the old
    class's version.
  - The cached bound method makes the instance refer to itself, so an
    instance that has made an overloaded call is only freed by the
    garbage collector, never by reference counting.
  - Every called instance gains a `__bound_dispatch_*__` entry in its
    `__dict__`.
  - `copy.deepcopy` is not affected: it rebinds the copied method to the
    copy.
- **Fix direction (DECIDED: drop the cache):** build the `MethodType` on
  every access, as Python does for plain methods. The rejected option was
  keying the cache by dispatcher identity, which would have left the
  reference cycle and the `__dict__` entries in place. `test_peek` in
  `tests/test_dispatch/test_dispatcher.py` tests the cache's recursion
  guard in `__get__` and goes away with the cache.
- **Tests:** `tests/test_overload/test_overload_binding.py`,
  `tests/test_overload/test_overload_footprint.py`.

### 3. `KeeBox[E](E.MEMBER)` as a default can resolve to a different member (verified)

- **Where:** `src/worktoy/keenum/_kee_box.py:114` (`_resolveNum`)
- **Cause:** there is no identity check. A member argument falls through
  to `valueType(*args)`; for an `int` value type that calls
  `int(member)`, which is the member's index, and then matches by value.
  For other value types it usually raises `KeeBoxValueError` instead. The
  setter path is fine because `__instance_set__` checks
  `isinstance(value, self.fieldType)` first; the default (get) path does
  not.
- **Repro:**
  ```python
  class Slot(KeeNum):
    LEFT = Kee[int](2)
    CENTER = Kee[int](0)
    RIGHT = Kee[int](1)

  class Widget:
    align = KeeBox[Slot](Slot.LEFT)

  Widget().align  # Slot.CENTER
  ```
- **Fix direction:** in `_resolveNum` (and per argument in
  `_resolveFlags`), return the argument directly when it is already a
  member of the field enumeration.

### 4. EZHook turns interpreter-set names into fields (verified)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:142` (`setItemPhase`), with
  the pass-through list in `src/worktoy/mcls/space_hooks/_reserved_names.py:32`
- **Cause:** every class-body value that is not a function and has no
  descriptor methods becomes an `EZField`. That includes names the
  interpreter writes into the namespace:
  - `__classcell__` (any method using `super()` or `__class__`): the
    cell never reaches `type.__new__`, so class creation fails.
  - `__orig_bases__` (from `Generic[T]` bases): becomes a slot and
    breaks `Generic.__init_subclass__`.
  - also worth checking on 3.13+ / 3.14: `__classdictcell__`,
    `__conditional_annotations__`, `__type_params__`.
- **Repro:**
  ```python
  class Base(EZData):
    x = EZField[int](0)
    def __post_init__(self): pass

  class Sub(Base):
    def __post_init__(self): super().__post_init__()
  # RuntimeError: __class__ not set defining 'Sub' ... __classcell__

  class Box(EZData, Generic[T]):
    x = EZField[int](0)
  # TypeError: argument of type 'member_descriptor' is not a container

  class Holder(EZData):
    x = EZField[int](0)
    class Inner: pass
  tuple(Holder.__ez_fields__), Holder().Inner  # (('x', 'Inner'), <class 'type'>)
  ```
- **Fix direction:** pass through the interpreter-set dunders above.
  **DECISION:** should classes (and other bare class constants) in an
  EZData body become fields at all? A nested class currently becomes a
  field whose default is `type(Inner)(Inner)`, which is `type`.

### 5. flexCall rejects keyword arguments for positional parameters (verified, DECISION)

- **Where:** `src/worktoy/dispatch/_flex_call.py:105` (the wrapper),
  applied to every plain method by
  `src/worktoy/mcls/space_hooks/_flex_call_hook.py:40`, which is on
  `AbstractNamespace`, so it affects BaseObject, KeeNum, EZData and
  everything built on them.
- **Cause:** `minPos` is checked against `len(args)` only; parameters
  supplied by keyword are not counted.
- **Repro:**
  ```python
  class Plain(BaseObject):
    def bar(self, x): return x

  Plain().bar(x=1)     # TypeError: requires at least '2' positional ...
  Plain().bar(1, 2, 3) # returns 1, extras silently dropped
  ```
- **Fix direction:** subtract names present in `kwargs` from the missing
  list before raising. **DECISION:** whether silent truncation of extra
  positionals on ordinary methods should stay, given the fail-fast
  philosophy in `waitaminute`.

### 6. `KeeBox` over `KeeFlags` fails for combined members (verified)

- **Where:** `src/worktoy/keenum/_kee_box.py:161`
- **Cause:** the lookup key is `frozenset(h.name for h in highs)`, so a
  combined member contributes `'READ_WRITE'` instead of
  `{'READ', 'WRITE'}`.
- **Repro:**
  ```python
  class Perm(KeeFlags):
    READ = KeeFlag(); WRITE = KeeFlag()

  class File:
    mode = KeeBox[Perm]('READ')

  f = File(); f.mode = 'READ_WRITE'  # KeyError: frozenset({'READ_WRITE'})
  class File2:
    mode = KeeBox[Perm](3)
  File2().mode                       # same KeyError
  ```
- **Fix direction:** build the key from the union of `h.names`.

### 7. Inherited overloads beat subclass overrides (verified)

- **Where:** `src/worktoy/mcls/_base_space.py:76` (inherited variadics
  appended first, never deduplicated),
  `src/worktoy/dispatch/_dispatcher.py:189` and `:199` (FAST passes are
  first-registered-wins)
- **Cases:**
  - A subclass that re-declares a variadic overload gets its own version
    for short calls (the concrete expansions are replaced) but the
    parent's for calls longer than `__variadic_fastpath_limit__`.
  - A subclass that re-declares `@overload(THIS)`: an argument that is an
    instance of a further subclass matches the parent's `(Parent,)`
    signature first, so the parent's version runs.
- **Repro:**
  ```python
  class VParent(BaseObject):
    @overload(int, ARGS[int])
    def f(self, *a): return 'parent'
  class VChild(VParent):
    @overload(int, ARGS[int])
    def f(self, *a): return 'child'
  VChild().f(1, 2)           # 'child'
  VChild().f(*range(10))     # 'parent'

  class TParent(BaseObject):
    @overload(THIS)
    def g(self, o): return 'parent'
  class TChild(TParent):
    @overload(THIS)
    def g(self, o): return 'child'
  class TGrand(TChild): pass
  TChild().g(TGrand())       # 'parent'
  ```
- **Also affected (verified, added in the group A session):** a class
  inheriting both registrations without declaring anything (a
  grandchild) gets the parent version too, in both cases.
- **Complication:** `ARGS[int] is not ARGS[int]`, and `TypeSig` compares
  its entries by identity, so two variadic signatures written the same
  way never compare equal. An override can only replace an equal
  inherited variadic once `ARGS` instances compare and hash by their
  inner type.
- **Fix direction:** let own variadics replace inherited ones with an
  equal signature, and order own registrations ahead of inherited ones
  in the FAST passes (or rank inherited last).
- **Tests:** `tests/test_overload/test_override_precedence.py`.

### 8. Non-frozen EZData accepts wrongly typed assignment (verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:312` (only frozen classes
  get a generated `__setattr__`)
- **Repro:** `class Pt(EZData): x = EZField[float](0.0)`, then
  `p = Pt(1); p.x = 'not a float'` succeeds.
- **Note:** `badDelAttrFactory` refuses deletion to protect "every field
  always holds a value of the declared type", which assignment currently
  breaks. **DECISION:** add a casting `__setattr__` for non-frozen
  classes, or narrow the documented guarantee.

### 9. Two EZData bases with fields cannot be combined (verified, DECISION)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:332` (`slotsFactory` puts
  every inherited field into `__slots__` again)
- **Repro:** `class C(A, B)` where both `A` and `B` are EZData classes
  with fields raises `TypeError: multiple bases have instance lay-out
  conflict`.
- **Note:** `EZSpace.__init__` and `initFactory` document merging fields
  from several bases. **DECISION:** support it (would need a different
  storage layout) or reject it early with a clear worktoy exception and
  fix the docstrings.

### 10. `__class_init__` on a KeeNum is silently ignored (verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:429`
- **Cause:** `KeeMeta.__init__` never calls `AbstractMetaclass.__init__`,
  which is what routes `__class_init__` (and `_notifySubclassHook`).
- **Repro:** a KeeNum subclass with an `@classmethod __class_init__`
  that appends to a list; the list stays empty.

### 11. Custom `KeeMeta` subclasses break `mroNum` and `base` (verified)

- **Where:** `src/worktoy/keenum/_kee_meta.py:136` and `:155`
- **Cause:** `_createBase` special-cases the literal class name
  `'KeeNum'`. The root built for `FontMeta.keeNum` is named
  `'FontMetaNum'`, so it is treated as an ordinary enumeration.
- **Repro:**
  ```python
  class FontMeta(KeeMeta): pass
  class FontNum(FontMeta.keeNum):
    ARIAL = Kee[int](1)
  FontNum.base    # the root 'FontMetaNum', where KeeNum children get themselves
  FontNum.mroNum  # ValueError: ... must have exactly one base, but received none!
  ```
- **Fix direction:** `_getKeeNum` already sets `__root_class__ = True` in
  the root namespace; test for that marker instead of the name.

### 12. Shared sampler state (verified)

- **Where:** `src/worktoy/work_test/samplers/_lorem_sampler.py:33`
  (`sentence = Sentence()` at class level), and the class-level samplers
  on `BaseTest` (`src/worktoy/work_test/_base_test.py:76`)
- **Repro:** two `LoremSampler()` instances; setting `charCount` on one
  gives `(100, 100, True)` for both counts and `a.sentence is b.sentence`.
- **Knock-on:** tests change the shared `BaseTest` samplers (for example
  `test_symbolic_name.py:124`, `test_alias.py:21`, `test_sentence.py:29`,
  `test_point_2d.py:69`), and `tearDownClass` only unloads the test
  module, so those settings leak into later test classes.
- **Fix direction:** per-instance `Sentence` in `LoremSampler`
  (`AttriBox[Sentence]()`); per-test sampler instances or a reset in
  `BaseTest.setUp`.

### 13. Overloads from several bases ignore the method resolution order (verified, added in the group A session)

- **Where:** `src/worktoy/mcls/_base_space.py:62` (`BaseSpace.__init__`
  merges the direct bases left to right, and a later base overwrites an
  equal signature), `src/worktoy/mcls/space_hooks/_load_space_hook.py:74`
  (`postCompilePhase` only checks the class's own body for a plain
  definition)
- **Cases:**
  - `class Both(Left, Right)` with an equal overload in each base runs
    `Right`'s version, where Python's order says `Left`.
  - With an equal variadic overload in each base, short calls run
    `Right`'s version and calls longer than
    `__variadic_fastpath_limit__` run `Left`'s, so the winner changes
    with the length of the call.
  - A plain method in an earlier base (`class C(PlainMixin, Right)`) is
    shadowed by a dispatcher built from `Right`'s overloads. The diamond
    `class LoudRight(Loud, Right)`, where `Loud(Right)` overrides with a
    plain method, runs `Right`'s overload instead of `Loud`'s override.
- **Decision:** signatures from all bases keep merging into one
  dispatcher. On an equal signature the class first in the method
  resolution order wins in every pass. A plain method earlier in that
  order shadows overloads contributed only by later classes.
- **Tests:** `tests/test_overload/test_base_precedence.py`.

---

- **L3. `str()` of a variadic `TypeSig` raises (verified).**
  `src/worktoy/dispatch/_type_sig.py:213` uses `t.__name__`; an
  `ARGS[int]` instance has none. The tests in
  `tests/test_dispatch/test_variadic_type_sig.py` pin the rendering
  `TypeSig(int, ARGS[int])`, mirroring how the signature is written.
- **L5. `SubTest` used without calling it raises an empty
  `RuntimeError` (verified, new).** `with self.subTest:` never pushes a
  label, and `__exit__` pops one in its `finally`
  (`src/worktoy/work_test/_sub_test.py:208`), so `_popCurrent` raises a
  bare `RuntimeError` (`:122`). Raised from `finally`, it also replaces
  whatever the block itself raised. Only `with self.subTest(...):` works.
  Fix direction: push the fallback label in `__enter__` when nothing was
  pushed, or raise a typed exception naming the required call.
- **T1. Fixture bug.** `tests/test_keenum/examples/_prime_valued.py:37`
  loops `while cls.isPrime(p)`, so `indexPrime(0..4)` gives
  `[2, 9, 15, 21, 25]`. `testPrimeValued` only checks divisibility, so it
  passes anyway.
- **T2. Misspelled keyword hides behind a repr check.**
  `tests/test_ezdata/test_ez_field.py:198` and `:208` pass `givenName=` to
  a `FullName` whose field is `givenNames`; EZData drops unknown keywords
  silently and the test only inspects the repr.
- **T3. Tests that check nothing:**
  - no body: `tests/test_mcls/test_hooks/test_duplicate_hook.py`,
    `tests/test_mcls/test_space/test_more_space.py` (`test_str_repr`)
  - no test cases: `tests/test_desc/test_notification.py`
  - no assertions: `tests/test_dispatch/test_dispatcher.py`
    (`test_str_repr`), `tests/test_dispatch/test_space_point.py`
    (`test_dispatcher`)
  - `tests/test_mcls/test_meta/test_class_hash.py` never calls
    `hash(cls)`, only `__class_hash__()` directly.
- **T4. FullName fixture mismatch.** `tests/test_ezdata/examples/_full_name.py`
  says family name first, the fields are `givenNames, familyName`, and
  `test_full_name.py` passes family names first.
- **T5. Weak or no-op lines.** `tests/test_desc/test_field.py:204` and
  `:216` set `__deleter_keys__` / `__delete_keys__` on the instance, which
  has no effect; `tests/test_work_test/test_word_sampler.py:25` iterates
  the characters of one word and checks each is a `str`.
