# Better testing plan for worktoy (rc12 handoff)

Date: 2026-06-08
Audience: a future context window (Claude or otherwise) continuing work on worktoy.
This note ships as part of the rc12 commit. It documents two silent bugs fixed
in rc12 (overload override discarded, AttriBox shared default) as the motivating
evidence, then lays out the testing strategy that would have caught them and
should catch the next ones: contract tests and differential testing against
CPython.

## TL;DR

1. Two silent, critical bugs were found and fixed in the session that produced
   rc12. Both passed the full suite at 100 percent branch coverage before the
   fix, because both were bugs of absence (a case never handled) and interaction
   (broke only under subclassing or under more than one instance).
2. rc12 lands both fixes, their regression tests, and this note, and removes the
   scratch reproduction `main_tester_class00.py`. The standing rule still holds
   for any new work: do not commit or push without the maintainer saying so in
   the moment, and releases are manual.
3. The lasting takeaway is a process change, not these two patches: the suite
   needs contract tests (one invariant, run across a whole family of types) so
   this class of bug stops slipping past coverage. See "The recommended process
   fix" below. That is the real open work.

## What rc12 contains

Source fixes:
- `src/worktoy/desc/_attri_box.py`: `AttriBox._resolve`. Bug 2 fix (mutable
  default sharing). Also added `from copy import deepcopy` and updated two
  docstrings.
- `src/worktoy/mcls/space_hooks/_load_space_hook.py`:
  `LoadSpaceHook.postCompilePhase`. Bug 1 fix (plain override discarded).

Tests:
- `tests/test_desc/test_default_uniqueness.py`: NEW. Regression for Bug 2.
- `tests/test_desc/test_attri_box.py`: `test_prebuilt_value_passes_through`
  renamed to `test_prebuilt_value_is_copied_per_instance` and rewritten. The old
  name and its `is seed` assertion encoded the now-removed shared-default
  behavior, so it had to change with the contract.
- `tests/test_mcls/test_space/test_plain_override.py`: NEW. Regression for Bug 1.
  This replaces `main_tester_class00.py` as the durable check.

Removed:
- `main_tester_class00.py`: the maintainer's scratch reproduction for Bug 1, no
  longer needed now that `test_plain_override.py` covers it.

Untouched:
- `CONTRIBUTING.md`: modified at session start, unrelated to this work.

Verification after the fixes: `1177 passed, 10 subtests passed`, 100 percent
branch coverage, including both changed source files at 100 percent.

## Bug 1 (the motivating bug): a plain override of an overloaded method was silently discarded

Symptom: a subclass that reimplements an overloaded method as a plain function
had its override thrown away. With a base class whose `__init__` is overloaded,
a subclass `def __init__(self, *a, **k): ...` was silently replaced by a
`Dispatcher` rebuilt from the inherited overloads, so the subclass code never
ran.

Root cause: `BaseSpace.__init__` (in `src/worktoy/mcls/_base_space.py`) eagerly
copies every base-class overload into the subclass overload map before the class
body runs. Then `LoadSpaceHook.postCompilePhase` unconditionally built one
`Dispatcher` per overloaded name and wrote it into the namespace, clobbering the
plain function the class body had already placed there.

Fix: in `postCompilePhase`, skip names the class body bound plainly and drop
their inherited registrations. The signal needs no new bookkeeping. An
`@overload` declaration is claimed by `setItemPhase` and never reaches the
namespace dict, whereas a plain definition is stored there. So
`dict.__contains__(self.space, name)` is true exactly when the body plainly
overrode the name. Dropping the inherited maps also stops a subclass from
resurrecting the overloads, so the override holds all the way down the MRO.

## Bug 2 (adjacent, found first; not the motivating bug): AttriBox shared one mutable default across all instances

Symptom: `AttriBox[list]([1, 2, 3])` gave every instance the same list object.
Mutating one corrupted all of them. The classic mutable-default footgun, at
class scope.

Root cause: `AttriBox._resolve` returned the lone captured default argument
unchanged when it was already of the field type. The deferred default holds one
object, so every instance got that one object.

Fix: deepcopy per instance, guarded so an un-copyable value is stored unchanged
rather than raising (receiving a value of the exact field type must never
error). Atomic immutables (int, float, str) deepcopy to themselves, so the
common scalar default costs nothing and is unchanged.

Design note: the maintainer chose deepcopy deliberately, overriding the usual
stance that deepcopy is a bandage, because here the shared-state defect is real
and per-instance ownership is the correct model. The irreducible tension: a
value that cannot be copied can only be shared or rejected, and rejecting was
ruled out, so an un-copyable value is shared as a last resort. An earlier
version of this fix copied only builtin containers (shallow, via
`fieldType(args[0])`). It was superseded by the deepcopy version. If you find
references to container-only copying, they are stale.

