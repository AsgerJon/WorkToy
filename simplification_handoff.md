# Simplification hand-off

Written 2026-10-21 for the session that continues this work on its own
branch in a separate directory. The author of the plan is the previous
session; the person you are working with is Asger. Read this file first,
in full, before touching anything.

## 0. What this venture is

Delete leniency machinery from the four central packages (`core`,
`dispatch`, `desc`, `mcls`), one item at a time, tests first. The thesis
Asger accepted:

- Two kinds of edge-case code exist. **Typo guards** (`QuestionableSyntax`,
  `DelException`, `ReservedName`, `OverloadConflict`, `UnboundClassHook`,
  `ShadowedClassHook`, `NamelessCallback`, `DuplicateHook`) turn a silent
  mistake into a loud one, are small, and stay. **Leniency machinery**
  makes a wrong-shaped input work anyway, needs rules to say what "work
  anyway" means, and every rule has an edge. That is where the lines and
  the subtle bugs are, and that is what this venture removes.
- A fix that adds a predicate over the class body is the species that
  caused the bug-fix loop. Prefer deletions and premise corrections.
  Never add a guard without a failing test that needs it.

## 1. State at hand-off

- Asger commits the main checkout before creating the branch. That commit
  holds: the storage-name change (`AttriBox._getStorageName` builds from
  the field name as written, `StorageCollision` and its guard archived
  under `archive/storage_collision/`), its tests, a changelog section,
  `research_notes_20261021_163242.md` (a full line-by-line read of the
  four packages), `review_notes_20261021_172141.md` (the code review the
  plan comes from), and `design_notes_20261021_175705.md` (an intent-only
  read made by another session; not consulted for this plan). It also
  holds the `work_test` change of the same day: the testing support no
  longer imports `lorem_ipsum` (its samplers draw from `LOREM_WORDS`,
  `randomWord` and `loremSentence` in `worktoy.work_test.samplers`, and
  `BaseTest.stochWord` and `BaseTest.loremSentence` are gone), pinned by
  `tests/test_work_test/test_leaf_independence.py`, which reads every
  import statement in the package with `ast`. Asger intends to rewrite
  the test suite on this branch; `work_test` is what that rewrite stands
  on, so keep it free of the leaf packages.
- Suite at hand-off: 2253 passed, 50 skipped, 10 subtests passed.
  Interpreter: `/home/AsgerJon/miniforge3/envs/worktoy_env/bin/python`
  (3.14.5). Run it as

  ```
  cd <branch directory> && PYTHONDONTWRITEBYTECODE=1 <interpreter> -m pytest -q --no-cov -p no:cacheprovider
  ```

  Probes run with `PYTHONPATH=<branch directory>/src` and the same
  environment variable, from a script in the session scratchpad, never
  from inside the repository.
- Confirm the directory you are in is the branch directory, not
  `/home/AsgerJon/PycharmProjects/WorkToy`, before the first edit. Every
  path in a command is absolute and points into the branch directory.

## 2. Working method, every item

1. Write the tests that pin the behaviour *after* the change, in new
   files, one `TestCase` per file, subclassing the local base
   (`DescTest` in `tests/test_desc/_desc_test.py`, the equivalents in the
   other test packages). Run them: they must fail for the right reason.
2. Make the change. Run the new tests (green), then the whole suite.
3. Break the change deliberately, two or three ways, and check the new
   tests fail each time; restore the file and byte-compare it. A mutant
   that survives means a missing test, not a done item.
4. Tests that pinned the removed behaviour move with it: plain `mv` into
   `archive/<item name>/` beside the removed source file, never `git mv`
   or `git rm` (you run no git whatsoever; Asger stages). Tests in shared
   files that assert the removed behaviour lose those assertions only.
5. Add a `###` section under `## [1.0.1] - unreleased` in `changelog.md`
   in the existing prose style. Never touch the `## [...]` header lines
   or any version file.
6. One item per round. Report what was deleted, what the suite says, and
   what the item cost in behaviour. Then stop and let Asger decide the
   next item.

Standing rules that bite here: no sub-agents; no em-dash anywhere; no
`__pycache__` (the environment variable above); docstrings in natural
prose, single quotes for code, never imperative; `path:line` when you
name a symbol, with the code quoted beside the explanation; a decision is
led by an everyday class that hits the problem, run, with its output
shown. Line numbers below are from the hand-off commit; re-locate by
symbol name after any edit above them.

