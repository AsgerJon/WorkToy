# worktoy manual: utilities

`worktoy.utilities` is the toolbox the rest of worktoy is built with: a
converter, a few text helpers, and some odd jobs. They are yours to use
as well. This chapter shows what each one is for and how it behaves.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Three things hold throughout:

- Every helper imports from `worktoy.utilities`, and the three
  combinatorial ones from `worktoy.utilities.combinatorics`.
- The names are camelCase. That is worktoy's house style everywhere,
  not a slip.
- The exceptions come from `worktoy.waitaminute`, worktoy's package of
  exceptions, and each one is also the builtin you would expect: a
  `TypeCastException` or a `TypeException` is a `TypeError`, an
  `UnpackException` is a `ValueError`, and `MissingVariable`,
  `ReadOnlyError` and `ProtectedError` are `AttributeError`s. Your
  existing `except` clauses keep catching them. Each carries the facts
  of the refusal as attributes, so there is never a message to parse,
  and the wording of the messages may change in any release.

Contents:

1. Converting values: `typeCast` and `__cast_as__`
2. Will `typeCast` decide? `hasCastRule`
3. Writing messages: `textFmt`, `joinWords`, `wordWrap`
4. Splitting and replacing text: `stringList`, `replaceFlex`
5. Fallbacks and loose arguments: `maybe`, `unpack`
6. Read-only attributes: `QuickDesc`, `Directory`
7. Recording what a block raised: `ExceptionInfo`
8. Slices: `sliceLen`, `ValidSlice`
9. Classes and functions: `resolveMRO`, `argsCount`
10. Combinatorics: `bipartiteMatching`, `indexPermutations`,
    `Arrangement`, `Arrangements`


## 1. Converting values: `typeCast` and `__cast_as__`

`typeCast(target, value)` gives you `value` as a `target`, or refuses.
It is the conversion every part of worktoy uses, and its rules are
narrow on purpose: it never guesses, it never parses, and it never
loses information.

A value that already is a `target` comes back untouched:

```
>>> from worktoy.utilities import typeCast
>>> typeCast(int, 7)
7
>>> typeCast(int, True)
True

```

`True` comes back as `True` because in Python a `bool` is an `int`.

Numbers convert among `bool`, `int`, `float` and `complex` when nothing
is lost:

```
>>> typeCast(int, 3.0)
3
>>> typeCast(float, 3)
3.0
>>> typeCast(complex, 1.5)
(1.5+0j)
>>> typeCast(bool, 1)
True

```

And they are refused when something would be:

```
>>> from worktoy.waitaminute.dispatch import TypeCastException
>>> for target, value in [(int, 3.5), (bool, 2), (float, 2 ** 53 + 1)]:
...   try:
...     typeCast(target, value)
...   except TypeCastException as refusal:
...     print(refusal.type_.__name__, 'refused', refusal.arg)
int refused 3.5
bool refused 2
float refused 9007199254740993

```

`3.5` is no whole number. Only `0` and `1` are booleans, so `2` is
refused: `typeCast` is not a truth test. And a `float` holds every
whole number exactly only up to `2 ** 53`, so `2 ** 53 + 1` would come
back as a different number. That last refusal depends on the value,
not the type: the same cast that works for `2 ** 53` refuses
`2 ** 53 + 1`.

Text converts among `str`, `bytes` and `bytearray`, always as UTF-8:

```
>>> typeCast(str, b'hello')
'hello'
>>> typeCast(bytes, 'hi')
b'hi'

```

Bytes in another encoding are for you to decode first.

Three things `typeCast` never does:

```
>>> from decimal import Decimal
>>> for target, value in [(int, '3'), (str, 5), (int, Decimal(3))]:
...   try:
...     typeCast(target, value)
...   except TypeCastException:
...     print('refused:', repr(value))
refused: '3'
refused: 5
refused: Decimal('3')

```

- It never parses a string. Reading `'3'` as a number is a decision
  about format (is `'3,5'` three and a half? is `'0x3'` hex?) that
  belongs to your code. When you mean it, call `int('3')` yourself.
