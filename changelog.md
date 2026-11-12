# Changelog

This changelog covers stable releases. Development ('-dev') and release
candidate ('-rc') builds are not logged on their own; their changes are
rolled into the release they lead up to.

## [1.2.1] - 2026 November 12

This release repairs 1.2.0. In making every failed `subTest` block
count, 1.2.0 broke three things that worked in 1.1.0: a test base built
by a metaclass of its own could no longer be based on `BaseTest`, and a
test class could no longer write a `doCleanups` or a `debug` of its
own. All three work again, and a failed block is still reported. The
release also carries a concentrated pass over `worktoy.ezdata`, which
changes behaviour in the places listed below, one of them a promise
taken back. Every change of behaviour was made test first. The suite
passes on every Python from 3.7 to 3.15, with every statement and
branch covered on 3.15, and every file whose code changed since 1.2.0
was mutation tested after its last change.

### A test base may bring a metaclass of its own again

In 1.2.0 `BaseTest` was built by a new metaclass, `TestMeta`, in a
namespace that refused the line of a class body binding `doCleanups` or
`debug`. A test base built by a metaclass of its own, based on
`BaseMeta`, then met a metaclass conflict and was not created at all,
and a test class overriding `doCleanups` or `debug` and handing on,
which is ordinary `unittest`, was refused.

    class OwnMeta(BaseMeta):
      pass

    class AppTest(BaseTest, metaclass=OwnMeta):  # TypeError in 1.2.0
      pass

`BaseTest` is built by `BaseMeta` again. The report of the failed
blocks comes from the class hook `__class_init__`, which runs for every
test class under any metaclass based on `BaseMeta`. Each test method
reports as it ends, and the class is given a `doCleanups` and a `debug`
that report, built around the ones it would use otherwise. So a failed
block still fails its test whatever the class does in `tearDown`,
`doCleanups`, `debug` or `run`. A test base that writes a
`__class_init__` of its own hands on to the one of `BaseTest`.
`TestMeta` and `TestSpace` remain for a test base that chooses them, and
under them a class body binding `doCleanups` or `debug` is still
refused.

Different from 1.2.0, and to know:

- A failed block in a test marked `unittest.expectedFailure` is that
  expected failure.
- A test with failed blocks both in its method and in `tearDown` or a
  cleanup fails twice, once for each report.
- A failing test shows one frame more in its traceback, the line that
  calls the test method.

### `BaseTest` leaves the class teardown to `unittest`

`BaseTest.tearDownClass` took the file of the test class out of
`sys.modules` after its tests and ran the garbage collector. 1.1.0
removed it. 1.2.0 brought it back, and its changelog did not say so.

`unittest` looks the file of a test class up in `sys.modules` after the
class has torn down. So under `python -m unittest` the `tearDownModule`
of a file holding a `BaseTest` class never ran, nor any function given
to `addModuleCleanup`, and the run said OK. A second test class of the
same file ran with its file unloaded, so pickling a class of that file
failed there. Under pytest `tearDownModule` ran, since pytest takes the
function when it collects the file.

`BaseTest` has no `tearDownClass` of its own now. A class that a test
builds is freed when Python collects garbage, as under a plain
`unittest.TestCase`, and no longer before the next test class runs. A
test that must not see what an earlier test class built calls
`gc.collect()` itself.

### A name in an `EZData` body is a field or something else, not both

A class body that binds a method, a descriptor or an overload at the
name of a field of the class, declared in the body or inherited, is
refused with `DuplicateError`, and so is a field bound at the name of a
method or a descriptor of the body.

    class Shape(EZData):
      area = 0.0

      def area(self) -> float:  # refused here, with 'DuplicateError'
        ...

Such a class was created before, and then hid the method behind the
value of the field, could not be instantiated, or gave every instance
the default of the field whatever it was given. A subclass may still
declare an inherited field again as a field, with another default or
type.

### A promise taken back: equality across two orders of the fields

1.2.0 promised that two `EZData` instances are equal when their values
are and they are of one lineage. For a subclass holding its fields in
another order than the class it is compared with, as a class based on
two dataclasses declaring the same names in opposite orders does, that
sentence read two ways, by position and by name, and each reading made
the other false. Two classes whose fields come in different orders are
no longer congruent, and their instances are not equal. A class and a
subclass holding the same fields in the same order are equal over equal
values as before. The promise is written up in `promises/confessions`.

### A subclass of `EZField` takes options of its own

The parentheses of `Sub[T](...)` reach the `__init__` of a subclass of
`EZField`, as those of a subclass of `AttriBox` do, so a field class of
a project may take options beside the default. The field a subclass of
the dataclass inherits keeps the class and the options of the field it
comes from. A field that belongs to a class refuses new arguments with
a `TypeError`, as a placed box does.

### `EZData` instances are made, written and compared faster

No answer changed but the one named last. Measured on Python 3.15, a
dataclass of two floats:

- An instance is made in about 1.4 microseconds, where 1.2.0 took about
  2.2. The constructor skips its keyword passes when no keyword is
  given and stores a value of exactly the field type without the cast.
- An assignment takes about 190 nanoseconds, where it took about 250.
- A comparison between an instance and one of a frozen subclass takes
  about 2 microseconds, where it took about 29.
- A class without a `__post_init__` no longer pays for a failed lookup
  at every construction. The price: `hasattr(cls, '__post_init__')` is
  true on every dataclass now, with `None` as the value for a class
  that has none.

### Smaller corrections

- `replace` of an `EZData` class reads the fields themselves, so a class
  writing its own `asDict` keeps a working `replace`.
- A subclass of `EZHook` declared in a subclass of `EZSpace` acts in
  place of the hook that namespace inherits, which makes the extra
  spellings of the class keywords the docstring spoke of reachable.
- A default of a field that cannot be built says so, with a
  `TypeError` naming the field, where it reported a wrong value nobody
  gave, with a `TypeException`.
- `fields` shows the object it refuses by its `repr`, and
  `ReservedFieldError` says that a method may be written at a reserved
  name and only a field is refused.
- The docstrings of `worktoy.ezdata` and of `worktoy.work_test` say
  what the code does and open with the need the code answers. Among the
  sentences corrected: `EZField[T](...)` is named the recommended way
  to declare a field; a sampler class that leaves a hook out is
  created and cannot be instantiated; the `seed` of a sampler is no box
  and takes an `int` alone; `TestSpace` is the namespace of `TestMeta`,
  not of every test class.
- The manual chapter on `ezdata` and two promise docstrings were
  corrected where they said other than the code does. They said that
  every field has a default and named `__post_init__` among the
  generated methods, and neither is so. They now say how the default of
  a field is made from a lone value, and that `__match_args__` is empty
  for a keyword-only class.

## [1.2.0] - 2026 November 12

This release was rushed. It was moved up to this day because of a silent
defect in `BaseTest`: a test could be counted as passed while one of its
`subTest` blocks had failed. The defect is in 1.0.0 and 1.1.0 as well,
and it was found on 12 November, while the whole source was read against
its documentation. The same read turned up the other corrections of this
release, none of them of that weight, and they are released with the fix
together with the work that was finished since 1.1.0. Rushed does not
mean unchecked: every change of behaviour was made test first, the suite
passes with every statement and branch covered, and every line changed
since the last development build was mutation tested, with two gaps in
the tests found and closed that way. The release is the same code as
its only release candidate, 1.2.0-rc0, which was published the same
day; nothing but the version stamp differs.

### A failed `subTest` block is reported whatever `tearDown` does

`BaseTest` swallows what a `with self.subTest(...):` block raises and
records it, so that the other blocks of the test still run, and fails
the test afterwards with every record. That report ran in
`BaseTest.tearDown`. A test class that defined a `tearDown` of its own
without handing on to the base, which is the ordinary way to write one,
since the `tearDown` of `unittest.TestCase` does nothing, never ran the
report: a test with a failed block was counted as passed, and nothing
said so. Plain `unittest` reports such a block.

    class TestForgets(BaseTest):

      def tearDown(self) -> None:
        pass

      def test_block(self) -> None:
        with self.subTest(n=1):
          self.assertEqual(1, 2)  # passed in 1.0.0 and 1.1.0

The report now runs from `doCleanups`, which `unittest` calls after
every test whatever the test class does in `tearDown`, and at the end of
`debug`, which runs a test without collecting errors. `BaseTest` is
built by a new metaclass, `TestMeta`, in a new namespace, `TestSpace`.
The metaclass puts the library's own `doCleanups` and `debug` into every
test class before its body runs, and the namespace refuses the line of a
class body that binds either name, with `ReservedName`. A `tearDown` now
runs to its end before the report; `BaseTest` no longer defines one, and
a call of `BaseTest.tearDown` reaches `unittest.TestCase.tearDown`.

After the update a test based on `BaseTest` that passed only because of
this defect fails, with the labelled report of its blocks. A test class
that defines `doCleanups`, or binds the name `debug`, a flag
`debug = True` included, is refused when it is created.

### worktoy warns

`worktoy.waitaminute` holds a family of warnings beside the exceptions.
`WorkToyWarning` is the common base, and its `warn` method is the one
place a warning is given: it walks out of the library and gives the
warning at the line the user wrote, so no call counts a `stacklevel`. A
warning is given as an exception is raised, `RiskWarning('price',
price, 'a till that pays the customer').warn()`, and like
`TypeException` it is handed the things it is about and words the
sentence itself. `DeprecatedPromise` is the deprecation notice, a
`FutureWarning`, since Python hides a `DeprecationWarning` from
everyone but the author of the file that runs. `RiskWarning` and
`AlternativeWarning` say that something promised is risky, or has a
better way beside it, and `RedundantKeyword` says that a function
received a keyword it does not read. A project built upon worktoy gives
warnings of its own by subclassing them in a package of its own, and
the warning then lands on the line of that project's user.

### A keyword a helper does not read is warned about

`joinWords`, `unpack`, `textFmt`, `stringList`, `wordWrap` and
`resolveMRO` take their options as keywords and read the names they
know. A misspelled option, as in `joinWords('tea', 'coffee',
seperator='or')`, was dropped without a word, and the helper ran on its
default. Each of the six now gives a `RedundantKeyword` for a keyword
that is none of its options, at the line of the caller, and goes on as
before: the result of the call is unchanged.

### A message shows a value by its `repr`

Where a message of `worktoy.waitaminute` showed a value it mostly used
`str`, inside quote marks of its own. The string `'12'`, the number `12`
and a `Decimal` of 12 then read the same, and an empty string showed as
nothing. A value now goes into a message by its `repr`, without quote
marks around it, and a `repr` longer than 50 characters is cut:

    Unable to cast value '12' to type 'int'!
    Unable to cast value Decimal('12') to type 'int'!
    Unable to cast value '' to type 'int'!

Sixteen message classes changed, `TypeCastException`, `TypeException`,
`ProtectedError`, `ReadOnlyError`, `WriteOnceError` and
`KeeResolveError` among them; `TypeException` no longer doubles the
quote marks of a string. Names keep their quote marks. The text of
`WithoutException` and of `ReservedFieldError` passes through `textFmt`
as every other message does, and the docstring of `textFmt` says what
that does to a value quoted in a message: runs of whitespace in it are
collapsed. A test that compares the text of a message may have to
follow.

### A `__cast_as__` hook may be an overloaded classmethod

A class says how a value becomes one of its instances in a classmethod
`__cast_as__`, and may write that hook once for each type it converts
from, with `@classmethod` above `@overload(...)`. `typeCast` refused
such a hook with `UnboundCastHook`, saying `@classmethod` was missing,
because an overloaded name is held in the class as a `Dispatcher`. It
takes the hook now; a value that none of the overloads accepts is
refused with `TypeCastException`, as a value the hook answers with
`NotImplemented` is, and an overloaded hook that is no classmethod is
refused as before.

### `typeCast` refuses a number of no family for `bool`

The casts to `int` and `float` take the builtin numbers only and refuse
a `Decimal` or a `Fraction`. The cast to `bool` took any number equal to
0 or 1, so `typeCast(bool, Decimal(1))` gave `True`. It refuses such a
number now, as the other casts do and as the written promise says.

### An `EZData` field may be named `self` or `argCount`

A field of one of those names could not be given by keyword: the
generated `__init__` and `replace` failed with a `TypeError` about
multiple values for an argument, since the name met a parameter of the
generated code. Both names work now, as they do in `dataclasses`.

### Smaller corrections

- `ProtectedError` leaves the old value out of its message when it was
  handed none. It said `with value: 'None'` before, whatever the value
  was.
- A control-flow signal class may not bind `args`, the one plain name
  `Exception` holds as data; such a class carried state, which a signal
  is not to do.
- Reading a deleted value through a descriptor that was never placed on
  a class names the descriptor as the one without a name, where it named
  the instance read.
- `EZField[OWNER]`, a sentinel as the field type, is refused in the
  words of a field type, where the message spoke of an overload
  signature.
- Docstrings that said something other than the code were corrected:
  where `Object` keeps its frames, which defaults of `AbstractMetaclass`
  hand over with `super()`, the context of a `HookException`, what
  `KeeFlag`, `Kee`, `KeeWriteOnceError` and `PhantomBoxError` cover,
  when `hasCastRule` raises, `TypeException` on `None`, which draws of a
  sampler are checked, when two `EZData` classes are congruent, and who
  raises `SkipSet`.
- Imports and type aliases that nothing used were removed.

### A read through an `AttriBox` of a stored value builds no frame