## 3. The items, in order

### Item A. The old-value peek on delete

**What it is.** `Object.__delete__` (`src/worktoy/core/_object.py:318-342`)
reads the field before deleting it, passing `_deleting=True` to
`__instance_get__`, guards a `DELETED` result, and hands the value to
`__instance_delete__(instance, old, **kwargs)`. The only consumer of
`old` in the library is the message of `ProtectedError`
(`src/worktoy/waitaminute/desc/_protected_error.py:39-53`, "with value:
'%s'"). To serve the peek, `Field.__instance_get__` has a `_deleting`
branch and `Field._peekValue` (`src/worktoy/desc/_field.py:185-211`) that
swallows every exception of the getter; `AttriBox.__instance_get__`
(`src/worktoy/desc/_attri_box.py:606-616`) and `KeeBox.__instance_get__`
(`src/worktoy/keenum/_kee_box.py:93-95`) each have a `_deleting` branch.
The peek also provides the "second `del` raises `MissingVariable`"
behaviour through `_deletedGuard`.

**Confirm first.** On 2026-10-21, after this file was written, Asger said
the kwargs-sentinel peeks (`_recursion=True`, used all over the library)
are a mechanism he wants kept: side-effect-free peeking, the same shape
everywhere, so its complexity is paid once. The `_deleting=True` peek is
the same family. Ask whether item A still stands before writing its
tests. If he keeps the peek, item A is withdrawn and the venture starts
at item B; never touch a `_recursion=True` re-entry anywhere.

**Edits.**

- `core/_object.py`: `__delete__` becomes push context, `hookPreDelete`,
  `__instance_delete__(instance, **kwargs)`, `hookOnDelete`, pop.
  `__instance_delete__` (372-385) takes `(self, instance, **kwargs)` and
  raises `ProtectedError(instance, self)`. The class docstring: the
  subclassing contract (47-48), the "Deletion semantics" paragraph
  (116-122) and the example signature (131) drop the old value.
  `_deletedGuard` stays; `__get__` still uses it.
- `waitaminute/desc/_protected_error.py`: drop `oldVal` (slot, parameter,
  attribute docstring) and the "with value" clause.
- `desc/_field.py`: delete the `_deleting` branch and `_peekValue`;
  `__instance_delete__` (228-247) takes `(self, instance, **kwargs)` and
  raises `ProtectedError(instance, self)` with no deleters; class
  docstring 44-50 says deleters run in order, a second `del` runs them
  again.
- `desc/_attri_box.py`: delete the `_deleting` branch and its docstring
  sentences; `__instance_delete__` (667-675) takes `(self, instance,
  **kwargs)`. Decision point below on the second `del`.
- `desc/_fix_box.py:55-61`: `__instance_delete__(self, instance, **kwargs)`
  forwarding to `Object.__instance_delete__`.
- `keenum/_kee_box.py:93-95`: delete the `_deleting` branch and its
  comment. `keenum/_kee_num.py:162` passes a third argument to
  `ProtectedError`; read that method first, then drop the argument.
- Other raisers already use the two-argument form: `utilities/
  _quick_desc.py:82`, `utilities/_directory.py:55`, `desc/_alias.py:121`,
  `dispatch/_dispatcher.py:934`.

**Decision for Asger, before writing the tests.** Without the peek, a
second `del` on an `AttriBox` field stores `DELETED` again in silence.
Option A: keep Python's refusal with six local lines in
`AttriBox.__instance_delete__` (read the storage; if it holds `DELETED`,
raise `MissingVariable(instance, fieldName, object)`). Option B: accept
the silence, as `Field` must (it has no storage to ask). The previous
session leaned A for `AttriBox` and B for `Field`.

**Tests.** Write first, in `tests/test_desc/test_delete_without_peek.py`
(one class): deleting a never-read `AttriBox` field builds no default and
the next read raises `MissingVariable`; the second `del` per the decision
above; `del` on a `FixBox` raises `ProtectedError` whose message names
`Owner.field` and has no `oldVal` attribute and no "with value"; a
`Field` getter is *not* called by `del` (a counter stays at zero), its
deleters run in order, and with no deleter `ProtectedError`; `preDelete`
and `onDelete` callbacks still fire. Archive `tests/test_desc/
test_deletion_reads_storage.py` and `tests/test_desc/
test_field_delete_peeks_getter.py` into `archive/delete_peek/` (seventeen
tests; the behaviours that survive are the ones ported above). Drop the
`e.oldVal` assertions in `tests/test_desc/test_fix_box.py:240-275` (the
`e.oldValue` assertions at 149-217 belong to `WriteOnceError` and stay)
and in `tests/test_keenum/test_num.py:243`. Mutations: drop the local
`DELETED` check (if Option A), drop the `hookPreDelete` call, drop the
`exitContext` in `finally`.

**Cost.** One error message loses the value it showed. Around sixty lines
across five files and one kwargs protocol disappear.

### Item B. `Detached` and the trial pickling

**What it is.** `WorkToyException.__reduce__` (`src/worktoy/waitaminute/
_work_toy_exception.py:83-95`) tries to pickle every captured argument
(`_travels`, 28-37) and replaces one that fails with a `Detached`
stand-in (`src/worktoy/waitaminute/_detached.py`, 69 lines), so an
exception carrying a live descriptor survives a process pool. `Detached.
__getattr__` refuses dunders, so two messages break after a round trip
anyway (`WithoutException`, `ControlClassError`; review item 1.9, probe P1
in the review notes).

**Edits.** In `_work_toy_exception.py`: drop `from . import Detached`
(13) and `_travels`; `__reduce__` returns `_rebuild, (type(self),
self.__init_args__, dict(self.__init_kwargs__))`; the docstring paragraph
at 62-65 says instead that an argument that cannot be pickled makes the
exception unpicklable, as for any Python exception, and a process pool
then reports its own transport error. In `waitaminute/__init__.py`: drop
the import (24), the `__all__` entry (39) and the clause at 13-14. Move
`_detached.py` to `archive/detached/`.

**Tests.** Write first: `tests/test_waitaminute/
test_unpicklable_argument.py`, pinning that an exception built with a
lambda argument raises `pickle.PicklingError` on `pickle.dumps`, and that
an exception with picklable arguments still round-trips with its type
and message (that part exists in `test_work_toy_exception.py` and stays).
In `tests/test_waitaminute/test_work_toy_exception.py` move
`test_detached_argument` (124), `test_detached_answers_attributes` (136)
and `test_detached_travels` (150) with their import into
`archive/detached/`. Mutation: make `__reduce__` drop the kwargs and
check the captured-call test fails.

**Decision for Asger.** An exception holding an unpicklable argument no
longer pickles. If that is not acceptable, the alternative is review
option 1.9 A (capture strings at construction in the two broken
exceptions) and `Detached` stays; the previous session recommends the
deletion.

### Item C. Post-hoc installation and test-only switches

Four small, independent deletions; do them in one round.

- `Dispatcher._adoptOwner` (`src/worktoy/dispatch/_dispatcher.py:896-911`)
  and its call at 891, plus the docstring paragraph at 872-875. A
  dispatcher installed with `setattr` on a finished class then raises
  `MissingVariable` for `__field_name__` from `_createCachedFunction` on
  first use. Archive `tests/test_dispatch/test_dispatcher_lazy_adoption.py`
  (four tests) into `archive/dispatcher_lazy_adoption/`. Write first: the
  `MissingVariable` on first use.
- `AttriBox.__get__` (`src/worktoy/desc/_attri_box.py:679-702`): delete the
  whole override; the same `MissingVariable` comes from `getFieldType`
  a few frames deeper, which is all the override bought. Grep
  `tests/test_desc` for `MissingVariable` with `__field_type__` before
  deleting; tests asserting the type keep passing.
- `_strictMRO` in `src/worktoy/mcls/_abstract_namespace.py`: `__init__`
  (241-265) becomes a plain `self.__class_mro__ = resolveMRO(*bases, )`
  so an inconsistent order raises `TypeError` from the namespace;
  `_getLookupOrder` (170-186) returns `[*self.getMRO()]`; trim the
  docstrings at 171-177, 189-194, 242-248. Tests: `tests/test_mcls/
  test_space/test_lookup_order.py:69`, `test_deep_get_item.py:70` and
  `test_abstract_namespace.py:127-130` build namespaces with
  `_strictMRO=False`; rewrite them to expect the `TypeError`, or archive
  the fallback-specific ones. `tests/test_core/
  test_init_subclass_forwarding.py:71-76`, `tests/test_mcls/test_meta/
  test_class_keywords.py:45` and `tests/test_ezdata/
  test_class_keyword_spellings.py:69` pass `_strictMRO=True` as a class
  keyword "the namespace reads"; they stay green (the keyword is absorbed
  by `_Chill` and recorded in `__keyword_arguments__`) but their
  docstrings become stale; reword them.
- `_initialIterationCount` in `src/worktoy/utilities/_resolve_mro.py`:
  drop the `**kwargs`, the counter (64-65, 87-89), the `RecursionError`
  and the two docstring passages (27-31, 44-47). The C3 loop makes
  progress or raises `TypeError` on every pass, so the counter can never
  fire outside the test that forces it. Remove the test at
  `tests/test_utilities/test_resolve_mro.py:77`.

### Item D. `_RootAlias` and `PhantomBoxError`

**What it is.** `AttriBox[list[int]]` or `AttriBox[T]` written in a class
body without the trailing call stores a `typing` alias with no
descriptor behaviour. `_RootAlias` (`src/worktoy/desc/_root_alias.py`, 109
lines) re-clothes the alias so `__set_name__` refuses the binding with
`PhantomBoxError` (`src/worktoy/waitaminute/desc/_phantom_box_error.py`,
108 lines). The alias is needed only for `class Sub(AttriBox[T])`.

**Edits.** `AttriBox.__class_getitem__` (`desc/_attri_box.py:754-796`) and
`FastBox.__class_getitem__` (`desc/_fast_box.py:85-126`): a plain class
gives a box as now; a `TypeVar` returns `super().__class_getitem__
(fieldType)` unchanged (a plain alias, for subclassing); anything else
raises `TypeException('fieldType', fieldType, type, TypeVar)` at the
subscript. Drop the `_RootAlias` imports (`_attri_box.py:13`,
`_fast_box.py:11`), the docstring mention at `_attri_box.py:846`, the
import and Private group in `desc/__init__.py` (27-29, 36), and
`PhantomBoxError` from `waitaminute/desc/__init__.py` (4, 23, 34). Move
`_root_alias.py`, `_phantom_box_error.py` and `tests/test_waitaminute/
test_phantom_box_error.py` to `archive/phantom_box/`.

**Tests.** Write first: `AttriBox[list[int]]`, `AttriBox[Optional[int]]`
and the `FastBox` forms raise `TypeException` at the subscript;
`class Sub(AttriBox[T])` still builds (`tests/test_desc/
test_fast_box_generic.py` covers the `FastBox` side already). Rewrite
`tests/test_desc/test_attri_box_builtin_generic.py` and
`test_fast_box_builtin_generic.py` to the new refusal; in `tests/test_desc/
test_attri_box.py` drop the imports at 14 and 18 and the alias tests
around 333-360; in `tests/test_waitaminute/test_message_wording.py` drop
the import at 18 and the two assertions at 70-71.

**Decision for Asger.** `x = AttriBox[T]` with a `TypeVar` and no call,
bound in a body, is no longer refused; it reads back as the alias
object. `x = AttriBox[list[int]]`, the likelier mistake, is refused
earlier and plainer than before. Two unreleased changelog sections
("AttriBox declarations are settled when the class is created", first
paragraph, and "New exception: PhantomBoxError") describe the removed
behaviour; Asger rewrites or removes them, since 1.0.1 is unreleased.

### Items E and F. The two features. Decide after A to D.

**E. Set-time coercion in `AttriBox`.** Be precise about what is leniency:
`resolveText`, `resolveNumber` and the container rules of
`_callFieldType` refuse lossy constructors (`int(2.5)`, `str(None)`,
`list('abc')`) and serve the deferred default too, so they are
*strictness* and stay. The leniency is in `__instance_set__`
(`src/worktoy/desc/_attri_box.py:627-665`): the `typeCast` attempt with
`allowInstantiation=False`, the `_resolve(*self._assignedArgs(value))`
construction on assignment, `_assignedArgs` (528-538) and the tuple-splat
contract (class docstring 62-98, `_resolve` docstring 236-318). The
`_recursion=True` re-entry is a pattern Asger keeps everywhere (see the
note under item A); it only disappears where no re-entry is left. The
replacement is `FastBox.__set__`'s rule: an
instance of the field type is stored, anything else is
`TypeException(fieldName, value, fieldType)`. Around 120 to 150 lines.
Lost: `obj.n = '42'` into an `int` field, `obj.bar = 69, 420` into a
`complex` field, `obj.name = b'x'` into a `str` field. `EZData` fields
are boxes, so `ezdata` loses the same (`tests/test_ezdata/
test_field_default_text.py`, `test_field_number_default.py` and friends
will say exactly what). Tests to read first: `tests/test_desc/
test_attri_box.py`, `test_attri_box_text.py`, `test_attri_box_resolve_text.py`,
`test_attri_box_builtin_subclass.py`, `test_attri_box_number_default.py`.

**F. The cast tier of `Dispatcher`.** Regions in `src/worktoy/dispatch/
_dispatcher.py`: `castArg` (426-436), the SLOW and SLOW-variadic passes
(568-620), `castFuncs`/`castVariadics` setup (414-417), `_getCastOrder`
(277-307), the farthest-first use of `_getVariadicOrder`, the keyword
cast tier (497-510), the `strict` keyword and `__allow_flex__` plumbing
(1054, 1077-1080, 1176, 963-971), the `typeCast` import (15) and the tier
docstring (51-93). Also `TypeSig.__allow_flex__` and `namesTHIS`
(`_type_sig.py:33-43, 86, 103-113, 272-283`), `strict` and
`_refuseKeywords` in `_overload.py` (226-233, 247-260, 385-394). Around
150 lines plus docstrings; `typeCast` itself stays for the boxes. Lost:
`@overload(int)` matching `'42'` and, more importantly, `@overload(float)`
matching an `int` argument, since `isinstance(1, float)` is False and
only the cast tier admits it today. That second loss is the strongest
reason to keep F, or to keep a cast tier reduced to the numeric tower,
which would be a new rule and therefore needs Asger's explicit yes.
Tests to read first: `tests/test_overload/test_strict_load.py`,
`test_this_strict_default.py`, `test_this_cast_no_reentry.py`,
`test_load_args.py`, `test_overload_keywords.py`, `tests/test_dispatch/
test_dispatcher_clone_sigs.py`, `test_type_sig_declared_types.py`.

## 4. Not in this venture, so it is not lost

- Review item 1.13 (Major): box tags share names with `Object`'s
  placement record, so `hasattr(leaf, 'instance')` and
  `inspect.getmembers(leaf)` raise `WithoutException` on a box-created
  `BaseObject`. Fix: a placement flag set in `Object.__set_name__`
  (`core/_object.py:271-277`) and tested by `getContextInstance` and
  `getContextOwner` (221-247) in place of `__field_name__ is None`. Three
  lines plus a class variable. Not a simplification, so it waits for
  Asger's word, but it should land before 1.0.1 ships.
- Review Minors that are one-liners: 1.5 (`__slots__ = ()` on `_Chill`),
  2.4 (refuse sentinel classes other than `THIS` in
  `TypeSig.validateTypes`), 2.5 (the two refusals missing from
  `Dispatcher.overload`), 3.2 (`FastBox` on a `__slots__` owner), 4.4
  (`@overload` on a routed `__class_*__` hook). See
  `review_notes_20261021_172141.md`.
- The `Alias` object-swap wrinkle: on a fresh subclass instance, reading
  the alias before the redeclared field builds the parent's default.
  Pinned nowhere; an `Alias` design question for later.

## 5. Where to look

- `research_notes_20261021_163242.md`: entry 1.5 (`Object`), 3.5
  (`Field`), 3.6 (`AttriBox`), 3.7 (`FixBox`), S2 (`WorkToyException`), S4
  (`Detached`), 2.6 (`Dispatcher`), 2.5 (`TypeSig`), 4.8
  (`AbstractNamespace`), S22 (`resolveMRO`).
- `review_notes_20261021_172141.md`: 1.9, 1.10, 1.13, 2.13, 3.1, 3.11,
  3.13, 6.
- `archive/storage_collision/`: the shape of an archived item (source
  file and its test file side by side, no README).

Finished 2026-10-21.