- It never turns anything into text. `str(x)` works on every object
  there is, so a cast to text through it would accept everything.
- It converts no number outside the four builtins: `Decimal` and
  `Fraction` belong to neither family.

### Teaching your own class to convert

A class of your own converts through a classmethod named
`__cast_as__`. Read the name as "cast this value as me": it receives
the value and returns an instance of the class, or `NotImplemented` to
refuse.

```
>>> class Count(int):
...   @classmethod
...   def __cast_as__(cls, value):
...     return cls(typeCast(int, value))
>>> count = typeCast(Count, 3.0)
>>> count, type(count).__name__
(3, 'Count')
>>> class Even(int):
...   @classmethod
...   def __cast_as__(cls, value):
...     if isinstance(value, int) and not value % 2:
...       return cls(value)
...     return NotImplemented
>>> typeCast(Even, 4)
4
>>> try:
...   typeCast(Even, 5)
... except TypeCastException:
...   print('refused 5')
refused 5

```

The hook must be a classmethod, since `typeCast` calls it on the class
to make an instance, and a subclass looking it up then builds itself.
A `__cast_as__` without `@classmethod` raises `UnboundCastHook` at the
first cast. Whatever the hook returns must be an instance of the
class; anything else is refused.

A subclass of a builtin converts nothing until it has a hook. That is
deliberate: `typeCast` cannot know what your constructor does, so it
will not call `Meters(3.0)` behind your back.

```
>>> class Meters(float):
...   pass
>>> try:
...   typeCast(Meters, 3.0)
... except TypeCastException:
...   print('Meters needs a __cast_as__')
Meters needs a __cast_as__

```

One more rule, for class families: when the target has a hook and the
value is an instance of a subclass of the target, the hook is asked
anyway, so the target gets an instance of its own class back.

```
>>> class Celsius(float):
...   @classmethod
...   def __cast_as__(cls, value):
...     return cls(typeCast(float, value))
>>> class Precise(Celsius):
...   pass
>>> type(typeCast(Celsius, Precise(20.0))).__name__
'Celsius'

```

There is no registry for types you do not own, such as `datetime` or
`Path`: a class without a hook converts only its own instances. The
boxes and the overloads of worktoy convert through `typeCast`; their
chapters say how.


## 2. Will `typeCast` decide? `hasCastRule`

`hasCastRule(target)` tells your code whether `typeCast` owns the
conversion to `target`. It is True for the number and text builtins,
for every subclass of one, and for every class with a `__cast_as__`:

```
>>> from worktoy.utilities import hasCastRule
>>> hasCastRule(float), hasCastRule(Meters), hasCastRule(Count)
(True, True, True)
>>> hasCastRule(list)
False

```

True does not mean the cast will succeed. It means `typeCast` has the
final say, so your code should ask it and not call the class itself.
False means `typeCast` merely passes the class's own instances
through, and your code is free to convert by calling the class, as
`list((1, 2))` does. `Meters` answers True precisely so that nothing
builds a `Meters` by calling it. A `__cast_as__` without
`@classmethod` raises `UnboundCastHook` here too, rather than answer
False, since the class is broken, not ruleless.


## 3. Writing messages: `textFmt`, `joinWords`, `wordWrap`

### `textFmt`

A long message reads best in the source as an indented triple-quoted
string, and badly when printed that way. `textFmt` turns it into one
clean line:

```
>>> from worktoy.utilities import textFmt
>>> message = """Expected a positive width,
...     but received a negative one."""
>>> textFmt(message)
'Expected a positive width, but received a negative one.'

```

Every run of whitespace becomes one space. Where you want a line break,
write `<br>`, and for an indent, `<tab>`, which is two spaces:

```
>>> print(textFmt('Problems found:<br><tab>width is negative'))
Problems found:
  width is negative

```

`textFmt` fills in no placeholders. Format first, then tidy, or pass
several arguments, which are joined by spaces:

```
>>> textFmt('Received', 3, 'items')
'Received 3 items'

```

A line break is `os.linesep`, so `\r\n` on Windows. Pass
`newLineSymbol='\n'` to always get `\n`. If your text really contains
`<br>`, as HTML does, choose another token with `newLineToken`, and
likewise `tabToken` and `indentSymbol` for the indent.

