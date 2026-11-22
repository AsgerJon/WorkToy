# Planned work: `UNDERWAY`

Brought up to date: 2026-11-22.

The items of planned work that stand at `UNDERWAY`: being built. It is
in the tree and in no build.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## The release of 1.3.0

---

### Release 1.3.0

The minor release that lets a class declare abstract methods and
abstract overloads. The author proposed 1.3 for it on 2026-11-22, and
released 1.2.3 without it. It carries the item under overloads below.

- Status: UNDERWAY
- Level: minor
- Scale: medium
- Release: 1.3.0
- Next: the author's word on the open choices of the item it carries,
  then a Cosmic Ray sweep, then the press of `minor-dev`
- History:
  - 2026-11-22 UNDERWAY. What it carries is built in the tree and is
    in no build.

## Overloads

---

### Let a class declare abstract methods and abstract overloads

A class may declare a function it has nothing to run for, which every
class based on it has to write, as a model of a list has to say how
many rows it holds. `@abstract`, written directly above the `def`,
declares it, for a plain method, a classmethod, a staticmethod and the
signatures of an overloaded name. An overloaded name is abstract one
signature at a time: each signature stacked on an abstract function is
one a subclass has to write, by declaring that signature again or by
defining the name plainly. Making an object of a class that still
lacks something is refused before `__init__` runs, naming each,
whatever the class is based on. Python's `abc` cannot do this for an
overloaded name, whose class holds a dispatcher and no function. No
call costs more than before: an abstract class is given a
`__class_call__` that refuses, and a class statement costs about five
microseconds more.

- Status: UNDERWAY
- Level: minor
- Scale: medium
- Release: 1.3.0
- Next: the author says where `abstract` is imported from and confirms
  or overrules the choices made in the build; then a Cosmic Ray sweep
  over the changed files, the promise and the manual on his word, and
  the changelog
- History:
  - 2026-11-22 CONCEPTION. Asked for by the project wrapping Qt, whose
    abstract names are overloaded, and taken up on the author's word.
  - 2026-11-22 UNDERWAY. Built, tests first, with a name counted as
    written once a subclass declared any overload of it.
  - 2026-11-22 UNDERWAY. Rebuilt to the author's rule the same day:
    each signature has to be written. The check at every call was
    replaced by a hook that only an abstract class holds.