By far the most reads through an `AttriBox` are of a value already
stored, through a box with no read callback. Such a read now returns the
value without building the frame and running the hook phases, which
nothing would use: about 0.2 microseconds where it took about 2.1,
measured on a point with two float attributes on Python 3.15.2. The
first read of an instance, a deleted value, a box with a read callback
and a subclass that overrides a read hook take the full read as before,
and every read gives the value it gave.

### The enumerations answer from tables built once

A member of a `KeeNum` or a `KeeFlags` class is found, hashed and
combined from tables the class builds once. Measured on Python 3.15
against 1.1.0: a member as a dictionary key is looked up in about 0.1
microseconds where it took about 20, and `a ^ b` on two flags takes
about 0.6 microseconds where it took about 220. A class of 16 flags is
built in about a second; in 1.1.0 a class of 12 flags took about three.

Breaking: a member of an enumeration is no longer an `Object`. No box
tags a member, and a member bound in the body of another class is an
ordinary class attribute, which an instance may shadow.

### An enumeration may be based on several enumerations

A `KeeNum` or `KeeFlags` class may list several enumerations as bases.
It holds the very members of its bases; a member reached through two
bases is one member, and two members under one name, or bases of
different value types, are refused. `KeeFlags` is rebuilt the way
`KeeNum` works: every member is a combination of flags, one member
stands for each set of flags in the process, and the root `KeeFlags`
builds `NULL`. Members carry `owners`, the classes holding them, and
`Kee[str]()` takes the name of the member as its value.

Breaking: the default `value` of a `KeeFlags` member, the identity of
the members of a flags subclass, and `~NULL`, as listed below.

### Promises taken back in `KeeFlags`

Four things promised in 1.1.0 contradicted other promises and are no
longer true. They are written up in `promises/confessions`.

- The default `value` of a flags member was its bit mask. Equal members
  of related flags classes held different values.
- A flags subclass held members of its own for the flags of its base.
  It holds the very members of its base now, as a `KeeNum` subclass
  does; they were equal before and are the same object now.
- `~` of `NULL` gave the member with every flag. `NULL` is one member
  shared by every flags class and cannot say whose flags it lacks;
  `~NULL` raises `ZeroDivisionError`.
- An enumeration iterated in index order. It iterates in the order
  declared, the members of its bases first.

### Deprecated: `KeeBox`, `KeeFlag`, the `index` of a member, the old control-flow path

Each works as it did through the 1.x releases, gives a
`DeprecatedPromise` at the line that uses it, and is no longer promised
from the next major update.

- `KeeBox`. An `AttriBox` over the enumeration declares the same field.
  The parentheses of a `KeeBox` read a lone number as a position while
  assignment reads the same number as a value.
- `KeeFlag`. Flags are declared with `Kee`, as the members of a `KeeNum`
  are.
- `index` on a member of `KeeNum` and of `KeeFlags`, and with it
  `int(member)`, a member used as an index, and `Kee.index`. A member
  is one object shared by its enumeration and every subclass of it, so
  it can carry one index where two classes may hold it at two
  positions. The position belongs to the class, which answers `Day[x]`.
- The names of `worktoy.waitaminute.control_flow`. The signals live in
  `worktoy.core.control_flow`, and `ControlClassError` in
  `worktoy.waitaminute.meta`.

### The promises of the library are written down

The repository holds the promises of worktoy as tests, in `promises/`:
389 of them, grouped by package, each class saying in its docstring what
is promised and where the promise comes from. The four promises taken
back are in `promises/confessions`, and the four that end at the next
major update in `promises/deprecations`. `manual/` shows each package by
example.

## [1.1.0] - 2026 November 7

### Descriptors and namespace hooks keep their state per thread

A descriptor based on `Object` keeps a stack of frames so that its code
can ask for the instance and the owner of the access in progress, and
a record of the read hooks running so that a hook reading its own field
is refused rather than looping. Both lived on the descriptor, shared by
every thread, so two threads reading through the same descriptor at
once could see each other's frames: one read answered with the other
thread's instance, and two threads reading the same instance were taken
for a recursive read. A namespace hook had the same flaw one level up:
one hook object serves every class statement of its namespace class and
was bound to the namespace of the latest statement, so two threads
running class statements at once could hand each other's namespace to
the hooks, and a class could be built without the overloads of its
body. All three records now live in thread-local storage keyed by the
descriptor or the hook, nothing is kept on the object itself, and each
thread sees only its own. A frame never outlives the call that pushed
it, so an asyncio task cannot see the frames of another either. The
cost of an access did not rise: a frame is now pushed and popped on a
list in place where a copy of the list was written before, and reads
through an `AttriBox` measure the same or slightly faster. A test with
eight threads hammering one descriptor, and one with eight threads
running class statements, pin both.

### A FastBox write refuses the instance and the name before the value

`FastBox.__set__` checked the type of the value first and only then
fetched the instance dict and looked for the box's own name. On an
instance without a dict, or through a box that never learned its name,
a value of the wrong type was therefore refused as a type error, and
in the second case the refusal named the field `'None'`, pointing at
the value when the box itself was the problem. The write now refuses
the missing dict and the missing name first, as `__get__` and
`__delete__` always did, and the type of the value last. A write
through a placed box on an ordinary instance costs what it cost: one
check and one store.

### The bank tells its operations from lookalikes

`ComplexTest`, the bank of twenty-five tests that runs against any
implementation of `ComplexMixin`, checked reflected division with
`2 / target(1, 1)` and a power with `target(2, 0) ** 2`. Those operands
were unlucky: `2 - (1 + 1j)` is also `1 - 1j`, and `2 * 2` is also `4`,
so an implementation that subtracted in `__rtruediv__` or multiplied
in `__pow__` passed the bank. Mutation testing of the bank found both.
The two tests now use `4 / target(1, 1)`, which is `2 - 2j`, and
`target(3, 0) ** 2`, which is `9`, and the tests of the bank hold a
target that subtracts and one that doubles, each failing exactly the
tests of its wrong operation. A correct implementation passes as
before.

### Mutation testing checks the tests of every package

Coverage reports which lines the tests ran. It does not report whether
the tests would notice a wrong line, since a test can run a line and
assert nothing about what it did. Mutation testing asks that second
question. A tool, Cosmic Ray here, makes one small deliberate change to
the library at a time, called a mutant: a `<` becomes `<=`, a constant
changes, a statement is dropped, a `return` hands back something else.
It then runs the whole test suite against that one change. If some test
fails, the mutant is killed: the tests would catch that mistake. If
every test passes, the mutant survives: the tests would let that
mistake through. Each survivor is then read by hand. Most show a gap in
the tests, and a test is written to close it. Some cannot change what
the library does, as a check that comes out the same either way, and
such a mutant is called equivalent and recorded as such rather than
fought.

The tests of `utilities`, `core`, `dispatch`, `desc`, `mcls`, `keenum`,
`ezdata`, `lorem_ipsum` and `work_test` were written anew for this
release, to full line and branch coverage, with the exceptions of
`waitaminute` pinned by the packages that raise them, and each package
was then mutation-tested twice, the second pass over the tests the
first pass added. Every surviving mutant was killed by a new test or
examined and recorded as equivalent. Writing the tests turned up the
defects that the entries below correct; the mutants found gaps in the
tests, and in one place a gap in a shipped bank of tests, the entry
above.

From here on, every release is preceded by a mutation run restricted to
the code changed since the last release tag, and a release does not
ship with a surviving mutant that is not recorded as equivalent. The
procedure is in `CONTRIBUTING.md` under "Mutation Testing Before a
Release".

### 'replace' refuses an unknown field as the constructor does

Giving `replace` a name that is no field of the dataclass raised a
plain `TypeError` with a wording of its own, while giving the same name
to the class raised `ExtraKeywordException`, which names the class, the
keyword and the fields and can be caught as such. `replace` now leaves
the refusal to the generated `__init__`, which builds the new instance
anyway, as `dataclasses.replace` leaves it to the constructor. One
exception, one message. A caller catching `TypeError` is unaffected,
since `ExtraKeywordException` is one.

### A cast asks the target's hook about a member of a subclass

A flags class promises that a member of a related class resolves to its
own member, as an enumeration's call never hands back a member of
another class. The call and the subscript kept that promise, the cast
did not: `typeCast` returned any instance of the target unchanged, and
a member of a subclass is an instance of the base, so a `KeeBox` field
assigned a subclass member stored that foreign member. `typeCast` now
asks the target's `__cast_as__` about an instance of a strict subclass,
and for a flags class that hook is the call, so the cast resolves as
the call does. A target without a hook, `bool` for `int` and every plain
class included, keeps returning a subclass instance as it is.

### An 'EZData' subclass inherits 'ordered'

A class built on an ordered dataclass used to lose the ordering unless
it wrote `ordered=True` again, and lost it without a word: its
instances compared equal as before but refused `<` with a `TypeError`.
That was easy to trip over and unlike the rest of the options, where a
subclass of a frozen class is held to the freeze. A subclass now
compares as its base does, over all of its fields, and a subclass that
wants no ordering says `ordered=False`.

In detail: `EZHook.postCompilePhase` reads an absent `ordered` keyword
from the nearest `EZData` class along the resolution order, through
`_inheritedFlag`, the way `_refuseThawing` reads the frozen flag; an
explicit `ordered=False` still installs the shared `_unorderable`
comparison, which then shadows the ordering methods of the base.
`kwOnly` stays per class. Comparing an instance of the base with one of
the subclass still raises `TypeError`, as a `dataclass` refuses it.

### A lorem generator takes 'None' by position as it takes it by keyword

`Clause(charCount=None)` kept the default count of forty, while
`Clause(None)` was refused by the dispatcher, so a count a caller passes
through as "nothing given" worked in one spelling and not the other.
`BaseGenerator.__init__` has a third overload for a lone `None`, which
keeps the default, so `Clause(None)`, `Sentence.first(None)` and the
keyword form agree.

### A class is an iterable or an iterator, as Python has it

Python keeps two ideas apart. An iterable, like a list, hands out a
fresh iterator every time and is left as it was; it may have a length.
An iterator, like a generator or an open file, hands out each item once
and is used up; it has no length, and `len()` on it raises. The worktoy
class hooks now follow the same split. A class with `__class_iter__` is
an iterable, a class returning itself from it beside `__class_next__` is
an iterator, and `len(cls)` works only where the class defines
`__class_len__`. Before, `len(cls)` on a class without `__class_len__`
counted the class by iterating it, which emptied an iterator class in
the process; `list(cls)` on such a class came back empty, because
`list` asks for the length first.

In detail: `AbstractMetaclass.__len__` without `__class_len__` now
raises the `TypeError` a plain class raises without `__len__`, and
`__bool__` without `__class_bool__` answers from `__class_len__` or is
`True`, never iterating. `in` keeps searching through `__class_iter__`,
as Python's `in` searches an object without `__contains__`, so it
consumes an iterator class as it consumes a plain one. The docstrings
of `AbstractMetaclass` say what Python expects of an iterable and of an
iterator, that hooks written outside those two shapes give undefined
behaviour in some circumstances, and that a plain class written the
same in-between way behaves no better.

### 'BaseTest.seedSamplers' seeds every sampler of a test at once

A test that wanted its draws reproducible seeded its six samplers one
by one. `self.seedSamplers(7)` in a `setUp` now seeds `randomInteger`,
`randomFloat`, `randomGaussian`, `randomSymbolicName`, `randomWord` and
`randomLorem` with one seed; a seed that is no `int` is refused with
`TypeException` before any sampler is seeded.

### 'ComplexTest' is a bank of tests listed before 'BaseTest'

`ComplexTest` was a `BaseTest`, so every test module importing it
collected the bank itself and ran its twenty-five tests against nothing,
skipped one by one; the suite showed fifty such skips. The bank now has
no base of its own: a test class lists it before `BaseTest`,
`class TestMyComplex(ComplexTest, BaseTest): targets = (MyComplex,)`,
and no loader collects the bank. A class listing the bank without a
test case, the shape it had before, is refused at the class statement
with a `TypeError` naming the shape to write, so its tests cannot vanish
from a run unnoticed; a class without targets still skips every test.

### 'count' is the row count on every sampler

`SymbolicSampler(count=4)` set the word count while `count` was the
alias of `rowCount` on every sampler, so the same instance read `count`
back as 1. `count` now means the row count everywhere, by keyword and
by alias, and the word count keeps `wordCount`, `numWords`, `num_words`
and `word_count`.

### 'BaseTest' no longer unloads the module of a test class

`BaseTest.tearDownClass` popped the module of every test class from
`sys.modules` after its tests and ran the garbage collector, on a claim
that `unittest` pinning the classes leaked metaclass state between
them; the suite runs identically without it on every supported Python,
a module whose test class ran while the module was being imported
vanished from under the import system with `KeyError`, and
`ComplexTest` had to guard its own library file. `BaseTest` leaves
`tearDownClass` to `unittest.TestCase` now, and the guard on
`ComplexTest` is gone.

### A failed sub-test block is reported with its label and its traceback

A block of `with self.subTest(target=x):` that failed or raised was
recorded as the exception alone and reported by `tearDown` as
`FAIL: 5.0 != 4.0`, with no label and a traceback pointing at
`tearDown`, so a failing target in a loop could not be told from the
others. `SubTest` now records the label with each fail and each error,
read as `failLabels` and `errorLabels` beside `fails` and `errors`, and
`tearDown` reports `FAIL [target=Broken]: 5.0 != 4.0` or
`ERROR [n=3]: ValueError('three')` followed by the traceback of what
the block raised, so the report names the line that failed; the framed
report of `SubTest` shows the labels too. One failure per test is still
counted, as before.

