# Planned work: `PENDING`

Brought up to date: 2026-11-16.

The items of planned work that stand at `PENDING`: decided for, and
something has to happen first. `Next` says what the item waits for.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## Warnings, deprecations and the next major version

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

### Let a `KeeFlags` class take `strictCase`

A `KeeFlags` class does not read the keyword: `strictCase=False` on its
class statement is passed over, and a flag that is not upper case
raises `KeeCaseException` with a message that does not mention the
keyword. The name of a flag is also part of the name of every
combination it belongs to, joined by `_`, so a flag in another case
reaches further than a member in another case does.

- Status: PENDING
- Level: minor
- Scale: small
- Release: none
- Next: the author's word; deferred while the keyword was finished
- History:
  - 2026-11-16 UNDECIDED. Found while the keyword was mutation tested,
    as one of its consequences.
  - 2026-11-16 PENDING. Deferred by the author.

## ezdata

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
