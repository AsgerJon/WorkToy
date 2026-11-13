# The template of a planned item

Planned work on worktoy is kept as items in `planned_items.md`, beside
this file: one item for each piece of work, from the first idea until
it is released or rejected, and one for each release. Every item is
written by the template
below, so that each answers the same questions: what it is, where it
stands, which kind of release it needs, how much work it is, what has
to happen next, and when it moved.

## The template

Copy the block into the section of the part of worktoy it belongs to,
and fill it in. The horizontal line belongs to the block: it stands
above the name of every item, with an empty line on each side of it.

```text
---

### <The title of the item: what is to be done, verb first>

<Description: what it is and why, in a few sentences. What changes for
someone using worktoy, and what it costs.>

- Status: CONCEPTION
- Level: unset
- Scale: unsized
- Release: none
- Next: <what has to happen next, and who does it>
- History:
  - <YYYY-MM-DD> CONCEPTION. <where the idea came from>
```

## Description

What the item is and why it is wanted, written for a reader who was not
there when it came up.

The title above it says what is to be done, beginning with the verb:
`Release 1.2.1`, `Optimize attribute access on worktoy classes`,
`Remove the four deprecated names`. It uses the proper word for the
work, as "optimize", and names the thing as its users name it. It is not
a statement of fact, which a reader cannot tell to be true or not, and
not a bare topic, which does not say what is wanted.

## Status

An item has one status at a time. The statuses come in this order:

```text
CONCEPTION
DESCRIBED
  UNDECIDED
  REJECTED
  PENDING
READY
  UNDERWAY
  DEV
  RC
  LTS
```

- `CONCEPTION`: an idea. It is named, perhaps measured, and nobody has
  written what it would take.
- `DESCRIBED` is the step that follows: the description says what the
  item changes and what it costs. A described item stands at one of
  three:
  - `UNDECIDED`: the author has not decided. `Next` holds the question.
  - `REJECTED`: decided against. The item stays in the file with the
    reason, so that it is not proposed again.
  - `PENDING`: decided for, and something has to happen first. `Next`
    says what the item waits for.
- `READY`: nothing stands in the way, and work may start. A ready item
  then moves through four:
  - `UNDERWAY`: being built. It is in the tree and in no build.
  - `DEV`: published in a dev build.
  - `RC`: published in a release candidate.
  - `LTS`: released.

Only the author moves an item out of `UNDECIDED`. Work on a `READY`
item starts on the author's word. `DEV`, `RC` and `LTS` follow the
release buttons.

## Releases

A release is an item as well. Its title is `Release` and the version,
its `Level` is the level of its release buttons, and its
`Status` says how far it has come: `UNDERWAY` while what it carries is
being built, then `DEV`, `RC` and `LTS` as its builds are published.
Its description says what the release is for.

Every other item names in `Release` the release that carries it. When
a release moves to `DEV`, `RC` or `LTS`, the items it carries are moved
with it, in the same edit.

## Level

The kind of release the item needs, which is the level of the release
button that may carry it.

- `micro`: a repair, a correction, speed or text.
- `minor`: something new.
- `major`: something promised is removed or changed.
- `none`: it ships in no release, as tooling, tests and notes.
- `unset`: not known yet.

A release cycle is pressed at the highest level among the items it
carries.

## Scale

How much work the item is.

- `small`: one sitting; a few lines, or one file with its tests.
- `medium`: a day or two; one package, with its tests and its mutation
  sweep.
- `large`: more than that, or work in the core that other packages
  rest on.
- `unsized`: nobody has looked yet.

## Release

The version of the release that carries the item, as `1.2.1` or
`2.0.0`, or `none` while no release does. For an item that is a
release, its own version.

## Next

What has to happen next, and who does it: a question the author has to
answer, the thing a pending item waits for, the press of a button, or
`nothing` for an item that is rejected or released.

## History

One line for every change of status: the date, the status, and a few
words. The first line is the conception and says where the idea came
from. The last line tells when the item last moved.

## Keeping the file

- A `REJECTED` item stays in the file.
- An item that reached `LTS` stays until the release after it, and is
  then taken out; the changelog holds it from there.
- An item of level `none` is taken out when it is done.
- To list every item with its status:

  ```text
  grep -n -e "^### " -e "^- Status:" planned_items.md
  ```
