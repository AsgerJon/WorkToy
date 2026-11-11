# worktoy manual: dispatch

Python keeps only the last function bound to a name in a class body,
so a method cannot be written once per signature. `worktoy.dispatch`
makes that possible: declare the method once per signature with
`@overload`, and each call goes to the declaration its arguments match.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Contents:

1. Where overloading works
2. Declaring a method per signature
3. How a call finds its declaration
4. Several signatures, any order, a tail, a fallback
5. Classmethods, staticmethods and subclasses
6. Mistakes caught at the declaration
7. The building blocks


## 1. Where overloading works

`@overload` works in the body of a class built by `BaseMeta`, the
metaclass behind `BaseObject`, which the metaclass chapter describes.
The decorator only records a signature; the class turns the records of
each name into one dispatcher as it is created. So there is no
overloading of a module-level function, and an `@overload` left in a
plain class is refused as that class is created, as section 6 shows.

The classes go in the decorator. The annotations of the function are
not read, so write them as you like, or leave them out. And the name
`overload` is not `typing.overload`, which serves type checkers only;
if a file needs both, import one of them under another name.


## 2. Declaring a method per signature

```
>>> from worktoy.mcls import BaseObject
>>> from worktoy.desc import AttriBox
>>> from worktoy.dispatch import overload
>>> class Money(BaseObject):
...   amount = AttriBox[float](0.0)
...   currency = AttriBox[str]('EUR')
...   @overload(float, str)
...   def __init__(self, amount, currency):
...     self.amount, self.currency = amount, currency
...   @overload(float)
...   def __init__(self, amount):
...     self.amount = amount
...   @overload()
...   def __init__(self):
...     pass
>>> usd = Money(2.5, 'USD')
>>> usd.amount, usd.currency
(2.5, 'USD')
>>> Money(4.0).currency
'EUR'
>>> Money().amount
0.0

```

The classes listed are those of the positional arguments after
`self`. Any method may be overloaded this way, `__init__` and the
operators included.


## 3. How a call finds its declaration

Only the positional arguments of a call are matched. Keywords play no
part in the choice and pass to the declaration chosen. Two things
follow that are easy to trip over:

```
>>> try:
...   Money(amount=2.5)
... except TypeError:
...   print('no positional arguments: the empty declaration took it')
no positional arguments: the empty declaration took it
>>> class Greeter(BaseObject):
...   @overload(str)
...   def greet(self, name, loud=False):
...     return name.upper() if loud else name
>>> Greeter().greet('ada', loud=True)
'ADA'
>>> from worktoy.waitaminute.dispatch import DispatchException
>>> try:
...   Greeter().greet('ada', True)
... except DispatchException:
...   print('(str, bool) is not declared')
(str, bool) is not declared

```

A call by keyword alone is matched as a call with no positional
arguments, and a defaulted parameter given by position is one more
positional argument to match. Pass optional parameters by keyword.

The positional arguments are matched in steps, and the first step that
finds a declaration decides:

1. Their exact classes.
2. As instances, so a subclass instance matches its base. The class's
   own declarations come before inherited ones, and within one class
   the first declaration written that accepts the arguments wins.
3. A conversion that loses nothing, as `typeCast` of the utilities
   chapter allows: an `int` for a `float`, `2.0` for an `int`, and a
   class with a `__cast_as__` hook converts there too.
4. The fallback of section 4, if there is one.
5. Otherwise `DispatchException`, a `TypeError`, holding the dispatcher
   as `dispatch`, and the arguments as `posArgs` and `keyArgs`.

Step 2 does not look for the most specific declaration. It takes the
first one written, so write the specific ones first:

```
>>> class Kind(BaseObject):
...   @overload(object)
...   def kind(self, value):
...     return 'object'
...   @overload(int)
...   def kind(self, value):
...     return 'int'
>>> Kind().kind(1)
'int'
>>> Kind().kind(True)
'object'

```

`1` is an `int` exactly and step 1 finds it. `True` is a `bool`, which
no declaration names, so step 2 asks each declaration in order, and
`object` comes first. Reordering the declarations changes the answer,
so their order is part of what the class means.

An argument accepted in step 2 arrives as it was passed, so `True`
reaches an `int` declaration as `True`. One converted in step 3 arrives
converted:

```
>>> class Scale(BaseObject):
...   @overload(float)
...   def ratio(self, value):
...     return value
>>> Scale().ratio(3)
3.0

```


## 4. Several signatures, any order, a tail, a fallback

Decorators stack, so one function may serve several signatures:

```
>>> class Halver(BaseObject):
...   @overload(int)
...   @overload(float)
...   def half(self, value):
...     return value / 2
>>> Halver().half(4), Halver().half(3.0)
(2.0, 1.5)

```

`overload.flex` takes its classes in any order, and the function
receives them in the order declared:

```
>>> class Label(BaseObject):
...   @overload.flex(str, int)
...   def __init__(self, text, size):
...     self.text, self.size = text, size
>>> Label(12, 'Title').text
'Title'

```

`THIS` in a signature stands for the class being declared, which does
not exist yet while its body runs; it is how an operator takes another
instance of its own class:

```
>>> from worktoy.core.sentinels import THIS
>>> class Vector(BaseObject):
...   @overload(float, float)
...   def __init__(self, x, y):
...     self.x, self.y = x, y
...   @overload(THIS)
...   def __add__(self, other):
...     return Vector(self.x + other.x, self.y + other.y)
>>> total = Vector(1.0, 2.0) + Vector(3.0, 4.0)
>>> total.x, total.y
(4.0, 6.0)

```

It is the same marker the core chapter fills in with the instance
during an access. Where a value is built, it means the instance; in a
signature, where a class is listed, it means the class.

`ARGS[int]`, last in a signature, takes any number of further
integers, none included, converting them as a single entry would. A
signature that matches exactly wins over a tail:

```
>>> from worktoy.core.sentinels import ARGS
>>> class Summary(BaseObject):
...   @overload(str, ARGS[int])
...   def total(self, label, *numbers):
...     return label, sum(numbers)
...   @overload(str)
...   def total(self, label):
...     return label, 'nothing to add'
>>> Summary().total('apples', 1, 2, 3)
('apples', 6)
>>> Summary().total('pears')
('pears', 'nothing to add')

```

A bare `ARGS`, or `*ARGS`, takes any number of anything. Mind that it
takes a mistaken call as well: a declaration of `ARGS` alone catches
every call nothing else accepts, typos included.

`@overload.fallback` declares the function for every call no
declaration accepts, and `@overload.finalize` one that runs after every
call, whichever declaration took it and whether or not it raised. Both
receive the positional arguments and the keywords of the call, and a
subclass inherits both:

```
>>> class Job(BaseObject):
...   @overload(int)
...   def run(self, n):
...     return n * 2
...   @overload.fallback
...   def run(self, *args, **kwargs):
...     return 'cannot run %r' % (args,)
...   @overload.finalize
...   def run(self, *args, **kwargs):
...     print('done')
>>> Job().run(21)
done
42
>>> Job().run('x')
done
"cannot run ('x',)"

```


## 5. Classmethods, staticmethods and subclasses

An overloaded name may be a classmethod, as an alternative constructor
taking several kinds of argument, or a staticmethod. Write
`@classmethod` or `@staticmethod` above `@overload` or below it:

```
>>> class Color(BaseObject):
...   @classmethod
...   @overload(int)
...   def make(cls, code):
...     return 'code %d' % code
...   @overload(str)
...   @classmethod
...   def make(cls, name):
...     return 'named ' + name
>>> Color.make(1), Color.make('red')
('code 1', 'named red')

```

All the declarations of one name are one kind of method; a name
declared as two kinds raises `MixedMethodKind`.

A subclass overloading a name it inherits keeps the inherited
declarations and adds its own, and a declaration of an equal signature
replaces the inherited one:

```
>>> class Shape(BaseObject):
...   @overload(int)
...   def describe(self, n):
...     return 'shape int'
...   @overload(str)
...   def describe(self, s):
...     return 'shape str'
>>> class Square(Shape):
...   @overload(int)
...   def describe(self, n):
...     return 'square int'
>>> Square().describe(1), Square().describe('a')
('square int', 'shape str')

```

A subclass defining the name as a plain method instead hides every
inherited declaration, as a plain definition does.


## 6. Mistakes caught at the declaration

A mistaken declaration fails at its line or as the class is created,
never at the first call:

- `@overload` without parentheses raises `BareOverload`.
- An entry that is no class raises `TypeException`; `None` raises a
  `TypeError`, since a call passing `None` is declared with
  `type(None)`.
- A class `isinstance` cannot check, such as a `Protocol` not marked
  `@runtime_checkable`, raises `UncheckableType`.
- One body declaring the same signature twice for a name raises
  `DuplicateSignature`.
- An `@overload` in a class not built by `BaseMeta` raises a `TypeError`
  as the class is created, which Python wraps in a `RuntimeError`
  before 3.12. Calling what `@overload` returns raises a `TypeError`
  too, since it only records a signature.

```
>>> from worktoy.waitaminute.dispatch import DuplicateSignature
>>> try:
...   class Twice(BaseObject):
...     @overload(int)
...     def f(self, x):
...       return 1
...     @overload(int)
...     def f(self, x):
...       return 2
... except DuplicateSignature:
...   print('(int) is declared twice')
(int) is declared twice

```


## 7. The building blocks

The parts of the machinery are public too, for a project building its
own:

- `flexCall(func)` wraps a plain function so it drops surplus
  positional arguments, still raising `TypeError` for a missing one; it
  suits a callback that some caller hands more arguments than it needs.
  Keywords pass unchanged. `isFlex` tells a wrapper from a plain
  function.
- `TypeSig` is the classes of a call, in order, equal and hashing alike
  for the same classes; `TypeSig.fromArgs(1, 'a')` is `TypeSig(int,
  str)`. It is not equal to a plain tuple.
- `CallMeMaybe` holds a function and calls it, never binding it as a
  method; `Permuter` calls a function with its arguments put back in the
  order an `Arrangement` restores, which is what `overload.flex` needs.
- `Dispatcher` is what the class holds at an overloaded name:
  `vars(Money)['__init__']` is one, while `Money.__init__` reads as a
  callable.

```
>>> from worktoy.dispatch import flexCall
>>> def onClick(position):
...   return 'clicked at %s' % (position,)
>>> flexCall(onClick)((3, 4), 'left button', 2)
'clicked at (3, 4)'

```
