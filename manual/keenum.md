# worktoy manual: keenum

`worktoy.keenum` holds worktoy's enumerations: `KeeNum`, a set of named
members with typed values, and `KeeFlags`, a set of flags with every
combination as a member. Both work with the boxes of the desc chapter,
which turn a name or a value assigned to a field into the member.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Three things are deprecated since 1.2.0: `index` on a member, `KeeBox`
and `KeeFlag`. Each works as it did through the 1.x releases, gives a
deprecation notice where it is used, and is no longer promised from the
next major update. Section 8 lists them with the promises 1.2.0 took
back.

Contents:

1. Declaring an enumeration
2. Finding a member
3. The enumeration and its members
4. Extending an enumeration
5. Enumerations in boxes, and `KeeBox`
6. Flags: `KeeFlags`
7. A metaclass of your own
8. Deprecated and taken back in 1.2.0


## 1. Declaring an enumeration

```
>>> from worktoy.keenum import KeeNum, Kee
>>> class WeekDay(KeeNum):
...   MONDAY = Kee[str]('Mandag')
...   TUESDAY = Kee[str]('Tirsdag')
...   SATURDAY = Kee[str]('Lordag')
...   def isWeekend(self):
...     return self is WeekDay.SATURDAY
>>> WeekDay.MONDAY.value, WeekDay.MONDAY.index
('Mandag', 0)
>>> WeekDay.SATURDAY.isWeekend()
True

```

- `Kee[str]('Mandag')` builds the value by calling the type, so
  `Kee[int]()` holds `0` and `Kee[int]('3')` holds `3`.
- Every value has the type of the first member; a second type raises
  `KeeTypeException`.
- Member names are upper case; another name raises `KeeCaseException`.
- Values need not be unique. Anything in the body that is no `Kee`,
  a method or a plain value, stays an ordinary class attribute, and a
  method is a method of every member.
- A name declared twice raises `KeeDuplicate`, and a plain value at a
  member's name `KeeMemberNameError`.

Coming from Python's `enum`, mind the differences: a lookup by call
takes names as well as values, a subscript takes positions, a miss
raises `KeeResolveError`, which is no `ValueError`, and an enumeration
may be extended by a subclass.


## 2. Finding a member

`WeekDay(x)` and `WeekDay[x]` look for a member in this order:

1. `x` is already a member;
2. a name, in any case;
3. the answer of `__class_resolve__`, a classmethod of your own;
4. for `WeekDay[x]` only, a position, as list indexing, `WeekDay[-1]`
   the last;
5. a value, the first member holding it.

```
>>> class Rank(KeeNum):
...   LOW = Kee[int](2)
...   MID = Kee[int](5)
...   HIGH = Kee[int](9)
>>> Rank('mid').name, Rank(9).name
('MID', 'HIGH')
>>> Rank(2).name, Rank[2].name
('LOW', 'HIGH')

```

`Rank(2)` is a value and `Rank[2]` a position, so for an enumeration of
integers the two disagree, and `Rank[5]` is a value only while there are
fewer than six members. Use the call for values and the subscript for
positions, and give an integer enumeration a `__class_resolve__` to
settle what its integers mean:

```
>>> class Level(KeeNum):
...   LOW = Kee[int](1)
...   HIGH = Kee[int](10)
...   @classmethod
...   def __class_resolve__(cls, identifier):
...     if identifier == 'max':
...       return cls.HIGH
...     return NotImplemented
>>> Level('max').name, Level('low').name
('HIGH', 'LOW')

```

A name wins over a value, and a value shared by two members gives the
first. A `bool` is no position and no value of an integer enumeration.
A miss raises `KeeResolveError`, with the enumeration as `keeNum` and the
identifier as `identifier`:

```
>>> from worktoy.waitaminute.keenum import KeeResolveError
>>> try:
...   Rank('top')
... except KeeResolveError as miss:
...   print(miss.identifier)
top

```