### 'BaseSampler' is abstract through 'SamplerMeta'

`BaseSampler()` was built, and a sampler of a project that left out
`_getItem` or `_getValueType` was built too and failed at its first row
inside `isinstance`, since `ABC` and `abstractmethod` were stand-ins at
runtime to avoid the metaclass conflict with `BaseObject`. The samplers
are now built by `SamplerMeta`, `BaseMeta` combined with `ABCMeta` as
the `mcls` package documents, so the two hooks are abstract and a
sampler without both is refused at construction with Python's own
"Can't instantiate abstract class".

### The sizing settings are constructor keywords

`IntSampler(colCount=3)`, `IntSampler(width=3)`, `WordSampler(rowCount=2)`
and `LoremSampler(charCount=20)` were refused as unexpected keywords, so
a sized sampler took an assignment after construction. `colCount`
(`width`, `size`), `rowCount` (`height`) and the `charCount` (`chars`)
of a `LoremSampler` are now keywords of every constructor, a count below
one refused with `ValueError` as by assignment; `count` stays the alias
of `rowCount` and is no keyword.

### Every sampler is seedable

No sampler held a generator or took a seed; every draw went to the
state of the `random` module, which `random.seed` seeds for the whole
process at once, so two samplers could not be seeded alike and a
failing test could not be rerun with the same draws. Each sampler now
draws from a `random.Random` of its own, `sampler.random`, and takes
`seed` (`randomSeed`) by keyword or by assignment, which seeds that
generator: `IntSampler(1, 6, seed=7)` and `self.randomInteger.seed = 7`
draw the same values again whatever else draws in between, `seed` reads
back as given and `None` when never seeded, and a seed that is no `int`
is refused with `TypeException`. `randomWord` and `loremSentence` take
a generator as an optional second argument.

### A bound given by keyword alone is kept ordered

`IntSampler(minVal=300)` held the bounds reversed and raised Python's
`ValueError` at the first draw, `FloatSampler(minVal=2.0)` drew from
the reversed interval, a `FloatSampler()` given `minVal = 2.0` afterwards
did the same, and `FloatSampler(5.0, minVal=2.0)` lost the keyword to
the default, since the reorder stood down while a bound was unset and
the default written next was skipped as unchanged. Both bounds always
exist now, the reorder compares them at every write, and a pair given
together, by position or by two keywords, is written as a pair, so a
lone keyword crossing the other bound is corrected as an assignment is,
`IntSampler(minVal=300)` giving `(255, 300)`, and
`FloatSampler(5.0, minVal=2.0)` gives `(2.0, 5.0)`.

### The settings of the samplers are boxes

Each setting of a sampler was a hand-written field over a private name
with a fallback, a creator method, a `_recursion` peek and a setter
casting through `typeCast`, read by a constructor that re-derived every
default from three class-level tables; two tests of the suite said two
default mechanisms were "under consideration". The settings are now
`AttriBox`es, `minVal = AttriBox[int](0)` and the like, which hold the
type and the default, build the default for each instance, cast an
assigned value that converts without loss and refuse the rest with
`TypeException` naming the setting; the keyword constructor keeps the
synonyms of `__key_groups__`, merged along the resolution order, and
the `TypeError` for an unknown keyword. Of the behaviour a test could
see: `FloatSampler` names a refused bound `minVal` and `maxVal` where
its setters named their parameters `minValue` and `maxValue`, an `int`
assigned to `mean` is stored as the `float` the docstring promises, and
`SymbolicSampler().wordCount = 2.5` is refused at the assignment where
it was stored and failed at the first draw. The `repr` of a sampler now
names its settings, as `IntSampler(minVal=0, maxVal=255, colCount=1,
rowCount=1, seed=None)`.

### The refusals of an 'EZData' class-body line are 'SyntaxError's

`ReservedFieldError`, `ReservedMethodError`, `ReservedAttributeError`
and `DuplicateError` were `AttributeError`s, and
`IncompleteFieldException` and `ClassFieldError` were `TypeError`s, so
`except SyntaxError` around a class statement caught every refusal of
a class-body line the core makes and missed the six the `EZData`
namespace makes, and the `AttributeError` base made Python 3.12 add
"Did you mean" to their messages. All six subclass `SyntaxError` now,
as the core's refusals do, keep `WorkToyException`, and show their
message in a traceback through `msg`. The refusals of a call,
`ExtraPositionalException`, `ExtraKeywordException`,
`RepeatedFieldException` and `KwargsOnlyException`, stay `TypeError`s,
as Python's own refusals of the same calls are.

### A lone default of an 'EZField' is deep-copied for every instance

`EZField[dict]({'a': [1]})` gave each instance a dictionary of its own
whose list was shared by all of them, since a lone default already of
the field type was copied shallowly, and an `EZData` instance given as
a default shared its own fields the same way. The default is now
deep-copied, as `AttriBox` deep-copies its default, so instances share
nothing of it; a default that cannot be copied, as a lock, is refused
at the first instantiation with "The default of the field 'guard' is a
'lock' that cannot be copied, so each instance cannot have its own.
Give the field the arguments of the 'lock' constructor instead:
'EZField[lock](...)'", where the interpreter's "cannot pickle" used to
surface. An enumeration member and an immutable value copy to
themselves and are kept.

### A mutable 'EZData' instance lets an attribute that is no field go

The generated `__delattr__` refused every deletion on every `EZData`
class, with the field guarantee as its reason, so `del reading.note`
failed for an attribute the instance had taken beside its fields. On a
mutable class it now refuses the fields alone, "EZData class 'Reading'
does not allow deleting field 'value': every field holds a value of its
declared type", and hands any other name to `object`, as a non-frozen
dataclass does; a frozen class keeps refusing every deletion, now with
"'Reading' is frozen; cannot delete attribute 'note'!", the words of its
`__setattr__`.

### A class based on a frozen 'EZData' class is frozen too, or refused

The options of an `EZData` class are read from its own class statement,
so `class Child(Frozen)` without the keyword built a mutable, unhashable
class whose instances compared equal to the frozen ones, without a
word. Such a statement is now refused with a `TypeError`: "'Child' is
based on the frozen class 'Frozen' and does not declare 'frozen=True'
itself. A class based on a frozen 'EZData' class is frozen too", as
`dataclasses` refuses a non-frozen dataclass based on a frozen one,
wherever the frozen class stands along the resolution order. A frozen
subclass of a mutable class stays allowed; `ordered` and `kwOnly` stay
per class.

### An 'Alias' of a method works in an 'EZData' body; the black list is gone

An `EZData` body refused every `Alias` and every `Dispatcher` with
`BlackListedType`, a list kept because the body test for a descriptor
took both for values. With that test corrected, the list is gone: an
alias of a method works as in any worktoy body, an alias of a field is
refused by the core with `DanglingAlias` as the class is created, since
a field is a plain attribute of the instance and no class holds its
name, and a hand-wired `Dispatcher`, which worktoy no longer supports,
is guarded by nothing. `EZStore`, the descriptor placed at a field name
that a data descriptor further along the resolution order would take
over, now defines `__get__` alone: it shadows that descriptor, the
instance dictionary answers every populated read and takes every write,
and an alias of such a field reads through it while a write or a
deletion through the alias is refused by the alias. `BlackListedType`
leaves `worktoy.waitaminute.ezdata`.

### The '__post_init__' of an 'EZData' class is found on the class as it holds it

The generated `__init__` looked up `__post_init__` with `getattr`, so a
class whose `__class_getattr__` hook answers every missing name handed
the constructor a hook it never defined. The lookup now reads the class
with `type.__getattribute__`, along the resolution order as before, and
asks no `__class_getattr__`. The other branches the leaf kept in a
default argument of `dict.get`, the qualified name of a generated method
for a class built from a plain dictionary among them, are written out
and unchanged in effect.

### An 'EZField' outside an 'EZData' body is refused in plain words

`x = EZField[int](0)` in the body of a `BaseObject` or a plain class
was placed as every `Object` is: `Plain().x` read the field object
itself and `Plain().x = 5` raised `ReadOnlyError`, neither saying what
was wrong. Such a placement is now refused with a `TypeError`: "An
'EZField' declares a field of a dataclass and belongs in the body of an
'EZData' subclass, but 'Plain' is bound to one at 'x' and 'Plain' is no
'EZData' subclass." Before Python 3.12 the interpreter hands it on
wrapped in `RuntimeError`. In an `EZData` body the namespace claims the
field before the interpreter places it, so nothing changes there.

### '__slots__' in an 'EZData' body is refused by the core alone

An `EZData` class body binding `__slots__` has been refused with
`SlotsRefused` since every worktoy class body was (2026-11-03), so the
leaf's own refusal of the name with `ReservedAttributeError`, and the
message it had for it, could not be reached. The name leaves
`EZSpace.__reserved_ez_attributes__` and the message leaves
`ReservedAttributeError`, which renders its one message for every
attribute it is raised for.

### A descriptor based on 'Object' that reimplements '__get__' stays a class attribute of an 'EZData' body

An `EZData` body keeps a descriptor as a class attribute and turns every
other value into a field, and it told the two apart for an `Object` by
whether its class overrides `__instance_get__` or `__instance_set__`. A
descriptor that reimplements `__get__`, `__set__` or `__delete__`
directly, as a project may write one on `Object` and as the core's
`Alias` and `Dispatcher` do, became a field holding the descriptor as
its default. An `Object` now counts as a descriptor when its class
overrides any of the three Python methods or the three instance hooks,
and any other value when its class defines `__get__`, `__set__` or
`__delete__`, which is how Python tells a descriptor; a descriptor
defining `__delete__` alone was a field before and is a class attribute
now. An `EZData` instance, a `KeeNum` member and a `SymbolicName` still
become fields.

### Two instances of one 'EZData' class compare without the congruence question

The generated `__eq__` asked `EZMeta.isCongruent` for every pair of
instances, and `isCongruent` builds the field-type signature of both
classes through the `Field` descriptors of the metaclass at every call,
so `Point(1, 2) == Point(1, 2)` cost fifty microseconds, four hundred
times the dataclass. Two instances of one class are congruent by
definition, so the question is now asked only when the classes differ;
the same comparison costs a microsecond. Equality across congruent
classes, and its refusal across unrelated ones, is unchanged.

### The subscript of an 'EZField' is checked as the subscript of a box is

`EZField[Any]` built its class on Python 3.11 and later, where
`typing.Any` is a class, and the first instantiation or assignment then
failed with the interpreter's own "typing.Any cannot be used with
isinstance()"; a `Protocol` that is not `@runtime_checkable` failed the
same way at the first default, and `EZField[THIS]` built a class whose
first instantiation failed with a message about `THIS`. The subscript
now goes through `TypeSig.validateTypes`, the one check of a declared
type in worktoy, so an uncheckable class is refused at the subscript
with `UncheckableType` naming `EZField[Any]`, and `THIS` is refused with
a `TypeError` saying that a field needs a default and no value of the
class being declared exists while its body runs.

### An '@overload' at a method 'EZData' generates is refused as a plain definition is

An `EZData` class body overloading `__init__`, `__eq__`, `__hash__`, an
ordering method, `__iter__`, `__len__`, `__setattr__` or `__delattr__`
with `@overload` built the class with the generated method and lost the
overloads without a word, since the namespace claims an `@overload`
binding before the `EZData` hook could refuse it, while the plain `def`
of the same name was refused with `ReservedMethodError`. Both spellings
now raise `ReservedMethodError` naming the method, the overloaded one as
the class is created. An optional name such as `asDict` and the
`__post_init__` hook may still be overloaded, and a plain base
overloading `__init__` still gives way to the generated constructor.

### The members of one flags lineage agree on equality, membership, resolution and the operators

A flags class based on another holds flags of its own and members of
its own, and the members of the two classes were strangers in some
views and kin in others: `PermExt.READ == Perm.READ` was False and
`PermExt.READ | Perm.WRITE` was refused, while `PermExt.READ in Perm`
was True and `Perm(PermExt.READ)` handed back the subclass member,
which is in no `Perm.memberList`. Across a lineage a member is now
identified by the names of its high flags: a member of the base or of
the subclass is equal to the member here with the same flags and hashes
alike, resolves through a call, a subscript or `typeCast` to this
class's own member when this class holds every one of its flags and is
refused with `KeeResolveError` otherwise, is in the class exactly when
such a member exists, and takes part in the operators, the class of the
left operand answering when it holds every flag and the class of the
right one through the reflected operator otherwise, so `Perm.READ |
PermExt.EXEC` is `PermExt.READ_EXEC`. Members of unrelated flags
classes stay strangers.

### A 'Kee' or a 'KeeFlag' in the wrong body is refused in plain words

`A = Kee[int](1)` in the body of a class that is no enumeration was
refused with "Expected object at name 'owner' to be an instance of
'KeeMeta'", a type mismatch naming the metaclass, and a `KeeFlag` the
same way naming `KeeFlagsMeta`. Each is now a `TypeError` saying where
the declaration belongs: "A 'Kee' declares a member of an enumeration
and belongs in the body of a 'KeeNum' subclass, but 'Foo' is bound to one
at 'A' and 'Foo' is no enumeration." Before Python 3.12 the interpreter
still hands it on wrapped in `RuntimeError`.

### 'valueType' reads no member

`KeeMeta.valueType` checked every member's value against the declared
type at every read, and a lookup by value read it twice, so resolving a
member by value in a 200-member enumeration cost a few milliseconds,
hundreds of times a lookup by name. The getter now returns the type the
namespace pinned as the body ran and reads no member: the namespace
refuses a second declared type at the class statement, and each value is
checked against the declared type by its own `Kee` at every read, so
nothing the check found is lost.

