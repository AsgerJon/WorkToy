# Planned work: `UNDERWAY`

Brought up to date: 2026-11-16.

The items of planned work that stand at `UNDERWAY`: being built. It is
in the tree and in no build.

The items are written by `item_template.md`, beside this file, and
`planned_items.md` lists the files of the other statuses. An item that
changes its status is moved, whole, to the file of the new one, under
the heading of its area.

## keenum

---

### Let a `KeeNum` class name its members in any case

The names of the members of an enumeration are held to upper case, so
a class whose members are named otherwise, as the names of another
system are, could not be an enumeration. The class statement may now
give the class keyword `strictCase=False`, and the body of that class
then names its members in any case. Without the keyword nothing
changes. The check moved from the name setter of `Kee` into the
namespace hook, which can read the keywords of the class statement. The
keyword is promised in `promises/keenum` and shown in the manual.

- Status: UNDERWAY
- Level: minor
- Scale: small
- Release: none
- Next: the author chooses the release that carries it
- History:
  - 2026-11-15 CONCEPTION. The author's: a keyword that lets a class
    escape the upper-case rule takes no promise back.
  - 2026-11-15 UNDERWAY. Built, with its tests.
  - 2026-11-16 UNDERWAY. Mutation tested, promised on the author's
    word, and written into the manual and the changelog.
  - 2026-11-16 UNDERWAY. The keyword is held to a `bool` as the
    namespace is created, so a body without members is checked as well.
  - 2026-11-16 UNDERWAY. On the author's word a subclass takes the
    choice of its base: a class statement without the keyword follows
    the nearest class along its resolution order that gave it.

---

### Refuse members whose names differ only by case

Under `strictCase=False` one class could hold members whose names
differed only by case, as `mW` and `MW`. A lookup by name ignores case
and reads a table keyed by the lower-cased name, in which the two
shared one entry: `Power('mW')`, `Power['mW']` and a box given `'mW'`
all answered `MW`, the member declared last. The second of such a pair
is now refused with `KeeDuplicate` at its line, as a name declared
twice is, and so are a subclass adding `MW` to an inherited `mw` and
two bases holding such a pair. `KeeDuplicate` holds the name of the
enumeration and names it in its message. The changelog, the promise
and the manual say so.

- Status: UNDERWAY
- Level: micro
- Scale: small
- Release: none
- Next: the author chooses the release, which is the one carrying the
  keyword
- History:
  - 2026-11-16 UNDECIDED. Found while the keyword was mutation tested.
  - 2026-11-16 UNDERWAY. Decided by the author: such a pair is
    refused. Built, tests first, and mutation tested.
  - 2026-11-16 UNDERWAY. On the author's word the refusal is promised
    and shown in the manual, and `KeeDuplicate` takes the name of the
    class.

---

### Refuse a member named as something its class uses

The upper-case rule kept the name of a member apart from every name the
enumeration class, its bases and its metaclass use, none of which is
upper case. Under `strictCase=False` nothing did: a member named
`space` or `members` made the class statement fail on a property of
the metaclass, with Python's "property 'space' of 'KeeMeta' object has
no setter", and a member named `fromValue`, `mro` or `owners`, or as a
method of a base, took the place of that name on the class without a
word. Where the upper-case rule does not hold, a member at a name a
base or the metaclass holds now raises `ReservedName` at its line.
`index` is among those names for as long as the deprecated accessor
lives. `name` and `value` are free, since each member holds them and
the class does not. A class that keeps the upper-case rule is as it
was. The changelog says so; the promise and the manual do not name it.

- Status: UNDERWAY
- Level: micro
- Scale: small
- Release: none
- Next: the author chooses the release, which is the one carrying the
  keyword, and says whether the promise and the manual name the refusal
- History:
  - 2026-11-16 UNDECIDED. Found while the work on the keyword was
    finished, by naming a member after each name of the class.
  - 2026-11-16 UNDERWAY. Decided by the author: such members are
    banned. Built, tests first, and mutation tested.