### `joinWords`

`joinWords` writes a list the way a person does:

```
>>> from worktoy.utilities import joinWords
>>> joinWords('red', 'green', 'blue')
'red, green and blue'
>>> joinWords('tea', 'coffee', sep='or')
'tea or coffee'
>>> joinWords('Tom', ['Dick', 'Harry'])
'Tom, Dick and Harry'

```

`sep` is the word before the last one, not the separator between all
of them. Lists and tuples among the words are flattened, a string is
always one word, and no words at all give `''`. It writes no comma
before the last word.

### `wordWrap`

`wordWrap(width, *text)` reflows text into lines of at most `width`
characters. The width comes first. It returns one string with the
lines joined by `os.linesep`; split it if you want a list:

```
>>> from worktoy.utilities import wordWrap
>>> print(wordWrap(12, 'lorem ipsum dolor sit amet'))
lorem ipsum
dolor sit
amet
>>> print(wordWrap(20, 'first half <br> second half'))
first half
second half

```

A `<br>` in any case forces a break, or pass another token as
`newLine`. The line breaks already in the text are whitespace like any
other and get reflowed. A word longer than the width gets a line of
its own, unbroken. A width that is no `int`, or a piece of text that is
no `str`, raises `TypeException`, and a width below one raises
`ValueError`.


## 4. Splitting and replacing text: `stringList`, `replaceFlex`

### `stringList`

`stringList` splits strings into a clean list: every piece stripped,
the empty ones dropped.

```
>>> from worktoy.utilities import stringList
>>> stringList('a, b, c')
['a', 'b', 'c']
>>> stringList('a;b,c', separator=[',', ';'])
['a', 'b', 'c']

```

Watch the default separator: it is `', '`, a comma and a space, so
text without the space does not split at all. Say `separator=','`
when that is what you have:

```
>>> stringList('a,b')
['a,b']
>>> stringList('a,b', separator=',')
['a', 'b']

```

A list or tuple of separators splits by each in turn. A separator of
any other type raises `TypeException`.

### `replaceFlex`

`replaceFlex(text, old, new, n)` replaces only the `n`-th occurrence,
counted from one; without `n`, the first:

```
>>> from worktoy.utilities import replaceFlex
>>> replaceFlex('foo bar foo baz foo', 'foo', 'X', 2)
'foo bar X baz foo'
>>> replaceFlex('aaa', 'aa', 'X', 2)
'aX'

```

Occurrences may overlap, unlike in `str.count`: `'aaa'` holds `'aa'`
twice, from the first letter and from the second. With fewer than `n`
occurrences the text comes back unchanged, so compare the result with
the text when you need to know. An `n` below one raises `ValueError`,
so there is no counting from the end.


## 5. Fallbacks and loose arguments: `maybe`, `unpack`

### `maybe`

`maybe` gives the first of its arguments that is not `None`, like
`COALESCE` in SQL. Unlike `or`, it keeps the falsy values `0` and `''`:

```
>>> from worktoy.utilities import maybe
>>> maybe(None, 'fallback')
'fallback'
>>> maybe(0, 'fallback')
0
>>> maybe(None, None) is None
True

```

Its natural home is a keyword left at `None`:
`width = maybe(width, 80)`. Python works out every argument before
the call, so a fallback that is expensive to build belongs in an `if`.

### `unpack`

`unpack` flattens the iterables among its arguments into one tuple, all
the way down:

```
>>> from worktoy.utilities import unpack
>>> unpack([1, 2], (3, [4, 5]))
(1, 2, 3, 4, 5)
>>> unpack([1, [2, 3]], shallow=True)
(1, [2, 3])
>>> unpack('abc', [1, 2])
('abc', 1, 2)

```

Text is never split into characters. Its everyday use is a function
that takes its values loose or in one list alike:

```
>>> def total(*numbers):
...   return sum(unpack(*numbers, strict=False))
>>> total(1, 2, 3), total([1, 2, 3])
(6, 6)

```