## Why 100 percent branch coverage missed both

Branch coverage proves every line ran, not that any behavior is correct. Both
bugs were bugs of absence. The buggy `postCompilePhase` had no override branch
to miss, so coverage hit 100 percent precisely because the special case was
missing. You cannot get a coverage gap for logic that was never written.

Both were also interaction bugs. Coverage is per line, correctness is per
scenario. "Subclass plainly overrides an inherited overload" and "two instances
of a class with a mutable default" are points in a combinatorial space that no
single test stood on, even though every line was visited by other tests.

Mutation testing would not have caught either, for the same reason. It mutates
code that exists and asks whether a test notices, which hardens assertions on
present behavior. It does not detect a missing case.

## The recommended process fix: contract tests

A contract test states one invariant and runs it across a whole family of types.
Adding a new family member becomes a one line change that buys all the invariant
coverage, which is how you tame a combinatorial surface without enumerating the
combinations.

The project already has this pattern once. `ComplexTest` in `worktoy.work_test`
runs a dunder suite against every class in its `targets` tuple. Generalize that
instinct to the other families.

Families and their invariants:
- Boxes (AttriBox, FixBox, FastBox, KeeBox): wrong type rejected, per-instance
  default uniqueness (the Bug 2 invariant), value round-trip. Type-specific
  extras stay separate (FixBox write-once, FastBox strict and no coercion,
  AttriBox coercion).
- Members and overrides: an explicit class-body definition is what runs (the
  Bug 1 invariant). Run it over a grid of (how the parent defines a member) by
  (how the child redefines it): plain function, @overload, AttriBox or Field,
  classmethod, staticmethod, property. The existing suite covered the cell
  (parent @overload, child @overload) via `test_base_space`. The bug was the
  adjacent cell (parent @overload, child plain).
- KeeNum and KeeFlags members: resolve by name (case-insensitive), by index, by
  value; member identity; hash and eq consistency.
- Descriptor protocol (Object subclasses): get on class returns the descriptor;
  get on instance returns the value; read-only raises on set, protected on
  delete; the context stack is balanced after every access, including on
  exception.

Sketch in project style (a mixin of invariant methods, plus one thin concrete
TestCase per type that supplies the factory):

```python
class BoxContract:
  boxType = None  # AttriBox, FixBox, FastBox, ...

  def _ownerWith(self, fieldType, *args):
    box = self.boxType
    class Owner(BaseObject):
      field = box[fieldType](*args)
    return Owner

  def test_mutable_default_is_unique_per_instance(self):
    Owner = self._ownerWith(list, [1, 2, 3])
    a, b = Owner(), Owner()
    self.assertIsNot(a.field, b.field)
    a.field.append(99)
    self.assertEqual(b.field, [1, 2, 3])
```

```python
class TestAttriBoxContract(BoxContract, DescTest):
  boxType = AttriBox
```

The hard part is not the plumbing. It is writing the invariants down truthfully.
Each of the four composition questions becomes an invariant: what if a subclass
overrides this, what if it is purely inherited, what if there are two instances,
what if it is combined with another feature. Both bugs in rc12 die on exactly
one of those questions.

When contract tests are not enough: they catch missing cells of grids you draw.
For a failure mode no invariant you wrote covers, use generative methods that
produce inputs you did not enumerate. Property-based testing with hypothesis
(random class hierarchies, overload sets, arg tuples). Differential oracles
against CPython (see the dedicated section below). Fuzzing. Mutation testing
(mutmut or cosmic-ray, run incrementally on the diff in CI plus a periodic full
sweep) is a second-order net that tells you which existing assertions are
load-bearing, not a detector of missing cases.

## Differential testing against CPython (cheap, very high yield)

worktoy reimplements several behaviors that CPython or the standard library
already computes. Every such reimplementation is a free oracle: generate random
inputs, run both the worktoy version and the reference, and assert they agree.
This finds correctness bugs that no hand-picked example would, and it runs in a
fraction of a second for tens of thousands of cases.

This session used it to clear `resolveMRO`, the hand-rolled C3 linearization in
`worktoy.utilities`. The suite only checked one trivial diamond, so it was a
prime silent-bug candidate. The differential test built random consistent class
hierarchies and compared `resolveMRO(*bases)` against the linearization CPython
itself produced (`type.__mro__`). 17090 checks, zero mismatches, well under a
second:

