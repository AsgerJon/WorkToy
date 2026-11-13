# Planned work on worktoy

Brought up to date: 2026-11-13.

Every piece of planned work is an item here, from the first idea until
it is released or rejected, and so is every release. The items are
written by
`item_template.md`, beside this file, which says what the words of
`Status`, `Level` and `Scale` mean. In short, a status is one of
`CONCEPTION`, `UNDECIDED`, `REJECTED`, `PENDING`, `READY`, `UNDERWAY`,
`DEV`, `RC` and `LTS`, in that order.

To list every item with its status:

```text
grep -n -e "^### " -e "^- Status:" planned_items.md
```

## Contents

1. [The release of 1.2.1](#the-release-of-121)
2. [The speed of the core](#the-speed-of-the-core)
3. [Warnings, deprecations and the next major
   version](#warnings-deprecations-and-the-next-major-version)
4. [keenum](#keenum)
5. [ezdata](#ezdata)
6. [work_test](#work_test)
7. [The release tooling](#the-release-tooling)
8. [The promises and the manual](#the-promises-and-the-manual)
9. [Testing and mutation testing](#testing-and-mutation-testing)
10. [Thread and task safety](#thread-and-task-safety)
11. [Reviews of the source](#reviews-of-the-source)

## The release of 1.2.1

The first item is the release itself. The seven after it are what it
carries, one for each heading of its section in `changelog.md`.

---

### Release 1.2.1

The micro release that repairs what 1.2.0 broke: a test base built on
`BaseTest` by a metaclass of its own could no longer be created, and a
test class could no longer write a `doCleanups` or a `debug` of its
own. By the author's decision it carries everything else in the tree
as well. Three dev builds are out. The last, `1.2.1.dev2`, is the tree
byte for byte and passes on every Python from 3.7 to 3.15.

- Status: DEV
- Level: micro
- Scale: medium
- Release: 1.2.1
- Next: the two edits by hand, then the press of `micro-rc` and of
  `micro-lts`, by the author
- History:
  - 2026-11-12 CONCEPTION. The report on what 1.2.0 broke.
  - 2026-11-12 UNDERWAY. The repair built; the author decided that the
    release carries everything in the tree.
  - 2026-11-12 DEV. Builds `1.2.1.dev0` and `1.2.1.dev1`.
  - 2026-11-13 DEV. Build `1.2.1.dev2`, checked against the tree.

---

### Let a test base bring a metaclass of its own again

1.2.0 made `TestMeta` the metaclass of `BaseTest` and refused the names
`doCleanups` and `debug` in every test class. A test base built by a
metaclass of its own could no longer be created, and a test class could
no longer write either method. `BaseTest` is built by `BaseMeta` again
and reports the failed `subTest` blocks from `__class_init__`.

- Status: DEV
- Level: micro
- Scale: medium
- Release: 1.2.1
- Next: it moves with the release of 1.2.1
- History:
  - 2026-11-12 CONCEPTION. The report on what 1.2.0 broke.
  - 2026-11-12 UNDERWAY. Built the same day, on the author's decision.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.

---

### Remove `BaseTest.tearDownClass`

`BaseTest.tearDownClass` took the file of the test class out of
`sys.modules` and ran the garbage collector, which kept
`tearDownModule` from running under `unittest`. The method is removed,
and is not to come back.

- Status: DEV
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: it moves with the release of 1.2.1
- History:
  - 2026-11-12 CONCEPTION. Found while the package was read.
  - 2026-11-12 UNDERWAY. Removed on the author's word.
  - 2026-11-12 DEV. In build `1.2.1.dev1`.

---

### Refuse a name bound as a field and as something else

One body binding a name as a field and as a method, a descriptor or an
overload is refused, and so is a method or a descriptor at the name of
an inherited field.

- Status: DEV
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: it moves with the release of 1.2.1
- History:
  - 2026-11-12 CONCEPTION. Found reading `ezdata` against the core.
  - 2026-11-12 UNDERWAY. Built, and kept on the author's ruling.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.

---

### Take back equality across different field orders

Two classes whose fields come in different orders were equal by
position, which contradicted equality by name. They are no longer
equal, and the promise is confessed in `promises/confessions`.

- Status: DEV
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: it moves with the release of 1.2.1
- History:
  - 2026-11-12 UNDECIDED. Every repair made one promise false.
  - 2026-11-12 UNDERWAY. The author decided to take the promise back.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.

---

### Let a subclass of `EZField` take options of its own

The parentheses of `EZField[T](...)` reach the `__init__` of a
subclass, as those of a box do, and a field called again after its
class exists is refused.

- Status: DEV
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: it moves with the release of 1.2.1
- History:
  - 2026-11-12 UNDECIDED. Nothing promised a subclass of `EZField`.
  - 2026-11-12 UNDERWAY. The author decided for it.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.

---

### Optimize creation, assignment and comparison of `EZData` instances

An instance is made in 1377 ns where 1.2.0 takes 2162 ns, and an
assignment takes 191 ns where it took 250 ns. The `__post_init__` a
class does not have is answered from the metaclass.

- Status: DEV
- Level: micro
- Scale: medium
- Release: 1.2.1
- Next: it moves with the release of 1.2.1
- History:
  - 2026-11-12 CONCEPTION. Measured during the read of `ezdata`.
  - 2026-11-12 UNDERWAY. The part that changes no answer first, then
    the `__post_init__` lookup on the author's decision.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.

---

### Make the smaller corrections of 1.2.1

`replace` no longer goes through `asDict`. A subclass of `EZHook`
declared in a subclass of `EZSpace` acts in place of the inherited
hook. A default that cannot be built says so with a `TypeError`. The
docstrings of `ezdata` and `work_test` say what the code does.

- Status: DEV
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: it moves with the release of 1.2.1
- History:
  - 2026-11-12 CONCEPTION. Found reading `ezdata` and `work_test`.
  - 2026-11-12 UNDERWAY. Each held against the promises first.
  - 2026-11-12 DEV. In builds `1.2.1.dev0` and `1.2.1.dev1`.

---

### Make the hand edits before 1.2.1 is released

The header of the changelog section carried the date it was written.
Two promise docstrings said "the update after 1.2.0" where the version
belongs. Reading the whole source against the changelog entry found
two more: a sentence of the entry naming the wrong exception for an
overload at the name of a field of the same body, and the docstring of
the package naming Python 3.14 as the newest it targets.

- Status: UNDERWAY
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: the author commits the five edits; they move with the release
- History:
  - 2026-11-12 PENDING. Known since the changelog section was written.
  - 2026-11-13 READY. The author gave the word: "all five".
  - 2026-11-13 UNDERWAY. All five made and staged, in no build yet.

---

### Run worQt against a build of 1.2.1

worQt builds on worktoy, and its test base is what 1.2.0 broke. It has
not been run against a build of 1.2.1.

- Status: READY
- Level: none
- Scale: small
- Release: 1.2.1
- Next: the author runs it
- History:
  - 2026-11-12 READY. Possible since build `1.2.1.dev0`.

## The speed of the core

Measured on 2026-11-12 with Python 3.15:

| operation               | plain Python | worktoy |
| ----------------------- | -----------: | ------: |
| stored box read         |        15 ns |  243 ns |
| computed attribute read |        25 ns | 3135 ns |
| class attribute read    |        13 ns |   78 ns |
| hash of a class         |        33 ns |  371 ns |
| overloaded call         |        30 ns |  937 ns |
| instance made           |        65 ns | 1244 ns |

---

### Skip empty hook phases in the full read

Every read but that of a stored box with no read callback runs both
read hook phases through the recursion guard, about 700 ns each, even
when nothing is registered. A computed attribute always pays it. The
plan is to skip a phase that has nothing to run, as the read of a box
does since 1.2.0.

- Status: READY
- Level: micro
- Scale: medium
- Release: none
- Next: the author's word to start
- History:
  - 2026-11-09 READY. One of two changes planned for the 1.2 line; the
    other, the read of a stored box, went out in 1.2.0.

---

### Optimize attribute access on worktoy classes

13 ns in plain Python against 78 ns. The cost was put on the fallback
of the metaclass for a missing attribute.

- Status: CONCEPTION
- Level: micro
- Scale: unsized
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-09 CONCEPTION. Measured for the plan of the 1.2 line.

---

### Optimize hashing of worktoy classes

33 ns against 371 ns. The hash is computed in Python, and an overloaded
method pays it at every call that is given a worktoy class.

- Status: CONCEPTION
- Level: micro
- Scale: unsized
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-09 CONCEPTION. Measured for the plan of the 1.2 line.

---

### Optimize Dispatcher calls on overloads

30 ns for a plain method against 937 ns.

- Status: CONCEPTION
- Level: micro
- Scale: unsized
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-09 CONCEPTION. Measured for the plan of the 1.2 line.

---

### Optimize instance creation

65 ns against 1244 ns. `BaseObject()` took 392 ns on 2026-11-09, and
why it tripled has not been looked into.

- Status: CONCEPTION
- Level: micro
- Scale: unsized
- Release: none
- Next: someone finds where the time goes
- History:
  - 2026-11-09 CONCEPTION. Measured for the plan of the 1.2 line.
  - 2026-11-12 CONCEPTION. Measured again, three times slower.

## Warnings, deprecations and the next major version

A promise of the library taken back at once is a confession. One kept
through the 1.x releases and taken back at the next major version is a
deprecation, announced by the warning `DeprecatedPromise`.

---

### Release 2.0.0, the next major version

Nobody has planned it. The deprecation notices name it: what is
deprecated in 1.x goes "beginning with the next major update". By the
counting of the release tooling it is 2.0.0. Two items below wait for
it.

- Status: CONCEPTION
- Level: major
- Scale: unsized
- Release: 2.0.0
- Next: someone writes what it would carry
- History:
  - 2026-11-11 CONCEPTION. Named by the deprecations of 1.2.0.

---

### Remove the four deprecated names

A member's `index` in all its spellings, `KeeBox`, `KeeFlag` and the
import path `worktoy.waitaminute.control_flow` work through 1.x and
give the notice. At the next major version they go.

- Status: PENDING
- Level: major
- Scale: medium
- Release: 2.0.0
- Next: the next major version, which is at its conception
- History:
  - 2026-11-11 PENDING. Decided with the deprecations, in 1.2.0.

---

### Confirm the other spellings of `index` as deprecated

`int(member)`, a member as a list index and `Kee.index` were deprecated
along with `index`, and were never confirmed one by one.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none
- Next: the author says yes or no to each of the three
- History:
  - 2026-11-11 UNDECIDED. Built as deprecated, in 1.2.0.

---

### Settle the names `RiskWarning` and `AlternativeWarning`

The two general warnings of the family carry names chosen while the
family was built.

- Status: UNDECIDED
- Level: unset
- Scale: small
- Release: none
- Next: the author keeps the names or gives others
- History:
  - 2026-11-11 UNDECIDED. Built with these names, in 1.2.0.

---

### Refuse a test class's own `doCleanups` or `debug` in 2.0

A proposal of the report on what 1.2.0 broke: refuse it at the line of
the class body in the next major version, and warn at most in 1.x.

- Status: UNDECIDED
- Level: major
- Scale: small
- Release: 2.0.0
- Next: the author says whether it is wanted
- History:
  - 2026-11-12 UNDECIDED. Proposed in the report.

---

### Warn about a lambda call in a decoration, and about `exec`

One for a lambda with a call in a decoration, one for `exec` or `eval`.
Finding them means parsing every file a class comes from: 152 ms at
every start, where importing worktoy takes 199 ms.

- Status: PENDING
- Level: minor
- Scale: medium
- Release: none
- Next: a way to find them that costs nothing at start
- History:
  - 2026-11-10 PENDING. Proposed by the author and put aside the same
    day for the cost, as he had asked.

## keenum

---

### Settle the default value of a combination of valued flags

A flags member defaults to its name. What a combination defaults to
when its flags declare values of their own, as `Kee[int](4)`, is not
settled.

- Status: UNDECIDED
- Level: unset
- Scale: small
- Release: none
- Next: the author says what the value is
- History:
  - 2026-11-11 UNDECIDED. The one open line of the plan of the rebuild.

---

### Confirm four choices of the keenum rebuild

Made while building, and never confirmed: a diamond of bases is one
member, and two objects under one name are refused; the name `owners`;
`KeeFlag` deprecated; `Kee[str]()` holds its name.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none; all four are in 1.2.0
- Next: the author says yes or no to each
- History:
  - 2026-11-11 UNDECIDED. Built as picked.

---

### Look over five consequences of the keenum rebuild

A `_getValue` of a subclass values only the members that subclass
builds. `NULL` is valued the text `NULL` in every class. `valueType` is
the type of the value of the first flag. A member of a subclass handed
to the call of the class is answered as it is. `&` of two unrelated
flags classes gives `NULL`, while `|` and `^` raise.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none; all five are in 1.2.0
- Next: the author says which, if any, is wrong
- History:
  - 2026-11-11 UNDECIDED. Found while building, and listed for him.

---

### Run each test file in an interpreter of its own

Built against test classes that stay alive from one test file to the
next, and retired the same day, since the run of all tests in one
process is green.

- Status: REJECTED
- Level: none
- Scale: small
- Release: none
- Next: nothing
- History:
  - 2026-11-11 UNDERWAY. Built for the rebuild.
  - 2026-11-11 REJECTED. Retired on the author's word.

## ezdata

---

### Settle the receiver name `__ez_self__` of generated methods

The generated `__init__` and `replace` name their receiver
`__ez_self__`, so that a field may be named `self`.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none; the name is in 1.2.0
- Next: the author keeps the name or gives another
- History:
  - 2026-11-12 UNDECIDED. Chosen while the repair was built.

---

### Settle how a namespace class records its acting hook

A subclass of `EZHook` declared in a subclass of `EZSpace` acts in
place of the inherited hook, and the namespace class records which
hook acts. The shape of that record was chosen while building.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none; the record is in the builds of 1.2.1
- Next: the author keeps the shape or gives another
- History:
  - 2026-11-12 UNDECIDED. Chosen while building.

---

### Choose "attribute" or "field" for the prose of `ezdata`

Three lines say "attribute" on the author's word, to avoid confusion
with the class `Field`. The rest of the package says "field", as its
names do.

- Status: UNDECIDED
- Level: micro
- Scale: medium
- Release: none
- Next: the author says whether the rest follows
- History:
  - 2026-11-12 UNDECIDED. Three lines changed, the rest left.

---

### Unify the two rules for a default not of the field type

`AttriBox[int]('3')` gives 3, since a box builds its default through
the constructor. `EZField[int]('7')` is refused, since a field casts.

- Status: UNDECIDED
- Level: major
- Scale: small
- Release: none
- Next: the author says whether the two stay apart
- History:
  - 2026-11-10 UNDECIDED. A question of a newcomer reading the
    promises.

---

### Unify how the options of an `EZData` class inherit

`order` is inherited, `kwOnly` is not, and `frozen` must be declared
again by a subclass.

- Status: UNDECIDED
- Level: unset
- Scale: unsized
- Release: none
- Next: the author says whether the three stay as they are
- History:
  - 2026-11-10 UNDECIDED. A question of a newcomer reading the
    promises.

---

### Kill the tolerated mutants on public names of `ezdata`

17 mutants that remove a `@staticmethod` or a `@classmethod` survive
the mutation sweep, since the library never calls the method the other
way round. One assertion each would kill them.

- Status: PENDING
- Level: none
- Scale: small
- Release: none
- Next: the author's word; they are tolerated for now
- History:
  - 2026-11-12 PENDING. Offered, and put off by the author.

## work_test

---

### Inspect `work_test` thoroughly, by the author

Announced when the package was reworked to working order.

- Status: PENDING
- Level: none
- Scale: unsized
- Release: none
- Next: the author
- History:
  - 2026-11-05 PENDING. Announced by the author.

---

### Decide whether `TestMeta` and `TestSpace` are deprecated

Since the repair of 1.2.1 `BaseTest` is not built by them. They stay
exported for a test base that chooses them.

- Status: UNDECIDED
- Level: minor
- Scale: small
- Release: none
- Next: the author says whether they are deprecated
- History:
  - 2026-11-12 UNDECIDED. Left open by the repair.

---

### Promise the three usages that 1.2.0 broke

A test base with a metaclass of its own, and a test class writing its
own `doCleanups` or its own `debug`, are tested and promised nowhere.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none
- Next: the author says whether they are promised
- History:
  - 2026-11-12 UNDECIDED. Left open by the repair.

---

### Report failed blocks when a base's `__class_init__` hands nothing on

Such a base loses the report of failed blocks for its classes. It is
the one case of eleven that the repair of 1.2.1 does not catch.

- Status: CONCEPTION
- Level: micro
- Scale: unsized
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-12 CONCEPTION. Known and left when the other ten were
    closed.

---

### Report failed blocks as an `async def` test method ends

Its failed blocks are reported among the cleanups of the test, not as
the method ends.

- Status: CONCEPTION
- Level: micro
- Scale: unsized
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-12 CONCEPTION. Known and left.

## The release tooling

---

### Publish micro updates on an older release line

The tooling publishes one line of releases: once 1.2.0 is released, no
button can publish a 1.1.1. An older line that a new Python breaks
could not be repaired.

- Status: PENDING
- Level: none
- Scale: large
- Release: none
- Next: an older line that needs a repair; not for a long time
- History:
  - 2026-11-12 PENDING. Recorded as a known limitation, on the author's
    word.

---

### Have the tooling make the hand edits of a release

The date in the header of the changelog, the token ledger and the
table of `SECURITY.md` are edited by hand, and 1.2.0 went out without
them.

- Status: CONCEPTION
- Level: none
- Scale: unsized
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-12 CONCEPTION. Noted after the release of 1.2.0.

## The promises and the manual

---

### Refuse or redirect `Parent.x.onSet` in the body of a subclass

Written in the body of a subclass, it registers on the box of the
base, so a write on an instance of the base fails for want of the
method. `THIS[Parent].x.onSet` is the way that works.

- Status: UNDECIDED
- Level: unset
- Scale: unsized
- Release: none
- Next: the author says whether it is refused or left
- History:
  - 2026-11-10 UNDECIDED. A question of a newcomer reading the
    promises.

---

### Let `lorem_ipsum` take a project's own words and generator

`Sentence` and `Paragraph` take no words of a project's own, and the
package draws from Python's global `random`, so its text repeats only
through `random.seed`.

- Status: CONCEPTION
- Level: minor
- Scale: unsized
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-10 CONCEPTION. A question of a newcomer reading the
    promises.

---

### Notice a misspelled class keyword

A keyword in a class statement that nothing reads is dropped without a
word. A forwarded keyword and a misspelled one cannot be told apart,
and a guard around `__init_subclass__` is ruled out.

- Status: UNDECIDED
- Level: unset
- Scale: unsized
- Release: none
- Next: the author; it is his standing question
- History:
  - 2026-10-19 UNDECIDED. Listed as the author's open question.

## Testing and mutation testing

---

### Add contract, property and differential tests

A plan of 2026-06-08: one invariant run across the family of boxes,
property tests with `hypothesis` for the dispatcher, and tests against
CPython for `resolveMRO`, slices and `isinstance`. The suite went
another way in November 2026, to full branch coverage and Cosmic Ray,
and holds none of the three.

- Status: UNDECIDED
- Level: none
- Scale: large
- Release: none
- Next: the author says whether they are wanted beside the sweeps
- History:
  - 2026-06-08 UNDECIDED. Proposed in a hand-off, and never taken up.

---

### Narrow the `except TypeError` of the exact-match lookup

`src/worktoy/dispatch/_dispatcher.py`, line 801. It is written for an
argument whose class cannot be hashed, and would also hide a defect
inside the lookup.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none
- Next: the author says whether it is narrowed
- History:
  - 2026-11-06 UNDECIDED. Left to the author when the tests were
    written anew.

---

### Remove five small redundancies from the source

`True` and `False` beside `1` and `0` in the cast to `bool`, the
shortcut for a single base in `resolveMRO`, the two-word branch of
`joinWords`, the early check for an empty slot in `bipartiteMatching`,
and the filler value of `Arrangement.inverse`.

- Status: UNDECIDED
- Level: micro
- Scale: small
- Release: none
- Next: the author says which go
- History:
  - 2026-11-06 UNDECIDED. Pointed at by the mutation sweeps.

## Thread and task safety

---

### Probe the thread safety under real threads

Descriptors and namespace hooks keep their state per thread since
1.1.0. The review before 1.2.0 read that code and did not run it under
threads.

- Status: CONCEPTION
- Level: none
- Scale: unsized
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-12 CONCEPTION. Named as not examined by the review.

---

### Find out what a generator pausing in a hook, and gevent, do

What becomes of the state of an access in either case is answered
nowhere.

- Status: CONCEPTION
- Level: unset
- Scale: unsized
- Release: none
- Next: someone tries both
- History:
  - 2026-11-10 CONCEPTION. A question of a newcomer reading the
    promises.

## Reviews of the source

---

### Review README, manual, promises, docs and tests against the code

The review before 1.2.0 compared the docstrings with the code, and
left these out.

- Status: CONCEPTION
- Level: none
- Scale: large
- Release: none
- Next: someone writes what it would take
- History:
  - 2026-11-12 CONCEPTION. Named as not examined by the review.

---

### Run the suite on Windows

It never has. One finding of the review, on the line break of
`textFmt`, rests on a simulation.

- Status: CONCEPTION
- Level: none
- Scale: unsized
- Release: none
- Next: someone with a Windows machine
- History:
  - 2026-11-12 CONCEPTION. Named as not examined by the review.

---

### Add a root `CLAUDE.md` with the rule on reading the core

The rule that `core`, `dispatch`, `desc` and `mcls` are read whole in
every session is kept in notes outside the repository. A file at the
root would put it into the repository.

- Status: UNDECIDED
- Level: none
- Scale: small
- Release: none
- Next: the author says whether he wants it
- History:
  - 2026-11-12 UNDECIDED. Offered, and not answered.