`strict=False` matters there. By default `unpack` insists on receiving
at least one iterable, and raises `UnpackException` otherwise, with the
arguments it got as `posArgs`:

```
>>> from worktoy.waitaminute import UnpackException
>>> try:
...   unpack(1, 2)
... except UnpackException as refusal:
...   print(refusal.posArgs)
(1, 2)

```

A worktoy class is kept whole, although Python sees it as iterable,
since its metaclass offers iteration to classes that ask for it:

```
>>> from worktoy.mcls import BaseObject
>>> class Plain(BaseObject):
...   pass
>>> unpack(Plain, [1])[0] is Plain
True

```

Lists, tuples, generators and any mix of them are promised. What
`unpack` does with a dict, a set or an endless iterator is not.


## 6. Read-only attributes: `QuickDesc`, `Directory`

### `QuickDesc`

On a worktoy class, an attribute belongs in an `AttriBox` or a `Field`.
On a plain class, `QuickDesc(key)` gives a read-only view of the
attribute named `key`:

```
>>> from worktoy.utilities import QuickDesc
>>> class Box:
...   __value__ = 42
...   value = QuickDesc('__value__')
>>> box = Box()
>>> box.value
42

```

worktoy spells its private names `__value__` by house style; the key
may be any attribute name. Writing raises `ReadOnlyError` and deleting
raises `ProtectedError`, both `AttributeError`s, with the instance and
the attribute on them:

```
>>> from worktoy.waitaminute.desc import ReadOnlyError
>>> try:
...   box.value = 7
... except ReadOnlyError as refusal:
...   print(refusal.instance is box, refusal.newVal)
True 7

```

A `ProtectedError` has `oldVal` too, which may be `None` when the value
is not known.

### `Directory`

`Directory()` gives a class the folder its source file lives in, as an
absolute path in a `str`, so it can find files kept beside it:

```python
# resources.py
from worktoy.utilities import Directory


class Resource:
  home = Directory()


Resource().home  # the absolute path of the folder holding resources.py
```

Read it through an instance. A class defined where no file stands
behind it, as under `exec`, raises `MissingVariable` naming the
attribute, and writing or deleting raises `ReadOnlyError` or
`ProtectedError`. (This example is the one in this chapter that cannot
run as written here, since it depends on a file; the promise in
`promises/utilities/promise_directory.py` runs it.)


## 7. Recording what a block raised: `ExceptionInfo`

`ExceptionInfo` is a recorder, not a judge. Give it the exception you
expect, run the block inside it, and read afterwards what happened:

```
>>> from worktoy.utilities import ExceptionInfo
>>> with ExceptionInfo(ValueError) as info:
...   int('three')
>>> info.actualExcType is ValueError
True
>>> info.actualName
'ValueError'

```

With an expected type, any exception from the block is recorded and
swallowed, even one of another type. Nothing is decided for you:
compare the two types yourself.

```
>>> with ExceptionInfo(ValueError) as info:
...   {}['missing']
>>> info.actualExcType is info.expectedExcType
False
>>> info.actualName
'KeyError'

```

That is the opposite of `assertRaises` and `pytest.raises`, which fail
on a wrong type. Without an expected type, nothing is swallowed and
`report` stays empty:

```
>>> info = ExceptionInfo()
>>> try:
...   with info:
...     {}['missing']
... except KeyError:
...   print('propagated')
propagated
>>> info.report
''

```

A `KeyboardInterrupt` or any other `BaseException` that is no
`Exception` always gets through. When nothing was raised, `actualName`
is `'No Exception'` and `actualException` and `actualExcType` are
`None`. `report` is a summary for a person to read, not for code to
parse.


## 8. Slices: `sliceLen`, `ValidSlice`

`sliceLen(s, length)` tells how many elements the slice `s` selects
from a sequence of `length` elements, without needing the sequence:

```
>>> from worktoy.utilities import sliceLen
>>> sliceLen(slice(0, 10, 2), 10)
5
>>> sliceLen(slice(5, 100), 10)
5

```

A step of zero raises `ValueError`, as slicing does.

`ValidSlice` is a check, not a thing to build. Python accepts anything
in a slice and complains only when it is used; `isinstance(s,
ValidSlice)` tells you at once whether start, stop and step are each
`None`, an `int` or something with an `__index__`:

```
>>> from worktoy.utilities import ValidSlice
>>> isinstance(slice(1, 10), ValidSlice)
True
>>> isinstance(slice(0, 10, 'step'), ValidSlice)
False

```

It checks the shape, not the values: `__index__` is never called, so
one that would fail still passes. Calling `ValidSlice()` raises
`TypeError`.


## 9. Classes and functions: `resolveMRO`, `argsCount`

`resolveMRO(*bases)` gives the resolution order a class with these
bases would have, the class itself left out, before any such class
exists. A metaclass needs that while it builds one:

```
>>> from worktoy.utilities import resolveMRO
>>> class A:
...   pass
>>> class B(A):
...   pass
>>> class C(A):
...   pass
>>> [base.__name__ for base in resolveMRO(B, C)]
['B', 'C', 'A', 'object']
>>> class Foo(B, C):
...   pass
>>> resolveMRO(B, C) == Foo.mro()[1:]
True

```

Bases Python would refuse in a class statement raise `TypeError`.

`argsCount(func)` counts the positional parameters of a function,
leaving out `*args`, `**kwargs` and keyword-only parameters:

```
>>> from worktoy.utilities import argsCount
>>> argsCount(lambda a, b, *args, c=0: None)
2
>>> class Greeter:
...   def greet(self, name):
...     return name
>>> argsCount(Greeter().greet)
2

```

Mind the bound method: `argsCount` counts the parameters of the
function behind it, `self` included, not the arguments you pass. You
call `greet` with one argument; subtract one when that is what you
want to know.


## 10. Combinatorics

### `bipartiteMatching`

`bipartiteMatching(slots)` gives every slot an index of its own, chosen
from that slot's candidates, no two alike. Seating three guests: Ada
may take chair 0 or 1, Bob only chair 0, Cy chair 1 or 2:

```
>>> from worktoy.utilities import bipartiteMatching
>>> bipartiteMatching([(0, 1), (0,), (1, 2)])
[1, 0, 2]

```

When several answers fit, which one you get is not promised. When none
fits, it raises `ValueError`.

### `indexPermutations`

`indexPermutations(n)` gives every ordering of `0` to `n - 1`, `n!` of
them, in lexicographic order:

```
>>> from worktoy.utilities.combinatorics import indexPermutations
>>> list(indexPermutations(3))
[(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]

```

That is what `itertools.permutations(range(n))` gives too; this one
refuses a negative `n` with `ValueError` at the call, before you draw
anything from it.

### `Arrangement`

An `Arrangement` is one ordering of some items, with the bookkeeping to
go both ways. `forward` says, for each slot, which item fills it;
`inverse` says, for each item, which slot it went to:

```
>>> from worktoy.utilities.combinatorics import Arrangement
>>> arrangement = Arrangement(('north', 'east', 'south'), (2, 0, 1))
>>> arrangement.values
('south', 'north', 'east')
>>> arrangement.inverse
(1, 2, 0)

```

`applyTo` puts values given in the order of the items into the order of
the arrangement, and `restoreFrom` puts them back. With the headings of
the three directions:

```
>>> arrangement.applyTo(0, 90, 180)
(180, 0, 90)
>>> arrangement.restoreFrom(180, 0, 90)
(0, 90, 180)

```

Either raises `ValueError` when given the wrong number of values.

### `Arrangements`

`Arrangements(*items)` holds every distinct ordering of the items, each
an `Arrangement`. Repeated items collapse, so three letters with one
repeated give three orderings, not six:

```
>>> from worktoy.utilities.combinatorics import Arrangements
>>> [a.values for a in Arrangements('A', 'A', 'B')]
[('A', 'A', 'B'), ('A', 'B', 'A'), ('B', 'A', 'A')]
>>> len(Arrangements('red', 'green', 'blue'))
6

```

Mind the size: `n` items have `n!` orderings, 3,628,800 for ten. Note
the two names, one letter apart: `Arrangement` takes the items as one
tuple and a recipe, `Arrangements` takes the items loose.
