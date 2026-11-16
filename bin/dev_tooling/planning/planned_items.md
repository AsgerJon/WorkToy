# Planned work on worktoy

Brought up to date: 2026-11-16.

Every piece of planned work is an item, from the first idea until it is
released or rejected, and so is every release. The items are written by
`item_template.md`, beside this file, which says what the words of
`Status`, `Level` and `Scale` mean.

The items are kept in one file for each status, in the order an item
passes through them. An item that changes its status is moved to the
file of the new one.

| status | file | items |
| --- | --- | ---: |
| `CONCEPTION` | [conception.md](conception.md) | 13 |
| `UNDECIDED` | [undecided.md](undecided.md) | 23 |
| `REJECTED` | [rejected.md](rejected.md) | 1 |
| `PENDING` | [pending.md](pending.md) | 6 |
| `READY` | [ready.md](ready.md) | 2 |
| `UNDERWAY` | [underway.md](underway.md) | 0 |
| `DEV` | [dev.md](dev.md) | 4 |
| `RC` | [rc.md](rc.md) | 0 |
| `LTS` | [lts.md](lts.md) | 9 |

To list every item with its file:

```text
grep -n "^### " conception.md undecided.md rejected.md pending.md \
  ready.md underway.md dev.md rc.md lts.md
```

## The areas

Within a file the items stand under the heading of their area. What is
to be known about an area as a whole is said here, once.

### The release of 1.2.1

The release itself is an item. So is each thing it carries: one item for
each heading of its section in `changelog.md`, and one for the edits
made by hand before it.

Items: 1 at `READY`, 9 at `LTS`.

### The release of 1.2.2

The release itself is an item, and so is each thing it carries: the
three items under keenum that stand at `DEV`.

Items: 1 at `DEV`.

### The speed of the core

Measured on 2026-11-12 with Python 3.15:

| operation               | plain Python | worktoy |
| ----------------------- | -----------: | ------: |
| stored box read         |        15 ns |  243 ns |
| computed attribute read |        25 ns | 3135 ns |
| class attribute read    |        13 ns |   78 ns |
| hash of a class         |        33 ns |  371 ns |
| overloaded call         |        30 ns |  937 ns |
| instance made           |        65 ns | 1244 ns |

Items: 4 at `CONCEPTION`, 1 at `READY`.

### Warnings, deprecations and the next major version

A promise of the library taken back at once is a confession. One kept
through the 1.x releases and taken back at the next major version is a
deprecation, announced by the warning `DeprecatedPromise`.

Items: 1 at `CONCEPTION`, 3 at `UNDECIDED`, 2 at `PENDING`.

### keenum

Items: 3 at `UNDECIDED`, 1 at `PENDING`, 1 at `REJECTED`, 3 at `DEV`.

### ezdata

Items: 5 at `UNDECIDED`, 1 at `PENDING`.

### work_test

Items: 2 at `CONCEPTION`, 2 at `UNDECIDED`, 1 at `PENDING`.

### The release tooling

Items: 1 at `CONCEPTION`, 1 at `PENDING`.

### The promises and the manual

Items: 1 at `CONCEPTION`, 2 at `UNDECIDED`.

### Testing and mutation testing

Items: 3 at `UNDECIDED`.

### Thread and task safety

Items: 2 at `CONCEPTION`.

### Reviews of the source

Items: 2 at `CONCEPTION`, 1 at `UNDECIDED`.

### The documentation

The pages are built by markwork, a package of its own, and published
at Read the Docs and at GitHub Pages. These items came up on
2026-11-13, the day 1.2.1 was released, while the author had not yet
decided where markwork goes next. Three decisions stand and frame
them: the docs job exists in the three lts workflows alone, so
publishing docs means cutting a release; Read the Docs is set, on its
own site, to build on release tags alone, so its `latest` is switched
off; and GitHub Pages deploys from GitHub Actions, not from a branch.

Items: 4 at `UNDECIDED`.
