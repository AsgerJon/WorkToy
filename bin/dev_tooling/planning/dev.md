# Planned work: `DEV`

Brought up to date: 2026-11-22.

The items of planned work that stand at `DEV`: published in a dev build.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## The release of 1.3.0

---

### Release 1.3.0

The next minor release, which the author proposed on 2026-11-22 for
abstract classes. It carries the item under abstract classes below.

- Status: DEV
- Level: minor
- Scale: medium
- Release: 1.3.0
- Next: the author arms and presses `minor-rc`, or presses `minor-dev`
  again for a further dev build, which needs no safety
- History:
  - 2026-11-22 UNDERWAY. Filed while a first build of what it carries
    lay in the tree.
  - 2026-11-22 CONCEPTION. That build was rolled back on the author's
    word.
  - 2026-11-22 UNDERWAY. Built anew on the design the author laid out.
  - 2026-11-22 UNDERWAY. The changelog section, the table of supported
    versions and the token ledger were written for it on the author's
    word.
  - 2026-11-22 UNDERWAY. The safety of `minor-dev` was armed on the
    author's word, in the commit that carries the build.
  - 2026-11-22 DEV. `1.3.0-dev0` was published by `minor-dev` and
    checked from PyPI: both files against their hashes, the wheel
    against the source, and the suite, the design tests and the manual
    against the wheel on Python 3.15, 3.11 and 3.7.

## Abstract classes

---

### Let a class be abstract

A class built by `ABCMeta` of `worktoy.mcls` declares methods with
`@abstract` of `worktoy.dispatch`, which the classes based on it have
to write. A class is abstract for as long as it lacks an
implementation, and is never declared so. A subclass may write any of
the abstract methods or none, and may declare abstract methods of its
own. Making an object of an abstract class raises
`MissingImplementation`. A method written wrongly, as another kind of
method or one that cannot receive what is declared, raises
`WrongImplementation` as its class is created. An overloaded name is
abstract one signature at a time, and is written by a plain function at
the name or by every one of its signatures, which Python's `abc`
cannot ask for, since such a name holds a dispatcher in every class.

- Status: DEV
- Level: minor
- Scale: medium
- Release: 1.3.0
- Next: it moves with the release
- History:
  - 2026-11-22 CONCEPTION. Asked for by the project wrapping Qt, whose
    abstract names are overloaded, and taken up on the author's word.
  - 2026-11-22 UNDERWAY. Built twice in a day, before the design was
    laid out.
  - 2026-11-22 CONCEPTION. Rolled back on the author's word: the
    builds went for the nearest solution.
  - 2026-11-22 UNDERWAY. The author laid the design out one rule at a
    time, and it was built on those rules, tests first, to full branch
    coverage and a Cosmic Ray sweep.
  - 2026-11-22 UNDERWAY. Promised on the author's word: the promises
    and the refusals in `design`, section 7 of the part on
    `worktoy.mcls` in the manual, and the changelog.
  - 2026-11-22 UNDERWAY. The author ruled on what was left open: a
    class built by `ABCMeta` may write `__class_call__`; a builtin is
    no implementation; a record carries `__abc_only__`, set by the
    namespace of an abstract class, and `__declaring_class__`.
  - 2026-11-22 DEV. Published in `1.3.0-dev0`.
  - 2026-11-22 DEV. `ABCObject` added on the author's word, the base of
    the classes `ABCMeta` builds, as `BaseObject` is of the others. It
    is in the tree and goes out with the next dev build.