A call takes exactly one argument. `Rank.fromValue(9)` looks up a value
and nothing else, raising `TypeException` for a value of another type.
And `Rank.low` is `Rank.LOW`: attribute access takes a name in any case.


## 3. The enumeration and its members

An enumeration iterates its members in order, counts them with `len`,
and holds them in `members`. A member has `name`, `value` and
`valueType`, and is an instance of its enumeration. It has `index` too,
which is deprecated:

```
>>> [day.name for day in WeekDay]
['MONDAY', 'TUESDAY', 'SATURDAY']
>>> type(WeekDay.MONDAY) is WeekDay, isinstance(WeekDay.MONDAY, WeekDay)
(True, True)
>>> WeekDay.MONDAY in WeekDay, 'MONDAY' in WeekDay
(True, False)

```

- A member equals itself alone, not its name or value.
- It hashes when its value hashes, so a member with a list value is no
  dict key.
- A copy, a deep copy and a pickle give the member itself. A pickle
  holds the member's name, so renaming a member breaks old pickles.
- Members are frozen. Setting or deleting an attribute of one, or
  rebinding a member's name on the class, raises `KeeWriteOnceError`.
- There is no ordering of members.
- How a member reads as text is not promised: use `name` or `value`.


## 4. Extending an enumeration

A subclass holds the members of its base, the same objects, and adds
its own after them:

```
>>> class LongWeek(WeekDay):
...   SUNDAY = Kee[str]('Sondag')
>>> [day.name for day in LongWeek]
['MONDAY', 'TUESDAY', 'SATURDAY', 'SUNDAY']
>>> LongWeek.MONDAY is WeekDay.MONDAY
True
>>> LongWeek.SUNDAY in WeekDay, isinstance(LongWeek.SUNDAY, WeekDay)
(True, True)

```

So `in` and `isinstance` admit the members of subclasses too, while
iterating `WeekDay` gives its own. Code that must know every member it
can receive iterates the enumeration it was written for.


## 5. Enumerations in boxes, and `KeeBox`

An `AttriBox` over an enumeration takes whatever a call takes, so a
name or a value assigned to the field becomes the member:

```
>>> from worktoy.mcls import BaseObject
>>> from worktoy.desc import AttriBox
>>> class Calendar(BaseObject):
...   day = AttriBox[WeekDay](WeekDay.MONDAY)
>>> calendar = Calendar()
>>> calendar.day = 'tuesday'
>>> calendar.day is WeekDay.TUESDAY
True
>>> calendar.day = 'Lordag'
>>> calendar.day is WeekDay.SATURDAY
True

```

Anything the enumeration cannot resolve is refused with
`TypeException`. `typeCast` converts the same way, which is why a name
becomes a member while `typeCast` never parses a number: resolving a
name is the enumeration's own rule.

`KeeBox` is deprecated since 1.2.0; an `AttriBox` over the enumeration,
as above, declares the same field. A `KeeBox` is a box whose
parentheses take more: the member, a name, a
position, a value, or the arguments the value is built from. Over flags
it takes several names. The one place they part ways is a lone
integer:

```
>>> from worktoy.keenum import KeeBox
>>> class Board(BaseObject):
...   boxed = KeeBox[Rank](2)
...   plain = AttriBox[Rank](2)
>>> board = Board()
>>> board.boxed.name, board.plain.name
('HIGH', 'LOW')

```

The parentheses of a `KeeBox` read `2` as a position; those of an
`AttriBox` call `Rank(2)`, a value. Assignment to either converts as the
enumeration does. A `KeeBox` default no member matches raises
`KeeBoxValueError` at the first read.


## 6. Flags: `KeeFlags`

```
>>> from worktoy.keenum import KeeFlags, KeeFlag
>>> class FileAccess(KeeFlags):
...   READ = KeeFlag()
...   WRITE = KeeFlag()
...   EXECUTE = KeeFlag()
>>> len(FileAccess)
8
>>> (FileAccess.READ | FileAccess.WRITE) is FileAccess.READ_WRITE
True
>>> FileAccess('execute_read').names == {'READ', 'EXECUTE'}
True

```