### 'in' on a flags class answers by identity

`'read' in FileAccess` and `3 in FileAccess` were True, since
`KeeFlagsMeta.__contains__` resolved the object as a subscript does,
scanning every member for a name, while `'MONDAY' in WeekDay` was False.
An object is now in a flags class when it is one of its members, or a
member of a related flags class with flags the class holds, and a name,
an index, a value or a tuple of names is not, however it would resolve.
`cls[identifier]` with `KeeResolveError` caught is the test for whether
an identifier resolves.

### A 'KeeBox' converts an assigned value as the enumeration does

`KeeBox` resolved an assigned value by the rules of its parentheses, so
`holder.day = 1` stored the member at position one although
`WeekDay(1)` is refused, a refused assignment raised one of three
exceptions, and a lone value of the value type carried by no member was
handed to the constructor of the value type as its one argument and
reported as the object so built. Assignment, storage and deletion are
now those of `AttriBox`: a member is stored, any other value goes
through `typeCast` and the enumeration's `__cast_as__`, so a name, a
value or a tuple of flag names stores the member it resolves to and
anything the class cannot resolve is refused with `TypeException` naming
the field. The parentheses keep their rules, the arguments of the value
type with keywords included, a lone value matched by equality and a lone
`int` as a position; a lone value no member carries is refused with
`KeeBoxValueError` naming that value, and a lone `bool` for an `int`
enumeration is refused as the class refuses it.

### A flags class leaves its subclass check and its hash to the core

`KeeFlagsMeta` carried a `__subclasscheck__` of its own, walking the
declared bases of a flags class, which answered what the resolution
order answers, and a `__hash__` of the name and the file, where every
other worktoy class hashes through `AbstractMetaclass` once from its
name, bases and metaclass. Both stood ahead of `AbstractMetaclass` in the
metaclass order, so a flags body binding `__class_subclasscheck__` or
`__class_hash__` was refused with `ShadowedClassHook`. Both are gone: a
flags class hashes as every worktoy class does, `issubclass` follows the
resolution order as before, and a flags body may bind the two hooks.

### A flags class converts through 'typeCast'

`KeeFlags` declared no `__cast_as__`, so a flags class converted
nothing: `doc.access = 'WRITE'` on an `AttriBox[FileAccess]` was refused
with `TypeException`, and an overload taking a flags class refused a
name, where a `KeeNum` took both through `KeeBase.__cast_as__`. `KeeFlags`
now declares the same hook, resolving a value as calling the class
resolves it (a member, a name in any case and order, a tuple of names,
an index, a value) and declining what the class cannot resolve, so a box
or an overload over a flags class takes what the class takes.

### A flags class is built from a plain dictionary as from a class statement

`type('Perm', (KeeFlags,), {'READ': KeeFlag(), 'WRITE': KeeFlag()})`, or
the same call on `KeeFlagsMeta`, was refused with `KeeMemberNameError`
naming the first flag, because `KeeFlagsMeta.__new__` looked for the
names of the body in the dictionary it was called with, where the flag
names still stood, instead of in the namespace the plain-dictionary
branch of `AbstractMetaclass.__new__` had built and screened. The check
now reads the namespace the class carries, so a flags class generated
from a table builds as one written out does, and a dictionary binding
`NULL` or a combined name is still refused.

### A member declared without parentheses, or with a 'Kee' of another enumeration, is refused

`A = Kee[int]` in an enumeration body was accepted and gave `A` the
value `int()`, and one `Kee` object declared in two enumerations gave the
second body's position to the first enumeration's member, since the
namespace hook claimed every `Kee` before the box's own placement could
run and wrote the index onto the shared object. `KeeMeta._createMembers`
now places each new member's `Kee` on the enumeration, as a box is
placed on its class, so the core's refusals apply: a bare subscript is
refused with the box's `TypeError`, a `Kee` placed on another enumeration
already with `SharedDescriptor` naming both, before anything is written
on it; the index is assigned after the placement. A `Kee` so placed
knows its enumeration and member name, an `Object` value it builds is
tagged with them, and it pickles as the `kee` of its member.

### The statistics of a lorem distribution are held by the subclass, in boxes where they are per instance

`StochasticVariable` declared `mean`, `var`, `minVal` and `maxVal` as
fields with empty getters and refused, as a subclass was created, one
that did not define the getter names, so `GaussianLengths` kept its four
numbers in private names written by hand with `float()` and `int()`, and
a distribution a project held could not be retuned. The base now
declares nothing for the four: `GaussianLengths` holds them in boxes its
constructor writes, cast as a box casts and refusing a text with
`TypeException`, so `dist.mean = 50` retunes it; `StochasticWord` writes
them onto its class at the class statement, beside its word table; a
project's own subclass holds them however it likes, plain class
attributes included; and a subclass without them fails where it reads
them, with Python's own `AttributeError`, instead of at its class
statement. The draw, `round(gauss(mean, sqrt(var)))` clamped into the
bounds, lives on the base once, where the two subclasses each had a copy.

### A lorem partition reaches its count exactly or refuses

