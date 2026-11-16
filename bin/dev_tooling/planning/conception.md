# Planned work: `CONCEPTION`

Brought up to date: 2026-11-13.

The items of planned work that stand at `CONCEPTION`: an idea. It is
named, perhaps measured, and nobody has written what it would take.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## The speed of the core

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

## work_test

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