`KeeFlag` is deprecated since 1.2.0. It is still how this chapter
declares a flag, since what is written in its place is not promised
yet.

A flags class holds every combination of its flags as a member, built
as the class is created: 2 ** N members for N flags, `NULL` the one with
none. That costs memory and time at the class statement: the
`KeeFlags` docstring measured 16 flags at about
a third of a second on one machine, and the cost quadruples for every
two flags added.

- A member's `index` is its bit mask, which is also its position among
  the members. Flag `i` is bit `i` in the order declared; bits cannot be
  chosen. `index` is deprecated.
- A member's `name` joins its flag names by `_` in declaration order,
  so a flag name may not contain `_` itself, nor be `NULL`; either raises
  `KeeFlagNameError`. A body name a member takes raises
  `KeeMemberNameError`, so there are no aliases such as `ALL`.
- `names` is a frozenset of the flag names, `highs` and `lows` the flags
  on and off, and iterating a member gives its flags on.
- A call or subscript takes a member, a name in any case and flag order,
  several names or a tuple of them, an index or a value; `FileAccess()`
  is `NULL`.
- `|`, `&`, `^` and `~` give members; `NULL` is false, every other
  member true.
- A subclass overrides `_getValue` to give members values of its own.
  What `value` is without that is not promised.
- `~` of `NULL` is not promised.

A subclass adds flags. Members of the two with the same flags are equal
and hash alike, and combining them gives the member of the class that
holds every flag:

```
>>> class Extended(FileAccess):
...   APPEND = KeeFlag()
>>> Extended.READ == FileAccess.READ
True
>>> (FileAccess.READ | Extended.APPEND) is Extended.READ_APPEND
True

```


## 7. A metaclass of your own

`KeeNum` is built by `KeeMeta`. A project extending the metaclass bases
its enumerations on the root its own metaclass builds, `keeNum`, so the
customizations reach them:

```
>>> from worktoy.keenum import KeeMeta
>>> class FontMeta(KeeMeta):
...   pass
>>> class FontFamily(FontMeta.keeNum):
...   ARIAL = Kee[int](1)
...   TIMES = Kee[int](2)
>>> isinstance(FontFamily, FontMeta)
True

```

Basing `FontFamily` on `KeeNum` instead would build it with plain
`KeeMeta`, silently without the customizations.

`AccessNum`, last, is a small enumeration worktoy uses itself, of the
descriptor methods: `GET`, `SET` and `DELETE`, holding `'__get__'`,
`'__set__'` and `'__delete__'`.


## 8. Deprecated and taken back in 1.2.0

Deprecated: each works as it did through 1.x, gives a deprecation
notice, a `FutureWarning`, at the line that uses it, and is no longer
promised from the next major update.

- `index` on a member, of `KeeNum` and of `KeeFlags`. An index is a
  position in a class, and a member is one object shared by its
  enumeration and every subclass of it, so it can carry one index where
  two classes may hold it at two positions. The class still answers a
  position: `WeekDay[0]`.
- `KeeBox`. An `AttriBox` over the enumeration declares the same field,
  and reads a lone number in its parentheses the way assignment reads
  it.
- `KeeFlag`. What is written in its place is not promised yet.

Taken back: promised in 1.1.0, found to contradict another promise, and
no longer true in 1.2.0. Nothing is promised in their place.

- The default `value` of a flags member is its bit mask. Equal members
  of related flags classes held different values.
- A flags subclass holds members of its own for the flags of its base.
  The members are still equal and hash alike.
- `~` of `NULL` gives the member with every flag. `NULL` stands for no
  flag in every flags class alike, so it cannot say whose flags it
  lacks.
- An enumeration iterates in index order. The order of a class cannot
  be read off a number each member carries.
