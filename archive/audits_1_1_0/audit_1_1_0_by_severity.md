# worktoy 1.1.0 audit: open issues by severity

Started 2026-10-01.

This file lists every issue still open in `src/worktoy`, sorted into four
groups of severity, the most severe first within each group. It replaces
the audit kept from the 1.0.0 release to 2026-09-29, which is archived
unchanged at `archive/audits_1_1_0/audit_1_1_0_groups_a_to_l.md`. That
file keeps the record of the closed items (groups A to F and the done
items of G to L), the decisions the author has settled, and the drafts
for the 1.1.0 changelog, so look there before reopening a settled
question.

## Status

On 2026-10-01 a Claude session read every file in `src/worktoy` (168
files) a seventh time, in the layer order from `src/worktoy/__init__.py`,
and then re-ran the repro of every open item of the archived audit
against the current code. Every one of them still reproduces, and the
read added the items marked **new**. The suite then gave 1707 passed on
3.14 with 100% line and branch coverage, and caught none of the items
below.

Progress: on 2026-10-01 the text part of H01, all of H02 and H03, and
M01 were done; the suite gives 1760 passed on 3.14 with 100% line and
branch coverage.

Progress on 2026-10-03: every item that needs no decision is done, each
with its tests, a mutation check and, where users see a change, a
changelog draft. M10 was decided and its text part done; M13, M14 and
M24 were decided and done, M14 with a note for 1.2; and M32, found while
deciding M24, was decided and done as well. The suite gives 1998 passed
and 50 skipped on 3.14 with 100% line and branch coverage, 1986 passed
on 3.7 under pytest, and passes on 3.8 to 3.13 under unittest.

Later on 2026-10-03 a session read the source an eighth time, in the
layer order, and put M25 to the author, who chose to refuse the dead
hooks at the class statement, then M26, where the author turned the
proposal down and banned a second sentinel at a taken name instead, and
then M27, where names of the same words now compare equal, and M29,
where the author kept the expansion for 1.1, had the overlap refusal name
the two declarations now, and planned the redesign for 1.2, and L19,
where every miss on a flags class now raises `KeeResolveError`. All five
are done as far as 1.1 goes, with their tests, a mutation check and a
changelog draft. The suite gives 2041 passed and 50 skipped on 3.14 with
100% line and branch coverage, 2029 passed on 3.7 under pytest, and
passes on 3.8 to 3.13 under unittest.

L55 and the L45 point on short sentences were decided and done later
the same day; see their entries. No decision is open. The suite gives
2056 passed and 50 skipped on 3.14 with 100% line and branch coverage,
2044 passed on 3.7 under pytest, and passes on 3.8 to 3.13 under
unittest. D05 leaves one test helper, around `WORKTOY_DATA_DIR`, for the
author. The rest of H01, M28, M29 and M30 are planned for 1.2, and M31
is out of scope.

To resume: read this section and the source again in the layer order of
`src/worktoy/__init__.py`, as the author asks before any fix. What
remains for the release is the author's: the D05 helper, moving the
changelog drafts of the done items from this file into `changelog.md`,
whose header still reads 1.0.1 while `__version__` is '1.0.1-dev1', and
the version itself, which the release tooling moves.