`StochasticVariable.partition` and `partitionSpaced` took their count of
values from the mean alone and landed as near as the bounds allowed, so
a clause over a project's own word list, ten- and eleven-letter words
say, rendered eleven characters where fifteen were asked and said
nothing, and a first clause of 19 to 23 characters drew its filler word
from lengths the default list has and such a list may not, failing with
`IndexError`. The count is now held between the fewest and the most
values that can add up to the target, a target no count can reach is
refused with `ValueError` naming it and the bounds, a target of zero is
no values at all, and `partitionSpaced` takes the slots each value costs
(`partitionSpaced(target, 2)` for a sentence's `', '` and period). The
placeholder of a short first clause no longer draws a word.

### A first sentence lays out words in its first clause

A first sentence, and so the first sentence of a paragraph, rendered its
first clause as the `Lorem ipsum ...` placeholder inside the sentence
(`Lorem ipsum sensus..., elit cursus ...`) in a few percent of everyday
paragraphs and a quarter of first sentences near 65 and 105 characters,
because the settle gave the whole correction to one clause (two draws
near 40 settled to 59 became 14 and 45) and the placeholder threshold of
a first clause was a written 24. The correction is now spread over the
values, each taking its share, with what the clamps leave filled after,
so partitions stay near their draws (27 and 32); and a first clause lays
out words from the count that holds its lead-in, a space and one word of
its list (16 with the default words), the placeholder below it being the
lead-in cut to the count ahead of dots (`Lorem ipsum....` at fifteen).

### The placeholder of a lorem generator is exactly its count at any threshold

`BaseGenerator._shortText` gave as much of `Lorem Ipsum` as fits ahead
of three dots, fourteen characters at most, so a subclass raising
`__truncate_below__`, the count below which a generator renders the
placeholder instead of laying words out, rendered fourteen characters
for every count from fifteen up to its threshold. The dots now make up
the count past the whole lead, `Lorem Ipsum....` at fifteen, so the
placeholder is exactly `charCount` characters long whatever the
threshold. Below fifteen nothing changes.

### The first-word flag of a lorem generator is a box

`isFirst` on `BaseGenerator` was a read-only `Field` over a private flag
that only the `first` constructor wrote, so a generator built without
`first` could never be asked to open with `Lorem ipsum`, and a copy
copied the private name by hand. It is now an `AttriBox[bool]`, `False`
by default and `True` on `Paragraph`, which `first` sets, a copy copies,
and a project may assign; an assignment drops the cached layout, as an
assignment of `charCount` does, so the next rendering is laid out with
or without the lead-in at the same count. A text assigned to it is
refused by the box with `TypeException`.

### An overload record over a callable without a name prints and refuses in its own words

A `functools.partial` registered through `@overload` dispatches as any
function does, but the text of the record and the refusal of a call on
it read the `__name__` of the function, which a partial lacks, so both
failed with the interpreter's `AttributeError`. Both now name the
function as the decorator does elsewhere, by its name or else its repr.

### 'None' in an overload signature is refused pointing at type(None)

`@overload(None)` was refused as an entry that is no class, with a
message naming an internal position, `types[0]`, and saying nothing of
how a call passing `None` is declared. `TypeSig.validateTypes` now
refuses a `None` entry, bare, in a flexible declaration or as the inner
type of a final `ARGS`, with a `TypeError` naming its position in the
signature and `type(None)`, the class of `None`, as the entry to write.

### A FastBox placed on a second class is refused

One `FastBox` object bound in the bodies of two classes was accepted, and
the second class overwrote the owner the first had recorded, so the
refusal of a later call named the class that placed the box last. A
`FastBox` is now refused with `SharedDescriptor` as the second class is
created, as every descriptor based on `BaseDescriptor` is; a second name
in one class body still takes a clone.

### A box tags the Object it builds, and nothing else

`AttriBox._applyTags` wrote the three tags `__field_name__`,
`__field_owner__` and `__field_box__` onto a built value when the
declared field type had instances with a dict, so a box declared for
anything, `AttriBox[object]`, tagged nothing it built, while a plain
value was tagged although nothing could read the tags off it. The tags
exist so that a value can ask its box for the instance and the owner of
the access in progress, through `self.instance` and `self.owner`, which
only an `Object` can do. A box now tags exactly the `Object` it builds,
whatever field type it declares; a plain value, a builtin or a class is
held as its class made it.

### A name declared with a finalizer alone is documented by it

The dispatch function of an overloaded name takes the docstring of the
first concrete, flexible or variadic declaration, else of the fallback.
The finalizer was never asked, so a name declared with
`@overload.finalize` alone was documented by `getattr(None, '__doc__')`,
which from Python 3.13 is the docstring of the type of `None`, "The type
of the None singleton." The finalizer now documents such a name, and a
dispatcher holding no function documents nothing.

### SymbolicName.camel spells the words of a subclass

`SymbolicName.camel` rendered the words after the first by building a
new name of the same class from them, so a subclass giving every name a
common first word repeated it, `appAppFontSize`, and a subclass whose
constructor takes another argument read the words as that argument. The
tail is now spelled from the words themselves, as `pascal` is.

### The descriptors of worktoy.desc write their state past __setattr__

`Object` writes the arguments of a descriptor and its stack of frames
with `object.__setattr__`, past any `__setattr__` of a subclass, but the
classes of `worktoy.desc` wrote the rest through ordinary assignment: the
field type and storage key of a box, the declared value of a `FastBox`,
the names of the callbacks and accessors, the real name of an `Alias` and
the words of a `SymbolicName`. A subclass guarding its attributes with a
`__setattr__` saw one half of the bookkeeping and not the other. All of
it is now written past `__setattr__`.

### A control-flow signal body may not bind __namespace__

The `ControlSpace` of a signal body wrote itself under `__namespace__`,
which its list of admitted names let through for that purpose. `MetaType`
writes the entry into every class it builds anyway, so the namespace no
longer holds itself, and a signal body binding `__namespace__` is refused
with `ControlClassError` like any other name. The signal still holds the
namespace of its body under `__namespace__`.

### A namespace hook hands its placement keywords to hookSetName

`AbstractSpaceHook.__set_name__` called `Object.__set_name__` without the
keywords it received, so `hookSetName` of a hook never saw them, unlike
every other `__set_name__` of the library. The keywords are now handed
on.

### A bare '@overload' is refused with BareOverload

`@overload` written without parentheses, as `typing.overload` is written,
handed the function to the decorator as the first class of its
signature, and the refusal was a `TypeException` saying that a function
is no instance of `type`, which never named the missing parentheses.
`@overload` and `@overload.flex` now refuse it with `BareOverload`, a new
`TypeError` in `worktoy.waitaminute.dispatch`, naming the decorator and
the method, and the form with parentheses, as `@overload(int)`, or
`@overload()` for a call with no positional argument.

### Classmethod overloads of a class hook replace a plain base's hook

A routed class hook such as `__class_len__`, declared in a class body with
classmethod overloads, was held to the hook of a plain base holding the
name, and a base binding a plain function there refused the class with
`UnboundClassHook`, while a plain `@classmethod` at the same name was
accepted. The overloads now count as bound by the body, as the plain
`@classmethod` does, and the dispatcher they build replaces the base's
hook.

### QuickDesc reads its slot past '__getattr__'

`QuickDesc`, and the descriptors of `worktoy.dispatch` and
`worktoy.mcls` built like it, read their private slot with
`object.__getattribute__`, as the rest of the library reads its own
names. A `__getattr__` of the owning class used to be handed the private
key of a missing slot; it is now asked about the public name only, as
for any attribute.

### A callback is called by the kind of method found at its name

A descriptor finds each notification callback by name on the class of the
instance, and used to call what it found as a plain function with the
instance first: a subclass overriding a callback with a classmethod
received the instance as `cls`, a staticmethod received the instance as
its first argument, and a `classmethod` or `staticmethod` written below a
decorator was refused, before Python 3.10 with a bare `AttributeError`.
The callback is now called as Python would call `instance.name(value)`: a
method receives the instance, a classmethod the class of the instance, a
staticmethod the value alone, and an overloaded method is bound by its
dispatcher, whether the kind is written above the decorator, below it or
by a subclass. The cut of surplus arguments by `flexCall` applies to every
kind. `Field` accessors follow the same rule with exactly their
arguments, and a `setName` callback receives the class and the descriptor,
or the descriptor alone as a staticmethod. A `functools.partial` or a
builtin, which has no function to look up by name, is refused with
`TypeException` before a name is recorded, where a `partial` raised
`AttributeError` before.

A callback written as a staticmethod above its decorator that took the
instance first no longer receives it, and is written as a plain method
instead.

### A box alias called with parentheses raises PhantomBoxError

A box subscripted with a generic, a union or a `TypeVar`, as
`AttriBox[list[str]]` or `AttriBox[Optional[int]]`, is a type alias for
hints and bases, and binding it in a class body raises `PhantomBoxError`,
whose message names the subscript and the completed form. Written with
parentheses, `AttriBox[list[str]]([])`, the alias went through the call
of `typing` instead, which built a bare box with no field type, and the
class was refused as it was created with `MissingVariable` naming
`__field_type__`, before Python 3.12 inside a `RuntimeError`. Calling a
box alias now raises `PhantomBoxError` at the call, on the line of the
declaration, on every version. A generic subclass, `class
Sub(AttriBox[T])`, uses the alias as a base and never calls it.

### A type 'isinstance' refuses is refused with UncheckableType

A box typed with a class `isinstance` refuses, as `AttriBox[Any]()` from
Python 3.11 on or a box over a `Protocol` that is not
`@runtime_checkable`, was accepted as the class was created, and then
every read and write of the attribute failed with the interpreter's own
`TypeError`; on 3.7 to 3.10 the same `AttriBox[Any]()` was refused, so the
line was accepted or refused by version. `AttriBox` and `FastBox`, and
every subclass of them, now refuse such a type at the subscript, through
`TypeSig.validateTypes`, which checks the entries of overload signatures,
so one place decides for both.

The refusal is `UncheckableType`, a new exception in
`worktoy.waitaminute`, for overload signatures as well, where it was a
plain `TypeError`. It keeps the refused type, the declaration as written
(`'(float, Any)'` or `'AttriBox[Any]'`), the position of the type in a
signature, and the `TypeError` of `isinstance`, which it is chained from
and whose text its message quotes. It is a `TypeError` as well, so code
catching that catches it as before.

### A worktoy class named in a signature is not asked about None

To refuse a type `isinstance` cannot take, `TypeSig.validateTypes` calls
`isinstance(None, entry)`. For a worktoy class defining
`__class_instancecheck__`, that ran the class's own hook with `None` at
the decorator line, and a hook reading an attribute of what it is asked
about, as `obj.value > 0`, ended the class statement with an
`AttributeError`. A class built by a `MetaType` is no longer probed, since
`isinstance` always answers for it, and the same holds for a box over it.

### A plain branch of a diamond no longer cuts the overloads of the other

A class inherits the overloads of a name from its bases until a plain
definition of the name, or a declaration of it as another kind of
method, hides what lies behind it. That cut was made along the whole
resolution order of the class, so in a diamond a plain method on the
second branch hid what the first branch inherits: with `FixedShape`
replacing the overloaded `scale` of `Shape` by a plain method, and
`LabelledShape` adding an overload to it, `class Badge(LabelledShape,
FixedShape)` lost the overloads of `Shape`, and `Badge().scale(2)` raised
`DispatchException` where `LabelledShape().scale(2)` worked. A plain
definition now hides only what lies behind it on its own branch, so
`Badge` keeps every overload `LabelledShape` holds, as Python's lookup
gives it the method of `LabelledShape`. A class listing the plain branch
first, `class Tag(FixedShape, LabelledShape)`, still takes the plain
method. The plain `FixedShape.scale` takes no call the overloads of
`Badge` refuse, where a chain of `super()` calls would hand it one, just
as a plain method of a parent takes no part once a subclass overloads
the name.

### A placed FastBox refuses a new value, as an AttriBox does

`AttriBox.__call__` refuses a box that is placed already, since a call
through the class, as `Particle.charge(9.0)`, would change the default of
every instance not read yet. `FastBox.__call__` had no such check, so
`Particle.mass(9.0)` was accepted without a word: instances read before
kept the old value, and every later one received the new. It now refuses
with a `TypeError` naming the field, in the words `AttriBox` uses, and
the box records its owner at placement for that message. A clone not yet
placed still takes a value, and reading or writing a placed box costs
what it did.

### A Dispatcher is built by the namespace of its class, not wired by hand

A `Dispatcher` is built by the namespace of a class whose metaclass is
based on `BaseMeta`, from the `@overload` declarations of the class body
and of its bases. The support for wiring one by hand is gone: the
decorators a `Dispatcher` offered of its own, `overload`, `flex`,
`fallback` and `finalize`, with the stacking of them; a dispatcher
installed on a finished class with `setattr`, which now meets
`MissingVariable` at its first read, as a box installed that way does;
and extending an inherited dispatcher through `THIS[Parent].name`. A
`Dispatcher` written in a class body no longer stops the search for the
overloads a subclass inherits, as a plain definition does.

A reference through `THIS` to an overloaded name is refused at its line
with `OverloadReference`, a new `SyntaxError` in
`worktoy.waitaminute.desc`. Its clone of the parent's dispatcher
replaced the one the namespace of the subclass builds, so the subclass
lost the overloads its body declared, and a body refused at a later line
left the clone for the next subclass of the parent, which lost its
overloads without a word. A subclass declares its own overloads of an
inherited name with `@overload` in its body and keeps the inherited
ones.

A class whose metaclass comes from another library overloads its methods
through a metaclass combined with `BaseMeta`, as one combined with
`ABCMeta` serves `abc.ABC`:

    class ABCBaseMeta(BaseMeta, ABCMeta):
      pass

    class Shape(BaseObject, ABC, metaclass=ABCBaseMeta):

      @abstractmethod
      def perimeter(self) -> float:
        ...

      @overload(int)
      def scale(self, factor: int) -> Shape:
        ...

The methods the namespace registers through, `addSigFunc` and the
others, `clone`, `restoreTHIS` and the method kinds stay, as its
machinery.

#### Rationale

With a metaclass combined with `BaseMeta` serving every class whose
metaclass comes from another library, a dispatcher wired by hand had no
use left, and each way of wiring one had needed fixes of its own.

### An overloaded call passing the declared classes costs a tuple and a lookup

The dispatch function built a `TypeSig` for every call, hashed it and,
on a hit, compared it with the key through the Python methods of
`TypeSig`. A call passing exactly the declared classes, which the
dispatcher promises no more than a dictionary lookup, cost as much as one
matched through `isinstance`. The exact tables are now keyed by plain
tuples of classes, and a call takes the classes of its arguments once,
as such a tuple; only `DispatchException` still builds a `TypeSig`, for
its message. On Python 3.14 an exact hit fell from about 2.4 us to 0.9
us, and the `isinstance` tier is cheaper by the same `TypeSig`. Which
function a call reaches does not change. A metaclass of another library
defining its own `__eq__` is now asked by the tuple comparison, as it is
by any tuple holding its classes.

### An overload signature refuses a sentinel of any family

`TypeSig.validateTypes` refuses a sentinel in a declared signature, since
no call can match a class that cannot be instantiated, but it recognized
a sentinel by `issubclass(entry, Sentinel)`. A sentinel of a family a
project builds on `SentinelMeta` directly, as the sentinels package
invites and as `ARGS` itself is built, is no subclass of `Sentinel`, so
`@overload(PENDING)` registered a signature no call could reach, and the
first call failed with `DispatchException` far from the declaration. The
test is now `isinstance(entry, SentinelMeta)`, the one the boxes make for
their field type, and the class body fails at the line. `THIS` still
passes, and so do `ARGS[...]` and a bare `ARGS`, which `TypeSig.starARGS`
turns into an instance first.

### An overloaded name may be a classmethod or a staticmethod

`overload` refused a `classmethod` or `staticmethod` object with
`TypeException` when `@classmethod` or `@staticmethod` was written below
it. Written above it, the class statement succeeded: the record escaped
every guard, a second declaration at the name silently replaced the
first, and the first call failed with the advice to base the class on
`BaseObject`, which it already was. Both orders now declare an
overloaded classmethod or staticmethod, and so does the kind written
between two decorators of one stack, as an alternative constructor
taking several kinds of argument:

    class Temperature(BaseObject):
      kelvin = AttriBox[float](0.0)

      @classmethod
      @overload(float)
      def fromCelsius(cls, value: float) -> Temperature:
        ...

      @overload(str)
      @classmethod
      def fromCelsius(cls, text: str) -> Temperature:
        ...

The dispatcher at the name is bound to the class at every read, through
the class or an instance. A classmethod receives the class, a subclass
receiving itself, and a staticmethod receives the arguments alone, its
functions registered behind a wrapper that drops the receiver. Flexible
declarations, variadic signatures, the fallback and the finalizer take
part as for an instance method, and a routed class hook such as
`__class_call__` may be overloaded as a classmethod.

Every declaration at one name in one class body is the same kind of
method. A body mixing instance methods, classmethods and staticmethods
at one name is refused with `MixedMethodKind`, a `SyntaxError`, at the
declaration breaking the rule. So is a function decorated as both a
classmethod and a staticmethod, which Python itself reads differently
from version to version: the call is refused on 3.7 and 3.8, it acts as
a staticmethod on 3.9 to 3.12 and as a classmethod from 3.13. A subclass
overloading an inherited name as another kind of method overrides it as
a plain definition does, hiding the inherited overloads.
`Dispatcher.setMethodKind` sets the kind of a dispatcher before anything
is registered.

### A namespace of a project's metaclass sees the class body alone

`MetaType.__new__` writes the namespace of a class body into itself under
`__namespace__`, so that the class keeps a reference to it, and removes
the entry again once the class exists. It did both through the
namespace's own `__setitem__` and `__delitem__`, so a metaclass a project
bases on `MetaType` with a namespace of its own saw `__namespace__` as if
the class body had bound it: a namespace refusing unknown names refused
every class, and one recording its bindings recorded the name among them.
Both now go past the namespace, with the methods of `dict`, as the
`__annotations__` entry written beside them already did.

### A flexible overload keeps a whole float and an int in their roles

`typeCast` turns a whole `float` such as `2.0` into the `int` `2`, so in
the cast tier of the dispatcher an `int` parameter and a `float`
parameter both took `2.0` and `7`, and the first signature found decided
which went where. A flexible overload of a count and a weight handed the
weight to the count as soon as another argument needed a cast:

```python
class Parcel(BaseObject):
  #  Public Variables
  count = AttriBox[int](0)
  weight = AttriBox[float](0.)
  label = AttriBox[str]('')

  @overload.flex(int, float, str)
  def __init__(self, count: int, weight: float, label: str) -> None:
    self.count, self.weight, self.label = count, weight, label


Parcel(2.0, 7, b'fragile')   # count was 2 and weight 7.0
```

A call the exact and `isinstance` tiers miss now first tries every
signature with numbers widened only, `int` to `float` to `complex`, and
every other class cast as `typeCast` allows; nothing becomes an `int` or
a `bool` there. Only a call no signature takes that way reaches the full
cast, narrowing included, so `@overload(int)` called with `2.0` still
receives `2`. A signature that takes a call by widening now wins over one
declared earlier, or in a base, that would take it by narrowing: with
`@overload(int)` and `@overload(complex)`, `2.0` reaches the `complex`
one.

### An AttriBox write no longer reads the box's own type through a Field

The public `fieldType` of a box is a `Field` whose getter is
`getFieldType`, and the box read it as `self.fieldType` wherever it
needed its own type: on every write, while building the default and while
tagging it. Each such read ran the whole read protocol of a descriptor, so
more than half of every write went to the box asking itself for its type.
The box now calls `getFieldType` directly, which a box subclass
overriding it still decides, and `box.fieldType` stays for code holding a
box. A write of `1.0` to an `AttriBox[float]` went from about 5 to under 2
microseconds on Python 3.14, a write needing a cast from about 8 to 2.5.

### A worktoy class body binding __slots__ is refused

An instance of a class built by a worktoy metaclass always keeps a
`__dict__`, where `Object` and the boxes keep their state, so `__slots__`
in a `BaseObject` body did neither thing it is declared for: the dict
stayed, and `p.z = 7` still created an attribute. Such a body is now
refused at the line binding `__slots__` with `SlotsRefused`, a
`SyntaxError` in `worktoy.waitaminute.meta`, and so is
`dataclass(slots=True)`, which rebuilds the class with `__slots__`. A
plain base declaring slots, as many mixins do, is no concern of the
class body. A class that needs slots is written as a plain class.

### An undecorated override of a callback is wrapped once

A subclass replacing a notification callback by name with a method
written without the decorator had that method wrapped by `flexCall`
anew at every read, write or deletion of the field, which made each such
access about a third slower than with a decorated callback. A descriptor
now keeps the wrapper of each callback function it finds, keyed by the
function, so a class that replaces its callback later still gets the one
it holds.

### A read hook reading its own field is refused with RecursiveRead

An `onGet` callback comparing `self.wheel` with the wheel it was handed
read the field again, which ran the callback again, until Python gave up
with a bare `RecursionError` a thousand frames later; so did a `preGet`
reading its field, and two instances or two fields whose callbacks read
each other. Such a read is now refused at the line making it with
`RecursiveRead`, a `RecursionError` in `worktoy.waitaminute.desc`, naming
the field and the notification that was running. A read of another
instance or of another field from inside the hooks, a read made by the
getter itself, a read through the class and a write are not refused, and
a hook raising leaves later reads as they were.

### A flexible overload of more than three classes is registered once

`overload.flex` registered one signature for every order of its classes,
so a declaration of six classes made 720 signatures and one of seven
5040, and each was compared with every signature before it as the class
was created: six classes took a second, seven nearly a minute. A
declaration of up to three classes is still registered that way. A
longer one is registered once. A call whose arguments are of exactly the
declared classes, in any order, finds it in one dictionary lookup, and
each declared position takes the next argument of its class in the order
the caller gave them, as before. A call passing subclass instances, or
values that convert, falls back to the `isinstance` and cast passes,
where `bipartiteMatching` gives each argument a position it fits. One
body declaring the same classes again for another function, flexibly or
as one order, is refused with `DuplicateSignature` at that line, as
before; a subclass declaring one order takes that order and leaves the
rest to the inherited declaration.

### A box holding a class, or a shared default, reads it back untagged

An `AttriBox` tags each object it builds with `__field_box__`,
`__field_name__` and `__field_owner__`. A lone default already of the
field type is deep-copied for each instance, and `copy.deepcopy` hands
some objects back as they are: a class, a function, an object whose class
answers a copy with itself, as an enumeration member does. The box tagged
them all the same. On a class the write failed, since
`object.__setattr__` refuses every class, so
`exporterClass = AttriBox[type](CsvExporter)` raised `TypeError: can't
apply this __setattr__ to BaseMeta object` at the first read. On a
function or a shared object the write succeeded, on the project's own
object, and the last box to read it owned the tags of every holder. A
default whose copy is the default itself is now returned untagged, and
so is a class built by the constructor of a field type that is `type` or
another metaclass. Every object the box creates, by copy or by
constructor, is tagged as before.

#### Rationale

The tags mean built by this box. An object handed back unchanged was
built by no box, and a tag written on a class would be read through its
instances and subclasses as their own.

### An overload nothing claims is refused where the mistake is made

`overload` only records signatures; the namespace of a class built by a
metaclass based on `BaseMeta`, as `BaseObject` is, claims every record
and builds the dispatchers. In the body of any other class the record
stayed at its name, the class statement succeeded, and the first call
failed far away with "'overload' object is not callable". Such a class
statement now raises a `TypeError` naming the class, the name, and the
way out, a class based on `BaseObject` or built by a metaclass based on
`BaseMeta`; before Python 3.12 it arrives wrapped in a `RuntimeError`, as
every refusal from `__set_name__` does. A record called anywhere else, as
a function outside a class declared with `@overload`, raises the same
explanation at the call.

### An instance of a subclass of ARGS hashes as the equal ARGS instance

`ARGS` instances compare by their inner type, and take an instance of
any subclass of `ARGS` as equal to the `ARGS` instance of the same inner
type. The hash put the class name in as well, so `TAILARGS[int]` equalled
`ARGS[int]` while a set holding the one did not find the other, and
neither did a `TypeSig` ending in it. The hash now takes the inner type
beside a fixed tag, so equal instances hash alike whatever their class.

### A metaclass of another library listed after a worktoy one runs its __init__

`MetaType.__init__` marked the class and called no further `__init__`,
so in a metaclass combining a worktoy metaclass with one of another
library, as `class Meta(BaseMeta, PluginMeta)`, the `__init__` of
`PluginMeta` never ran for the classes `Meta` built, and whatever it did,
such as recording each class, was lost without a word. Listed first, the
other metaclass worked. `MetaType.__init__` now hands the class, with
every class keyword, to the next `__init__` along the resolution order of
the metaclass building it, so the order no longer matters, as long as
each metaclass hands on in turn. It does so with
`super(MetaType, type(cls))`: the zero-argument `super()` would search
the resolution order of a metaclass based on `MetaType`, such as
`SentinelMeta`, rather than that of the metaclass building it, and the
library would fail as it is imported.

#### Rationale

Python calls only the first `__init__` of a combined metaclass, and the
rest run only if each one hands on to the next. `MetaType` was the one
link that did not.

### THIS refuses a reference to a name the class body declares itself

`THIS[Parent].x` stands for the descriptor `x` as the subclass will hold
it: a clone of the inherited descriptor, placed on the subclass as it is
created. A subclass body that declared its own `x` and also decorated
`THIS[Parent].x` lost its own `x` to the clone without a word, so a
`LoudSpeaker(Speaker)` declaring `volume = AttriBox[int](11)` read the 5
of `Speaker`. The class statement now raises `ReferenceConflict`, a
`SyntaxError` in `worktoy.waitaminute.desc`, and the record of the clone
is removed first, so the next subclass of the parent does not take the
clone of the refused body. A name the body does not bind, and a body
binding the very clone the reference gave, are served as before.

#### Rationale

A silent fallback is a bug: the declaration line of the subclass was
dead. A body decorates a descriptor of its own directly, as in
`@volume.onSet`.

### WithoutException names an unplaced descriptor as unplaced

`WithoutException` names the descriptor of a context-less call as
'Owner.name'. It read the name through `getFieldName`, which never
answers None but falls back to the name of the descriptor class, so its
own fallback 'NO-FIELD' could not fire, and an `Object` no class holds,
popped with an empty context stack, was named 'NO-OWNER.<Object>'. The
field owner now decides: a descriptor a class holds is named as before,
and one no class holds is named 'NO-OWNER.NO-FIELD'.

### Calling a TypeSig substitutes THIS in a variadic tail too

Calling a `TypeSig` returns a copy with `THIS` replaced by the class
given as `this`. The call replaced a bare `THIS` only, so
`TypeSig(int, ARGS[THIS])(this=Node)` kept `ARGS[THIS]`, while
`swapTHIS(Node)`, which rewrites a signature in place once its class
exists, gave `ARGS[Node]`. The call now rebuilds a trailing `ARGS[THIS]`
as `ARGS` of the class as well, so the copy equals the signature
`swapTHIS` would rewrite. A call without `this`, the copy `LoadSpaceHook`
takes of every declared signature, keeps the sentinel as before.

#### Rationale

The two ways of putting a class in place of `THIS` should agree on what
`THIS` is, a variadic tail included.

### A write through an alias of a method is refused as worktoy refuses writes

An `Alias` may stand for a plain function, and reads through it give the
bound method as the real name does. A write or a deletion through such an
alias called `__set__` or `__delete__` on the function, which has
neither, and failed with the builtin "'function' object has no attribute
'__set__'". The alias now asks the type of what it forwards to first, as
Python does, and refuses a write with `ReadOnlyError` and a deletion with
`ProtectedError`, both naming the alias, as in "Attempted to overwrite
read-only attribute 'Greeter.hello'". Both are `AttributeError`s, as the
builtin error was, and the method stays as it was. An alias of a
descriptor that takes writes and deletions forwards them as before.

#### Rationale

Python would let the write shadow the method on the instance, which an
alias, being a data descriptor, cannot mirror, so a refusal is the
answer; it should be the one worktoy gives for every other write it
cannot serve, naming the attribute, rather than an error about a
function's missing attribute.

### A dangling reference through THIS is named as it was written

`DanglingAlias` named the refused object by its `__field_name__`, which
an `Alias` has and a reference through `THIS` does not, so a misspelled
`THIS[Parent].y` was reported as "The name 'Parent.alias' stands for
'y'", naming an alias that exists nowhere. The message now names the
reference as it was written: "The reference 'THIS[Parent].y' names 'y',
which no class along the resolution order of 'Parent' holds." The message
for a dangling `Alias` is unchanged but for its last sentence, which
speaks of an alias alone now that a reference has its own.

#### Rationale

The refusal arrives at the very line that made the mistake, and should
name what that line wrote.

### An AttriBox builds its storage name once

An `AttriBox` keeps the field object of each instance in the instance
dict under a storage name such as `__x__attribox_field_object__`, and
used to build that name, by formatting the field name and lower-casing
the name of its own class, on every read and every write. Both parts are
fixed once the box is placed, so the box now builds the name at its first
use and keeps it. Placing a box drops what it kept, so a clone of a box
already read, placed at another name, builds a storage name of its own
instead of storing under the name of the field it was cloned from. The
storage names themselves are unchanged. Measured on Python 3.14, a read
went from 1.57 to 1.09 microseconds and a write from 3.32 to 2.83.

#### Rationale

`AttriBox` is the box every attribute of a project class uses by
default, so a cost on its read is paid everywhere. Keeping a value that
cannot change is the smallest way to remove it.

### An Alias standing for its own name is refused as its class is created

An `Alias` bound at the very name it stands for, as in `w = Alias('w')`
written for `w = Alias('width')`, found itself as the descriptor of that
name. An `Alias` is a descriptor the class reads as itself, so it passed
every check of `Alias.__set_name__`, and the first read forwarded to the
alias, which forwarded to itself again, until `RecursionError`. The same
happened to an alias bound in a subclass at the name of the field it
meant, since the subclass's own dict holds the alias first. Such an alias
now raises `DanglingAlias` as the class is created, with a message saying
that the alias stands for its own name and so would forward every access
to itself. An alias of another name is unchanged.

#### Rationale

`Alias` promises that the alias is held to what it stands for as the
class is created, and a one-letter slip met that promise with a
`RecursionError` at some later read. A cycle through two aliases still
recurses on its first read; only deliberate effort writes one, so it is
left alone.

### A FastBox installed with setattr is refused, as an AttriBox is

Python calls `__set_name__` only for the values of a class body, so a
`FastBox` set on a finished class with `setattr` never learned the key it
stores under. It stored under the key `None` of the instance dict
instead, which every box installed that way on the class shared: with
`Particle.mass = FastBox[float](1.0)` and
`Particle.label = FastBox[str]('electron')`, both `p.mass` and `p.label`
read `1.0`, and `p.label = 'proton'` made `p.mass` read `'proton'`. Such a
box is now refused at its first read, write and deletion with
`MissingVariable` naming the box and `__field_name__`, as an `AttriBox`
installed that way already was. A box declared in a class body is
unchanged, and its read is still one lookup in the instance dict: the
test runs only on a miss, a write and a deletion.

#### Rationale

`FastBox.__get__` says it works as `AttriBox.__get__`, and the shared
slot gave fields values of another field's type, the one thing a box
exists to prevent. Refusing the route the way `AttriBox` does keeps the
two boxes alike and costs a placed box nothing on the read it is made
for.

### FastBox takes one value, checked at the class-body line

`FastBox` handed the arguments in its parentheses to the constructor of
its field type at the first read, so `FastBox[int]('abc')` passed the
class body and failed only when an instance first read the field. The
parentheses now take one value, checked by `FastBox.__call__` at the
class-body line: a value of the field type is kept as it is, and any
other goes through `typeCast`, which converts only among the numbers and
among `str`, `bytes` and `bytearray`, without loss, or through a
`__cast_as__` of the field type, and otherwise raises `TypeCastException`
there. `FastBox[float](1)` holds `1.0`; `FastBox[int]('abc')` and
`FastBox[int](2.5)` raise. Every instance shares the value, so one that
cannot be hashed, such as a `list`, raises `TypeError`, as do several
arguments or a keyword. Empty parentheses give each instance
`fieldType()` at its first read, and the constructor's own exceptions now
pass through as they are instead of turning into `TypeException`; a
`FastBox` declared without parentheses is refused as the class is
created. A write
is checked as before, by `isinstance` alone.

### A class attribute no longer replaces a metaclass helper

`AbstractMetaclass` called its helpers `_notifySubclassHook` and
`_skipHash` through the class it had built, so a class body defining
either name answered in their place: a method named `_notifySubclassHook`
kept the `__subclasshook__` of every base from being asked, for that class
and its subclasses, and a `_skipHash` attribute broke `hash` of the class.
Both are now called through the metaclass.

### A word is in a SymbolicName ignoring case

A `SymbolicName` ignores case for equality and hashing, so
`SymbolicName('Font', 'Size') == SymbolicName('font', 'size')`, but `in`
compared the words as written: `'Font' in SymbolicName('font', 'size')`
was False. `in` now ignores case as well, and anything but a `str` is in
no name.

### ARGS without a type is a tail of any type, with or without the star

`@overload(int, *ARGS)` now declares an `int` followed by any number of
arguments of any type, as `@overload(int, *ARGS[object])` does; it used
to fail with `Value after * must be an iterable`. A bare `ARGS`, written
without the star, means the same. It used to be accepted as a signature
whose last entry is the class `ARGS`, which no call could match, so
`@overload(int, ARGS)` failed only at the first call, with a
`DispatchException` listing `<TypeSig: [int, ARGS]>`. `overload` and
`overload.flex` read every bare `ARGS` as `*ARGS` through the new
`TypeSig.starARGS`, so `flex` refuses it with `TypeException`, as it
refuses `*ARGS`.

### The field object of an AttriBox is an instance of its field type

At the first read an `AttriBox` calls the constructor of its field type on
the arguments in its parentheses and keeps what it returns as the field
object. A constructor returning something else, such as a `__new__` that
returns another object or forgets to return at all, was kept without a
check: a foreign object with a `__dict__` sat in the field, and one
without failed in the tagging with an `AttributeError`, which `hasattr`
read as the field being absent. Such a field object now raises
`TypeException` naming the field, the object and the field type, at the
read, as `FastBox` and an assignment already did. A constructor returning
an instance of a subclass passes.

### An overload is bound once per class body

Binding an `overload` a second time in the class body that declared it,
as in `__radd__ = __add__`, gave the second name a copy of the overloads
of the first, but the copy counted the overloads the class inherits as
its own. The dispatcher tries a subclass's overloads before inherited
ones by exact type and through `isinstance`, and inherited ones first
through a cast, so the two names could call different functions: with
`@overload(complex)` declared beside an inherited `@overload(float)`,
`z + 1` reached the inherited function and `1 + z` the subclass's. A
second binding of one `overload` object in one class body, under another
name or the same one, now raises `ReboundOverload`, a `SyntaxError` new
in `worktoy.waitaminute.meta`, at its line. The second name takes a
method of its own, which may call the first, as in `def __radd__(self,
other): return self.__add__(other)`. Another class body may still bind
the same `overload` object.

### A sentinel as the field type of a box is refused

`AttriBox[THIS]()`, a natural attempt at a field holding an instance of
the enclosing class, was accepted as the class was created and failed at
the first read, when the box called `THIS()`, with `Expected object at
name 'next' to be an instance of 'THIS', but received object: '()' of
type 'tuple'!`. A sentinel stands for a meaning, such as the enclosing
class, and is no type of value a field could hold. `AttriBox`, the boxes
based on it, and `FastBox` now refuse a sentinel, any class built by
`SentinelMeta`, `ARGS` included, at the subscript itself: `AttriBox[THIS]`
raises a `TypeError` naming the subscript, before any class body binds
it.

### An overloaded method takes a keyword named 'instance'

The function an overloaded method compiles to named its first parameter
`instance`, and the wrapper of an `overload.flex` registration named its
first one `func`, so a call passing a keyword of either name, such as
`Serializer(data, instance=obj)`, failed with `got multiple values for
argument`, naming the method as if its own signature were at fault, while
a plain method with the same signature accepted it. Both now take those
arguments from their positional arguments without naming them, as
`functools.partial` and `functools.singledispatchmethod` do, so every
keyword passes through to the function the call selects. Called through
the class with no arguments, the compiled function refuses as before,
now naming `self` as the function of a plain method does. The `invoke`
methods of `CallMeMaybe`, `Permuter` and `PermuterMethod` take the
function, and the instance, by position only.

### A descriptor is placed on one class

One box object bound in the bodies of two classes, as `shared =
AttriBox[Point]()` followed by `p = shared` in `A` and in `B`, served
both: the second class took the box over, and the values the box built
for the instances of `A` named `B` as their owner in their tags. A
descriptor based on `BaseDescriptor`, such as an `AttriBox`, a `FixBox`
or a `Field`, placed on a second class, at the same name or another, is
now refused with `SharedDescriptor`, a `SyntaxError` new in
`worktoy.waitaminute.desc`, as that class is created (wrapped in a
`RuntimeError` on Python 3.7 through 3.11, as anything raised from
`__set_name__`). A field meant for several classes is declared in a common
base, or each class takes a descriptor of its own. Bound to
a second name in the same class body, every such descriptor places a
clone of itself, made by its `clone`, at that name, as a box already did;
`BaseDescriptor.__set_name__` now decides both cases. A `Field` bound to
two names used to be one object recording the second name, so its
messages named the wrong attribute.

### A renamed class keeps its place in a dict

The default hash of a class built by a metaclass based on
`AbstractMetaclass`, made from the names of the class, its bases and its
metaclass, was computed afresh at every hash. A class renamed after it
was hashed, as a factory names the class it built, then hashed by its new
name, and a dict or set holding it, such as a registry filled in
`__init_subclass__`, no longer found it. The default is now computed at
the first hash and kept in the class's own `__dict__` under
`__class_hash_value__`, so a class keeps its hash for life, as a plain
class does. The values are those of before, a class defining
`__class_hash__` is asked at every hash as before, and a subclass
computes its own. Hashing a class, which an overloaded call does for
every argument class on its exact-type pass, now costs less than a
quarter of what it did.

### A subclass overload wins every call it accepts

An overload a subclass declares beside inherited ones now takes every
call it accepts, by exact type or through `isinstance`, before any
inherited overload is tried. An inherited signature matching a call
exactly used to keep it, so with `@overload(int)` inherited and
`@overload(object)` declared in the subclass, `f(1)` reached the parent
while `f(True)` reached the subclass. Both now reach the subclass, and
the inherited overload keeps the calls the subclass does not accept. The
cast passes still try the inherited signatures first, so a signature a
subclass adds never takes a call its parent handles through a cast.

### The latest subclass variadic takes a call its parent declares

A variadic signature of a subclass that accepts a call a parent declares
explicitly, such as `ARGS[int]` beside the parent's `(int, int)`, takes
that call, so the subclass implementation wins. With two such variadics
in the subclass, `ARGS[int]` and `(int, ARGS[int])`, the parent's call
went to the one declared first, while every other call the two share
went to the most recent, as documented. The most recent declaration of
the nearest class now takes the parent's call as well: with
`(int, ARGS[int])` declared last, `f(69, 420)` reaches it, by exact type
and through `isinstance` alike.

### A private callback is found

Notification callbacks and `Field` accessors are recorded by name and
looked up on the class of the instance at each access. A callback written
with two leading underscores, such as `def __audit` decorated with
`@balance.onSet` in `Account`, was recorded as `__audit` while the class
body stores it as `_Account__audit`: the class was created, and the first
access failed with `AttributeError`, or, on an owner defining
`__getattr__`, silently read that method's answer in place of the field.
The decorators now record a private name as the class body stores it,
taking the class from the callback's `__qualname__`; like any private
name it is not overridden by a subclass. A private function whose
qualified name names no class, such as one made inside another function,
is refused with `NamelessCallback`.

### Two names bound to one box are two fields

`width = height = AttriBox[int](0)` binds one box to two names, and the
box took the last name for both, so the two attributes read and wrote one
storage slot: assigning `width` changed `height`. The box now keeps the
first name, and the second name receives a clone of it as the class is
created, carrying the field type, the captured default and the callbacks
registered on the box by then. `FixBox` and the other boxes based on
`AttriBox` follow, and so does `FastBox`, which gains a `clone` method
for it.

### A base listed after an Object class is initialized

`Object.__init__` called `object.__init__` directly, so the chain of
`__init__` calls stopped at `Object`: a base listed after a worktoy
class, as in `class Worker(BaseObject, threading.Thread)`, never had its
`__init__` run, and the object failed later, at its first use
(`RuntimeError: thread.__init__() not called`). `Object.__init__` now
records its arguments and then calls the next `__init__` along the
resolution order without them, so `threading.Thread`, `logging.Handler`
and cooperative mixins listed after a worktoy class are initialized as
in a plain class. A base whose `__init__` requires arguments, listed
after a worktoy class, now refuses at construction with its own
`TypeError` instead of being skipped; listed before it, it receives its
arguments as before.

### A box refuses an owner without an instance dict as the class is created

`AttriBox`, every box based on it (`FixBox`, `KeeBox`, `Kee`), and
`FastBox` keep the value of a field in the instance dict. Placed on a
class declaring `__slots__` without `__dict__`, `AttriBox` refused only
at the first access, and `FastBox` failed there with the bare
`AttributeError` of the missing `__dict__`, so `hasattr` answered `False`
as if the field were absent. Both now raise `MissingInstanceDict` from
`__set_name__`, as the class is created (wrapped in `RuntimeError` on
Python 3.7 through 3.11, as every `__set_name__` exception is), and a box
installed on such a class with `setattr` afterwards is refused with the
same exception at every access.

### A metaclass mixed in beside BaseMeta takes part

`AbstractMetaclass` called `MetaType` by name in `__new__`, in
`__init__` and in the defaults that apply when a class declares no hook,
those of `__call__`, `__instancecheck__`, `__subclasscheck__`, `__str__`,
`__repr__`, `__setattr__` and `__delattr__`. A metaclass of a project's
own, based on `MetaType` and mixed in beside `BaseMeta` as in
`class Meta(BaseMeta, OtherMeta)`, sits between `AbstractMetaclass` and
`MetaType` in the resolution order, and none of its versions of those
methods ever ran. They now hand over with `super()`, so they run in the
order of the metaclass resolution order, while a class hook still takes
its operation first. In the metaclasses of the library the next class
after `AbstractMetaclass` is `MetaType`, so nothing changes for them.

### Plain lookups read past the attribute hooks of a class

Where the library needs the ordinary attribute lookup on a class or on an
object it does not own, it now reads with `type.__getattribute__` or
`object.__getattribute__` instead of `getattr`, so no `__getattr__`,
`__class_getattr__` or reimplemented `__getattribute__` can answer in
its place. This covers:

- the `__no_box_tag__` opt-out `AttriBox` reads before tagging an object
  it built: a class whose hooks answered every name used to opt out of
  the tags without asking to, and its objects lost the link to the box
  that built them;
- the notification and `setName` callbacks of a descriptor, and the
  accessors of a `Field`, found by name on the class of the instance;
- the `__skip_hash__` flag the default class hash reads off each base,
  and the `__namespace__` that `getMROSpace` collects from the classes
  along the resolution order;
- the marker `isFlex` reads.

A name the class does not hold now raises the plain `AttributeError` of
the lookup there, rather than whatever a hook answers for it.

### A variadic signature declared twice in one class body is refused

`BaseSpace.addVariadic` recorded every variadic declaration, and
collecting them for the `Dispatcher` kept the first of two equal
signatures, so a second `@overload(ARGS[int])` under one name in one
class body was dropped without a word, although the docstrings said the
most recent declaration wins. A second equal variadic signature bound to
a different function now raises `DuplicateSignature` at its line, as an
equal concrete signature always did; the same function bound again
changes nothing. Different variadic signatures that overlap, such as
`ARGS[int]` and `(int, ARGS[int])`, remain no conflict, and the most
recent declaration of the nearest class takes a call both accept. A
subclass may still redeclare a variadic signature it inherits.

### A BaseObject subclass without an initializer refuses constructor arguments

`Object.__init__` records whatever arguments it receives, which a
descriptor needs for its deferred default, so a `BaseObject` subclass
that defined no `__init__` of its own accepted any arguments and dropped
them: `Point(3, 4)` built a point at its defaults without a word.
`BaseObject.__init__` now raises the `TypeError` Python raises for a
plain class without an initializer, `Point() takes no arguments`, when
the class defines neither `__init__` nor `__new__` below `BaseObject`.
A subclass whose `__init__` hands its arguments on to `super().__init__`
still has them recorded, an overloaded initializer receives its
arguments as before, and `Object` and the descriptors built on it are
unchanged.

### An overloaded method carries the docstring of its function

The compiled dispatch a class exposes for an overloaded name carries the
docstring of the first registered function, else of the first variadic
one, else of the fallback, and the module of its owner, so `help` and
the documentation tools see what the author wrote; it used to carry only
its name and qualified name. A flexible declaration, `@overload.flex`,
registers a `PermuterMethod` around the function, and the dispatch read
the docstring of that wrapper's class whenever the flexible declaration
came first; it now reads the function the wrapper holds.

### A sentinel other than THIS is refused in an overload signature

`TypeSig.validateTypes` refused `OWNER` by name and accepted every other
sentinel class, so `@overload(DESC)` registered a signature nothing
could ever match, a sentinel class having no instances. `THIS` is now
handled first and passes, alone or inside a trailing `ARGS`, since
placement swaps it for the class; every other `Sentinel` subclass,
`OWNER`, `DESC`, `DELETED`, `METACALL` and `Sentinel` itself, is refused
with `TypeError` naming its position and the sentinel, at the decorator.

### Every exception shares a common base, WorkToyException

Every exception of `worktoy.waitaminute`, the control-flow signals
aside, subclasses `WorkToyException` ahead of the builtin it is based
on, so `except WorkToyException` catches every exception of the library
at once while `except TypeError`, `except AttributeError` and the other
builtin clauses keep working as before. The base adds nothing else: it
declares empty slots so that it stands beside `SyntaxError`, whose
layout is wider than that of `Exception`, and it carries no pickling or
copy support.

### A deleted plain name may be overloaded, through a deletion phase for the hooks

`LoadSpaceHook` records every plain binding of the class body so that
one body does not give a name both a plain definition and overloads,
and it kept that record past a deletion: `f = 1`, `del f`,
`@overload(int) def f` raised `OverloadConflict` although no plain
binding survived. The namespace hooks gained a deletion phase,
`delItemPhase(key, value)`, run by `AbstractNamespace.__delitem__` with
the name and the value being removed before the namespace removes it; a
hook returning `True` claims the deletion and the name stays. In that
phase `LoadSpaceHook` forgets the plain name, so the sequence above
builds and dispatches. A deleted overloaded name is still refused with
`ClaimedName` as the class is created.

### A routed class hook is a classmethod and nothing else

`NamespaceHook` used to refuse a plain function or a `staticmethod` at
a routed `__class_*__` hook name with `UnboundClassHook`, and let
anything else through. An `@overload` there passed, became a
`Dispatcher` at compile time, and broke the operation at the first
call: `len(Y)` on a class whose body overloaded `__class_len__` raised
a `TypeError` about a missing instance. The rule is now the one the
documentation stated: a hook is a classmethod, and anything else at a
hook name, in the class body or supplied by a plain base, is refused
at the class-body line. The `METACALL` sentinel, which means the
metaclass's own implementation, passes, and so does a classmethod bound
again under a second hook name.

### A boxed value answers for its context through the box that made it

An `AttriBox` tags every object it creates with `__field_box__`,
`__field_name__` and `__field_owner__`, naming the box. An `Object` uses
the latter two names for its own placement record, and
`Object.getContextInstance` told "a value no class holds" from "a placed
descriptor read outside a frame" by `__field_name__` alone, so a boxed
value that is an `Object`, a `BaseObject`, a
`SymbolicName`, any descriptor, was taken for a placed descriptor:
`hasattr(value, 'instance')` raised `WithoutException` instead of
answering, and so did `inspect.getmembers` and anything else that walks
attributes.

A boxed value now answers `instance` and `owner` through the box that
made it. While that box has a frame, during the read that built or
fetched the value, `value.instance` is the instance read from and
`value.owner` the owner class, which an `onGet` callback can use.
Outside any frame the value is an ordinary object holding no context:
it raises `AttributeError`, `hasattr` answers `False`, and `inspect`
walks it. A placed descriptor read outside a frame still raises
`WithoutException`, and a value no box made is as it was.

### A subclass expands on an inherited descriptor through THIS

A class body may add notifiers to a descriptor it inherits by decorating
it through `THIS`, naming the base that holds the descriptor:

    class Child(Parent):

      @THIS[Parent].x.onGet
      def _onGetX(self, value) -> None:
        ...

`THIS[Parent].x` refers to the descriptor `x` that `Parent` holds, as the
class being built will hold it. Reading it takes a clone of `Parent.x`,
which derives the same storage name and so shares the field with the
parent's descriptor as a redeclared field does. The role decorators of
the reference, `preGet`, `onGet`, `preSet`, `onSet`, `preDelete`,
`onDelete` and `setName`, apply to that clone and hand the function back
as the descriptor's own decorators do, so the roles stack. `Parent`
receives an `__init_subclass__` that places the clone on the subclass as
it is created and names it there; `Parent.x` is never touched. Every
parent named takes a hook of its own, beside one a base of it holds, and
a hook hands over to the next along the resolution order as it runs, so
the parents may be named in any order across class bodies.
`THIS[GrandParent].x` is `THIS[Parent].x` for an `x` that `Parent`
inherits from `GrandParent`: one reference with one clone, named once.
Naming the
base is also what lets a static checker resolve the reference to
`Parent.x`, so a misspelled name is flagged and the roles complete. A
name `Parent` does not hold is refused at the line with `DanglingAlias`.
`BaseDescriptor` gained the `clone` that makes the copy, carrying the
captured arguments, the field type of a box and every registered
callback name, and no owner.

Decorating `Parent.x` directly from a subclass body still registers on
the parent's descriptor, which is what that line says.

A decorator may hold a subscript only from Python 3.9 on (PEP 614). On
3.7 and 3.8 the same decoration is written as a call after the method:

    class Child(Parent):

      def _onGetX(self, value) -> None:
        ...

      _onGetX = THIS[Parent].x.onGet(_onGetX)

Like the decorator, the call is written only inside the body of a
subclass of `Parent`. No other subclass of `Parent` may be created
before that body ends: the clone goes to the next subclass of `Parent`
created, so a subclass of `Parent` nested in the body would
take it and leave the enclosing class without the decoration. `worktoy`
is designed around custom metaclasses rather than nested classes; a
nested class may work, but edge cases such as this one are not
supported, as the package docstring now says.

`AttriBox.__get__` declares, as `BaseDescriptor` already did, that class
access gives the box itself, which the static resolution rests on.

### Alias forwards every access and keeps nothing

An `Alias` is a second name for a descriptor of its class or of a base:
`width = AttriBox[int](240)` beside `w = Alias('width')`. Through an
instance the alias now forwards each read, write and deletion to the
descriptor the real name holds on the class of that instance, found
afresh at every access as the first class dict along the resolution
order holds it, with no `__get__` run on it; the alias then runs that
protocol once itself. So `g.w` is the very object `g.width` gives, and
a subclass that redeclares the field is served by its own box whichever
name is read first. Read from the class, the alias is itself.

The alias used to replace itself on the class with the target object as
the class was created, whenever the target already resolved, and forward
only otherwise. A subclass redeclaring the field then kept reaching the
parent's box through the alias, and since both boxes store under the one
name the field derives, the first name read on a fresh subclass instance
decided what both names held afterwards. That swap is gone, and with it
the hand-written scan of the class dicts, the fallback to a name only
the metaclass supplies, and the three rules for a target holding a plain
value. A real name holding something that is not a descriptor is refused
with the new `NotADescriptor`, a `TypeError` naming the alias and the
value, since there is no protocol to forward to; a plain value takes a
second name by assignment. A value counts as a descriptor when its type
defines `__get__`, as for Python itself, so a proxy that answers
`__get__` only through `__getattr__` is refused too. As the class is
created the alias is held to
what it stands for, with two new refusals: a name no class along the
resolution order holds raises `DanglingAlias`, and a name holding a plain
value raises `NotADescriptor`. Both refusals come again from an access
should the name be removed or replaced on the class afterwards. A plain
function, a `staticmethod`, a `classmethod` and an overloaded method may
be aliased, and an instance reads through the alias what it reads through
the real name, so `__radd__ = Alias('__add__')` follows the overloads a
subclass adds to `__add__`. Two things change for a
user: read from the class, an alias is no longer the box it stands for,
and an alias follows the name it stands for in the class body or in a
base, since an alias of a name a subclass supplies later is refused.

#### Rationale

A second name should mean what the first name means, found the way the
first name is found, every time. The copy taken at class creation was a
shortcut that broke under redeclaration, and the rules kept around it
served cases an alias is not for.

### Keyword arguments pass through overload dispatch

An overloaded call is dispatched on the types of its positional
arguments alone. Its keyword arguments play no part in choosing the
overload and pass through unchanged to the function the positional
types select. A call with no positional arguments selects the empty
signature, `@overload()`, so a class that takes keywords declares that
overload and handles them there, forwarding from its other overloads
with `if kwargs: self.__init__(**kwargs)`, as the samplers of
`work_test` have always done. A keyword the selected function does not
take is refused by that function with Python's own `TypeError`, which
names it. A call no signature accepts still goes to the fallback, else
`DispatchException`, which still lists the keywords received.

The dispatcher used to bind keywords to the parameter names of every
registration, so that `Point(x=69, y=420)` reached `@overload(int, int)`
declared on `(self, x, y)` without an empty signature. That binding
needed rules of its own: which keyword fills which name, how a keyword
beyond the signature is absorbed by a later parameter or `**kwargs`,
how a `flex` registration binds its canonical names, why a variadic one
binds none, and a second set of three matching tiers over the bound
values. The list it bound against held one entry per function, so a
function stacked under several signatures was reachable by keyword
through its first signature only. All of it is gone. What a project
loses is the keyword form of a positional overload without a handler
for it: `Point(x=69, y=420)` now needs `@overload()` on `Point`, or is
refused, and `Point(69, y=420)` dispatches on `(int,)`, not on
`(int, int)`.

#### Rationale

One lenient acceptance, that a keyword call should still find a
positional overload, had grown a binder with its own rule set, each
rule with an edge, and the first bug found in it needed one more
condition. The plain rule needs none, and the forwarding pattern it
rests on was already how the library's own constructors took keywords.

### AttriBox declarations are settled when the class is created

Several ways of writing an `AttriBox` declaration used to be accepted in
silence and then misbehave later, or never behave at all. Each is now
settled at the declaration itself, which is where the offending line
actually sits.

A subscript naming something other than a plain type, such as
`AttriBox[list[int]]` or `AttriBox[T]`, is handed to the generic
machinery and comes back as a type alias rather than a box. An alias
carries none of the descriptor protocol, so the attribute quietly
answered with the alias object on every read. Such a declaration now
raises `PhantomBoxError` while the class is being built. The subscript
on its own remains legal, because `class Sub(AttriBox[T])` asks for
exactly that alias and a base-class entry is not a namespace value. What
is refused is the alias landing in a class body as an attribute.

A box that never captured a field type, written `AttriBox()`, has nothing
to build from and no later chance to learn a field type, since the
subscript is the only place one is ever assigned. It now raises
`MissingVariable` as the class is created, rather than at the first read
of the attribute. Calling one of the aliases above refuses with
`PhantomBoxError` at the call; see "A box alias called with parentheses
raises PhantomBoxError" above.

A subscript written without its trailing call, `bar = AttriBox[int]`, is
refused with a `TypeError` naming the field as the class is created, as
is the same declaration of a `FixBox` or a `FastBox`. Empty parentheses,
`bar = AttriBox[int]()`, give the box no arguments. The parentheses of an
`AttriBox` reach the `__init__` of the class of the box, so a subclass of
`AttriBox` takes options of its own there, and one whose `__init__` does
not hand on to `AttriBox.__init__` is refused the same way.

A box installed on a finished class through `setattr` never reaches
`__set_name__`, so both refusals above are repeated on read for that
route.

#### Rationale

A malformed declaration used to surface as a puzzling value or an
exception raised several frames inside the descriptor machinery, at
whatever unrelated line happened to read the attribute first. The class
body that caused it could be in another file entirely. Refusing at class
creation names the attribute, the owning class and the subscript as
written, and does so before any instance exists.

The three spellings are refused alike. A subscript the box declines to
claim, or no subscript at all, leaves no field type and therefore
nothing to construct. A missing pair of parentheses leaves the box
without the call that hands its arguments to the class of the box, so a
box is written the one way, with parentheses, empty for no arguments.

### New exception: PhantomBoxError

`PhantomBoxError` is added to `worktoy.waitaminute.desc` and raised when
a class-body subscript produced a type alias in place of a box. Its
message reports the attribute name, the owning class, and the subscript
as it was written, along with the completed form the declaration wanted.

It subclasses `DescriptorException` and deliberately does not subclass
`AttributeError`. A declaration error that presented as an
`AttributeError` would be swallowed by `hasattr` and by `getattr` with a
default, turning a broken class body into a silently absent attribute.

`AccessError`, `ProtectedError`, `ReadOnlyError` and `PhantomBoxError`
now share the `DescriptorException` base, so a single
`except DescriptorException` still catches all of them.

### Object reports inconsistent state instead of failing obscurely

`Object` now checks the invariants its accessors depend on and reports
the missing piece by name. `getContextInstance` and `getContextOwner`
refuse an absent context stack, which a subclass can produce by
overriding the public `hasContext` in a way that disagrees with the
stack it summarises. `getPrivateName` reports a missing field name
rather than building an attribute name out of `None`, which is reachable
whenever a descriptor is used without having gone through a class body.
The deleted-value guard likewise reports a missing field name rather
than naming the deleted attribute `None`.

### Box storage names are the field name as written

A box stores the value of a field on each instance under a name derived
from the field name. That name used to be the snake-cased private name
of the field, so `fooBar` and `foo_bar`, or `X` and `x`, derived one
storage name and shared one slot; such a pair was refused with
`StorageCollision` as the class was created, and a subclass redeclaring a
field its parent exposed under a second name through `Alias` was refused
by the same guard, wrongly, since the guard met the parent's box under the
alias name and compared it with itself.

The storage name now takes the field name as written, wrapped in double
underscores and followed by the lower-case name of the box class and
`_field_object__`: an `AttriBox` named `fooBar` stores at
`__fooBar__attribox_field_object__`. Two different field names can never
derive one storage name, so two near names are two fields with two slots,
as plain Python has them, the guard is gone, and `StorageCollision` with
it. An instance pickled by an earlier release holds its values under the
old storage names; loaded under this one, those fields rebuild their
defaults on the first read.

### The testing support no longer depends on lorem_ipsum

`worktoy.work_test` drew its random text from `worktoy.lorem_ipsum`: the
word and symbolic-name samplers from `StochasticWord`, the lorem sampler
from a `Sentence` of its own, and `BaseTest` exposed both generators as
`stochWord` and `loremSentence`. The samplers now draw from a small
vocabulary of their own, `LOREM_WORDS` in `worktoy.work_test.samplers`,
through `randomWord` and `loremSentence`, which builds a sentence of
exactly the requested number of characters. `LoremSampler.charCount` is a
plain per-sampler setting, forty by default, refusing a count below one;
the `sentence` attribute is gone, and so are `BaseTest.stochWord` and
`BaseTest.loremSentence`. `work_test` therefore depends on the central
packages alone, which a test pins by reading the import statements of
every module in the package.

## [1.0.0] - 2026 May 29

First stable release. The public API is frozen for the 1.0 series.

### Relicensed from AGPL-3.0 to Apache-2.0

worktoy is now distributed under the Apache License 2.0, replacing the
AGPL-3.0 license used throughout the pre-1.0 development series.

#### Rationale

AGPL-3.0 was originally chosen for one reason: to stop a large company
from folding worktoy into a closed-source product. The clearest version
of that worry is training data, and AGPL was meant to make such use a
copyleft violation rather than a free lunch.

In practice it changed nothing about that threat. Long-removed, renamed
internals of worktoy (for example the abandoned `monoSpace` feature)
already surface in the pre-knowledge of commercial language models,
which means the source was ingested into training weights regardless of
the license. If copying source into training data and model weights is
not treated as derivation, then the one outcome AGPL was chosen to
prevent is simply not prevented.

So the restrictive license bought nothing against the actor it was aimed
at, while it did deter the honest ones: many organizations refuse AGPL
dependencies outright as a matter of policy. A lock that only stops the
law-abiding and waves the scrapers through is not worth keeping.

Apache-2.0 keeps worktoy freely usable, adds an explicit patent grant,
and has clearer terms than a bare permissive license such as MIT.

#### Scope

The `LICENSE` file now holds the canonical Apache-2.0 text. The per-file
license headers, the `pyproject.toml` classifier, the README badge and
license section, and the Code of Conduct were all updated to match.
Copyright remains with Asger Jon Vistisen; only the license terms
changed.

The relicense first shipped in 1.0.0-rc7. Earlier candidates, up to and
including 1.0.0-rc6, remain available under AGPL-3.0; every release from
1.0.0-rc7 onward is Apache-2.0.