```python
import random
from worktoy.utilities import resolveMRO

def rand_hierarchy(seed):
    random.seed(seed)
    classes, order = {}, []
    for i in range(random.randint(4, 9)):
        name = 'C%d' % i
        cands = order[:]; random.shuffle(cands)
        k = random.randint(0, min(3, len(cands)))
        bases = tuple(classes[c] for c in cands[:k])
        try:
            cls = type(name, bases or (object,), {})
        except TypeError:
            continue  # CPython itself rejects this MRO; skip
        classes[name] = cls; order.append(name)
    return classes, order

mismatches = checked = 0
for seed in range(3000):
    classes, order = rand_hierarchy(seed)
    for name in order:
        cls = classes[name]
        try:
            mine = resolveMRO(*cls.__bases__)
        except Exception:
            continue
        real = list(cls.__mro__)[1:]   # the oracle: CPython's own MRO
        checked += 1
        if mine != real:
            mismatches += 1
            print('MISMATCH', name, [b.__name__ for b in cls.__bases__])
print('checked=%d mismatches=%d' % (checked, mismatches))
```

The same approach cleared `sliceLen` against real Python slicing
(`sliceLen(s, L) == len(list(range(L))[s])`) over 20000 random slices.

Where to point this next, at every place worktoy stands in for the interpreter
or the stdlib:
- `resolveMRO` against `cls.__mro__` (done this session, promote it to a
  permanent randomized test).
- `sliceLen` against `len(list(range(L))[s])` (done this session, promote it).
- isinstance and issubclass on ordinary BaseObject subclasses must still match
  plain Python. A metaclass that breaks normal `isinstance` for non-custom
  classes is a silent disaster. Diff a zoo of normal subclasses against the
  default behavior.
- The dispatcher against a reference resolver. Not CPython, but the same shape:
  write the documented FASTEST then FAST isinstance order as a tiny independent
  function and assert the real dispatcher agrees over random overload sets and
  argument tuples. This session did exactly that and it came back clean.

The principle: if worktoy recomputes something the language already knows, never
trust a single example. Diff the two over randomized inputs and let CPython be
the judge.

## Suggested next steps, in priority order

1. Build `BoxContract` (type enforcement, per-instance default uniqueness,
   round-trip) and wire AttriBox, FixBox, FastBox to it. Locks in the Bug 2
   invariant across the family.
2. Build `OverrideWinsContract` (explicit definition wins) and fill the
   (definition kind) by (override kind) grid for overloaded methods and box and
   Field members. Locks in the Bug 1 invariant.
3. Add hypothesis property tests for the dispatcher (random overload sets and
   arg tuples against a reference resolver) and for namespace and overload
   inheritance (random class hierarchies).
4. Promote the differential probes into permanent randomized tests: resolveMRO
   against `cls.__mro__`, sliceLen against real slicing, isinstance and
   issubclass parity for ordinary subclasses, and the dispatcher against its
   reference resolver. See "Differential testing against CPython" above.

## House rules the next context must respect

- Run tests with the project interpreter:
  `PYTHONDONTWRITEBYTECODE=1 ~/miniforge3/envs/worktoy_env/bin/python -m pytest -q`.
  The suite enforces 100 percent branch coverage through `pytest.ini`, so any new
  branch needs a test that exercises it.
- For ad hoc scripts, use `PYTHONPATH=src`.
- Do not commit or push without the maintainer saying so in the moment. Releases
  are manual.
- One class per file, including tests. Each TestCase gets its own `test_*.py` and
  subclasses the package base (DescTest, MCLSTest, KeeTest, EZTest, and so on),
  not raw BaseTest.
- No em-dash anywhere, in code or prose. The maintainer reacts strongly to this.
  Use a colon, a comma, or two sentences.
- No AI authorship trailers on commits or PRs.
- Python 3.7 is the floor. No walrus, no runtime X | Y unions.
- deepcopy is normally treated as a smell here. The AttriBox use is a
  deliberate, diagnosed exception, not a precedent to copy elsewhere.

## How to reproduce and verify

- Full suite:
  `PYTHONDONTWRITEBYTECODE=1 ~/miniforge3/envs/worktoy_env/bin/python -m pytest -q`.
- Bug 1 regression: `tests/test_mcls/test_space/test_plain_override.py` (this is
  the durable replacement for the removed `main_tester_class00.py`).
- Bug 2 regression: `tests/test_desc/test_default_uniqueness.py`.
- Proof that the Bug 1 contract test catches the bug, without editing source:
  monkeypatch `LoadSpaceHook.postCompilePhase` back to the unconditional
  Dispatcher rebuild (no plain-override skip), then assert that a subclass plain
  override of an overloaded method runs. It goes red.