| Group | Items | What belongs there |
|---|---|---|
| [Critical](#critical) | none | data corrupted or an ordinary, documented use broken |
| [High](#high) | H01 to H03 | a wrong result without a word, in ordinary use of a core feature |
| [Medium](#medium) | M01 to M32 | a wrong result in a narrower case, a crash with a misleading message, or a design question |
| [Low, style, cosmetic and docstrings](#low-style-cosmetic-and-docstrings) | L01 to L60, D01 to D27 | edge cases, messages, style, and text out of step with the code |

Each item says what it was in the archived audit ("archived 30",
"archived L20"), so its history and any discussion can be found there.
New numbers start at H01, M01, L01 and D01, zero-padded so they cannot be
mistaken for the archived L1 to L54.

Tags:

- **to do**: the fix is clear and needs no decision.
- **DECISION**: the author decides KEEP or CHANGE before tests are
  written.
- **DECIDED**: the author has decided; only the code is missing.
- **planned 1.2**: decided for the 1.2 release.
- **out of scope**: not scheduled.

## How to work

Run the suite as:

```
PYTHONDONTWRITEBYTECODE=1 ~/miniforge3/envs/worktoy_env/bin/python -m pytest -p no:cacheprovider tests
```

It must give 100% line and branch coverage over `src/worktoy` and
`tests`. The `base_3_7` to `base_3_13` environments cover the older
versions; only `base_3_7` has pytest, and the others run:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ~/miniforge3/envs/base_3_11/bin/python -m unittest discover -s tests -t . -q
```

Probes are throwaway scripts in the scratchpad, run as:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:. ~/miniforge3/envs/worktoy_env/bin/python probe.py
```

The method for each item:

- Probe first, and look for the cases around the repro.
- Put a DECISION to the author one item at a time, with a proposal and
  the reason for it. The author turns down batches of questions, and
  prefers the fix that changes the least behaviour.
- Write failing tests first, one `TestCase` per file, based on the
  package's own test base (`EZTest`, `KeeTest`).
- Fix the source, not the test.
- Mutation check: break the fix on purpose in a copy of `src/worktoy`
  and confirm the new tests fail.
- Record the item as done here, with what changed and the tests, and
  add its user-visible change to the changelog drafts in the archived
  file or in `changelog.md`.

The repros assume these imports:

```python
from typing import Generic, TypeVar

from worktoy.core.sentinels import ARGS, THIS, OWNER, Sentinel
from worktoy.desc import AttriBox, FastBox, Field, Alias, SymbolicName
from worktoy.dispatch import overload, Dispatcher, Permuter
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag, KeeBox, KeeMeta
from worktoy.lorem_ipsum import Clause, Sentence, Paragraph, StochasticWord
from worktoy.mcls import BaseObject, BaseMeta
from worktoy.utilities import typeCast, unpack, ExceptionInfo
from worktoy.utilities.combinatorics import Arrangement


class MyInt(int):
  pass


class MyStr(str):
  pass


class Perm(KeeFlags):
  READ = KeeFlag()
  WRITE = KeeFlag()
```

---

## Critical

None. No open issue corrupts data or breaks an ordinary, documented use
of the library on its common paths.

---

## High

### H01. `AttriBox` turns any value into its field type through the constructor (archived 30; text part DONE, rest planned 1.2)

- **Where:** `src/worktoy/desc/_attri_box.py:417-457`
  (`__instance_set__`) and `:177-346` (`_resolve`).
- **Problem:** an assignment tries a lossless `typeCast` first, and when
  the cast refuses, every field type except `bool`, `int`, `float` and
  `complex` falls back to calling the field type on the value. For the
  most common field types that call never fails, so a typed attribute
  accepts anything and stores a converted value without a word. A
  declared default never reaches `typeCast` at all. `EZField` refuses the
  same values, so the two disagree.
- **Repro:**
  ```python
  class Foo(BaseObject):
    name = AttriBox[str]('x')
    data = AttriBox[bytes](b'')
    n = AttriBox[int](0)

  foo = Foo()
  foo.name = None    # stores 'None' (new, 2026-10-01)
  foo.name = [1, 2]  # stores '[1, 2]' (new, 2026-10-01)
  foo.data = 5       # stores b'\x00\x00\x00\x00\x00'
  foo.n = (2.5,)     # stores 2, where foo.n = 2.5 raises
  AttriBox[int](2.5) # default 2
  ```
- **Fix direction (decided for 1.2):** `_resolve` sends a single value
  through `typeCast`, as `EZData` does, and keeps its own code only for
  several arguments, keyword arguments, and copying a default already of
  the field type. A compatibility change for the changelog.
- **Text part DONE (2026-10-01).** The author took the text types out of
  the 1.2 plan and into 1.1.0: `str`, `bytes` and `bytearray` follow one
  rule, since their constructors accept almost anything. Settled with
  the author:
  - `typeCast` has handlers for `bytes` and `bytearray` beside the one
    for `str`: the three convert into each other as UTF-8, and anything
    else is refused with `TypeCastException`, a `str` that UTF-8 cannot
    encode chained from its `UnicodeEncodeError`
    (`src/worktoy/utilities/_type_cast.py`, `_encodeText`, `_castBytes`,
    `_castByteArray`). This also fixes the `bytes` half of H02.
  - `AttriBox.resolveText(value)` turns a single value into the value of
    a text field, and explicitly defers to `typeCast`. It is public so a
    subclass can make text fields more or less strict, or convert them
    some other way; what it returns must still be an instance of the
    field type. A field counts as text when its type is a text type or
    based on one (`_isTextField`).
  - Both paths reach it: a default given as a single argument without
    keywords, and an assigned value not already of the field type. The
    assignment skips the generic cast for a text field, so `resolveText`
    alone decides. Several arguments or keyword arguments, as in naming
    an encoding, still go to the constructor; a default already of the
    field type is still copied for each instance.
  - On the way, the constructor call of `_resolve` moved to
    `_callFieldType`, and the turning of an assigned value into
    arguments to `_assignedArgs`, without change of behaviour.

  Tests: `tests/test_utilities/test_type_cast_text.py`,
  `tests/test_desc/test_attri_box_text.py`,
  `tests/test_desc/test_attri_box_resolve_text.py`,
  `tests/test_dispatch/test_cast_text.py` and
  `tests/test_ezdata/test_field_text_cast.py`. Of the first 18 tests, 13
  failed before the change and 5 are guards; the mutation check then
  added a nineteenth, a field typed with a subclass of `str` reaching
  `resolveText`, and a keyword default to a guard. The suite gives 1726 passed on
  3.14 with 100% line and branch coverage, 1715 passed on 3.7, and passes
  on 3.8 to 3.13. A mutation check caught all twelve breaks (each
  handler removed, the encode error left raw, a `bytearray` cast giving
  `bytes`, the `bytearray` branch of the `bytes` cast removed, the
  assignment or the default skipping `resolveText`, a lenient
  `resolveText`, exact text types instead of subclasses, the instance
  check removed, the container tuple unwrapped, keywords reaching
  `resolveText`), with the control passing.

  Changelog draft: "A field of type `str`, `bytes` or `bytearray` no
  longer accepts any value its constructor accepts. `foo.name = None`
  on an `AttriBox[str]` used to store `'None'`, and `foo.data = 5` on an
  `AttriBox[bytes]` five zero bytes; both now raise `TypeException`.
  Text converts between the three types as UTF-8. The new
  `AttriBox.resolveText` decides this, and a subclass may replace it.
  `typeCast` to `bytes` or `bytearray` follows the same rule, so
  `EZField[bytes]` refuses an `int`, and an overloaded method no longer
  passes one to a `bytes` signature as zero bytes."
- **Later the same day, with H02:** a field typed with a subclass of a
  text type follows `castRule` inside `resolveText`: held to the text
  rule when it keeps its builtin's constructor, trusted when it brings
  its own.
- **Still open, planned 1.2:** the other field types. `AttriBox[int](2.5)`
  still defaults to `2`, `foo.n = (2.5,)` still stores `2`, and any
  other field type still falls back to its constructor.

### H02. `typeCast` to a subclass of a builtin, or to `bytes`, skips the lossless rules (archived 58, DONE)

- **Where:** `src/worktoy/utilities/_type_cast.py:220-241`.
- **Problem:** the handlers of `str`, `bool`, `int`, `float`, `complex`
  and `dict` are looked up by the exact target, so a subclass of one goes
  to the constructor fallback, which rounds or truncates. The builtins
  without a handler, such as `bytes`, use the same fallback. This reaches
  every cast in the library: an `EZField[MyInt]` stores `2.5` as `2`
  where an `EZField[int]` refuses it, and the cast pass of an overloaded
  method hands an integer to a `bytes` overload as zero bytes.
- **Repro:**
  ```python
  typeCast(int, 2.5)    # TypeCastException
  typeCast(MyInt, 2.5)  # 2
  typeCast(bytes, 3)    # b'\x00\x00\x00'

  class Disp(BaseObject):
    @overload(bytes)
    def f(self, b):
      return ('bytes', b)

    @overload(str)
    def f(self, s):
      return ('str', s)

  Disp().f(3)  # ('bytes', b'\x00\x00\x00')
  ```
- **Fix direction:** find the first class along the target's method
  resolution order that has a handler, cast to it, then build the target
  from the result and keep the instance check.
- **`bytes` half DONE (2026-10-01, with H01):** `typeCast` has handlers
  for `bytes` and `bytearray`, so `typeCast(bytes, 3)` raises and
  `Disp().f(3)` no longer reaches the `bytes` overload.
- **Subclass half DONE (2026-10-01).** Settled with the author:
  - The cast keeps the subclass: the result is always an instance of
    the target, never of the bare builtin, so
    `AttriBox[SomeStr]("""Never gonna give you up""")` holds a `SomeStr`.
  - A subclass that keeps the constructor of its builtin is the builtin
    under another name and is held to its rule: the value is cast to
    the builtin, unless it is already of it, and the subclass is built
    from the result. This counts as part of the cast, so it also happens
    under `allowInstantiation=False`.
  - A subclass with a constructor of its own has stated its own
    conversion and is trusted: it goes to the ordinary fallback, its
    constructor called with the value as given, as an `IntEnum` or
    `collections.Counter` expects. "Its own" means that the `__new__` or
    `__init__` it resolves to is not that of its builtin, so a
    constructor inherited from a class in between, or an `__init__` from
    a mixin after the builtin, counts too.
  - The rule is centralized, so that `AttriBox`, `EZData` and the
    overload dispatch decide the same way: the new public
    `castRule(target)` in `worktoy.utilities` names the builtin whose
    rule applies, or `None` when the constructor decides. `typeCast`
    follows it, and the numeric check of `AttriBox.__instance_set__`,
    which makes a refused cast final instead of falling back to the
    constructor, asks it too (`castRule(fieldType) in (bool, int,
    float, complex)`), so a trusted `int` subclass such as an `IntEnum`
    keeps its own lookup.
  - Limit: the container rules of `AttriBox._resolve` stay exact, since
    a `tuple` subclass such as a `namedtuple` must keep taking several
    arguments as its fields. That belongs to the 1.2 part of H01.

  Code: `src/worktoy/utilities/_type_cast.py` (`_ruledBase`,
  `_ownsConstructor`, `castRule`, `_castRuled`, `_castSubclass`),
  `src/worktoy/utilities/__init__.py` (export), and
  `src/worktoy/desc/_attri_box.py` (the numeric check). Tests:
  `tests/test_utilities/test_type_cast_subclass.py`,
  `tests/test_utilities/test_cast_rule.py`,
  `tests/test_desc/test_attri_box_builtin_subclass.py`,
  `tests/test_ezdata/test_field_builtin_subclass.py` and
  `tests/test_dispatch/test_cast_builtin_subclass.py`. The tests of the
  plain-subclass rule failed before the first change, and those of the
  trusted constructors before the second, with the guards passing (the
  author's `SomeStr` example among them). The suite gives 1748 passed on
  3.14 with 100% line and branch coverage, 1737 passed on 3.7, and passes
  on 3.8 to 3.13. A mutation check caught all twelve breaks (never
  trusting, trusting every subclass, counting `__new__` alone, looking
  only in the subclass's own namespace, casting a value already of the
  builtin, dropping the instance check, the builtin named in the
  exception, the build left uncaught, the build refused without
  instantiation, and the `AttriBox` check made exact or `issubclass`),
  with the control passing.

  Changelog draft: "`typeCast` holds a subclass of a builtin to the rule
  of that builtin unless the subclass brings a constructor of its own.
  `class Name(str): pass` now refuses `None` and `5` as `str` does,
  where it used to store `'None'` and `'5'`, and an `int` subclass
  refuses `2.5` instead of rounding it, in `AttriBox`, `EZData` and the
  cast pass of an overloaded method alike; the value is always built as
  an instance of the subclass. A subclass with its own `__new__` or
  `__init__`, such as an `IntEnum`, is trusted and receives the value as
  given. The new `castRule` tells which applies."
- **Status:** DONE.

### H03. A plain method followed by `@overload` of the same name drops the overloads (new, DONE)

- **Where:** `src/worktoy/mcls/space_hooks/_load_space_hook.py:32-64`
  (`setItemPhase`) and `:86-98` (`postCompilePhase`).
- **Problem:** `LoadSpaceHook.setItemPhase` claims an `overload` without
  storing it in the namespace, and `postCompilePhase` builds no
  `Dispatcher` for a name the namespace holds plainly. So a plain
  definition wins whatever its position in the class body, and overloads
  written after it are discarded without a word. Python's own rule is
  that the later binding wins; with the order reversed, the result is
  right.
- **Repro:**
  ```python
  class A(BaseObject):
    def foo(self):
      return 'plain'

    @overload(int)
    def foo(self, x):
      return 'int'

  A().foo()   # 'plain'
  A().foo(1)  # TypeError: takes 1 positional argument but 2 were given
  ```
- **Fix direction:** when an `overload` arrives under a name the
  namespace already holds plainly, remove the plain entry, so the later
  binding wins as in Python. Refusing the combination with a clear
  message is the alternative; settle which while probing.
- **DONE (2026-10-01).** The author settled the rules for a name that is
  overloaded in one place and defined plainly in another:
  1. One class body giving a name both overloads and a plain definition
     raises at once, in either order. This was new.
  2. A subclass overloading a name its parent defines plainly replaces
     the plain method with the `Dispatcher` its overloads build.
  3. A subclass overloading an inherited overloaded name adds its
     signatures to the parent's, replacing the parent's function where
     the signature is the same.
  4. A subclass defining a plain method at an inherited overloaded name
     replaces the overloads entirely.

  Probes showed rules 2 to 4 already held; rules 3 and 4 were pinned by
  `test_override_precedence.py`, `test_base_precedence.py` and
  `test_plain_override.py`, and rule 2 gets a guard test of its own.
  For rule 1, settled with the author: a plain definition is any binding
  that is not an `overload` (a function, a `property`, a
  `staticmethod`, a constant, or a value another hook claims, such as an
  `EZField`); the refusal comes at the second binding, so the traceback
  points at the line that clashes; binding one overload under a second
  name, or again under its own, stays allowed.

  Code: the new `OverloadConflict` in `worktoy.waitaminute.meta`, a
  `SyntaxError` like the other refusals of a class-body line, with
  `className`, `overloadName` and `overloadsFirst`, and its message
  saying which came first. `BaseSpace` records the names the class body
  binds plainly (`getPlainNames`, `addPlainName`) and answers whether the
  body registered anything under a name (`hasOverloads`).
  `LoadSpaceHook.setItemPhase` consults both and raises; it runs ahead of
  the hooks of the namespace subclasses, so it sees a value they then
  claim. The branch of `postCompilePhase` that let a plain definition in
  the same body settle an ambiguity between two variadics is gone, since
  such a body is now refused.

  Tests: `tests/test_overload/test_overload_plain_conflict.py` (six
  tests, five of which failed before the change),
  `tests/test_overload/test_overload_replaces_plain.py` (the guard for
  rule 2), and `tests/test_overload/test_variadic_prefix_overlap.py`,
  whose `test_plain_definition_overrides` pinned the old behaviour of
  rule 1 and was rewritten as `test_plain_definition_refused`. The suite
  gives 1755 passed on 3.14 with 100% line and branch coverage, 1744
  passed on 3.7, and passes on 3.8 to 3.13. A mutation check caught all
  nine breaks (either check removed, plain names never noted or noted
  for functions alone, fallbacks not counted, `any` made `all`, the
  order flag swapped, the order ignored in the message, `msg` not set),
  with the control passing.

  Changelog draft: "A class body may no longer give one name both
  overloads and a plain definition. Such a body used to keep one of the
  two without a word, the plain method winning whichever came first; it
  now raises `OverloadConflict` at the second of them. A subclass may
  still replace what it inherits: a plain method with overloads, or
  overloads with a plain method."
- **Status:** DONE.

---

## Medium

Silent wrong results in narrower cases come first, then crashes with a
misleading message, then design questions.

### M01. A second fallback or finalizer replaces the first without a word (archived 40, DONE)

- **Where:** `src/worktoy/mcls/_base_space.py:430-466` (`addFallback`,
  `addFinalizer`).
- **Problem:** both store by name in a dict, so a second
  `@overload.fallback` or `@overload.finalize` for one name in one class
  body wins silently, where a duplicate signature raises
  `DuplicateSignature` and a second fallback on a `Dispatcher` raises
  `VariableNotNone`.
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
  with `VariableNotNone`; an inherited fallback stays replaceable.
- **DONE (2026-10-01).** Asked first, the author noted that replacing
  without a word is Python's own rule for a name defined twice, and then
  chose the rule worktoy already applies to two explicit declarations of
  one signature: `DuplicateSignature`, not `VariableNotNone`.
  `BaseSpace.addFallback` and `addFinalizer` raise it for a second,
  different function under one name in one class body; the same
  function registered again, as when an overload is bound again under its
  own name, changes nothing, and a subclass may still replace an
  inherited fallback or finalizer, which `collectFallback` and
  `collectFinalizer` already found the class body's own first. A fallback
  has no signature, so `DuplicateSignature.sig` may now hold the role,
  `'fallback'` or `'finalizer'`, and the message reads "'Dispatcher'
  already has a fallback function registered".

  Tests: `tests/test_overload/test_duplicate_fallback.py` (four tests,
  two of which failed before the change; the same function bound again
  and the subclass replacing its inherited ones are the guards). The
  suite gives 1759 passed on 3.14 with 100% line and branch coverage,
  1748 passed on 3.7, and passes on 3.8 to 3.13. A mutation check caught
  all five breaks (either check removed, the same function refused, the
  role not rendered, the roles swapped) with the control passing, after
  the message assertions were tightened to catch the fourth.

  Later the same day, at the author's request, `Dispatcher` followed:
  `setFallbackFunction` and `setFinalizerFunction` raise
  `DuplicateSignature` with the role for a second fallback or finalizer,
  where they raised `VariableNotNone`. They stay strict, refusing the
  same function too, as `Dispatcher.addSigFunc` refuses an equal
  signature whatever the function. `test_callback_setter` in
  `tests/test_dispatch/test_dispatch_umbrella.py` pinned
  `VariableNotNone` and now expects `DuplicateSignature`, and the new
  `test_second_callback_names_both` there pins which function is the
  existing one and which the duplicate. A mutation check caught all four
  breaks (either check removed, the two functions swapped, the
  finalizer's role misnamed). Suite: 1760 passed on 3.14 with 100% line
  and branch coverage; 3.7 to 3.13 pass.

  Changelog draft: "A class body registering a second
  `@overload.fallback` or `@overload.finalize` under one name raises
  `DuplicateSignature`, as two declarations of one signature do, rather
  than letting the second replace the first. The `setFallbackFunction`
  and `setFinalizerFunction` of a `Dispatcher` raise
  `DuplicateSignature` for a second fallback or finalizer as well, where
  they raised `VariableNotNone`."
- **Status:** DONE.

### M02. The stacking order decides whether a duplicate signature is caught (archived 41)

- **Where:** `src/worktoy/dispatch/_overload.py:160-203` (`_addSigFunc`),
  `src/worktoy/mcls/_base_space.py:344-402` (`_resolveCollision`).
- **Problem:** with `@overload(int)` stacked above `@overload(ARGS[int])`,
  the explicit `(int,)` is stored under the key object of the expansion,
  which carries the `__expanded_from_variadic__` marker, so a later
  explicit `@overload(int)` displaces it silently. With the decorators
  swapped the same body raises `DuplicateSignature`.
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

  Foo().bar(1)  # 'B'
  ```
- **Fix direction:** in `_addSigFunc`, remove the old entry before
  storing an explicit signature that meets an expansion.
- **DONE (2026-10-02).** `overload._addSigFunc` calls the new
  `_dropExpansion` before storing an explicit signature, which removes an
  equal signature expanded from a variadic, so the explicit one is stored
  under its own key and ranks as explicit on the namespace. It takes the
  place of the expansion at the end, as `BaseSpace._resolveCollision`
  already does; an equal explicit signature stacked twice keeps its
  place.

  Tests: `tests/test_overload/test_stacked_variadic_duplicate.py` (five
  tests, two of which failed before the change). A mutation check caught
  all three breaks (the call removed, every equal key dropped, identity
  in place of equality), with the control passing.

  Changelog draft: "An explicit `@overload` signature stacked above a
  variadic one of the same function now counts as an explicit
  declaration, as it already did stacked below it. A later declaration of
  that signature in the same class body raises `DuplicateSignature`
  instead of replacing it without a word."
- **Status:** DONE.

### M03. An `overload` bound in a second class under another name is dropped (archived 70)

- **Where:** `src/worktoy/mcls/space_hooks/_load_space_hook.py:32-53`.
- **Problem:** `__claimed_name__` is written on the `overload` object and
  outlives the class body, so a second class binding the same object
  under another name is read as an alias of a name it never bound, and
  gets no attribute.
- **Repro:**
  ```python
  ov = overload(int)(lambda self, n: ('int', n))

  class A(BaseObject):
    foo = ov

  class B(BaseObject):
    bar = ov

  'bar' in B.__dict__  # False
  ```
- **Fix direction:** keep the record of claimed names on the namespace.
- **DONE (2026-10-02).** `BaseSpace` records the name each `overload`
  object is first bound to (`addClaimedName`, `getClaimedName`, by
  identity), and `LoadSpaceHook.setItemPhase` reads that record instead
  of a `__claimed_name__` attribute on the overload, which it no longer
  writes. A second class starts without a record, so it registers the
  object under its own name; within one class body a later binding
  under another name is still an alias.

  Tests: `tests/test_overload/test_overload_rebound.py` (four tests, three
  of which failed before the change; the same name in a second class is
  the guard), with the alias tests of
  `tests/test_mcls/test_space/test_shadow_reads.py`. A mutation check
  caught all three breaks (the record never found, never written, and
  shared between namespaces), with the control passing.

  Changelog draft: "An `overload` object bound in the bodies of two
  classes is dispatched in both, under whatever name each class binds it
  to. A second class binding it under another name used to get no
  attribute at all."
- **Status:** DONE.

### M04. `Alias` breaks a staticmethod or a classmethod (archived 52)

- **Where:** `src/worktoy/desc/_alias.py:56-67`.
- **Problem:** `__set_name__` copies `getattr(owner, realName)`, which
  has already applied the descriptor protocol: a staticmethod comes back
  as a plain function that then binds as a method, and a classmethod
  comes back bound to the class declaring the alias, so subclasses get
  the wrong class.
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

  Child().h(3)    # TypeError: takes 1 positional argument but 2 were given
  GrandChild.w()  # 'Child'
  ```
- **Fix direction:** copy the raw attribute from the `__dict__` of the
  classes along the MRO, as `inspect.getattr_static` does.
- **DONE (2026-10-02).** The probe found the same break in the
  forwarding path, an alias declared on a base before the name exists:
  its staticmethod received the instance too. The new
  `Alias._getRealObject` returns the first entry under the real name in
  the `__dict__` of the classes along the MRO, and only for a name none
  of them holds, such as one a metaclass supplies, reads it from the
  class as before. `__set_name__` and the three forwarding methods all
  use it.

  Tests: `tests/test_desc/test_alias_method_kinds.py` (five tests, three
  of which failed before the change), with `tests/test_desc/test_alias.py`
  as the guard of the descriptor case. A mutation check caught all four
  breaks (the lookup reverted to `getattr`, the own namespace alone,
  `__get__` or `__set_name__` alone reverted), with the control passing.

  Changelog draft: "An `Alias` of a staticmethod or a classmethod behaves
  as the method it names. An alias of a staticmethod used to receive the
  instance when read from one, and an alias of a classmethod stayed bound
  to the class declaring the alias, so a subclass read the wrong class."
- **Status:** DONE.

### M05. `KeeBox` applies the keywords of its default to an assigned value (archived 68)

- **Where:** `src/worktoy/keenum/_kee_box.py:133-163` (`_resolveNum`).
- **Problem:** positional arguments come from the call when given, but
  keyword arguments always come from the captured default, so an
  assignment can resolve to a different member than the value names.
- **Repro:**
  ```python
  class Num(KeeNum):
    TEN = Kee[int](10)
    SIXTEEN = Kee[int](16)

  class Holder(BaseObject):
    n = KeeBox[Num]('10', base=16)

  h = Holder()
  h.n = '10'
  h.n  # Num.SIXTEEN
  ```
- **Fix direction:** read the captured keywords only when building the
  default.
- **DONE (2026-10-02).** `KeeBox._resolveNum` takes the captured
  positional and keyword arguments together, and only when called
  without arguments, that is, for the default; an assigned value is
  resolved with no keywords.

  Tests: `tests/test_keenum/test_kee_box_keywords.py` (three tests, one of
  which failed before the change; the default and a second instance are
  the guards). A mutation check caught both breaks (keywords always
  read, keywords never read), with the control passing.

  Changelog draft: "A value assigned to a `KeeBox` is resolved from the
  value alone. The keyword arguments of the default used to apply to it
  too, so `KeeBox[Num]('10', base=16)` read an assigned `'10'` in base 16
  as well."
- **Status:** DONE.

### M06. Calling an enumeration ignores extra arguments (archived L20, raised from low)

- **Where:** `src/worktoy/keenum/_kee_meta.py:313-323` (`__call__`),
  `src/worktoy/keenum/_kee_flags_meta.py:179-182` and `:268-282`.
- **Problem:** `KeeMeta.__call__` resolves the first argument and drops
  the rest, keywords included, and `KeeFlagsMeta` drops keywords the same
  way. A call with a second value silently returns the member of the
  first. A call without an identifier raises a `TypeException` saying it
  expected an instance of `object` and got `None`, which contradicts
  itself.
- **Repro:**
  ```python
  class Color(KeeNum):
    RED = Kee[int](10)
    BLUE = Kee[int](20)

  Color('RED', 'junk', x=1)  # Color.RED
  Color(10, 20)              # Color.RED
  Perm('READ', bogus=2)      # Perm.READ
  Perm(read=True)            # Perm.NULL
  Color()                    # TypeException ... instance of 'object' ...
  ```
- **Fix direction:** refuse more than one argument and any keyword with
  Python's `TypeError`, and a missing identifier with a message that says
  one is required.
- **DONE (2026-10-02).** `KeeMeta.__call__` hands its arguments to the
  new `_refuseCallArguments`, which raises a plain `TypeError` for any
  keyword ("Color() takes no keyword arguments, but received 'x'.") and
  for other than one positional argument ("Color() takes exactly one
  argument, the identifier of a member, but received 2."), the missing
  identifier included. `KeeFlagsMeta.__call__` refuses keywords the same
  way and still combines several positional identifiers, or gives `NULL`
  for none.

  Tests: `tests/test_keenum/test_kee_call_arguments.py` (six tests, four
  of which failed before the change; one identifier, and several or none
  for flags, are the guards). `test_call_empty` in
  `tests/test_keenum/test_num_mro.py` pinned the self-contradicting
  `TypeException` and now expects the `TypeError`. A mutation check
  caught all four breaks (each refusal removed, the count check loosened
  either way), with the control passing.

  Changelog draft: "Calling a `KeeNum` class takes exactly one argument,
  the identifier of a member, and calling a `KeeFlags` class takes no
  keyword arguments; anything else raises `TypeError`. `Color(10, 20)`
  used to return the member of `10` without a word, and keywords were
  dropped. Calling a `KeeNum` class without an identifier raises the
  same `TypeError` in place of a `TypeException` that contradicted
  itself."
- **Status:** DONE.

### M07. The lorem generators keep their layout when `charCount` changes (archived 69)

- **Where:** `src/worktoy/lorem_ipsum/_base_generator.py:49`, the caches
  of `_clause.py:58-59`, `_sentence.py:41-42` and `_paragraph.py:45-46`,
  and `src/worktoy/work_test/samplers/_lorem_sampler.py:52-80`.
- **Problem:** nothing clears the cached layout when `charCount` is
  assigned, so a rendered generator ignores the new count until `reset()`.
  `LoremSampler` serves one draw at the old length after
  `sampler.charCount = n`.
- **Repro:**
  ```python
  s = Sentence(40)
  str(s)
  s.charCount = 90
  len(str(s))  # 40
  ```
- **Fix direction:** an `onSet` callback on `charCount` in
  `BaseGenerator` that calls a `clear()` the subclasses extend.
- **DONE (2026-10-03).** `BaseGenerator` registers `_onSetCharCount` on
  `charCount`, which calls `clear`; the base `clear` caches nothing and
  the `clear` of `Clause`, `Sentence` and `Paragraph` replaces it. The
  copy constructors assign `charCount` before copying the caches, so a
  copy keeps the layout it copies. `LoremSampler` needed no change of
  its own, since it assigns the count to its sentence.

  Tests: `tests/test_lorem_ipsum/test_char_count_relayout.py` (five
  tests, four of which failed before the change; a layout kept between
  reads is the guard) and
  `tests/test_work_test/test_lorem_sampler_length.py` (one test, which
  failed before). A mutation check caught both breaks (the callback not
  registered, the callback doing nothing), with the control passing.

  Changelog draft: "Assigning `charCount` to a `Clause`, `Sentence` or
  `Paragraph` lays it out anew at the new count. A generator rendered
  once used to keep its old layout until `reset()`, and a `LoremSampler`
  served one draw at the old length."
- **Status:** DONE.

### M08. `onSet` receives the value as assigned, not as stored (archived L10, DECIDED)

- **Where:** `src/worktoy/core/_object.py:267-282` (`__set__`).
- **Problem:** `hookOnSet` is handed the incoming value, while the box
  stores a cast one, so an `onSet` callback on an `AttriBox[float]` sees
  `2` while the field holds `2.0`. The docstrings promise the stored
  value.
- **Repro:**
  ```python
  got = []

  class Foo(BaseObject):
    x = AttriBox[float](0.0)

    @x.onSet
    def _on(self, value):
      got.append(value)

  Foo().x = 2
  got  # [2]
  ```
- **Decision:** `preSet` receives the value as assigned, `onSet` the
  value as stored. Having `__instance_set__` report what it stored avoids
  running a `Field` getter a second time.
- **DONE (2026-10-03).** `__instance_set__` returns the value it stored,
  and `Object.__set__` hands that to `hookOnSet`, or the value as
  assigned when it returns None, so a descriptor written against the old
  contract, such as the example in the `Object` docstring, keeps working.
  `AttriBox`, `FixBox` and `KeeBox` return what they store; `Field`
  stores nothing itself and is unchanged, so its `onSet` receives the
  value its setters received. The docstrings of `Object`, `__set__`,
  `__instance_set__` and `hookOnSet` say so.

  Tests: `tests/test_desc/test_on_set_stored.py` (seven tests, four of
  which failed before the change; `preSet`, a value already of the field
  type, `Field` and a descriptor reporting nothing are the guards). A
  mutation check caught all five breaks (`onSet` given the assigned
  value, the fallback removed, and each box not reporting), with the
  control passing.

  Changelog draft: "An `onSet` callback receives the value as the field
  stores it, and a `preSet` callback the value as assigned: assigning `2`
  to an `AttriBox[float]` hands `preSet` the `2` and `onSet` the `2.0`.
  `onSet` used to receive the value as assigned as well. A descriptor
  built on `Object` reports what it stored by returning it from
  `__instance_set__`; one returning nothing hands `onSet` the value as
  assigned, as before."
- **Status:** DONE.

### M09. `typeCast(bool, x)` lets `x.__eq__` decide (archived 37)

- **Where:** `src/worktoy/utilities/_type_cast.py:52-55` (`_castBool`),
  and the cast passes of `src/worktoy/dispatch/_dispatcher.py:273-324`.
- **Problem:** `arg in (True, False, 0, 1)` compares with `==`, so an
  `__eq__` that always answers `True` casts anything to `True`, and one
  that raises escapes as its own exception, which the cast passes do not
  catch, so the fallback is never tried.
- **Repro:**
  ```python
  class AlwaysEqual:
    def __eq__(self, other):
      return True
    __hash__ = object.__hash__

  typeCast(bool, AlwaysEqual())  # True
  ```
- **Fix direction:** compare only numbers (`numbers.Number`) with `0` and
  `1`.
- **DONE (2026-10-03).** `_castBool` compares a value with `0` and `1`
  only when it is a `numbers.Number`, so anything else is refused with
  `TypeCastException` without its `__eq__` being asked, and the cast
  passes of an overloaded method move on to the next signature or the
  fallback. The `typeCast` docstring says so.

  Tests: `tests/test_utilities/test_type_cast_bool.py` (five tests, three
  of which failed before the change; the numbers equal to 0 or 1, among
  them `Fraction`, `Decimal` and `complex`, and the numbers equal to
  neither are the guards). A mutation check caught all three breaks (the
  guard removed, the comparison removed, `int` in place of `Number`),
  with the control passing.

  Changelog draft: "`typeCast` to `bool` accepts only a number equal to
  0 or 1. An object whose `__eq__` answers `True` to anything used to cast
  to `True`, and one whose `__eq__` raises let that exception escape, past
  the fallback of an overloaded method; both are now refused with
  `TypeCastException`."
- **Status:** DONE.

### M10. `EZField` defaults skip `typeCast` (archived 54, text part DONE, rest with H01 in 1.2)

- **Where:** `src/worktoy/ezdata/_ez_field.py:85-128` (`_construct`), used
  by the default recipes of `src/worktoy/ezdata/_ez_hook.py:656-666` and
  by `defaultValue`.
- **Problem:** a default is built by calling the field type, while an
  argument or an assignment goes through `typeCast`, so one class accepts
  as a default what it refuses as an argument.

  | Declaration | Default | Same value as an argument |
  |---|---|---|
  | `EZField[list]('abc')` | `['a', 'b', 'c']` | `TypeException` |
  | `EZField[int](2.5)` | `2` | `TypeException` |
  | `EZField[str](5)` | `'5'` | `TypeException` |
  | `EZField[bool](2)` | `True` | `TypeException` |
  | `EZField[str](b'ab')` | `"b'ab'"` | `'ab'` |

- **Proposal so far:** settle with H01 in 1.2, but apply the text
  refusal for container defaults (archived item 17) in 1.1.0, since
  `EZField[list]('abc')` splits the text where `AttriBox[list]('abc')`
  refuses it.
- **Decided (2026-10-03):** the author chose the fix `AttriBox` already
  has, the text part of H01, for `EZField` as well.
- **Text part DONE (2026-10-03).** `EZField._construct` follows the rules
  `AttriBox` has for its default: a lone default without keywords for a
  text type, or a subclass of one, goes through `typeCast` by the new
  `_castText`, which raises `TypeException` naming the field when the
  cast refuses, and a builtin container refuses a lone text default. A
  lone default already of the field type is still copied, and several
  arguments or keywords still go to the constructor. Rows one, three and
  five of the table now behave as an argument does. The docstrings of
  `EZField` point to `_construct` for the rules. Tests:
  `tests/test_ezdata/test_field_default_text.py` (seven; four failed
  before, and the mutation check added the subclass test and made the
  keyword guard one that only the constructor passes). Mutation check:
  the text cast removed, the container refusal removed, a lenient cast,
  exact text types instead of subclasses, `bytearray` left out of the
  text types, and keywords reaching the cast, all caught. Changelog
  draft: "An `EZField` default follows the text rules of `AttriBox`: a
  lone default for a `str`, `bytes` or `bytearray` field is cast as an
  argument is, so `EZField[str](b'ab')` defaults to `'ab'` and
  `EZField[str](5)` raises `TypeException`, and a container field refuses
  a lone text default, as in `EZField[list]('abc')`."
- **Still open, with H01 in 1.2:** the other field types, rows two and
  four: `EZField[int](2.5)` still defaults to `2`, as `AttriBox[int](2.5)`
  does.
- **Status:** text part DONE; the rest planned 1.2 with H01.

### M11. `del` in a class body does not take effect (archived 67)

- **Where:** `src/worktoy/mcls/_abstract_namespace.py:240-287`.
- **Problem:** every binding is recorded in the shadow space, which reads
  fall back to, and there is no `__delitem__`, so after `del name` the
  class body still reads the deleted value; deleting a name a hook
  claimed raises `NameError`.
- **Repro:**
  ```python
  tmp = 'GLOBAL'

  class Foo(BaseObject):
    tmp = 'LOCAL'
    del tmp
    seen = tmp

  Foo.seen  # 'LOCAL'; a plain class gives 'GLOBAL'
  ```
- **Fix direction:** a `__delitem__` that removes the name from the
  shadow space too. Whether deleting a hook-claimed name undoes its
  registration is settled while probing; refusing it is the smaller fix.
- **DONE (2026-10-03).** `AbstractNamespace.__delitem__` removes the name
  from the namespace and the shadow space alike, and raises `KeyError`,
  which the interpreter reports as `NameError`, for a name never bound.
  Deleting a name whose latest binding a hook claimed (`_isClaimed`: the
  namespace holds no value, or another one, than the shadow space) is
  refused: undoing it would need each hook to unregister, a `Kee` even
  to renumber the members after it. The probe showed the refusal cannot
  be raised from `__delitem__`: the interpreter's `DELETE_NAME` replaces
  any exception a deletion raises with its own `NameError` ("name 'foo'
  is not defined"), on every version from 3.7. So the deletion is
  recorded (`getClaimedDeletions`) and `compile` raises the new
  `ClaimedName` (`worktoy.waitaminute.meta`, a `SyntaxError` with
  `className` and `keyName`) as the class is created, before anything is
  compiled. The name `ClaimedName` follows `ReservedName`, and is open to
  review.

  Tests: `tests/test_mcls/test_space/test_class_body_del.py` (six tests,
  four of which failed before the change; a name never bound or deleted
  twice, and a name bound again after deletion, are the guards), with
  `tests/test_mcls/test_space/test_shadow_reads.py`. A mutation check
  caught all five breaks (the shadow kept, no claim found, `compile`
  silent, the identity check removed, the missing-name check removed),
  with the control passing.

  Changelog draft: "`del` in the class body of a worktoy class deletes
  the name, as in a plain class: a later read in the class body no longer
  finds the deleted value. Deleting a name an `overload`, `EZField`,
  `Kee` or `KeeFlag` claimed raises the new `ClaimedName` as the class is
  created, since the value is registered already; it used to raise a
  `NameError` saying the name was not defined."
- **Status:** DONE.

### M12. `FastBox` defaults skip the instance rule and the text refusal (archived 34)

- **Where:** `src/worktoy/desc/_fast_box.py:175-193` (`_build`).
- **Problem:** `_build` returns whatever the field type returns, without
  the two checks `AttriBox._resolve` makes: the result must be an
  instance of the field type, and a container type refuses text.
- **Repro:**
  ```python
  class Foo:
    baz = FastBox[list]('abc')

  Foo().baz  # ['a', 'b', 'c']
  ```
- **Fix direction:** make both checks in `_build`, which runs once per
  instance and field.
- **DONE (2026-10-03).** `FastBox._build` refuses a lone `str`, `bytes`
  or `bytearray` default for a builtin container field type, and a value
  the field type returns that is not an instance of it, both with
  `TypeException` naming the field. `_fast_box.py` keeps its own copies of
  the container and text tuples, since it loads before `_attri_box.py`.

  Tests: `tests/test_desc/test_fast_box_default_rules.py` (three tests,
  two of which failed before the change; an iterable for a container and
  text for a text field are the guard), with
  `tests/test_desc/test_fast_box.py`. A mutation check caught all four
  breaks (either rule removed, text refused for every field type, `bytes`
  not counted as text), with the control passing.

  Changelog draft: "The default of a `FastBox` follows the rules of
  `AttriBox`: a container field type refuses a lone text default, as in
  `FastBox[list]('abc')`, which used to default to `['a', 'b', 'c']`, and a
  field type whose constructor returns something other than an instance
  of it raises `TypeException`."
- **Status:** DONE.

### M13. A flag named `NULL` collides with the empty member (archived 28, DONE)

- **Where:** `src/worktoy/keenum/_kee_flags_space.py:70-92`
  (`addKeeFlag`), `src/worktoy/keenum/_kee_flags_meta.py:122-131`.
- **Problem:** the empty member is named `NULL`, and so is the member of
  a flag named `NULL`; the class attribute gets the later one while name
  lookup returns the first. **Addition (new, read):** the binding at
  `_kee_flags_meta.py:126` happens while the write guard is down, so a
  member also replaces, without a word, any class-body attribute of the
  same name, such as a constant `READ_WRITE = 'rw'` beside the flags
  `READ` and `WRITE`.
- **Repro:**
  ```python
  class Odd(KeeFlags):
    NULL = KeeFlag()
    ONE = KeeFlag()

  Odd.NULL.index         # 1
  Odd['NULL'] is Odd(0)  # True
  ```
- **Proposal so far:** refuse `NULL` as a flag name next to the `'_'`
  check, together with L09; refuse a member name the class body already
  binds.
- **Decided (2026-10-03):** refuse both, as proposed.
- **DONE (2026-10-03).** `KeeFlagsSpace.addKeeFlag` raises
  `KeeFlagNameError` for the flag name `NULL` beside the `'_'` check, and
  the message says the member with no flag high takes that name.
  `KeeFlagsMeta.__new__` raises the new `KeeMemberNameError` for a
  class-body binding whose name a member takes, before it binds that
  member, so `READ_WRITE = 'rw'` beside `READ` and `WRITE`, or `NULL = 0`,
  is refused whichever comes first in the body. It is raised as the class
  is created, since the flags making up the name may come after the
  binding, and subclasses `SyntaxError`, as the other refusals of a
  class-body line do; it keeps the name at `memberName`, not at `name`
  (see L46). Tests: `tests/test_keenum/test_kee_flags_member_names.py`
  (five; four failed before, the first at collection). Mutation check:
  the `NULL` refusal removed, the `NULL` message dropped, the member-name
  refusal removed, and the wrong class named, all caught. Changelog
  draft: "A `KeeFlags` class body refuses a flag named `NULL`, the name of
  the member with no flag high, with `KeeFlagNameError`, and a class-body
  attribute named as one of the members, such as `READ_WRITE` beside the
  flags `READ` and `WRITE`, with the new `KeeMemberNameError`; the member
  replaced such an attribute without a word."
- **Status:** DONE.

### M14. Deleting a `Field` runs its getter first, so a getter that raises blocks the deleter (new, DONE for 1.1, note for 1.2)

- **Where:** `src/worktoy/core/_object.py:284-308` (`__delete__`), via
  `src/worktoy/desc/_field.py:167-181`.
- **Problem:** `Object.__delete__` reads the old value through
  `__instance_get__` before deleting, which for a `Field` calls the
  user's getter. Only `AttributeError` is caught, so a getter raising
  anything else stops a registered `@x.DELETE` from running, and a getter
  with side effects runs on every `del`.
- **Repro:**
  ```python
  class Bar(BaseObject):
    x = Field()

    @x.GET
    def _getX(self):
      raise ValueError('not ready')

    @x.DELETE
    def _delX(self):
      print('deleter ran')

  del Bar().x  # ValueError: not ready; the deleter never runs
  ```
- **Fix direction:** have `Field` answer the `_deleting=True` read
  without calling the getter, since its deleters do not use the old value
  and only the `ProtectedError` message does.
- **Probe (2026-10-03):** the getter does a second job on deletion. A
  deleter that stores `DELETED`, as the `Field` docstring suggests, makes
  the getter return `DELETED` on the next `del`, and `Object.__delete__`
  turns that into `MissingVariable`; skipping the getter would run the
  deleter again without a word. Three assertions pin the present
  behaviour: in `tests/test_desc/test_field.py`, `test_field` expects a
  second `del foo.v` to raise `AttributeError`, and expects the getter's
  own `Secret` to propagate from `del`, which is the behaviour this item
  calls the bug; `test_bad_delete` expects `ProtectedError.oldVal` to be
  the value the getter returned. So the item needs a decision after all.
- **Decided (2026-10-03):** skip the getter on deletion for 1.1, with a
  note for 1.2, which may do something more complete.
- **DONE (2026-10-03).** `Field.__instance_get__` answers the
  `_deleting=True` read with None, without calling the getter, so the
  deleters run whatever the getter would do. As the decision accepted, a
  second `del` runs the deleters again, and `ProtectedError` reports no
  old value. The docstrings of `Field`, its `__instance_get__` and its
  `__instance_delete__` say so. Five assertion sites pinned the old
  behaviour and now pin the decided one: in `tests/test_desc/test_field.py`
  the second `del foo.v`, the getter's `Secret`, and the getter's
  `ReadOnlyError` on `del foo.y`, which are now reads, followed by the
  deletion; the `oldVal` of `test_bad_delete`; and
  `test_field_getter_runs_once` in
  `tests/test_desc/test_deletion_reads_storage.py`, now
  `test_field_getter_not_run`. Tests:
  `tests/test_desc/test_field_delete_skips_getter.py` (four; three failed
  before). Mutation check: the getter called on deletion again, caught.
  Changelog draft: "Deleting a `Field` no longer calls its getter, so a
  getter that raises no longer stops the deleters. A second `del` runs
  the deleters again, and `ProtectedError` for a `Field` without deleters
  reports no old value."
- **Note for 1.2:** revisit with something more complete, which reports
  the old value and notices a second deletion, as the getter did,
  without a getter that raises stopping the deleters.
- **Status:** DONE for 1.1; the note above for 1.2.

### M15. `Dispatcher.clone` shares its signatures with the original (archived 61)

- **Where:** `src/worktoy/dispatch/_dispatcher.py:606-632` (`clone`),
  `src/worktoy/dispatch/_type_sig.py:279-300` (`swapTHIS`).
- **Problem:** the clone holds the original's `TypeSig` objects, and
  `swapTHIS` rewrites them in place, so clones of a dispatcher still
  holding `THIS` resolve it to whichever class came first.
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

  B().y(B())  # DispatchException; the signature of 'B.y' reads [A]
  ```
- **Fix direction:** copy the signatures, carrying `__allow_flex__` and
  the variadic marker.
- **DONE (2026-10-03).** The probe showed the original is rewritten too:
  after the first clone was placed, `d` itself read `[A]`. `Dispatcher.clone`
  copies every concrete and variadic signature through the new
  `_copySig`, which calls the signature with no substitutions, keeping
  its types and `__allow_flex__`, and carries over
  `__expanded_from_variadic__`; the lists are new as well.

  Tests: `tests/test_dispatch/test_dispatcher_clone_sigs.py` (four tests,
  all of which failed before the change), with
  `tests/test_dispatch/test_dispatch_umbrella.py`. A mutation check caught
  all four breaks (the concrete or the variadic signatures shared again,
  the marker or the flag dropped), with the control passing.

  Changelog draft: "Each clone of a `Dispatcher` holds signatures of its
  own, so clones placed on different classes resolve `THIS` to their own
  class. The first class to receive a clone used to fix `THIS` for the
  original and every other clone."
- **Status:** DONE.

### M16. `KeeMeta` takes any attribute of the base for an inherited member (archived 53)

- **Where:** `src/worktoy/keenum/_kee_meta.py:183-194`
  (`_createMembers`); for flags, `src/worktoy/keenum/_kee_flags_space.py:98-109`.
- **Problem:** `getattr(cls.base, key)` also finds plain class
  attributes, which then land in the member list and break the class with
  a message unrelated to the cause. `KeeFlagsSpace` likewise reads
  `flags` off every base, so a plain mixin carrying a `flags` attribute
  breaks a flags class.
- **Repro:**
  ```python
  class Base(KeeNum):
    A = Kee[int](1)
    LIMIT = 10

  class Derived(Base):
    LIMIT = Kee[int](5)
  # AttributeError: 'int' object has no attribute 'name'

  class Mixin:
    flags = ['not a flag']

  class P(KeeFlags, Mixin):
    READ = KeeFlag()
  # AttributeError: 'str' object has no attribute '__member_name__'
  ```
- **Fix direction:** accept only a `KeeBase` member from the lookup, and
  take flags only from bases that are instances of `KeeFlagsMeta`.
- **DONE (2026-10-03).** The probe found a wider case: a member of some
  other enumeration, held by the base as a plain attribute, became a
  member of the subclass, so a `KeeBase` check alone would not do.
  `KeeMeta._createMembers` asks the new `_getInheritedMember`, which
  accepts what the base holds under the name only when it is a member of
  the base (`isinstance(member, cls.base)`) and otherwise builds a new
  member. `KeeFlagsSpace.__init__` reads `flags` only off bases that are
  instances of `KeeFlagsMeta`, imported locally since that file loads
  later.

  Tests: `tests/test_keenum/test_inherited_member_lookup.py` (five tests,
  four of which failed before the change; a member the base declares is
  the guard), with `tests/test_keenum/test_num_mro.py`. A mutation check
  caught all three breaks (any attribute accepted, any `KeeBase`
  accepted, flags read off every base), with the control passing.

  Changelog draft: "An enumeration takes from its base only what is a
  member there. A member named like a plain class attribute of the base
  used to break the class with an unrelated `AttributeError`, and one
  named like an attribute holding a member of another enumeration took
  that member. A plain mixin with a `flags` attribute no longer breaks a
  `KeeFlags` class."
- **Status:** DONE.

### M17. `@overload` accepts anything as a type (archived 57)

- **Where:** `src/worktoy/dispatch/_overload.py:223-254`, the
  `isinstance` passes of `src/worktoy/dispatch/_dispatcher.py:244-272`.
- **Problem:** nothing checks the entries of a signature; a call that
  misses the exact-type lookup reaches `isinstance` with a non-class and
  raises Python's `TypeError` before any later signature, cast or
  fallback.
- **Repro:**
  ```python
  class Foo(BaseObject):
    @overload(list[int])
    def bar(self, x):
      return 'list'

    @overload(str)
    def bar(self, x):
      return 'str'

  Foo().bar(MyStr('x'))  # TypeError: isinstance() argument 2 cannot be a
                         # parameterized generic
  ```
- **Fix direction:** refuse in the decorator every entry that is neither
  a class (`issubclass(type(entry), type)`) nor an `ARGS` of one;
  `Dispatcher.overload` wants the same check. `OWNER` passes that test
  and needs its own refusal (L22).
- **DONE (2026-10-03).** The new `TypeSig.validateTypes(*types,
  variadic=True)` raises `TypeException` naming the position
  (`'types[1]'`) for an entry that is not a class, the last one excepted
  when it is an `ARGS`, whose inner type is checked instead. `overload`,
  `Dispatcher.overload`, and with `variadic=False` `overload.flex` and
  `Dispatcher.flex`, call it at the declaration, before any function is
  decorated; a flexible signature takes no `ARGS`, since its entries are
  rearranged. The probe found two more entries the check refuses: an
  `ARGS` before the end, which also reached `isinstance`, and a
  `typing.Union`, which `isinstance` happens to accept from 3.10 on,
  though not on 3.7 to 3.9; it is refused on every version now. `OWNER`
  stays for L14. `test_overload_call` in
  `tests/test_dispatch/test_dispatcher.py` passed a `TypeSig` and a
  function to `overload` as types, to call the decorator wrongly; it
  now passes `int, int`, keeping its intent.

  Tests: `tests/test_overload/test_overload_entry_types.py` (eight
  tests, six of which failed before the change; the accepted classes,
  abstract bases, `THIS` and final `ARGS` are the guard). The mutation
  check first left `isinstance(entry, type)` in place of the metaclass
  test alive on 3.14, since the two differ only where `__class__` is
  forwarded, as `list[int]` does on 3.9 and 3.10; `test_pretender_refused`
  pins that on every version. It then caught all seven breaks (that
  test, `ARGS` accepted anywhere, its inner type unchecked, `ARGS` let
  through to the flexible declarations, and each of the three call sites
  removed), with the control passing.

  Changelog draft: "A declared overload signature holds classes only,
  the last entry optionally an `ARGS` of a class. `overload`,
  `overload.flex`, `Dispatcher.overload` and `Dispatcher.flex` refuse
  anything else at the declaration with `TypeException`: a parametrized
  generic such as `list[int]`, a `typing.Union`, an `ARGS` before the end,
  or any `ARGS` in a flexible signature. Such an entry used to build the
  class and make the first call that reached `isinstance` raise Python's
  own `TypeError`, past any later signature and the fallback. A
  `typing.Union`, which `isinstance` accepts from Python 3.10, is refused
  as well, since it is no class and fails on earlier versions."
- **Status:** DONE.

### M18. Flags looked up by several members or indices raise `AttributeError` (archived 43)

- **Where:** `src/worktoy/keenum/_kee_flags_meta.py:240-247`
  (`_resolveNames`), reached from `__getitem__`, `__call__` and
  `__contains__`.
- **Problem:** `_resolveNames` calls `.upper()` on every identifier, and
  `__contains__` does not catch `AttributeError`.
- **Repro:**
  ```python
  Perm[Perm.READ, Perm.WRITE]  # AttributeError: ... no attribute 'upper'
  (1, 2) in Perm               # the same
  ```
- **Fix direction:** resolve each identifier through `_resolveMember` and
  join the names, as `KeeBox._resolveFlags` does.
- **DONE (2026-10-03).** The probe found a combined name among several
  identifiers, `Perm['READ_WRITE', 'EXEC']`, missing too. `_resolveNames`
  resolves each identifier through `_resolveMember` and returns the
  member of the union of their names, so members, names in any case,
  combined names and indices mix; a miss raises what a single lookup of
  that identifier raises, the `KeyError` of a name among them.

  Tests: `tests/test_keenum/test_kee_flags_several.py` (eight tests, six
  of which failed before the change; names in any case and an unknown
  name are the guards), with `tests/test_keenum/test_kee_flags.py`. A
  mutation check caught both breaks (names upper-cased again, the last
  identifier alone), with the control passing.

  Changelog draft: "A `KeeFlags` class looked up, called or tested for
  membership with several identifiers resolves each as a single lookup
  would: `Perm[Perm.READ, Perm.WRITE]`, `Perm[1, 2]`, `Perm('read', 4)` and
  `Perm['READ_WRITE', 'EXEC']` all work, where members and indices used to
  raise `AttributeError` and a combined name matched nothing."
- **Status:** DONE.

### M19. A KeeNum lookup by an unhashable value raises `TypeError` (archived 59)

- **Where:** `src/worktoy/keenum/_kee_meta.py:491-519`
  (`_resolveFromValue`), reached from `_resolveMember` and `fromValue`.
- **Repro:**
  ```python
  class Pairs(KeeNum):
    A = Kee[tuple]((1, 2))

  Pairs((1, [2]))  # TypeError: cannot use 'tuple' as a dict key
  ```
- **Fix direction:** hash the identifier first, and fall back to the
  linear scan when that fails.
- **DONE (2026-10-03).** `_resolveFromValue` hashes the identifier
  before the cache lookup and, when that fails, compares it with each
  member value through the new `_scanValues`, which the path for an
  unhashable member value now shares. An unhashable identifier matching
  nothing raises `KeeResolveError`, and one equal to a member value, such
  as a tuple subclass refusing to be hashed, finds the member.

  Tests: `tests/test_keenum/test_kee_unhashable_value.py` (five tests,
  four of which failed before the change; a hashable value is the
  guard). A mutation check caught both breaks (the hash check removed, a
  miss returned in place of the scan), with the control passing.

  Changelog draft: "A `KeeNum` looked up by a value that cannot be
  hashed, through a call, a subscript or `fromValue`, compares it with
  the member values instead of raising Python's own `TypeError`, and
  raises `KeeResolveError` when none matches."
- **Status:** DONE.

### M20. A `__class_resolve__` without `@classmethod` breaks the lookups past the names (archived 60)

- **Where:** `src/worktoy/keenum/_kee_meta.py:277-294`
  (`_validateClassResolve`) and `:561-564`.
- **Problem:** only callability is checked, so a plain function passes
  and every lookup reaching the hook calls it unbound.
- **Repro:**
  ```python
  class Num(KeeNum):
    A = Kee[int](1)

    def __class_resolve__(cls, identifier):
      return NotImplemented

  Num(1)  # TypeError: missing 1 required positional argument
  ```
- **Fix direction:** refuse a plain function or a staticmethod there with
  `UnboundClassHook`, from `KeeSpace`.
- **DONE (2026-10-03).** `KeeSpaceHook.setItemPhase` raises
  `UnboundClassHook` when the class body binds `__class_resolve__` to a
  plain function or a staticmethod, at that line. The probe showed a
  staticmethod taking the identifier alone did work, since the hook is
  called as `cls.__class_resolve__(identifier)`; it is refused all the
  same, as `NamespaceHook` refuses a staticmethod for every routed
  `__class_*__` hook, and the classmethod stays the one form. Open to
  review if a working staticmethod should be kept.

  Tests: `tests/test_keenum/test_kee_class_resolve_unbound.py` (three
  tests, two of which failed before the change; the classmethod is the
  guard). A mutation check caught all three breaks (the check removed,
  staticmethods let through, every name checked), with the control
  passing.

  Changelog draft: "A `KeeNum` class body binding `__class_resolve__`
  without `@classmethod` raises `UnboundClassHook` at that line. A plain
  function used to pass and make every lookup that reached it raise
  Python's own `TypeError`; a staticmethod is refused as well, as for the
  other class hooks."
- **Status:** DONE.

### M21. `KeeFlagsMeta.__eq__` raises when the other operand's hash fails (archived 39)

- **Where:** `src/worktoy/keenum/_kee_flags_meta.py:201-209`.
- **Problem:** `__eq__` hashes the other operand and re-raises every
  `TypeError` whose wording lacks `'hashable type'`, so comparing a flags
  class with a member of unhashable value raises, as does `in` on a list
  holding one. The method only ever returns `NotImplemented` or `False`.
- **Repro:**
  ```python
  class Bag(KeeNum):
    A = Kee[list]([1, 2])

  Perm == Bag.A  # TypeError: Enumeration member 'Bag.A' is unhashable ...
  ```
- **Fix direction:** remove `__eq__` and keep `__hash__`.
- **DONE (2026-10-03).** `KeeFlagsMeta.__eq__` is gone, so a flags class
  compares by identity, as `type` does, and an object of another type
  decides through its own `__eq__`; `__hash__` stays. Two tests in
  `tests/test_keenum/test_kee_flags_meta.py` pinned the method removed:
  `testEqualityOperatorTrue` called `KeeFlagsMeta.__eq__` directly and
  now checks identity for every pair of example classes, and
  `testNotImplementedEqualOperator` expected `cls == Breh(69)` to raise
  the hash error of the other operand, the very behaviour of this item;
  it now checks that the other operand decides and is never hashed.

  Tests: `tests/test_keenum/test_kee_flags_class_eq.py` (four tests, two
  of which failed before the change; identity and use as a dict key are
  the guards). A mutation check caught both breaks (the method restored,
  the hash removed), with the control passing.

  Changelog draft: "Comparing a `KeeFlags` class with an object that
  cannot be hashed, such as a member of an unhashable value, answers
  `False` instead of raising, and so does `in` on a list holding one. A
  flags class compares by identity."
- **Status:** DONE.

### M22. An EZData `__class_init__` sees fields without an owner (archived 42)

- **Where:** `src/worktoy/ezdata/_ez_meta.py:206-228` (`EZMeta.__init__`).
- **Problem:** the inherited `__init__` runs `__class_init__` before the
  owners are bound.
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
  `__init__`, as `KeeMeta` does.
- **DONE (2026-10-03).** `EZMeta.__init__` binds `__field_owner__` on
  every field, own and inherited, before calling the inherited
  `__init__`, which runs `__class_init__` and notifies the bases.

  Tests: `tests/test_ezdata/test_class_init_owner.py` (two tests, both of
  which failed before the change). A mutation check caught the break
  (the owners bound after again), with the control passing.

  Changelog draft: "The `__class_init__` of an `EZData` class sees each
  field bound to its owner, the class itself for inherited fields too.
  It used to raise `MissingVariable` reading `fieldOwner`."
- **Status:** DONE.

### M23. `EZField[list[int]]` is not refused at the subscript (archived 33)

- **Where:** `src/worktoy/ezdata/_ez_field.py:331-355`
  (`__class_getitem__`), `:202-226` (`_getFieldType`).
- **Problem:** any subscript is stored. On 3.9 and 3.10 the class builds
  and the first instance fails inside `isinstance`; from 3.11 the class
  is refused by a general check whose message names `'__field_type__'`
  rather than the field.
- **Fix direction:** judge the subscript in `__class_getitem__` with
  `issubclass(type(fieldType), type)` and refuse anything else there.
- **DONE (2026-10-03).** `EZField.__class_getitem__` raises
  `TypeException` naming `fieldType` for a subscript whose type is not a
  metaclass: a parametrized generic from `typing` or the builtins, an
  object posing as a class through `__class__`, and a `TypeVar`, which
  `EZField`, unlike the boxes, has no generic use for.

  Tests: `tests/test_ezdata/test_field_generic_subscript.py` (four
  tests, three of which failed before the change; a plain class and an
  abstract base are the guard). A mutation check caught both breaks (the
  check removed, `isinstance` in place of the metaclass test, caught by
  the posing object), with the control passing.

  Changelog draft: "`EZField[list[int]]` and any other subscript that is
  not a class raise `TypeException` at the subscript, naming
  `fieldType`. Such a field used to build a class on Python 3.9 and
  3.10 whose first instance failed inside `isinstance`, and on later
  versions failed the class statement with a message naming
  `__field_type__`."
- **Status:** DONE.

### M24. `@overload` stacked on `@overload.flex` or `@overload.fallback` fails late (archived 29, DONE)

- **Where:** `src/worktoy/dispatch/_overload.py:205-217`
  (`_extendLatest`) and `:244-252`.
- **Problem:** under `flex` the stacked signature lands on a
  `PermuterMethod` of the wrong arity and fails at call time; under a
  fallback-only overload the class body raises a bare `RuntimeError`. The
  other order fails at class creation with messages naming neither
  decorator.
- **Repro:**
  ```python
  class Baz(BaseObject):
    @overload(int)
    @overload.fallback
    def bar(self, *args):
      return args
  # RuntimeError: no function has been registered on this 'overload' yet
  ```
- **Proposal so far:** refuse the combination, in either order, with a
  message naming both decorators.
- **Probe (2026-10-03):** every stacking failed, `finalize` alike with
  `fallback`. `@overload` asks the object below for the function it
  decorates, `__latest_func__`, which `fallback` and `finalize` never set
  and `flex` left at the wrapper of its last arrangement, of the wrong
  arity; and `flex`, `fallback` and `finalize` took an `overload` below
  them for the function.
- **Decided (2026-10-03):** the author chose to allow the stacking, since
  it has a reasonable behaviour to expect, and stacking is very helpful.
- **DONE (2026-10-03).** A stack decorates one function, and each
  decorator adds one role for it, in any order. The new
  `overload._stackOn` gives `flex`, `fallback` and `finalize` the
  `overload` from below with its function, or a new one decorating the
  plain function, which it records as `__latest_func__`; `flex` leaves the
  plain function there, not a wrapper. `LoadSpaceHook.setItemPhase`
  registers every role an `overload` carries, where it stopped at a
  fallback or a finalizer. `str()` of an `overload` lists each role. The
  class docstring describes the stacking. Tests:
  `tests/test_overload/test_overload_stacked_roles.py` (four, failing
  before at collection), with everyday classes: a `Money` whose text
  overload is also its fallback, a `Label` taking a lone text or text and
  size in either order, and a method that is also its finalizer, each in
  both orders. Mutation check: `flex` leaving its wrapper as the
  function, an `overload` below ignored, a role decorator not recording
  its function, the hook stopping at a fallback, the hook stopping at a
  finalizer, and the fallback missing from `str()`, all caught; the test
  `Money('12')` was added when the first run let the fallback stop
  through. Changelog draft: "`@overload` stacks with `@overload.flex`,
  `@overload.fallback` and `@overload.finalize` in any order: each
  decorator of a stack adds a role for the one function, so a function
  can be both the `str` overload and the fallback, or serve a lone `str`
  beside both orders of `str` and `int`. These stacks used to fail."
- **Status:** DONE.

### M25. `__class_*__` hooks are ignored on KeeNum and KeeFlags classes (archived 48, DONE)

- **Where:** `src/worktoy/keenum/_kee_meta.py:313-433`,
  `src/worktoy/keenum/_kee_flags_meta.py:78-212`.
- **Problem:** both metaclasses override the operations
  `AbstractMetaclass` hands to `__class_*__` hooks, without handing over,
  so such hooks in an enumeration body are accepted and never called;
  `__class_call__` replaces member creation and breaks the class
  statement.
- **Repro:**
  ```python
  class Num(KeeNum):
    A = Kee[int](1)

    @classmethod
    def __class_len__(cls):
      return 69

  len(Num)  # 1
  ```
- **Proposal so far:** refuse, in an enumeration body, the hooks its
  metaclass overrides.
- **Probe (2026-10-03):** a `Weekday` with a `__class_len__` of five
  working days still measured seven, and its `__class_contains__` and
  `__class_str__` were never called. A `__class_call__` giving a default
  colour broke the class statement with `AttributeError: type object
  'Color' has no attribute 'RED'`: `KeeMeta` creates the members through
  the inherited `__call__`, which handed the call to the hook before any
  member existed. On a `KeeFlags` the hooks were honoured inconsistently,
  `__class_str__` working since `KeeFlagsMeta` leaves `__str__` alone,
  `__class_len__` dead. `EZMeta` has had the same gap for `__class_iter__`,
  `__class_len__` and `__class_contains__` since L11.
- **Decided (2026-10-03):** refuse at the class statement, as proposed,
  with the check in the shared namespace hook so that it covers `EZData`
  too; the hooks that work today keep working.
- **DONE (2026-10-03).** `NamespaceHook.setItemPhase` raises the new
  `ShadowedClassHook` (`worktoy.waitaminute.meta`, a `SyntaxError` like
  `UnboundClassHook`, with `className`, `hookName`, `metaclassName` and
  `methodName`) for a routed `__class_*__` hook whose operation a
  metaclass between the one building the class and `AbstractMetaclass`
  implements in its own namespace (`_getShadowingMetaclass`), naming
  that metaclass, so an enumeration of a `FontMeta(KeeMeta)` is told
  that `KeeMeta` implements `__len__`. The check reads the metaclass
  alone, so it covers `KeeMeta`, `KeeFlagsMeta`, `EZMeta` and a user
  metaclass alike, and refuses only what is dead: `__class_hash__` on a
  `KeeNum`, `__class_str__` on a `KeeFlags` and every hook on a
  `BaseObject` pass as before. `__class_init__` is exempt
  (`_getChainedHooks`), since every metaclass `__init__` hands over to
  the inherited one, which calls it. The shadow check runs ahead of the
  `UnboundClassHook` check, since no form of a dead hook could run, and
  a namespace built for a metaclass not based on `AbstractMetaclass`
  refuses none. The docstrings of `NamespaceHook`, `AbstractMetaclass`,
  `KeeMeta`, `KeeFlagsMeta` and `EZMeta` say so.

  Tests: `tests/test_mcls/test_hooks/test_shadowed_class_hook.py`
  (seven), `tests/test_keenum/test_kee_shadowed_class_hook.py` (nine),
  `tests/test_ezdata/test_ez_shadowed_class_hook.py` (four) and a fourth
  test in `tests/test_waitaminute/test_syntax_error_message.py`;
  thirteen failed before the change, and the hooks the metaclasses leave
  alone, `__class_init__`, a `BaseObject` with every hook and the
  namespace of a plain metaclass are the guards. The suite gives 2019
  passed and 50 skipped on 3.14 with 100% line and branch coverage, 2007
  passed on 3.7, and passes on 3.8 to 3.13. A mutation check caught all
  eight breaks (the check removed, `AbstractMetaclass` searched too,
  `__class_init__` not exempt, the building metaclass named instead of
  the implementing one, the unbound check run first, the hook name
  reported as the method, `msg` not set, the guard for a plain metaclass
  removed), with the control passing.

  Changelog draft: "A class body binding a `__class_*__` hook that its
  metaclass never calls, because the metaclass implements the operation
  itself, raises the new `ShadowedClassHook` at that line. `KeeMeta`
  implements calling, length, iteration, membership, printing, attribute
  access and the instance and subclass checks for its enumerations,
  `KeeFlagsMeta` most of the same and hashing, and `EZMeta` iteration,
  length and membership over its fields, so a `__class_len__` in such a
  body used to be accepted and never called, and a `__class_call__` in an
  enumeration body broke the class statement with an unrelated
  `AttributeError`. The hooks for the operations a metaclass leaves alone
  keep working."
- **Status:** DONE.

### M26. Sentinels are unique by bare name across the process (archived 47, DONE)

- **Where:** `src/worktoy/core/sentinels/_sentinel.py:38-84`.
- **Problem:** one registry keyed by `__name__`, so a sentinel of the
  same name in another library receives the first one, docstring and
  all.
- **Repro:**
  ```python
  class THIS(Sentinel):
    pass

  from worktoy.core import sentinels
  THIS is sentinels.THIS  # True
  ```
- **Proposal so far:** key the registry by module and qualified name.
- **Probe (2026-10-03):** a `ledger` module declaring `PENDING` and a
  `mailer` module declaring its own got one sentinel: `mailer.PENDING`
  carried the ledger's docstring and module, and the ledger's
  `post(mailer.PENDING)` posted it. An app's own `DELETED` was worktoy's.
- **Decided (2026-10-03):** the author turned the proposal down. A
  sentinel defines one concept for the whole process, and two modules
  each declaring their own take on a concept misunderstand the premise,
  so a second sentinel at a taken name is banned, with a precise
  exception in place of the silent return of the first, which was the
  bug.
- **DONE (2026-10-03).** `SentinelMeta.__new__` raises the new
  `DuplicateSentinel` (`worktoy.waitaminute.meta`, a `TypeError` like
  `IllegalInstantiation`, with `sentinelName`, `existing` and `module`)
  for a class statement at a registered name. The message names the
  sentinel, the module of the existing one and the module of the refused
  class statement, or "a class statement" for a namespace naming no
  module, as a plain dict given to `SentinelMeta` by hand. The
  `_recursion` re-fetch after registration went with the path that
  returned the existing sentinel. No worktoy module is ever reloaded in
  the suite, so nothing re-runs a sentinel class statement. Two tests in
  `tests/test_core/test_sentinels.py` pinned the old machinery and were
  removed: `test_registry_singleton` expected a `class THIS(Sentinel)` in
  the test module to receive worktoy's `THIS`, the very behaviour of this
  item, and `test_recursion` the guard of the removed re-fetch. The
  docstrings of `SentinelMeta`, `Sentinel` and the `sentinels` package
  say so.

  Tests: `tests/test_core/test_duplicate_sentinel.py` (five; four failed
  before, two sentinels of distinct names being the guard). The suite
  gives 2022 passed and 50 skipped on 3.14 with 100% line and branch
  coverage, 2010 passed on 3.7, and passes on 3.8 to 3.13. A mutation
  check caught all six breaks (the existing sentinel returned again, the
  module dropped, the wrong existing named, the registration dropped, the
  message for a namespace without a module gone, the module of the
  existing one unnamed), with the control passing.

  Changelog draft: "A class statement declaring a sentinel at a name a
  sentinel already holds raises the new `DuplicateSentinel`, naming the
  existing sentinel and both modules. A sentinel defines one concept for
  the whole process. The second class statement used to receive the
  existing sentinel without a word, docstring and module included, so
  two unrelated modules each declaring a `PENDING` shared one object, and
  a `DELETED` of one's own was worktoy's."
- **Status:** DONE.

### M27. `SymbolicName` compares by identity (archived 49, DONE)

- **Where:** `src/worktoy/desc/_symbolic_name.py:23-154`.
- **Repro:** `SymbolicName('a', 'b') == SymbolicName('a', 'b')` is
  `False`, although the class behaves as a value everywhere else.
- **Proposal so far:** compare and hash by its words, perhaps ignoring
  case, since every rendering normalises it.
- **Probe (2026-10-03):** a settings table keyed by names grew a second
  entry for `SymbolicName('font', 'size')` and raised `KeyError` looking
  it up again, `{a, b}` held two, and an `EZData` with a `SymbolicName`
  field never equalled another, `Option() == Option()` included; the one
  EZData test holding a name compares `.words` to get around it.
- **Decided (2026-10-03):** compare and hash by the words, ignoring
  case, as every rendering does.
- **DONE (2026-10-03).** `SymbolicName.__eq__` compares the lower-cased
  words of two names (`_getKey`), in order, and answers `NotImplemented`
  for anything else; `__hash__` hashes the same tuple, so a name serves
  as a key. The class docstring says so. Tests:
  `tests/test_desc/test_symbolic_name_equality.py` (seven; five failed
  before, the different words and the other types being the guards). The
  suite gives 2029 passed and 50 skipped on 3.14 with 100% line and
  branch coverage, 2017 passed on 3.7, and passes on 3.8 to 3.13. A
  mutation check caught all six breaks (`__eq__` removed, `__hash__`
  removed, case kept, order ignored, `False` in place of
  `NotImplemented`, the hash case-sensitive), with the control passing.

  Changelog draft: "Two `SymbolicName` objects of the same words compare
  equal and hash alike, ignoring case, as every rendering of them is the
  same string, so a name serves as a dict key and an `EZData` holding one
  equals another of the same name. A name used to compare and hash by
  identity."
- **Status:** DONE.

### M28. Worktoy values are read-only descriptors as class-level defaults (archived 56, planned 1.2)

- **Where:** `src/worktoy/core/_object.py` (`__set__`,
  `__instance_set__`), `src/worktoy/keenum/_kee_num.py:156-158`.
- **Problem:** `EZData`, `KeeBase` and `BaseObject` instances are
  `Object`s and so data descriptors; as a class-level default they refuse
  assignment on instances.
- **Repro:**
  ```python
  class Car:
    color = Color.RED

  Car().color = Color.BLUE
  # ReadOnlyError: ... read-only attribute 'Car.None' ...
  ```
- **Direction:** the value classes stop being based on the descriptor
  base, a redesign for 1.2.
- **Status:** planned 1.2.

### M29. Variadic declarations are expanded into concrete signatures (archived 55, message part DONE, rest planned 1.2)

- **Where:** `src/worktoy/dispatch/_overload.py:160-203` and `:97`,
  `src/worktoy/mcls/_base_space.py:344-416`,
  `src/worktoy/mcls/space_hooks/_load_space_hook.py:86-91`.
- **Problem:** `@overload(int, ARGS[str])` is stored as six concrete
  signatures plus the variadic one, so the registrations mix declarations
  with machinery copies, which needs collision rules, an ambiguity record
  and an arbitrary limit of five, and causes M02, L13 and L33. The
  expansions also detect two variadics overlapping on a prefix, which a
  redesign has to keep.
- **Proposal so far:** one registration per variadic declaration, an
  exact-type pass over the variadic signatures, and a direct overlap
  check.
- **Probe (2026-10-03):** a `Stats` with `@overload(ARGS[float])` and
  `@overload(str, ARGS[float])` holds twelve concrete signatures and two
  variadic ones behind the two declarations; both dispatch, and `str()`
  lists the declarations as written. A call of six samples, one past the
  limit, leaves the hash lookup and takes about twice as long as one of
  five (0.064s against 0.141s for 20000 calls). Two variadics overlapping
  on a prefix, `@overload(ARGS[int])` beside `@overload(int, ARGS[int])`,
  were refused with a `DuplicateSignature` naming `<TypeSig: [int]>`, an
  expansion neither declaration wrote.
- **Decided (2026-10-03):** keep the expansion for 1.1 and fix the
  message now; the redesign is planned for 1.2.
- **Message part DONE (2026-10-03).** Each signature expanded from a
  variadic declaration records that declaration at
  `__expanded_from_variadic__`, where it held `True`, so the marker still
  reads as a flag everywhere it is tested and names the declaration;
  `Dispatcher._copySig` carries it over. The ambiguity record of
  `BaseSpace` holds both equal expansions, `(name, sig, oldSig, oldFunc,
  newFunc)`, and `LoadSpaceHook.postCompilePhase` raises the new
  `VariadicOverlap` (`worktoy.waitaminute.dispatch`, a
  `DuplicateSignature`, so the two tests expecting that still hold) with
  `overloadName`, `firstSig` and `secondSig` beside the inherited `sig`,
  `existing` and `duplicate`. Its message names the two declarations as
  written, the shared signature both accept, the two functions, and the
  way to settle it: the shared signature declared explicitly on the
  function meant to receive it. Tests:
  `tests/test_overload/test_variadic_overlap_message.py` (five; four
  failed before, the plain duplicate being the guard), with
  `tests/test_overload/test_variadic_prefix_overlap.py` and
  `tests/test_dispatch/test_dispatcher_clone_sigs.py`, whose marker
  assertions hold unchanged. The suite gives 2034 passed and 50 skipped
  on 3.14 with 100% line and branch coverage, 2022 passed on 3.7, and
  passes on 3.8 to 3.13. A mutation check caught all six breaks (the
  plain `DuplicateSignature` raised again, the declarations swapped, the
  marker left `True`, the message showing the shared signature alone,
  the clone dropping the declaration, the record without the old
  expansion), with the control passing.

  Changelog draft: "Two variadic overload declarations of different
  functions that both accept the same call, such as
  `@overload(ARGS[int])` beside `@overload(int, ARGS[int])`, are refused
  with the new `VariadicOverlap`, a `DuplicateSignature` naming the two
  declarations as written and the call they share. The refusal used to
  name only a signature neither declaration wrote."
- **Planned 1.2:** one registration per variadic declaration, an
  exact-type pass over the variadic signatures keyed by prefix and
  length, so that no call falls off the fast path at the sixth argument,
  and a direct prefix-overlap check in place of the expansions, the
  collision rules, the ambiguity record and the limit of five.
- **Status:** message part DONE; the rest planned 1.2.

### M30. An EZData class refuses the class keyword of a base's own `__init_subclass__` (archived 66, planned 1.2)

- **Where:** `src/worktoy/ezdata/_ez_hook.py:98-115` (`preparePhase`).
- **Repro:**
  ```python
  class Tagged:
    def __init_subclass__(cls, tag=None, **kwargs):
      super().__init_subclass__(**kwargs)
      cls.tag = tag

  class Point(EZData, Tagged, tag='hello'):
    x = EZField[int](0)
  # ClassKeywordError: ... the class keyword 'tag' ...
  ```
- **Direction:** accept a keyword that an `__init_subclass__` along the
  bases declares, or let such a base declare its keywords.
- **Status:** planned 1.2.

### M31. On 3.14, classes of some metaclasses report the wrong `__annotations__` (archived 15, out of scope)

- **Where:** every worktoy metaclass whose own body holds annotations:
  `EZMeta`, `KeeMeta`, `KeeFlagsMeta`, `KeeMetaMeta`, `MetaFlow`,
  `_MetaARGS`.
- **Problem:** without `from __future__ import annotations`, on 3.14
  `cls.__annotations__` finds the metaclass's own dict and falls through
  to a base's, such as that of `Object`.
  `annotationlib.get_annotations(cls)` answers correctly.
- **Status:** out of scope; a proper fix needs a change to the language.

### M32. Stacked decorators of a hand-wired `Dispatcher` register the dispatcher itself (new, DONE)

- **Where:** `src/worktoy/dispatch/_dispatcher.py` (`overload`, `flex`,
  `fallback` and `finalize`).
- **Problem:** each decorator returns the dispatcher, so a decorator
  stacked above another receives the dispatcher itself and registers it:
  as the body of its signature, which raises "'Dispatcher' object is not
  callable" when a call reaches it, or as the fallback or the finalizer,
  which raises as the class is created. The docstring of
  `Dispatcher.overload` promised that stacked layers work. Found while
  deciding M24.
- **Repro:**
  ```python
  class Temperature:
    __init__ = Dispatcher()

    @__init__.overload(float)
    @__init__.overload(int)
    def __init__(self, degrees) -> None:
      self.degrees = float(degrees)

  Temperature(20)    # 20.0
  Temperature(20.5)  # TypeError: 'Dispatcher' object is not callable
  ```
- **Decided (2026-10-03):** the author asked whether a `Dispatcher.__call__`
  could catch this. A prototype forwarding such a call to the last
  function given showed it cannot: at call time the dispatcher knows only
  its last function, which may belong to another stack, so with a later
  `@__init__.overload(str)` the call `Temperature(20.5)` ran the `str` body
  without a word. A `__call__` would also make every dispatcher callable,
  where `setFallbackFunction` and `setFinalizerFunction` refuse what is
  not. The author chose to catch it in the decorators.
- **DONE (2026-10-03).** The new `Dispatcher._stackedFunction` records the
  function a decorator is given, and gives a decorator that receives the
  dispatcher itself the function of its stack instead, raising
  `MissingVariable` when the dispatcher is given itself before any
  function. All four decorators go through it, so a stack decorates one
  function and each decorator adds one role for it, in any order, as the
  `overload` decorators of a `BaseObject` do since M24. No `__call__` was
  added. Tests: `tests/test_dispatch/test_dispatcher_stacked_decorators.py`
  (five, failing before at collection), with the `Temperature` above
  beside a later `str` overload, and a `Money`, a `Label` and a `Ticker`
  on plain classes in both orders. Mutation check: the redirect removed,
  the function not recorded, the guard against no function removed, and
  each of the four decorators skipping the helper, all caught. Changelog
  draft: "The decorators of a `Dispatcher` wired by hand stack: in
  `@d.overload(float)` above `@d.overload(int)`, both signatures run the
  one function, where the outer layer registered the dispatcher itself
  and a call raised `TypeError`. `flex`, `fallback` and `finalize` stack
  the same way, in any order."
- **Status:** DONE.

---

## Low, style, cosmetic and docstrings

### Behaviour

Ordered roughly by how easily ordinary code reaches them.

- **L01. `TypeException` and `MissingVariable` cannot render a `typing`
  alias on 3.7 to 3.9 (new; D14 covers the docstring example).**
  `src/worktoy/waitaminute/_type_exception.py:51` and
  `src/worktoy/waitaminute/_missing_variable.py:75,78` read `__name__`
  off each expected type, which `typing.Callable` lacks before 3.10, so
  `str(TypeException('f', 3, Callable))` raises `AttributeError` on 3.7.
  `KeeTypeException` already uses `getattr(t, '__name__', str(t))`.
  **DONE (2026-10-03):** both read `getattr(t, '__name__', str(t))`.
  Tests: `tests/test_waitaminute/test_unnamed_expected_type.py` (four;
  three failed before, since an object without `__name__` reproduces
  on 3.14 what `typing.Callable` does on 3.7 to 3.9). Mutation check:
  either renderer reverted, caught. Changelog draft: "`TypeException`
  and `MissingVariable` render an expected type without a `__name__`,
  such as `typing.Callable` before Python 3.10, where their own message
  used to raise `AttributeError`."
- **L02. A `StochasticWord` subclass with a gap in its word lengths fails
  at random (new).** `src/worktoy/lorem_ipsum/_stochastic_word.py:102-146`.
  The docstring assumes the lengths are gapless across `[minVal,
  maxVal]` and nothing checks it: with words of lengths 2, 6 and 8,
  `realize()` raised `IndexError` in 115 of 200 draws. Refusing a gap in
  `__class_init__` moves the failure to the class statement.
  **DONE (2026-10-03):** `__class_init__` calls the new `_refuseGaps`,
  which raises `ValueError` naming the class and the missing lengths;
  the class docstring says so. Tests:
  `tests/test_lorem_ipsum/test_stochastic_word_gap.py` (two; one failed
  before). Mutation check: the call removed, caught. Changelog draft: "A
  `StochasticWord` subclass whose words leave a length out between the
  shortest and the longest is refused with `ValueError` at its class
  statement, where `realize` used to raise `IndexError` at random."
- **L03. Every worktoy class claims to be iterable (new).**
  `src/worktoy/mcls/_abstract_metaclass.py:212-264` defines `__iter__`,
  `__len__` and `__contains__` on the metaclass, so every worktoy class
  passes `isinstance(cls, collections.abc.Iterable)` and then raises
  `TypeError` when iterated. `unpack([BaseObject, int])` raises "type
  object 'BaseObject' is not iterable" (`src/worktoy/utilities/_unpack.py:66`).
  Related to L13.
  **DONE (2026-10-03):** the claim itself is inherent to the
  `__class_iter__` hook, which needs `__iter__` on the metaclass, so the
  fix is in `unpack`: the new `_iterate` keeps the `Iterable` check and
  then asks `iter()`, as Python's documentation recommends, and an
  object refusing iteration with `TypeError` is kept whole. An
  enumeration, which iterates, is flattened as before. Tests:
  `tests/test_utilities/test_unpack_classes.py` (three; two failed
  before). Mutation check: the claim trusted again, caught. Changelog
  draft: "`unpack`, and so `joinWords`, keep a worktoy class whole
  instead of raising `TypeError`: every such class claims to be
  iterable, through the `__iter__` its metaclass defines for the
  `__class_iter__` hook."
- **L04. `Arrangement` accepts a non-permutation (new).**
  `src/worktoy/utilities/combinatorics/_arrangement.py:67-79` checks only
  the length of `forward`: `Arrangement(('a', 'b', 'c'), (0, 0, 2))`
  builds a wrong `inverse`, and `restoreFrom(applyTo(1, 2, 3))` gives
  `(1, 1, 3)`.
  **DONE (2026-10-03):** `Arrangement.__init__` raises `ValueError` when
  the sorted recipe is not `range(len(items))`. Tests:
  `tests/test_utilities/test_arrangement_permutation.py` (three; two
  failed before). Mutation check: the check removed, caught. Changelog
  draft: "`Arrangement` refuses a `forward` recipe that is not a
  permutation of the positions of its items with `ValueError`."
- **L05. A `Generic` base under a worktoy metaclass still sends class
  keywords to `object` (new).** `src/worktoy/core/_meta_type.py:55-65`.
  `_takesKeywords` counts `Generic.__init_subclass__` as accepting
  keywords, but it forwards them to `object`, so
  `class H(Generic[T], metaclass=BaseMeta, trustMeBro=True)` raises
  `TypeError`. A class also based on `Object` is unaffected.
  **DONE (2026-10-03):** `_takesKeywords` skips `typing.Generic` as it
  skips `object`; on 3.14 its `__init_subclass__` is a C-level
  classmethod handing the keywords on. `typing.Protocol` needs no entry,
  since its metaclass conflicts with the worktoy ones. Tests:
  `tests/test_core/test_generic_class_keywords.py` (two; one failed
  before, a base with its own `__init_subclass__` is the guard).
  Mutation check: `Generic` counted again, caught. Changelog draft: "A
  generic class of a worktoy metaclass, such as `class H(Generic[T],
  metaclass=BaseMeta, trustMeBro=True)`, takes class keywords; they used
  to reach `object.__init_subclass__` through `Generic` and raise."
- **L06. `Field(other)` drops the `setName` callbacks (archived L6).**
  `src/worktoy/desc/_field.py:228-237` copies every callback group but
  `__set_name_keys__`.
  **DONE (2026-10-03):** the group is copied. Tests:
  `tests/test_desc/test_field_copy_set_name.py` (one, which failed
  before). Mutation check: the group dropped again, caught. Changelog
  draft: "`Field(other)` copies the `setName` callbacks of `other`
  along with the others."
- **L07. `AttriBox[object](None)` is refused with a contradictory message
  (archived L26).** `src/worktoy/desc/_attri_box.py:308-324` uses `None`
  to mean "not built yet", so a lone `None` default goes to `object(None)`.
  **DONE (2026-10-03):** `_resolve` marks a copied default with a flag,
  not with `None`. Tests: `tests/test_desc/test_attri_box_none_default.py`
  (three; two failed before, `AttriBox[type(None)](None)` among them).
  Mutation check: `None` read as unbuilt again, caught. Changelog draft:
  "`AttriBox[object](None)` defaults to `None` instead of being refused
  with a message saying `None` is not an `object`."
- **L08. A builtin function in an EZData body becomes a field (archived
  L27, changed).** `src/worktoy/ezdata/_ez_hook.py:187-200` passes only a
  `FunctionType` through, so `helper = len` becomes a field. Since
  `_construct` copies a lone argument, the class now builds, and `len`
  shows up in the fields, the constructor, `asDict` and `repr`
  (`Foo()` gives `Foo(<built-in function len>)`). Pass any callable
  through, or refuse it as class objects are.
  **DONE (2026-10-03):** the probe showed bound methods and
  `functools.partial` already pass, as descriptors, so only builtins
  were caught. `setItemPhase` lets a `BuiltinFunctionType` through as it
  does a `FunctionType`; a callable instance of an ordinary class stays a
  value, and so a field, as any other instance does. Open to review if
  every callable should pass. Tests:
  `tests/test_ezdata/test_builtin_function_attribute.py` (three, all of
  which failed before). Mutation check: builtins made fields again,
  caught. Changelog draft: "A builtin function bound in an `EZData` class
  body, as in `helper = len`, stays a class attribute, as a function
  written in Python does, instead of becoming a field."
- **L09. A `KeeFlags` body accepts flag names that are not upper case
  (archived L7, DECIDED).** `src/worktoy/keenum/_kee_flags_space.py:77-78`.
  Decided: names are upper case in the body, lookups ignore case. Check
  `name.isupper()` next to the `'_'` check.
  **DONE (2026-10-03):** `addKeeFlag` raises `KeeCaseException`, which a
  `KeeNum` raises for the same rule, after the `'_'` check; its docstring
  and message now name flags too. The `NULL` half stays with M13. Tests:
  `tests/test_keenum/test_kee_flag_case.py` (three; two failed before).
  Mutation check: the check removed, caught. Changelog draft: "A
  `KeeFlags` class body refuses a flag name that is not upper case with
  `KeeCaseException`, as a `KeeNum` body refuses a member name; lookups
  still ignore case." The `NULL` half is DONE with M13.
- **L10. `skipTest` inside a sub-test block fails the test (archived
  L18).** `src/worktoy/work_test/_sub_test.py:217-230` records
  `unittest.SkipTest` as an error; let it propagate.
  **DONE (2026-10-03):** `SubTest.__exit__` returns `False` for a
  `SkipTest`, so it leaves the block as itself. Tests:
  `tests/test_work_test/test_sub_test_skip.py` (two, both of which failed
  before). Mutation check: the case removed, caught. Changelog draft:
  "`skipTest` inside a `subTest` block of a `BaseTest` skips the test,
  where it used to fail it."
- **L11. `len` and `in` refuse an EZData class that iterates (archived
  L14).** `EZMeta` defines `__iter__`
  (`src/worktoy/ezdata/_ez_meta.py:162-171`), but
  `AbstractMetaclass.__len__` and `__contains__` consult only
  `__class_iter__`: `len(Pt)` raises "has no len()".
  **DONE (2026-10-03):** `EZMeta` defines `__len__`, the number of
  fields, and `__contains__`, which finds a field by identity, beside its
  `__iter__`; `AbstractMetaclass` is unchanged, and `bool` of an EZData
  class stays `True`. Tests: `tests/test_ezdata/test_class_len_contains.py`
  (two, both of which failed before). Mutation check: a wrong length, any
  item accepted, caught. Changelog draft: "`len` and `in` work on an
  `EZData` class, over its fields, as iterating it does."
- **L12. A finalizer's exception is chained to one the caller is handling
  (archived L25).** `src/worktoy/dispatch/_dispatcher.py:329-337` asks
  `sys.exc_info()`, which also reports the caller's handled exception;
  keep the call's own exception instead.
  **DONE (2026-10-03):** the compiled `dispatch` records the exception of
  the call in an `except BaseException` that re-raises, and the finalizer
  chains from that alone; `sys` is no longer imported. Tests:
  `tests/test_overload/test_finalizer_chain.py` (three; one failed
  before). Mutation check: `sys.exc_info()` back, caught. Changelog
  draft: "An exception a finalizer raises is chained from the exception
  of the dispatched call only; a call made inside an `except` block no
  longer marks it as caused by the exception the caller is handling."
- **L13. `Dispatcher.overload` by hand ignores `ARGS` (archived L12).**
  `src/worktoy/dispatch/_dispatcher.py:638-663` stores `ARGS[int]` as one
  concrete entry, and a call of that length raises a raw `TypeError` from
  `isinstance`.
  **DONE (2026-10-03):** `Dispatcher.overload` sends a signature ending
  in an `ARGS` to `addVariadicSigFunc`; with M17 it is validated first.
  Tests: `tests/test_dispatch/test_dispatcher_variadic_by_hand.py` (two,
  both of which failed before). Mutation check: registered as concrete
  again, caught. Changelog draft: "`Dispatcher.overload` registers a
  signature ending in an `ARGS` as variadic, so it takes calls of any
  length, as `@overload` does."
- **L14. `@overload(OWNER)` builds, then every call fails (archived
  L23).** `src/worktoy/dispatch/_type_sig.py:190-204`; refuse `OWNER` in
  `overload`.
  **DONE (2026-10-03):** `TypeSig.validateTypes` (M17) raises a plain
  `TypeError` for `OWNER`, or an `ARGS` of it, naming the position and
  pointing to `THIS`, so `overload` and `Dispatcher.overload` both refuse
  it. A `TypeException` would have said `OWNER` is no instance of `type`,
  which it is. Tests: `tests/test_overload/test_overload_owner_refused.py`
  (four; three failed before, `THIS` in a class body is the guard).
  Mutation check: `OWNER` let through, caught. Changelog draft: "An
  overload signature holding `OWNER`, which has no role there, raises
  `TypeError` at the declaration; it used to build a class whose every
  call failed."
- **L15. `@overload` over `@staticmethod` or `@classmethod` fails at the
  first call (archived L40).** `src/worktoy/dispatch/_overload.py:244-252`;
  refuse both in the decorator.
  **DONE (2026-10-03):** the new `overload._refuseMethodKinds` raises
  `TypeException('func', ...)` for either kind, called by the decorator
  of `overload`, by `fallback` and by `finalize`; `overload.flex` refused
  them already, through `Permuter`. Tests:
  `tests/test_overload/test_overload_method_kinds.py` (four; three failed
  before). Mutation check: the check removed, caught. Changelog draft:
  "`@overload`, `@overload.fallback` and `@overload.finalize` refuse a
  staticmethod or a classmethod with `TypeException` at the decorator,
  where the class used to build and fail at the first call."
- **L16. Lookups on an enumeration without members raise a plain
  `TypeError` (archived L21).** `src/worktoy/keenum/_kee_meta.py:205-224`
  and `:572`: `Empty('x')` raises where `KeeResolveError` is documented.
  **DONE (2026-10-03):** `_resolveMember` asks for the value type only
  when there are members, and `fromValue` raises `KeeResolveError` for an
  enumeration without any; `valueType` itself still raises `TypeError`.
  Tests: `tests/test_keenum/test_kee_empty_lookup.py` (four; three failed
  before). Mutation check: either guard removed, caught. Changelog draft:
  "A lookup on an enumeration without members, by call, subscript or
  `fromValue`, raises `KeeResolveError` as any other miss does, instead of
  a `TypeError` about its value type."
- **L17. `KeeFlags` takes a bool as an index (archived L32).**
  `src/worktoy/keenum/_kee_flags_meta.py:278-279`: `Perm(True)` is
  `Perm.READ`. **Addition (new):** `KeeBox._resolveNum`
  (`src/worktoy/keenum/_kee_box.py:148`) also reads a bool as an index,
  so on an `int`-valued enumeration `KeeBox` refuses `True` with a raw
  `KeeResolveError` instead of a `KeeBox` error.
  **DONE (2026-10-03):** `KeeFlagsMeta._resolveMember` takes no `bool` as
  an index, and `_resolveValue` compares a `bool` with `bool` values
  alone, so `Perm(True)` and `Perm[False]` raise the `ValueError` of a
  value miss (see L19) and a flags class of `bool` values still finds its
  members. The addition is left as it is: refusing with a raw
  `KeeResolveError` is pinned deliberately by `test_bool_is_refused` in
  `tests/test_keenum/test_kee_box_int_identifier.py`, "as calling the
  enumeration does", and no wrong member comes back; a `KeeBox` error in
  its place is open to the author. Tests:
  `tests/test_keenum/test_kee_flags_bool_index.py` (three; one failed
  before). Mutation check: the index or the value rule reverted, caught.
  Changelog draft: "A `bool` is no index or value of a `KeeFlags` class
  unless the members have `bool` values: `Perm(True)` used to be the
  member of index 1."
- **L18. `KeeFlags` operators between a flags class and a derived one
  raise a raw `KeyError` (archived L50).**
  `src/worktoy/keenum/_kee_flags.py:256-286`: `Perm.READ | More.EXEC`
  raises `KeyError: frozenset({'READ', 'EXEC'})`. Return
  `NotImplemented` unless the types match.
  **DONE (2026-10-03):** `__or__`, `__and__` and `__xor__` return
  `NotImplemented` unless `type(other) is type(self)`, so mixing raises
  the `TypeError` Python raises for unsupported operands, in either
  order. Tests: `tests/test_keenum/test_kee_flags_mixed_operands.py`
  (two; one failed before). Mutation check: `isinstance` back, caught.
  Changelog draft: "The bitwise operators of `KeeFlags` members raise
  `TypeError` for a member of a derived flags class, instead of a raw
  `KeyError`."
- **L19. Which exception a `KeeFlags` lookup miss raises (archived 31
  review, DONE).** A name miss raised `KeyError`, an index miss
  `KeeResolveError`, a value miss `ValueError`, where every `KeeNum` miss
  raises `KeeResolveError`. The probe (2026-10-03) read a permission
  from a config entry with a fallback catching `KeeResolveError` around
  `Perm[entry]`: the fallback caught an index miss and let `'delete'`
  escape as `KeyError` and `3.5` as `ValueError`.
  **Decided (2026-10-03):** `KeeResolveError` for every miss, as for a
  `KeeNum`.
  **DONE (2026-10-03):** `KeeFlagsMeta._resolveName` and `_resolveValue`
  raise `KeeResolveError` naming the class and the identifier, so a miss
  among several identifiers and through a `KeeBox` raises it too, and
  `__contains__` catches that alone. The docstrings of `KeeFlagsMeta`,
  `KeeFlags` and `KeeResolveError` say so. Ten assertions in
  `tests/test_keenum/test_kee_flags.py`, `test_kee_flags_several.py`,
  `test_kee_flags_bool_index.py` and `test_kee_flags_foreign_value.py`
  pinned `KeyError` or `ValueError` and now pin `KeeResolveError`, two of
  them the message. Tests: `tests/test_keenum/test_kee_flags_miss.py`
  (seven; five failed before, the index miss and the membership of a
  member being the guards). The suite gives 2041 passed and 50 skipped on
  3.14 with 100% line and branch coverage, 2029 passed on 3.7, and passes
  on 3.8 to 3.13. Mutation check: `KeyError` back for a name, `ValueError`
  back for a value, `in` not catching the miss, the identifier dropped,
  and the metaclass named in place of the class, all caught. Changelog
  draft: "Every miss on a `KeeFlags` class raises `KeeResolveError`, as a
  miss on a `KeeNum` does: a name of no member used to raise `KeyError`
  and a value of no member `ValueError`, so one `except` clause now covers
  both enumerations and `KeeBox`."
- **L20. `KeeFlagsMeta` pins `_getValue`, which breaks a diamond
  (archived L33).** `src/worktoy/keenum/_kee_flags_meta.py:135-148`
  writes the chosen getter on every flags class, so in
  `class Both(Left, Right)` a base's getter pinned on `Left` beats
  `Right`'s override.
  **DONE (2026-10-03):** the pinning is gone from `KeeFlagsMeta.__new__`;
  the `value` field reads `_getValue` by name off the class of the
  member, so the ordinary method resolution order decides, and the
  existing tests of overrides, `super()` and multiple inheritance pass
  unchanged. Tests: `tests/test_keenum/test_kee_flags_value_diamond.py`
  (three; two failed before). Mutation check: the getter pinned again,
  caught. Changelog draft: "The value of a `KeeFlags` member comes from
  the `_getValue` the method resolution order finds, so in a diamond the
  override of the second base wins over the getter of the common base,
  as for any method."
- **L21. The root of a custom `KeeMeta` never runs its `__init__`
  (archived L19, read).** `src/worktoy/keenum/_kee_meta_meta.py:97-110`
  builds the root through `mcls.__new__` alone, and its namespace
  directly rather than through `mcls.__prepare__`.
  **DONE (2026-10-03):** `_getKeeNum` prepares the namespace through
  `mcls.__prepare__`, builds through `__new__`, caches the root, and then
  calls `__init__`; the cache has to come between, since `_createBase`
  recognises the root as `mcls.keeNum`. The root now has itself as its
  base, so the guard in `KeeMeta.__getattr__` for a base not yet set is
  read through `maybe`. Tests: `tests/test_keenum/test_kee_meta_root_init.py`
  (two; one failed before). Mutation check: `__init__` skipped, the
  namespace built directly, caught. Changelog draft: "The root a custom
  `KeeMeta` builds for its `keeNum` goes through the `__prepare__`,
  `__new__` and `__init__` of that metaclass, as its enumerations do."
- **L22. Deriving from the wrong root gives an unhelpful message
  (archived L8).** `src/worktoy/keenum/_kee_meta.py:139-168`: an
  enumeration of `FontMeta` based on `KeeNum` is told it "must have
  exactly one base, but received none"; say the base must be
  `FontMeta.keeNum` or an enumeration based on it.
  **DONE (2026-10-03):** the message reads "An enumeration of 'FontMeta'
  must be based on 'FontMeta.keeNum', its root, or on an enumeration
  based on it, but 'Font' has the bases: (KeeNum)." Tests:
  `tests/test_keenum/test_kee_wrong_root_message.py` (one, which failed
  before). Mutation check: the old message, caught.
- **L23. `KeeMeta.keeNum` is a `Field` without a getter (archived L42).**
  `src/worktoy/keenum/_kee_meta.py:118`: `WeekDay.keeNum` raises
  `AccessError`. Move it under `TYPE_CHECKING`.
  **DONE (2026-10-03):** the hint sits under `TYPE_CHECKING`, so
  `WeekDay.keeNum` raises a plain `AttributeError`. Tests:
  `tests/test_keenum/test_kee_meta_kee_num_hint.py` (two; one failed
  before). Mutation check: the field back, caught.
- **L24. A `KeyError` bound in a class body cannot be read back there
  (archived L41).** `src/worktoy/mcls/_abstract_namespace.py:248-265`
  uses `KeyError` as its missing marker; use a private marker object.
  **DONE (2026-10-03):** `__getitem__` keeps the miss in a variable of
  its own and raises that, so a bound `KeyError` reads back; the hooks
  still receive the `KeyError` of a miss as the value, as before. Tests:
  `tests/test_mcls/test_space/test_key_error_value.py` (two; one failed
  before). Mutation check: the value tested again, caught. Changelog
  draft: "A worktoy class body may bind a `KeyError` instance and read it
  back."
- **L25. A plain mixin's class hook is hidden in a class without worktoy
  bases (archived L24).** `src/worktoy/mcls/space_hooks/_name_hook.py:200-228`
  seeds `METACALL` that shadows a `__class_str__` on a plain mixin.
  **DONE (2026-10-03):** `preCompilePhase` seeds `METACALL` only where
  neither the namespace nor the `__dict__` of a class along the lookup
  order holds the name, which finds a plain mixin and replaces the 17
  calls of `deepGetItem` per class statement noted in L45. Tests:
  `tests/test_mcls/test_meta/test_mixin_class_hook.py` (three; one failed
  before). Mutation check: plain bases ignored again, caught. Changelog
  draft: "A class hook such as `__class_str__` on a plain mixin reaches a
  class of a worktoy metaclass that has no worktoy bases."
- **L26. `_strictMRO=False` crashes (archived L13).**
  `src/worktoy/mcls/_abstract_namespace.py:222-231` leaves the MRO unset
  and `getMROSpace` (`:166`) iterates it. Drop the keyword or document it
  as namespace-only.
  **DONE (2026-10-03):** kept and documented as namespace-only, since
  `test_lookup_order.py` and `test_abstract_namespace.py` build such
  namespaces and pin `getMRO()` as `None`. `_getLookupOrder`, with its
  fallback to the order of each base, moved from `BaseSpace` up to
  `AbstractNamespace`, and `getMROSpace` and `NamespaceHook` follow it.
  Tests: `tests/test_mcls/test_space/test_deep_get_item.py` (four,
  covering `deepGetItem` too, which lost its only caller with L25).
  Mutation check: `getMROSpace` back on `getMRO`, caught.
- **L27. Calling a worktoy metaclass with a plain dict skips
  `newClassPhase` (archived L29, read).**
  `src/worktoy/mcls/_abstract_metaclass.py:162-175` tests the given dict
  for `getHooks` rather than the namespace it built.
  **DONE (2026-10-03):** `__new__` copies a plain dict into a namespace of
  its own first and then works on that namespace alone, compiling it and
  running its hooks. Tests:
  `tests/test_mcls/test_meta/test_plain_dict_new_class_phase.py` (two;
  one failed before). Mutation check: the hooks skipped, caught.
  Changelog draft: "A worktoy metaclass called directly with a plain
  dict, as in `BaseMeta('Foo', (), {...})`, runs the `newClassPhase` of
  its hooks, as a class statement does."
- **L28. A `ControlFlow` subclass cannot use `super()` in `__str__`
  (archived L34, changed).**
  `src/worktoy/waitaminute/control_flow/_control_space.py:29-35` refuses
  the interpreter's `__classcell__`, and on 3.14 `__classdictcell__` as
  well; add both to the white list.
  **DONE (2026-10-03):** both are on the white list. Tests:
  `tests/test_waitaminute/test_control_flow_super.py` (two; one failed
  before, another method being refused is the guard). Mutation check:
  `__classcell__` off the list, caught. Changelog draft: "The `__str__`
  of a `ControlFlow` subclass may call `super()`."
- **L29. `Object.directory` fails without `__file__` (archived L35).**
  `src/worktoy/utilities/_directory.py:27-33` raises a bare
  `AttributeError` in the REPL or under `exec`.
  **DONE (2026-10-03), with L50:** `Directory.__get__` raises
  `MissingVariable` naming the field, "Missing 'Loose.where: str'!",
  chained from the `AttributeError` of the module. Tests:
  `tests/test_utilities/test_directory_without_file.py` (three, shared
  with L50; one failed before for each item). Mutation check: the bare
  error back, caught. Changelog draft: "`Object.directory` of a class
  defined without a source file, as in the REPL, raises `MissingVariable`
  naming the attribute, where it used to raise a bare `AttributeError`
  about the module."
- **L30. The copy constructors of the lorem generators drop `isFirst`
  and share their parts (archived L46).** `_clause.py:180-186`,
  `_sentence.py:103-109`, `_paragraph.py:109-115`:
  `Clause(Clause.first(40)).isFirst` is `False`, and the copies of
  `Sentence` and `Paragraph` share their clause and sentence objects.
  **DONE (2026-10-03):** the three copy constructors copy `__is_first__`,
  and `Sentence` and `Paragraph` copy each clause or sentence through its
  own copy constructor. Tests:
  `tests/test_lorem_ipsum/test_copy_constructor.py` (three, all of which
  failed before). Mutation check: the flag dropped, the clauses or the
  sentences shared, caught. Changelog draft: "Copying a `Clause`,
  `Sentence` or `Paragraph` through its constructor keeps whether it is
  the first, and gives the copy clauses and sentences of its own."
- **L31. The float samplers refuse an `int` keyword (archived L47).**
  `src/worktoy/work_test/samplers/_base_sampler.py:134-145`:
  `FloatSampler(minVal=0, maxVal=1)` raises `TypeException`.
  **DONE (2026-10-03):** the keyword constructor casts each setting
  through `typeCast` (`_castSetting`), as the setters do, and refuses a
  lossy value with `TypeException` naming the setting; so it also takes a
  numeric string, as the setters already did. Tests:
  `tests/test_work_test/test_sampler_keywords.py` (four, shared with
  L32; one failed before). Mutation check: the `isinstance` check back,
  caught. Changelog draft: "The float samplers take `int` bounds, as in
  `FloatSampler(minVal=0, maxVal=1)`."
- **L32. `BaseSampler` drops unknown keywords (new, read).**
  `src/worktoy/work_test/samplers/_base_sampler.py:117-145` reads only
  the keywords of its key groups, so a misspelled one such as
  `IntSampler(mni=3)` is ignored.
  **DONE (2026-10-03):** `_refuseUnknown` raises Python's `TypeError`,
  "IntSampler() got an unexpected keyword argument 'mni'", for a keyword
  that is no synonym of a setting. Four `test_init` methods passed junk
  keywords (`lmao=True`, `breh=False`) only to reach the branches that
  hand keywords on; they now pass real synonyms (`maximum=`, `minimum=`,
  `stdDeviation=`, `std_dev=`, `numWords=`) with the same assertions.
  Tests: `tests/test_work_test/test_sampler_keywords.py` (one failed
  before). Mutation check: the refusal removed, caught. Changelog draft:
  "The samplers refuse a keyword that names no setting with `TypeError`,
  where a misspelled one used to be dropped without a word."
- **L33. `ComplexTest` runs as a test wherever it is imported (archived
  L38).** `src/worktoy/work_test/_complex_test.py:18-36`: 50 passes of the
  suite run 25 methods against no targets, and its `tearDownClass` pops
  the library module. Skip itself from `setUpClass` when `targets` is
  empty.
  **DONE (2026-10-03):** the skip sits in `setUp`, not `setUpClass`, since
  `TestEZComplex` sets its targets in its own `setUpClass` after calling
  the inherited one; a check there skipped all of it. `tearDownClass`
  hands over to `BaseTest` only when there are targets, so the library
  file stays loaded. The suite now reports 50 skipped where it reported
  50 passes. Tests: `tests/test_work_test/test_complex_test_targets.py`
  (three; one failed before). Mutation check: the skip removed, the
  unload back, caught, the second once the test ran `ComplexTest`
  itself, whose file is the library's. Changelog draft: "`ComplexTest`
  skips its tests when it has no targets, and no longer unloads its own
  library file after running."
- **L34. `ComplexMixin` edge cases (archived L36).**
  `src/worktoy/work_test/_complex_mixin.py`: division by a small number
  raises `ZeroDivisionError`, `__init__` drops components past the
  second, and `ComplexMixin(1, 2)` equals `(1, 2)` and `'1+2j'` but
  hashes apart from them.
  **DONE (2026-10-03):** division refuses an exact zero alone, and the
  reflected division no longer asks `__bool__`, whose epsilon is kept;
  the constructor refuses a third component with `TypeError`; `__eq__`
  takes `ComplexMixin` instances and numbers only, which hash as
  `complex` does, while the arithmetic still takes tuples and text.
  Tests: `tests/test_work_test/test_complex_mixin_edges.py` (five; three
  failed before). Mutation check: the epsilon back, a third component
  dropped again, tuples equal again, caught. Changelog draft:
  "`ComplexMixin` divides by a small nonzero number, refuses a third
  component, and compares equal only to numbers and other
  implementations, which hash alike."
- **L35. Dispatch raises a raw `TypeError` for an argument whose class
  cannot be hashed (archived L51).**
  `src/worktoy/dispatch/_dispatcher.py:239-240`; catch the lookup's
  `TypeError` and go on to the `isinstance` pass.
  **DONE (2026-10-03):** the exact-type lookup catches the `TypeError`
  of hashing and goes on. Tests:
  `tests/test_dispatch/test_dispatch_unhashable_class.py` (two; one
  failed before). Mutation check: the error let through, caught.
  Changelog draft: "An argument whose class cannot be hashed is matched
  through `isinstance` instead of raising `TypeError` from the exact-type
  lookup."
- **L36. `unpack` recurses without end on an iterable that yields itself
  (archived L52).** `src/worktoy/utilities/_unpack.py:62-73`:
  `unpack(ARGS[int])` raises `RecursionError`.
  **DONE (2026-10-03):** the recursive branch moved to `_flatten`, which
  keeps whole an item that is the iterable itself, as an `ARGS` and a
  list holding itself yield. Tests:
  `tests/test_utilities/test_unpack_self_iterable.py` (three; two failed
  before). Mutation check: the item unpacked again, caught. Changelog
  draft: "`unpack` keeps whole an iterable that yields itself, such as
  `ARGS[int]`, instead of recursing until `RecursionError`."
- **L37. `ExceptionInfo` accepts an expected type it can never catch
  (archived L53).** `src/worktoy/utilities/_exception_info.py:107-138`:
  `ExceptionInfo(KeyboardInterrupt)` lets the interrupt propagate.
  **DONE (2026-10-03):** `__init__` refuses with `TypeError` a class or
  instance of a `BaseException` that is not an `Exception`, since those
  always propagate from the block. Tests:
  `tests/test_utilities/test_exception_info_base.py` (three; two failed
  before). Mutation check: accepted again, caught. Changelog draft:
  "`ExceptionInfo` refuses to expect an exception it can never catch,
  such as `KeyboardInterrupt`, with `TypeError`."
- **L38. `NoPickle` copies lose name-mangled slots (archived L44).**
  `src/worktoy/utilities/_no_pickle.py:40-49`.
  **DONE (2026-10-03):** `_slotNames` yields each name as instances
  store it, through the new `_mangled`, which prefixes an underscore and
  the class name without its leading underscores to a private name.
  Tests: `tests/test_utilities/test_no_pickle_mangled_slots.py` (three,
  all of which failed before). Mutation check: names unmangled, the
  underscores of the class kept, caught. Changelog draft: "Copies of an
  object of a worktoy class keep slots declared with a private name,
  such as `__secret`."
- **L39. A `Permuter` without an arrangement fails on an internal
  attribute (archived L48).** `src/worktoy/dispatch/_permuter.py:192-211`;
  raise `MissingVariable` naming `__arg_arrangement__`.
  **DONE (2026-10-03):** `Permuter._getArrangement` raises it, and
  both `invoke` methods use it. Tests:
  `tests/test_dispatch/test_permuter_without_arrangement.py` (three; two
  failed before). Mutation check: the guard removed, caught.
- **L40. `FastBox` resets on delete (archived L16).**
  `src/worktoy/desc/_fast_box.py:163-169`: the next read builds a fresh
  default, where every other box raises `MissingVariable`. Pinned as
  intended by `tests/test_desc/test_fast_box.py`; only the `FastBox`
  docstring leaves it unsaid.
  **DONE (2026-10-03), with D26:** the class docstring says that deleting
  the field removes its value, so the next read builds a fresh default,
  where the other boxes raise `MissingVariable`, and that deleting a
  field holding no value raises `MissingVariable`.
- **L41. `replaceFlex` with `n` below one (archived L17).**
  `src/worktoy/utilities/_replace_flex.py:40-46`:
  `replaceFlex('abc', 'b', 'X', 0)` is `'abXabc'`.
  **DONE (2026-10-03):** `n` below one raises `ValueError`. Tests:
  `tests/test_utilities/test_replace_flex_positive.py` (two; one failed
  before). Mutation check: zero let through, caught. Changelog draft:
  "`replaceFlex` refuses an occurrence number below one with
  `ValueError`."
- **L42. `typeCast(slice, ...)` reads a one-element sequence as a start
  (archived L31).** `src/worktoy/utilities/_type_cast.py:34-39`:
  `typeCast(slice, [5])` is `slice(5, None, None)`, where `slice(*[5])` is
  `slice(None, 5, None)`.
  **DONE (2026-10-03):** the sequence is read as `slice(*arg)`. Tests:
  `tests/test_utilities/test_type_cast_slice_sequence.py` (one, which
  failed before). Mutation check: the start reading back, caught.
  Changelog draft: "`typeCast(slice, [5])` is `slice(None, 5, None)`, as
  `slice(*[5])` is."
- **L43. `getKeyArgs()` on an EZData instance returns the class keywords
  (archived L28).** `src/worktoy/ezdata/_ez_hook.py:415` stores them at
  `__key_args__`, the name `Object` uses for constructor keywords.
  **DONE (2026-10-03):** `postCompilePhase` no longer writes them; they
  stay at `__keyword_arguments__`, where the namespace puts them for
  every worktoy class, and nothing read the copy. `__key_args__` stays
  reserved in an EZData body, now as the name `Object` keeps, and the
  docstrings and the message of `ReservedAttributeError` say "an
  attribute EZData keeps for itself". Tests:
  `tests/test_ezdata/test_instance_key_args.py` (two; one failed before).
  Mutation check: the copy written again, caught. Changelog draft:
  "`getKeyArgs()` on an `EZData` instance gives no keywords, where it
  gave the class keywords; those stay at `__keyword_arguments__` on the
  class."
- **L44. `AttriBox.__instance_set__` honours an undocumented `_root`
  keyword (archived L43, read).** `src/worktoy/desc/_attri_box.py:427`;
  nothing passes it. Remove it.
  **DONE (2026-10-03):** removed. Tests:
  `tests/test_desc/test_attri_box_no_root.py` (one, which failed before).
  Mutation check: the keyword honoured again, caught.
- **L45. Smaller points (archived L30, L37 and L49).**
  - `unpack` iterates a `bytearray`, which elsewhere counts as text
    (`src/worktoy/utilities/_unpack.py:63`; read).
    **DONE (2026-10-03):** `unpack` keeps a `bytearray` whole, as it keeps
    `str` and `bytes`, and the docstrings of `unpack`, `joinWords` and
    `UnpackException` say so. Tests:
    `tests/test_utilities/test_unpack_bytearray.py` (three, which failed
    before). Mutation check: `bytearray` dropped from the text types,
    caught. Changelog draft: "`unpack` keeps a `bytearray` whole, as it
    keeps `str` and `bytes`."
  - The lorem generators accept a negative `charCount`
    (`src/worktoy/lorem_ipsum/_base_generator.py:49`).
    **DONE (2026-10-03):** a `preSet` callback on `BaseGenerator.charCount`
    raises `ValueError` for a count below zero, read as the `int` the box
    casts it to; zero stays allowed, and a value the box cannot cast is
    left for the box to refuse. An assigned tuple, which the box hands to
    `int` as its arguments, is not read this way. Tests:
    `tests/test_lorem_ipsum/test_negative_char_count.py` (six; three
    failed before). Mutation check: the bound loosened, and an uncastable
    value raised from the callback, both caught. Changelog draft: "The
    lorem generators refuse a negative `charCount` with `ValueError`,
    given to the constructor or assigned later."
  - A `Sentence` below `__truncate_below__` renders `_shortText()` while
    its iteration and `repr()` build real clauses
    (`src/worktoy/lorem_ipsum/_sentence.py:146-158`).
    **DECISION (from probing, 2026-10-03):** `str()` and `len()` of a short
    `Sentence` give the placeholder, while `repr()`, iteration and
    `clausesArray` give clauses laid out for the count, which need not
    even match it: `Sentence(10)` renders 'Lorem I...' and iterates one
    clause of 13 characters. Making them agree means choosing what a
    short sentence holds. Proposal: lay the placeholder out as the
    content, as `Clause` does for a short first clause, so a short
    `Sentence` holds one clause of the placeholder words and every view
    agrees.
    **Decided (2026-10-03):** as proposed.
    **DONE (2026-10-03):** `Sentence._buildClauseLengths` gives a short
    sentence the one length `charCount`, and `_buildClausesArray` the one
    clause `_placeholderClause` builds, a `Clause` holding the words of
    `_shortText()` and their lengths, so `__str__` renders every sentence
    from its clauses and its shortcut to `_shortText()` is gone. The
    class docstring says so. Tests:
    `tests/test_lorem_ipsum/test_short_sentence_views.py` (six; four
    failed before, the full sentences and a caption counting its words
    being the guards). The suite gives 2056 passed and 50 skipped on 3.14
    with 100% line and branch coverage, 2044 passed on 3.7, and passes on
    3.8 to 3.13. Mutation check: the real clause built again, the lengths
    from the distribution again, the word lengths off by one, and the
    text of a short first `Clause` in place of the sentence's, all
    caught. Changelog draft: "A `Sentence` of fewer than fifteen
    characters holds its 'Lorem Ipsum...' placeholder as its one clause,
    so `repr()`, iteration and `clausesArray` show the text `str()`
    renders; they used to lay out a real clause of at least thirteen
    characters."
  - `KeeFlagsSpace.getKeeFlags()` merges the body's flags into
    `__base_flags__` in place (`src/worktoy/keenum/_kee_flags_space.py:50-55`;
    read).
    **DONE (2026-10-03):** `getKeeFlags` builds a new mapping, and
    `addKeeFlag` keeps the declared flags in a mapping of their own. The
    inherited mapping had come to hold the declared flags too, and every
    merged mapping was that one object; the class itself received the
    same flags either way. Tests:
    `tests/test_keenum/test_kee_flags_space_merge.py` (four, three of which
    fail on the old code), and the docstring of
    `testParentNotCorruptedByChild` in `test_kee_flags_inheritance.py` no
    longer describes the old merge. Mutation check: the merge into the
    inherited mapping restored, and the declared mapping merged again,
    both caught.
  - Every read of `flags` on a `KeeFlags` class clones all the flags
    again, and so does every `highs`, `lows`, `name`, `names` and hash of
    a member (`src/worktoy/keenum/_kee_flags_space.py:116-132`; read).
    **DONE (2026-10-03):** the `flags` getter of `KeeFlagsMeta` clones the
    flags onto the class on the first read and keeps them in the
    namespace of that class, so a subclass clones its own, and each read
    returns a new list of the same flags. The members reach them through
    `flags`. Tests: `tests/test_keenum/test_kee_flags_cached.py` (four; two
    failed before). Mutation check: the kept flags bypassed, and the kept
    tuple handed out, both caught. Changelog draft: "Reading `flags` on a
    `KeeFlags` class gives the same flag objects each time, and the
    members report those, instead of fresh clones on every read."
  - `SymbolicSampler.wordCount` accepts `0` and negative counts
    (`src/worktoy/work_test/samplers/_symbolic_sampler.py:85-87`; read).
    **DONE (2026-10-03):** the setter raises `ValueError` for a count below
    one, as those of the column and row counts do. Tests:
    `tests/test_work_test/test_symbolic_word_count.py` (three; two failed
    before). Mutation check: zero let through, caught. Changelog draft:
    "`SymbolicSampler` refuses a word count below one with `ValueError`."
  - `indexPermutations(-1)` raises its `ValueError` only at the first
    `next` (`src/worktoy/utilities/combinatorics/_index_permutations.py:41-42`).
    **DONE (2026-10-03):** `indexPermutations` checks the count and then
    returns the iterator of its inner generator, so the call itself
    raises. Tests: `tests/test_utilities/test_index_permutations_eager.py`
    (three; one failed before). Mutation check: the function made a
    generator again, caught. Changelog draft: "`indexPermutations` raises
    its `ValueError` for a negative count as it is called."
  - Calling a box through its class after the class exists, as in
    `Holder.n(99)`, captures a new default
    (`src/worktoy/desc/_attri_box.py:571-589`).
    **DONE (2026-10-03):** `AttriBox.__call__` raises `TypeError` for a box
    placed on a class; a box called again before its class exists still
    keeps the last call. Tests:
    `tests/test_desc/test_attri_box_bound_call.py` (three; two failed
    before). Mutation check: the guard removed, caught. Changelog draft:
    "Calling a box after its class exists, as in `Holder.n(99)`, raises
    `TypeError` instead of replacing the default."
  - `overload` takes an undocumented `strict=True` keyword and ignores
    any other (`src/worktoy/dispatch/_overload.py:246`; read).
    **DONE (2026-10-03):** the docstring documents `strict`, under which
    the cast passes skip the signature, and any other keyword raises
    Python's `TypeError`. Tests:
    `tests/test_overload/test_overload_keywords.py` (two; one failed
    before). Mutation check: other keywords let through, caught.
    Changelog draft: "`overload` raises `TypeError` for a keyword other
    than `strict`, which is now documented."
  - `bipartiteMatching` names the slot by its position in the reduced
    list when no assignment exists
    (`src/worktoy/utilities/_bipartite_matching.py:76`; read).
    **DONE (2026-10-03):** probing showed the slot named is an index of
    the original list, since every inner failure is caught, but it is the
    slot the search tried first, which need not lack a candidate:
    `[(1, 2), (0,), (1, 2), (1, 2)]` blamed slot 1, whose candidate is
    free. Both failures now raise one message naming no slot. Tests:
    `tests/test_utilities/test_bipartite_message.py` (two, which failed
    before). Mutation check: each old message back, caught. Changelog
    draft: "The `ValueError` of `bipartiteMatching` no longer names a
    slot, which was often one whose candidates were free."
  - `AbstractNamespace.deepGetItem` scans the namespace in a loop and
    builds the MRO namespace twice per call, 17 times per class statement
    (`src/worktoy/mcls/_abstract_namespace.py:104-115`; read).
    **DONE (2026-10-03), with L25 and L26:** `deepGetItem` asks the
    namespace with `dict.__contains__` and builds the MRO namespace once
    per call.

### Messages and cosmetics

- **L46. Tracebacks on 3.12 and later suggest a name for three
  exceptions (archived L15).** `DuplicateError`, `ReservedFieldError` and
  `ReservedMethodError` keep a slot named `name`, so the traceback of an
  EZData body defining `__setattr__` ends with "Did you mean:
  '__delattr__'?". Rename the slot.
  **DONE (2026-10-03):** the slot is `fieldName` on `DuplicateError` and
  `ReservedFieldError`, and `methodName` on `ReservedMethodError`, as
  `ClassFieldError` and `ReservedAttributeError` name theirs; the
  docstrings say why the name is not kept at `name`. The five tests that
  read `.name` read the new attributes. Tests:
  `tests/test_ezdata/test_exception_name_slot.py` (three, which failed
  before; the traceback check also passes on 3.13). Mutation check: the
  `name` slot declared and set again on each class, all three caught.
  Changelog draft: "`DuplicateError` and `ReservedFieldError` keep the
  field name at `fieldName`, and `ReservedMethodError` the method name at
  `methodName`, instead of at `name`, which made tracebacks from Python
  3.12 on suggest an unrelated name."
- **L47. A class-level `MissingVariable` names the metaclass (archived
  L4).** `src/worktoy/mcls/_abstract_metaclass.py:313-314`:
  `BaseObject.nope` reads "Missing 'BaseMeta.nope'!".
  **DONE (2026-10-03):** `MissingVariable` names the class itself when
  the instance it is given is a class, and the type of the instance
  otherwise. `AbstractMetaclass.__getattr__` is the only place that gives
  it a class. Tests:
  `tests/test_waitaminute/test_missing_variable_class.py` (two; one failed
  before). Mutation check: the class named never, and always, both
  caught. Changelog draft: "A `MissingVariable` raised for a class names
  the class, as in "Missing 'BaseObject.nope'!", instead of its
  metaclass."
- **L48. Generated EZData methods carry the factory's local name
  (archived L9).** `pt.asDict(1)` reads
  `EZHook.asDictFactory.<locals>.asDict() takes 1 positional argument`;
  name each generated function after the class and the method.
  **DONE (2026-10-03):** `EZHook._qualify` sets the `__qualname__` of
  every method `postCompilePhase` generates to the qualified name of the
  class and the method, so `pt.asDict(1)` reads 'Point.asDict() takes 1
  positional argument' from Python 3.10 on. A method found by hand along
  the bases, and the `_unorderable` every unordered class shares, keep
  their names. Tests: `tests/test_ezdata/test_generated_qualname.py`
  (five; three failed before). Mutation check: the call dropped, the
  shared function renamed, the plain class name used, the optional
  methods left out, and a hand-written method renamed, all caught.
  Changelog draft: "The methods `EZData` generates are named after their
  class, as 'Point.asDict', instead of after the factory that made them."
- **L49. `str()` of a `Dispatcher` lists the variadic expansions
  (archived L39).** `src/worktoy/dispatch/_dispatcher.py:586-598`; apply
  the filter `DispatchException` already uses.
  **DONE (2026-10-03):** `Dispatcher._getDeclaredSigs` returns the
  declared signatures, the expansions left out and the variadic
  declarations added, and both `Dispatcher.__str__` and
  `DispatchException` use it. Tests:
  `tests/test_dispatch/test_dispatcher_str_variadic.py` (two, which
  failed before). Mutation check: the expansions shown, and the variadic
  declarations left out, both caught. Changelog draft: "`str()` of a
  `Dispatcher` lists a variadic declaration as written, instead of the
  signatures expanded from it."
- **L50. The refusals of `Directory` name the field `object` (archived
  L45).** `src/worktoy/utilities/_directory.py`; give it a
  `__set_name__`.
  **DONE (2026-10-03), with L29:** `Directory.__set_name__` records the
  name, so `ReadOnlyError` and `ProtectedError` read 'Located.where'.
  Mutation check: the name not recorded, caught.
- **L51. `KeeNameConflict` always names the member 'Unknown' (archived
  L22).** `src/worktoy/waitaminute/keenum/_kee_name_conflict.py:41`
  reads `__name__`; use `str(self.member)`.
  **DONE (2026-10-03):** the message renders the member, as in "Name
  conflict for Kee member object '<Kee member: RED>'". Tests:
  `tests/test_keenum/test_kee_name_conflict_message.py` (one, which failed
  before). Mutation check: the `__name__` lookup back, caught.
- **L52. `DelException` quotes the bases as part of the metaclass name
  (archived L54).** `src/worktoy/waitaminute/meta/_del_exception.py:47-53`.
  **DONE (2026-10-03):** the quotes hold the metaclass name alone, and the
  bases follow them, as in "from the metaclass 'BaseMeta' with bases:
  (BaseObject)". Tests:
  `tests/test_waitaminute/test_del_exception_bases.py` (two; one failed
  before). Mutation check: the bases back inside the quotes, caught.
- **L53. Line breaks lost or misplaced in messages (archived D24 and
  L37).** `UnpackException` puts `\n` into a message that `textFmt`
  collapses (`src/worktoy/waitaminute/_unpack_exception.py:34-38`);
  `KeeMeta._createBase` joins the bases with `'<tab><br>'`, the tab
  before the break (`src/worktoy/keenum/_kee_meta.py:160`); `textFmt`
  keeps the space next to a `<br>`, so a line of the `DuplicateSignature`
  message starts with a space (`src/worktoy/utilities/_text_fmt.py:68-74`).
  **DONE (2026-10-03):** `UnpackException` writes `<br>` and `<tab>`, so
  each argument stands indented on a line of its own; `_createBase` joins
  the bases with `'<br><tab>'`; and `textFmt` drops the space on either
  side of a `<br>`. `test_lineBreak` in
  `tests/test_utilities/test_text_fmt.py` had pinned the space before a
  break, and expects it gone now. Tests:
  `tests/test_utilities/test_text_fmt_breaks.py` (four),
  `tests/test_waitaminute/test_unpack_exception_lines.py` (one) and
  `tests/test_keenum/test_kee_multiple_bases_message.py` (one), all of
  which failed before. Mutation check: each of the two space removals
  dropped, the newline characters back, and the old join back, all
  caught. Changelog draft: "`textFmt` drops the spaces next to a `<br>`,
  so no line of a message starts or ends with one."
- **L54. Wording in messages (archived L37, read).**
  `ExtraPositionalException` says "has 1 fields"; `KeeMeta.__str__` says
  "1 members", and says `KeeNum` for enumerations of a custom metaclass;
  `PhantomBoxError` says "a 'AttriBox'"; `UnboundClassHook` says "plain
  function" for a staticmethod; `KwargsOnlyException` names `kw_only=True`
  where everything else leads with `kwOnly` (archived D13).
  **DONE (2026-10-03):** `ExtraPositionalException` and
  `KwargsOnlyException` put each count in the singular for one, the
  argument counts included, which were plural as well ("received 1
  positional arguments"); `KwargsOnlyException` names `kwOnly=True`;
  `KeeMeta.__str__` counts "1 member" and names the root of the
  metaclass as the kind, as in "<FontMetaNum 'Font': 2 members>";
  `PhantomBoxError` writes "an 'AttriBox'" and "a 'FastBox'"; and
  `UnboundClassHook` says the function lacks the '@classmethod'
  decorator, which holds for a plain function and a staticmethod alike.
  Tests: `tests/test_waitaminute/test_message_wording.py` (six; five
  failed before) and `tests/test_keenum/test_kee_meta_str.py` (two, which
  failed before). Mutation check: each plural and each name back, the
  article fixed to 'a', and "plain function" back, all caught.
- **L55. `QuickDesc` refuses writes and deletions with a plain
  `AttributeError` (archived L37, read).**
  `src/worktoy/utilities/_quick_desc.py:72-84`, where `Directory` raises
  `ReadOnlyError` and `ProtectedError`.
  **DECISION (from probing, 2026-10-03):** five tests in
  `tests/test_utilities/test_quick_desc.py` pin `AttributeError` for these
  refusals, and neither `ReadOnlyError` nor `ProtectedError` is an
  `AttributeError`, so raising them would break that contract. Proposal:
  base `ReadOnlyError` and `ProtectedError` on `AttributeError` as well, as
  `AccessError` is, and have `QuickDesc` raise them. The docstring of
  `worktoy.waitaminute` asks every exception to subclass the builtin that
  best matches its meaning, and Python refuses a write to a read-only
  attribute, or its deletion, with `AttributeError`; the five tests then
  stand unchanged.
  **Decided (2026-10-03):** as proposed, after a test file showing which
  of nine tests failed under the current code: a `Form` whose `load`
  skips what `setattr` refuses with `AttributeError`, as a property
  would be skipped, crashed with `ReadOnlyError` at its derived field;
  `AccessError` is the rarely used cousin of the two, so having it alone
  be an `AttributeError` was the inconsistency.
  **DONE (2026-10-03):** `ReadOnlyError` and `ProtectedError` subclass
  `AttributeError` beside `DescriptorException`, exactly as `AccessError`
  does, and `QuickDesc` raises the two in place of its bare
  `AttributeError`, as `Directory` does; the docstrings of the two
  exceptions, `DescriptorException`, the `desc` exception package and
  `QuickDesc` say so. The five QuickDesc tests, which pin
  `AttributeError`, stand unchanged. Tests:
  `tests/test_desc/test_read_only_attribute_error.py` (nine; seven
  failed before, the refusals caught by their own names and the QuickDesc
  refusals being `AttributeError`s the guards). The suite gives 2050
  passed and 50 skipped on 3.14 with 100% line and branch coverage, 2038
  passed on 3.7, and passes on 3.8 to 3.13. Mutation check: either base
  reverted, and either QuickDesc refusal made a bare `AttributeError`
  again, all caught. Changelog draft: "`ReadOnlyError` and
  `ProtectedError` are `AttributeError`s, as `AccessError` already was and
  as Python's own refusal of a write to a read-only attribute, or of its
  deletion, is, so code catching `AttributeError` to skip what cannot be
  set skips a worktoy attribute the same way; catching them by name
  works as before. `QuickDesc` raises the two instead of a bare
  `AttributeError` of its own."
- **L56. `repr(Arrangement(('a', 'b'), (1, 0)))` is
  `Arrangement(a, b, 1, 0)` (archived L37, read).**
  `src/worktoy/utilities/combinatorics/_arrangement.py:107-112`.
  **DONE (2026-10-03):** the repr is the call building the arrangement,
  as in "Arrangement(('a', 'b'), (1, 0))". `test_repr_shows_items_and_forward`
  in `tests/test_utilities/test_combinatorics/test_arrangement.py` had
  pinned the flattened form and expects the call now; it failed before.
  Mutation check: the old join back, caught. Changelog draft: "The repr
  of an `Arrangement` is the call building it, keeping the items apart
  from the recipe."

### Style

- **L57. Absolute imports at module level (archived L30, read).**
  `desc/_fix_box.py`, `lorem_ipsum/_clause.py`, `_sentence.py`,
  `_paragraph.py`, `work_test/_complex_mixin.py` and
  `waitaminute/keenum/_kee_resolve_error.py` import from `worktoy.` where
  the rest of the source imports relatively.
  **DONE (2026-10-03):** all six import relatively, `_fix_box.py` taking
  `AttriBox` from its own package with `from . import AttriBox`; no other
  module of the source imports from `worktoy.` at module level. No
  behaviour changed, so there is no test; the suite runs on the new
  imports.
- **L58. Unused state (archived L30 and L37, read).** `Field` writes
  `__prototype_object__` (`src/worktoy/desc/_field.py:226`), and
  `KeeMeta.__init__` writes `__class_name__`
  (`src/worktoy/keenum/_kee_meta.py:456`); nothing reads either. The
  aliases `ExcType`, `ExcVal` and `Trace` in
  `src/worktoy/core/_object.py:23-25` are used nowhere (archived D15).
  **DONE (2026-10-03):** removed, with the `TracebackType` import only
  `Trace` used. No reader existed, so there is no test.
- **L59. Type hints that say something else (archived L37 and L49,
  read).** `KeeFlags.__iter__` is hinted `Iterator[Self]` but yields
  `KeeFlag` objects (`src/worktoy/keenum/_kee_flags.py:235-236`);
  `Dispatcher.finalize` and `fallback` are hinted and documented as
  returning a `Decorator` but return the dispatcher
  (`src/worktoy/dispatch/_dispatcher.py:665-712`).
  **DONE (2026-10-03):** `KeeFlags.__iter__` is hinted
  `Iterator[KeeFlag]`, and `finalize` and `fallback` are hinted and
  documented as returning `Self`. Hints only, so there is no test.
- **L60. `assertIsSubclass` stand-ins ignore `msg` (archived L30,
  read).** `src/worktoy/work_test/_base_test.py:45-51`.
  **DONE (2026-10-03):** both pass `msg` on. Tests:
  `tests/test_work_test/test_base_test_subclass_msg.py` (two, which failed
  before on Python 3.13; Python 3.14 has its own versions, which pass).
  Mutation check, run on 3.13: each `msg` dropped again, both caught.

### Docstrings

- **D01.** `src/worktoy/waitaminute/desc/_descriptor_exception.py`: lists
  three subclasses; `PhantomBoxError` is a fourth (archived D1).
  **DONE (2026-10-03).** Both docstrings name the four.
- **D02.** `src/worktoy/waitaminute/meta/_illegal_instantiation.py`: says
  `ValidSlice` raises it; `ValidSlice` raises plain `TypeError` (archived
  D2).
  **DONE (2026-10-03).** `ValidSlice` is no longer named.
- **D03.** `src/worktoy/mcls/_abstract_metaclass.py:104-106`: says the
  overload protocol expects the default `__class_hash__`; the `TypeSig`
  docstring says nothing depends on it (archived D3).
  **DONE (2026-10-03).** The note says the namespace hashes the same
  tuple as the stand-in for `THIS`, and that nothing depends on the two
  being equal.
- **D04.** `tests/test_keenum/examples/_prime_num.py` and
  `tests/test_keenum/test_http_status.py`: say `cls(2)` resolves by
  index; only `cls[2]` does (archived D4).
  **DONE (2026-10-03).** The docstrings of `_prime_num.py` and of
  `examples/_http_status.py`, the resolver included, speak of subscripts.
  `test_indexRangeNotMistakenForValue` subscripted nothing: a call never
  indexes, so its three calls raised with or without the resolver. It
  subscripts now, which an enumeration without the resolver answers with
  its first members.
- **D05.** Test docstrings naming things that no longer exist:
  `worktoy.markwork` (`test_base_sampler.py`), `worktoy.work_test.mixins`
  (`test_complex_mixin.py`), `Ugedag` (`test_kee.py`), `WORKTOY_DATA_DIR`
  (`test_stochastic_word.py`), `strict=True` (`test_int_sampler.py`), RGB
  as an "EZData class" (`examples/_rgb.py`, `_rgb_num.py`), and the
  "Falsy because of name" comments in `examples/_compass.py` (archived
  D5).
  **DONE (2026-10-03)**, except `WORKTOY_DATA_DIR`, which is code rather
  than a docstring: `test_stochastic_word.py` saves and restores the
  variable around each test, in branches marked `pragma: no cover`, and
  nothing in the source reads it. Removing that is left to the author.
  `strict=True` was in the docstring of `test_int_sampler.py` only, as the
  signatures of `IntSampler`, which takes no such keyword; both
  `Compass` members are truthy, as every member is.
- **D06.** `src/worktoy/keenum/_kee_flags_space.py:28`: says
  `KeeFlagsSpace` subclasses `KeeSpace`; it subclasses `BaseSpace`
  (archived D6).
  **DONE (2026-10-03).**
- **D07.** `src/worktoy/mcls/__init__.py:3` and `:15-17`: "namespace uses"
  for "used", and a sentence broken across a stray line end (archived D7
  and D22).
  **DONE (2026-10-03).**
- **D08.** `src/worktoy/core/_meta_type.py:21-24`: says every worktoy
  metaclass subclasses `MetaType`; `SentinelMeta`, `MetaFlow` and
  `_MetaSlice` subclass `type` (archived D8).
  **DONE (2026-10-03).** The docstring says `AbstractMetaclass`, and every
  metaclass based on it, subclasses `MetaType` and derives from it or
  from a subclass such as `KeeMetaMeta`, and that the other three subclass
  `type`.
- **D09.** `src/worktoy/keenum/_kee_member.py:30-31` and `:91`,
  `src/worktoy/keenum/_kee_flag.py:40-41`: say the name comes from
  `__set_name__`; `KeeSpace.addNum` and `KeeFlagsSpace.addKeeFlag` set it
  (archived D10).
  **DONE (2026-10-03).**
- **D10.** `src/worktoy/keenum/_kee_meta_meta.py:26`: calls `KeeMeta` the
  only metaclass the library ships; `KeeFlagsMeta` ships too (archived
  D11).
  **DONE (2026-10-03).** It says `KeeMeta` alone of the shipped
  metaclasses derives from `KeeMetaMeta`, and that `KeeFlagsMeta` builds
  its root by a class statement.
- **D11.** `src/worktoy/waitaminute/meta/_hook_exception.py:25-28`: shows
  `raise HookException(...) from exception`; the namespace raises without
  `from` (`src/worktoy/mcls/_abstract_namespace.py:261`) (archived D12).
  **DONE (2026-10-03).** The example shows the code as written, the
  original exception kept at `initialException` and as the context.
- **D12.** `src/worktoy/waitaminute/_missing_variable.py:37-57`: the
  example uses `typing.Callable`, which makes its own `print` raise on
  3.7 to 3.9; see L01 (archived D14).
  **DONE (2026-10-03), with L01**, which renders such an alias by its
  `str`.
- **D13.** `src/worktoy/core/_object.py:357-363`: `createContext` returns
  `self` "so the descriptor can be used as a context manager", but
  `Object` has no `__enter__` or `__exit__` (archived D15).
  **DONE (2026-10-03).** It returns `self` so calls can be chained.
- **D14.** `src/worktoy/desc/_base_descriptor.py:100-102`: shows the
  accessors without `**kwargs`, and the deleter without `old` (archived
  D17).
  **DONE (2026-10-03).** The setter is shown returning the value stored,
  as M08 has it.
- **D15.** `src/worktoy/keenum/_kee_flags.py:70`: "Entries must be
  integer valued", while `_getValue` invites any object (archived D18).
  **DONE (2026-10-03).** The sentence is removed; the member attributes
  already say the value defaults to the index.
- **D16.** `src/worktoy/waitaminute/control_flow/_control_class_error.py:21-26`:
  "Any other attribute raises this exception", but `ControlSpace` lets
  through every non-callable name `Exception` already has (archived D19).
  **DONE (2026-10-03).** The docstring names those, and the two cells L28
  added to the white list.
- **D17.** `src/worktoy/waitaminute/_subclass_exception.py:29-40`: the
  example's continuation lines use `>>>` (archived D20).
  **DONE (2026-10-03).** They use `...`. The example still imports
  `TypeAlias`, which `typing` has from Python 3.10.
- **D18.** Stray line breaks inside sentences:
  `src/worktoy/waitaminute/__init__.py:4-6`,
  `lorem_ipsum/_base_generator.py:68-69`,
  `lorem_ipsum/_stochastic_variable.py:114-116`, `:211-214` and
  `:236-239`, `lorem_ipsum/_stochastic_word.py:111-114`,
  `lorem_ipsum/_clause.py:106-108` and `:150-152`, and
  `ezdata/_ez_data.py:38-39` (archived D21).
  **DONE (2026-10-03).** All of these, and the same kind found on the way:
  `_stochastic_variable.py` (the `_settle` docstring), `_ez_data.py` (the
  sentence on reserved attributes), `mcls/_abstract_namespace.py` (the
  class docstring) and `ezdata/_ez_hook.py` (`postCompilePhase` and
  `initFactory`).
- **D19.** `src/worktoy/work_test/_base_test.py:155-158`: says a
  representation longer than 48 characters is truncated; the code
  truncates the whole `<type: value>` line once it reaches 48 (archived
  D23).
  **DONE (2026-10-03).** It describes the line, the limit of 48 and the
  `chars` keyword that replaces it.
- **D20.** `src/worktoy/ezdata/_ez_field.py:28-31`, `:47-50`, `:54-58`,
  `:280-283` and `:312-315`: describe the default as
  `fieldType(*posArgs, **keyArgs)` and `type(v)(v)`; `_construct` copies
  a lone argument already of the field type (archived D25).
  **DONE (2026-10-03).** All five name the copy, or point to `_construct`.
- **D21.** `src/worktoy/waitaminute/ezdata/_class_field_error.py:16-19`
  and `src/worktoy/ezdata/_ez_hook.py:124-126`: give as the reason to
  refuse a class object that its rebuilt default would be its metaclass;
  it would be the class itself (archived D26).
  **DONE (2026-10-03).** Both say a class would become a field of type
  `type` with the class as its default, `ClassFieldError` adding that a
  nested class statement would quietly add a field.
- **D22.** `src/worktoy/mcls/_abstract_metaclass.py:308-312`: forbids the
  dot operator inside `__getattr__`, which itself reads
  `cls.__class_getattr__`, safely, since the metaclass defines it
  (archived D27).
  **DONE (2026-10-03).** It says the dot operator is safe for names the
  metaclass defines, and that any other name needs
  `type.__getattribute__`.
- **D23.** `src/worktoy/utilities/__init__.py:17-39` (comments): the
  import headings misfile `_join_words`, `_directory` and `_quick_desc`
  (archived D28).
  **DONE (2026-10-03).** Each import has a heading naming what it needs,
  `_exception_info` and `combinatorics` included; the order is unchanged.
- **D24.** `src/worktoy/lorem_ipsum/_stochastic_word.py:37-40` (new): says
  drawing a value follows the weighted word collection, but
  `sampleInteger` (`:169-182`) draws a clamped Gaussian of its mean and
  variance.
  **DONE (2026-10-03).**
- **D25.** `src/worktoy/lorem_ipsum/_stochastic_word.py:45-47` (new):
  says `realizeLength` draws with a single `bisect`; it calls
  `random.choices`, which bisects internally.
  **DONE (2026-10-03).**
- **D26.** `src/worktoy/desc/_fast_box.py:21-40` (new, with L40): does
  not say that a deleted field rebuilds its default on the next read.
  **DONE (2026-10-03), with L40.**
- **D27.** `src/worktoy/dispatch/_dispatcher.py:51-54` (new): says a
  variadic signature matches "when the call is longer than its fixed
  prefix"; the code accepts a call exactly as long as the prefix
  (`:258`).
  **DONE (2026-10-03).** "At least as long as its fixed prefix".
