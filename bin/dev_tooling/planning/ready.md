# Planned work: `READY`

Brought up to date: 2026-11-13.

The items of planned work that stand at `READY`: nothing stands in the
way, and work may start on the author's word.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## The release of 1.2.1

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
