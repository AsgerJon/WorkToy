# Planned work: `LTS`

Brought up to date: 2026-11-13.

The items of planned work that stand at `LTS`: released. An item stays
here until the release after its own, and is then taken out; the
changelog holds it from there.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## The release of 1.2.1

---

### Release 1.2.1

The micro release that repairs what 1.2.0 broke: a test base built on
`BaseTest` by a metaclass of its own could no longer be created, and a
test class could no longer write a `doCleanups` or a `debug` of its
own. By the author's decision it carries everything else in the tree
as well. Released on 2026-11-13, after four dev builds and one
release candidate. The release differs from the candidate in the
version stamp alone and passes on every Python from 3.7 to 3.15.

- Status: LTS
- Level: micro
- Scale: medium
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 CONCEPTION. The report on what 1.2.0 broke.
  - 2026-11-12 UNDERWAY. The repair built; the author decided that the
    release carries everything in the tree.
  - 2026-11-12 DEV. Builds `1.2.1.dev0` and `1.2.1.dev1`.
  - 2026-11-13 DEV. Build `1.2.1.dev2`, checked against the tree.
  - 2026-11-13 DEV. Build `1.2.1.dev3`, with the hand edits, checked
    against the tree.
  - 2026-11-13 RC. Candidate `1.2.1rc0`, checked against the tree.
  - 2026-11-13 LTS. Released as `1.2.1`, checked from PyPI.

---

### Let a test base bring a metaclass of its own again

1.2.0 made `TestMeta` the metaclass of `BaseTest` and refused the names
`doCleanups` and `debug` in every test class. A test base built by a
metaclass of its own could no longer be created, and a test class could
no longer write either method. `BaseTest` is built by `BaseMeta` again
and reports the failed `subTest` blocks from `__class_init__`.

- Status: LTS
- Level: micro
- Scale: medium
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 CONCEPTION. The report on what 1.2.0 broke.
  - 2026-11-12 UNDERWAY. Built the same day, on the author's decision.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.
  - 2026-11-13 RC. In the candidate `1.2.1rc0`.
  - 2026-11-13 LTS. Released in `1.2.1`.

---

### Remove `BaseTest.tearDownClass`

`BaseTest.tearDownClass` took the file of the test class out of
`sys.modules` and ran the garbage collector, which kept
`tearDownModule` from running under `unittest`. The method is removed,
and is not to come back.

- Status: LTS
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 CONCEPTION. Found while the package was read.
  - 2026-11-12 UNDERWAY. Removed on the author's word.
  - 2026-11-12 DEV. In build `1.2.1.dev1`.
  - 2026-11-13 RC. In the candidate `1.2.1rc0`.
  - 2026-11-13 LTS. Released in `1.2.1`.

---

### Refuse a name bound as a field and as something else

One body binding a name as a field and as a method, a descriptor or an
overload is refused, and so is a method or a descriptor at the name of
an inherited field.

- Status: LTS
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 CONCEPTION. Found reading `ezdata` against the core.
  - 2026-11-12 UNDERWAY. Built, and kept on the author's ruling.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.
  - 2026-11-13 RC. In the candidate `1.2.1rc0`.
  - 2026-11-13 LTS. Released in `1.2.1`.

---

### Take back equality across different field orders

Two classes whose fields come in different orders were equal by
position, which contradicted equality by name. They are no longer
equal, and the promise is confessed in `promises/confessions`.

- Status: LTS
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 UNDECIDED. Every repair made one promise false.
  - 2026-11-12 UNDERWAY. The author decided to take the promise back.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.
  - 2026-11-13 RC. In the candidate `1.2.1rc0`.
  - 2026-11-13 LTS. Released in `1.2.1`.

---

### Let a subclass of `EZField` take options of its own

The parentheses of `EZField[T](...)` reach the `__init__` of a
subclass, as those of a box do, and a field called again after its
class exists is refused.

- Status: LTS
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 UNDECIDED. Nothing promised a subclass of `EZField`.
  - 2026-11-12 UNDERWAY. The author decided for it.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.
  - 2026-11-13 RC. In the candidate `1.2.1rc0`.
  - 2026-11-13 LTS. Released in `1.2.1`.

---

### Optimize creation, assignment and comparison of `EZData` instances

An instance is made in 1377 ns where 1.2.0 takes 2162 ns, and an
assignment takes 191 ns where it took 250 ns. The `__post_init__` a
class does not have is answered from the metaclass.

- Status: LTS
- Level: micro
- Scale: medium
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 CONCEPTION. Measured during the read of `ezdata`.
  - 2026-11-12 UNDERWAY. The part that changes no answer first, then
    the `__post_init__` lookup on the author's decision.
  - 2026-11-12 DEV. In build `1.2.1.dev0`.
  - 2026-11-13 RC. In the candidate `1.2.1rc0`.
  - 2026-11-13 LTS. Released in `1.2.1`.

---

### Make the smaller corrections of 1.2.1

`replace` no longer goes through `asDict`. A subclass of `EZHook`
declared in a subclass of `EZSpace` acts in place of the inherited
hook. A default that cannot be built says so with a `TypeError`. The
docstrings of `ezdata` and `work_test` say what the code does.

- Status: LTS
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 CONCEPTION. Found reading `ezdata` and `work_test`.
  - 2026-11-12 UNDERWAY. Each held against the promises first.
  - 2026-11-12 DEV. In builds `1.2.1.dev0` and `1.2.1.dev1`.
  - 2026-11-13 RC. In the candidate `1.2.1rc0`.
  - 2026-11-13 LTS. Released in `1.2.1`.

---

### Make the hand edits before 1.2.1 is released

The header of the changelog section carried the date it was written.
Two promise docstrings said "the update after 1.2.0" where the version
belongs. Reading the whole source against the changelog entry found
two more: a sentence of the entry naming the wrong exception for an
overload at the name of a field of the same body, and the docstring of
the package naming Python 3.14 as the newest it targets.

- Status: LTS
- Level: micro
- Scale: small
- Release: 1.2.1
- Next: nothing
- History:
  - 2026-11-12 PENDING. Known since the changelog section was written.
  - 2026-11-13 READY. The author gave the word: "all five".
  - 2026-11-13 UNDERWAY. All five made and staged, in no build yet.
  - 2026-11-13 DEV. In build `1.2.1.dev3`.
  - 2026-11-13 RC. In the candidate `1.2.1rc0`.
  - 2026-11-13 LTS. Released in `1.2.1`.
