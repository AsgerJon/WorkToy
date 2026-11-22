# Planned work: `LTS`

Brought up to date: 2026-11-22.

The items of planned work that stand at `LTS`: released. An item stays
here until the release after its own, and is then taken out; the
changelog holds it from there.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## The release of 1.2.3

---

### Release 1.2.3

The micro release that lets one overloaded name hold bound methods,
classmethods and staticmethods together, with a fallback for each way
of reaching such a name, and that gathers the promises, the new
refusals, the confessions and the manual into the folder `design`. It
carries the two items under overloads and the two under the promises
and the manual below. Released on 2026-11-22, after two dev builds and
a release candidate.

- Status: LTS
- Level: micro
- Scale: medium
- Release: 1.2.3
- Next: nothing
- History:
  - 2026-11-21 UNDERWAY. Several kinds of method at one overloaded
    name built, on the author's word.
  - 2026-11-22 DEV. Build `1.2.3.dev0`, by `micro-dev`, checked from
    PyPI against the tree.
  - 2026-11-22 DEV. Build `1.2.3.dev1`, by `micro-dev`, with the two
    fallbacks and the folder `design`, checked from PyPI against the
    tree.
  - 2026-11-22 DEV. The changelog section written.
  - 2026-11-22 RC. A release candidate, by `micro-rc`, pressed by the
    author. No session checked it from PyPI.
  - 2026-11-22 LTS. Released as `1.2.3`, by `micro-lts`, pressed by
    the author. No session checked it from PyPI. The token ledger was
    advanced after the release, so the badge of the README shows it
    from the next one.

## Overloads

---

### Let one overloaded name hold several kinds of method

Some names are both a method of an object and a function of its class,
as `QFile.exists` is in Qt. Every declaration at one overloaded name
had to be one kind of method, and a second kind raised
`MixedMethodKind`. The overloads of one name may now be bound methods,
classmethods and staticmethods together: through the class the
classmethods and the staticmethods are tried, through an instance the
bound methods and the classmethods, and a staticmethod is not
considered through an instance where an overload of the name is a
bound method. A bound method and a staticmethod may share a signature.
A name holding bound methods beside another kind takes two
dispatchers, one for each way of reaching it. The rule is promised in
`design/promises/dispatch` and shown in the manual and the changelog.

- Status: LTS
- Level: micro
- Scale: medium
- Release: 1.2.3
- Next: nothing
- History:
  - 2026-11-21 CONCEPTION. Brought by a project wrapping Qt, whose
    names are both a method and a static function.
  - 2026-11-21 UNDERWAY. A first build was erased on the author's
    word. He then settled the rule in steps and had it built, tests
    first.
  - 2026-11-22 UNDERWAY. Mutation tested by two Cosmic Ray passes over
    the files of the change, and promised on the author's word. The
    two promise tests that pinned the refusal of a second kind went
    with that refusal.
  - 2026-11-22 DEV. Published in `1.2.3.dev0`. The author carries it
    in the micro cycle of 1.2.3, so its level reads micro, though the
    template calls something new minor.
  - 2026-11-22 RC. Published in the release candidate.
  - 2026-11-22 LTS. Released in `1.2.3`.

---

### Let a name hold a fallback for each way of reaching it

A name holding bound methods beside staticmethods is reached two ways,
and held one fallback for both. It may now hold two: the instance
bound fallback, declared as a bound method, takes a call through an
instance that nothing accepts, and the class bound fallback, declared
as a staticmethod, takes such a call through the class. A fallback
declared as a classmethod is both, and stands alone at its name. A
fallback or a finalizer is no overload: declared as a bound method, it
takes no call away from a staticmethod that accepts it. The changelog
says so; nothing in `design` promises it yet.

- Status: LTS
- Level: micro
- Scale: small
- Release: 1.2.3
- Next: nothing
- History:
  - 2026-11-22 CONCEPTION. Asked for by the project wrapping Qt.
  - 2026-11-22 UNDERWAY. Built on a scratch copy, tests first. The
    author ruled that a classmethod fallback stands alone, and had a
    bound fallback at a name of static overloads repaired before the
    build was moved into the tree.
  - 2026-11-22 UNDERWAY. Mutation tested by a Cosmic Ray pass over the
    two files with changed code, and once more over the hook file
    after its last line was reworded.
  - 2026-11-22 DEV. Published in `1.2.3.dev1`.
  - 2026-11-22 RC. Published in the release candidate.
  - 2026-11-22 LTS. Released in `1.2.3`.

## The promises and the manual

---

### Write a refused mistake as a refusal, in the folder `design`

The promises named the exception each mistake raises, which promised
the type of every exception. A mistake that raises is now a refusal: it
says that the mistake raises, and names the exception as of a stated
version, which is not promised and may be relaxed without a
deprecation. What an exception carries once it is raised stays a
promise of the exception itself. The folder `promises` became `design`,
holding `design/promises`, `design/refusals` and `design/confessions`.
186 exception checks left the promises and are 178 refusals.

- Status: LTS
- Level: micro
- Scale: medium
- Release: 1.2.3
- Next: nothing
- History:
  - 2026-11-22 CONCEPTION. The author's: particular exception types
    are not to be promised.
  - 2026-11-22 UNDERWAY. The word for it chosen by the author, the
    checks moved, the prose split by hand, the version named in place
    of the day, and the folder renamed, each on his word.
  - 2026-11-22 DEV. Published with `1.2.3.dev1`.
  - 2026-11-22 RC. Published with the release candidate.
  - 2026-11-22 LTS. Released with `1.2.3`.

---

### Join the manual into one file that continues the README

The manual was ten chapters in a folder of its own. It is one file
now, `design/manual.md`, which begins with the README, word for word,
and goes on from the class the README ends with into a part for each
package, what works and what is refused described together, closing
with what may be relied on. The release buttons write the README over
its top at every press, through `manual_stamp.py`, and commit it with
the other stamped files.

- Status: LTS
- Level: micro
- Scale: small
- Release: 1.2.3
- Next: nothing
- History:
  - 2026-11-22 CONCEPTION. The author's: one file holding the whole
    design, written for a curious reader, as a continuation of the
    README.
  - 2026-11-22 UNDERWAY. Joined, reordered and opened with the README
    on his word; the tooling and the nine workflows keep the copy in
    step.
  - 2026-11-22 DEV. Published with `1.2.3.dev1`, where the new step of
    the tooling ran for the first time.
  - 2026-11-22 RC. Published with the release candidate.
  - 2026-11-22 LTS. Released with `1.2.3`.
