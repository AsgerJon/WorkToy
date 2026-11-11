# worktoy manual: core

`worktoy.core` is the layer the rest of worktoy stands on. Most
projects never import from it: they subclass `BaseObject` and declare
their attributes with `AttriBox`, which later chapters describe. You
reach into `core` when you build something of your own, of the kinds
worktoy itself is built from:

- a descriptor, on `Object`;
- a marker no real value can be mistaken for, on `Sentinel`;
- a signal that steers a protocol, on `ControlFlow`;
- a metaclass, on `MetaType`.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Contents:

1. Writing a descriptor on `Object`
2. Hooks around every access
3. Arguments and placeholders: `THIS`, `OWNER`, `DESC`
4. The access in progress
5. An `Object` as a class value
6. Options under several names: `parseKwargs`
7. Sentinels
8. Control-flow signals
9. Metaclasses: `MetaType`


## 1. Writing a descriptor on `Object`

A descriptor is an object in a class body that decides what reading,
writing and deleting an attribute does on the instances; `property` is
the best known one. In plain Python a descriptor defines `__get__`,
`__set__` and `__delete__`. On `Object` you define three methods of
your own instead, and leave those three to `Object`, which uses them to
keep track of the access, run the hooks of the next section and handle
deletion:

```
>>> from worktoy.core import Object
>>> from worktoy.core.sentinels import DELETED
>>> class Counted(Object):
...   def __instance_get__(self, instance, owner, **kwargs):
...     return instance.__dict__.get('_count', 0)
...   def __instance_set__(self, instance, value, **kwargs):
...     instance.__dict__['_count'] = value
...   def __instance_delete__(self, instance, old=None, **kwargs):
...     instance.__dict__['_count'] = DELETED
>>> class Visit:
...   count = Counted()
>>> visit = Visit()
>>> visit.count
0
>>> visit.count = 3
>>> visit.count
3
>>> del visit.count
>>> hasattr(visit, 'count')
False

```

A few things to know before you write your own:

- Any class can hold one. `Visit` is a plain class; neither `MetaType`
  nor `BaseObject` is needed.
- Where the values live is yours to decide. `Counted` keeps them in the
  instance dictionary. The boxes of a later chapter, `AttriBox` first,
  do that bookkeeping for you.
- Deleting is yours too. `__instance_delete__` stores `DELETED` where
  the getter reads, and when the getter returns `DELETED`, `Object`
  turns the read into `MissingVariable`, an `AttributeError`. So
  `hasattr` answers False, and a second `del` raises as well.
- Always accept `**kwargs`. worktoy hands keywords to these methods,
  `_deleting` among them, as section 2 shows.
- `instance` arrives as an argument, and is also `self.instance` while
  the access runs, so a helper method you call from inside can ask for
  it instead of being handed it. `self.owner` is the class; during a
  write or a deletion that is the class of the instance. Both work
  through `ContextInstance` and `ContextOwner`, which you never need
  yourself.
- Read through the class, the attribute is the descriptor itself:
  `Visit.count` is the `Counted` object.
- A method you leave out keeps the default of `Object`: a read gives
  the descriptor itself, a write raises `ReadOnlyError` and a deletion
  raises `ProtectedError`. Section 5 shows why that is useful.


## 2. Hooks around every access

Around each access, `Object` calls hooks you may define:

- `hookPreGet(instance)` before a read, and `hookOnGet(instance,
  value)` after it, with the value about to be returned;
- `hookPreSet(instance, value)` before a write, with the value
  assigned, and `hookOnSet(instance, value)` after it;
- `hookPreDelete(instance)` and `hookOnDelete(instance)` around a
  deletion;
- `hookSetName(owner, name)` when the descriptor is placed in a class
  body.

A thermostat that refuses frost, skips a setting it already has, and
reports every change:

```
>>> from worktoy.core.control_flow import SkipSet
>>> class Setting(Object):
...   def __instance_get__(self, instance, owner, **kwargs):
...     return instance.__dict__.get('_target', 20)
...   def __instance_set__(self, instance, value, **kwargs):
...     instance.__dict__['_target'] = value
...   def hookPreSet(self, instance, value, **kwargs):
...     if value < 5:
...       raise ValueError('too cold')
...     if value == instance.__dict__.get('_target', 20):
...       raise SkipSet
...   def hookOnSet(self, instance, value, **kwargs):
...     print('target set to', value)
>>> class Thermostat:
...   target = Setting()
>>> room = Thermostat()
>>> room.target = 22
target set to 22
>>> room.target = 22
>>> try:
...   room.target = 2
... except ValueError as error:
...   print(error)
too cold
>>> room.target
22

```

- `hookPreSet` refuses a write by raising, and skips one silently by
  raising `SkipSet`: nothing is stored and `hookOnSet` is not called.
  `SkipSet` works there and nowhere else; any other exception, a
  signal of your own included, reaches the line that assigned. To store
  something other than what was assigned, convert it in
  `__instance_set__` and return what you stored.
- `hookOnSet` receives what `__instance_set__` returned, or the value
  assigned when it returned `None`. It runs after the value is stored,
  so raising there refuses nothing.
- A deletion first reads the old value through your getter, with
  `_deleting=True` among the keywords and without the read hooks, so
  side effects of your getter happen on `del` too, and a getter that
  builds defaults can see that it should not. Then come
  `hookPreDelete`, `__instance_delete__`, which receives the old value,
  and `hookOnDelete`.
- `hookSetName` runs when Python places the descriptor, in a class
  body. Python does not place an attribute set on a class afterwards.
- Each hook is one method of your class. For several callbacks on one
  field, the boxes of a later chapter take them as decorators.

The reads are guarded against loops, as section 4 shows; the writes
are not, so a `hookOnSet` assigning its own field runs again and again.


## 3. Arguments and placeholders: `THIS`, `OWNER`, `DESC`

An `Object` keeps the arguments it was created with, and
`getPosArgs()` and `getKeyArgs()` give them back. An argument is
written in the class body, where no instance exists yet, so three
placeholders stand in: during an access, an argument that is `THIS`
becomes the instance, `OWNER` the class, and `DESC` the descriptor
itself.

```
>>> from worktoy.core.sentinels import THIS
>>> class Greeting(Object):
...   def __instance_get__(self, instance, owner, **kwargs):
...     word, person = self.getPosArgs()
...     return '%s, %s' % (word, person.name)
>>> class Person:
...   greeting = Greeting('Hello', THIS)
...   def __init__(self, name):
...     self.name = name
>>> Person('Ada').greeting
'Hello, Ada'

```

This is what lets `AttriBox[...](THIS)` build a value from the instance
it belongs to.

- Only an argument that is the placeholder itself is replaced, not one
  inside a list or a dict. Build the container in `__instance_get__`
  from the filled-in arguments.
- Outside an access there is no instance, so `THIS` and `OWNER` stay
  themselves. `DESC` always becomes the descriptor, which always
  exists. Read the arguments during an access.
- `Object` takes any arguments and checks none of them: what they mean
  is up to your class. `hasSentinelArgs()` tells whether any is a
  placeholder.

`getPrivateName()` suggests a private name to store a field under:
`'__foo_bar__'` for a field named `fooBar`. The mapping is not one to
one: `foo_bar` gives `'__foo_bar__'` as well, and a field named `dict`
gives the `'__dict__'` Python uses itself. A descriptor no class holds
has no field name, and `getPrivateName()` raises `MissingVariable`.


## 4. The access in progress

`self.instance` and `self.owner` answer during an access, and only
then. Asked outside one, a descriptor placed in a class raises
`WithoutException`, short for "without an access in progress", a
`RuntimeError` and deliberately no `AttributeError`, since asking is a
mistake in the code; so `hasattr` raises it too. An `Object` no class
holds simply has no such attribute.

Code driving a descriptor by hand opens an access with
`createContext(instance, owner)` and closes it with `exitContext()`.
Accesses nest, and closing one brings back the one opened before:

```
>>> class Plain(Object):
...   pass
>>> class Holder:
...   thing = Plain()
>>> desc, holder = vars(Holder)['thing'], Holder()
>>> _ = desc.createContext(holder, Holder)
>>> try:
...   print(desc.instance is holder)
... finally:
...   _ = desc.exitContext()
True

```

Pair them in `try` and `finally` as shown. Closing with nothing open
raises `WithoutException`.

Each thread sees only its own accesses, so two threads reading through
one descriptor at the same moment each get their own instance. An
access lasts exactly one call, so asyncio tasks do not see each
other's either.

A read hook that reads its own field for the same instance would run
itself again forever. It is refused at that line with `RecursiveRead`,
a `RecursionError` that names the hook in `phase`, `'preGet'` or
`'onGet'`:

```
>>> from worktoy.waitaminute.desc import RecursiveRead
>>> class Gauge(Object):
...   def __instance_get__(self, instance, owner, **kwargs):
...     return instance._level
...   def hookOnGet(self, instance, value, **kwargs):
...     if instance.level != value:
...       print('changed')
>>> class Tank:
...   level = Gauge()
...   def __init__(self, level):
...     self._level = level
>>> try:
...   Tank(3).level
... except RecursiveRead as error:
...   print('refused during', error.phase)
refused during onGet

```

Reading the same field of another instance is allowed. Only the hooks
are guarded: a getter reading its own field ends in Python's own
`RecursionError`.


## 5. An `Object` as a class value

An `Object` that defines none of the three access methods is a value in
the class body, shared by every instance. Reading it through an
instance gives the object itself, and an instance may not replace or
delete it: worktoy holds its own objects in a class body to that rule.

```
>>> class Theme(Object):
...   pass
>>> class Config:
...   theme = Theme('dark')
>>> config = Config()
>>> config.theme is Config.theme
True
>>> config.theme.getPosArgs()
('dark',)
>>> from worktoy.waitaminute.desc import ReadOnlyError
>>> try:
...   config.theme = 'light'
... except ReadOnlyError as error:
...   print(error.newVal, 'refused')
light refused

```

`Object` is also the base of the ordinary objects of worktoy,
`BaseObject` among them. A base listed after an `Object` class still
has its `__init__` run, as `threading.Thread` needs, but without
arguments, so a base that requires some refuses with its own
`TypeError`; list such a base first.

An `Object` already uses these names, so a subclass should not take
them for something else: `instance`, `owner`, `directory`,
`getPosArgs`, `getKeyArgs`, `hasSentinelArgs`, `getFieldOwner`,
`getFieldName`, `getPrivateName`, `createContext`, `exitContext`,
`hasContext`, `getContextInstance`, `getContextOwner`,
`getContextualSentinels`, `filterSentinels`, `parseKwargs`, and the
hooks of section 2. `directory` is the folder of the file that defines
the class, as `Directory` in the utilities chapter gives it.


## 6. Options under several names: `parseKwargs`

An option sometimes goes by several names, as `readOnly` or `frozen`.
`Object.parseKwargs` reads it once: give it the names and the accepted
types, in any order, and the keywords:

```
>>> def connect(**options):
...   return Object.parseKwargs('readOnly', 'frozen', bool, **options)
>>> connect(frozen=True, timeout=5)
(True, {'timeout': 5})
>>> connect(timeout=5)
(None, {'timeout': 5})

```

It is a classmethod, so any function may use it. The first name present
wins, in the order you gave the names, and a second synonym stays among
the other keywords. A `float` accepts an `int`, a `complex` accepts
both, and a `bool` passes as an `int`; the value comes back as given,
not converted. A value of no accepted type raises `TypeException`.


## 7. Sentinels

A sentinel is a marker no real value can be mistaken for: "not given
yet", "deleted", "the class being defined". A project declares one with
a class statement, and the class itself is the marker. It reads well in
a traceback, it is equal to itself alone, and it cannot be
instantiated:

```
>>> from worktoy.core.sentinels import Sentinel, SentinelMeta
>>> class PENDING(Sentinel):
...   """The result has not arrived yet."""
>>> results = {'job1': PENDING}
>>> results['job1'] is PENDING
True
>>> from worktoy.waitaminute.meta import IllegalInstantiation
>>> try:
...   PENDING()
... except IllegalInstantiation:
...   print('a sentinel is never instantiated')
a sentinel is never instantiated

```

A name stands for one sentinel in the whole process, so a second class
statement at a name already taken raises `DuplicateSentinel`:

```
>>> from worktoy.waitaminute.meta import DuplicateSentinel
>>> try:
...   class PENDING(Sentinel):
...     pass
... except DuplicateSentinel as error:
...   print(error.sentinelName, 'is taken')
PENDING is taken

```

That holds wherever the second statement is: in another module, in
another library, in a Jupyter cell run again, or in a module reloaded.
Declare each sentinel once, in one module the rest import, and give it
a distinctive name.

To give sentinels behaviour, base a metaclass of your own on
`SentinelMeta`. Its sentinels share the one registry of names:

```
>>> class LightMeta(SentinelMeta):
...   def describe(cls):
...     return 'the light is %s' % cls.__name__.split('_')[-1].lower()
>>> class LIGHT_ON(metaclass=LightMeta):
...   pass
>>> LIGHT_ON.describe()
'the light is on'
>>> isinstance(LIGHT_ON, SentinelMeta)
True

```

`isinstance(x, SentinelMeta)` is the test that works for every
sentinel, those of a family included.

worktoy declares a few of its own. `DELETED` marks a deleted value, as
in section 1, and `THIS`, `OWNER` and `DESC` are the placeholders of
section 3. `METACALL` belongs to the metaclass chapter. `ARGS` belongs
to the overload chapter: unlike the others it is subscripted,
`ARGS[int]`, to an instance carrying its inner type, and instances of
one inner type are equal and hash alike.


## 8. Control-flow signals

Some exceptions steer a protocol instead of reporting a failure, as
`StopIteration` tells a loop to stop. worktoy calls them control-flow
signals. Each is a subclass of `ControlFlow`, so `except ControlFlow`
catches them all, and none is a worktoy error. `SkipSet`, from section
2, is the one worktoy raises, and worktoy catches it only around
`hookPreSet`.

A project declares a signal of its own with a class statement. A
signal is used by its type alone and carries nothing, so its body may
hold a docstring and, if you like, `__str__` and `__repr__`, and
nothing else:

```
>>> from worktoy.core.control_flow import ControlFlow
>>> class Retry(ControlFlow):
...   """The step should run again."""
>>> try:
...   raise Retry
... except ControlFlow as signal:
...   print('caught', type(signal).__name__)
caught Retry
>>> from worktoy.waitaminute.meta import ControlClassError
>>> try:
...   class Wait(ControlFlow):
...     seconds = 3
... except ControlClassError as error:
...   print('refused:', error.badKey)
refused: seconds

```

When the reason matters, raise a real exception instead. Mind that a
signal is an `Exception`, so an `except Exception` between the raise
and the place meant to catch it catches the signal as well.

The signals lived in `worktoy.waitaminute.control_flow` before. They
import from there as the same objects throughout the 1.x releases. That
path is deprecated since 1.2.0: each name read from it gives a
deprecation notice, a `FutureWarning`.
`MetaFlow` and `ControlSpace`, the metaclass and namespace behind the
signals, are public, but a project declaring signals never needs them.


## 9. Metaclasses: `MetaType`

Every worktoy class and metaclass is built on `MetaType`. A metaclass
of your own based on it gets two things plain `type` does not give.

A class statement may carry keywords, and a base whose
`__init_subclass__` takes one receives it:

```
>>> from worktoy.core import MetaType
>>> class Plugin:
...   registry = []
...   def __init_subclass__(cls, tag=None, **kwargs):
...     Plugin.registry.append(tag)
...     super().__init_subclass__(**kwargs)
>>> class Reader(Plugin, metaclass=MetaType, tag='reader', tagg='typo'):
...   pass
>>> Plugin.registry
['reader']

```

Mind the second keyword. Plain Python would end the class statement
with "takes no keyword arguments" for any keyword left over; worktoy
absorbs what no class takes, so a misspelled keyword is dropped
without a word.

And a metaclass of another library combines with a worktoy one in
either order. Python runs only the first `__init__` of a combined
metaclass, and each hands on to the next; `MetaType` hands on, so the
other one runs too, as long as it hands on in turn:

```
>>> class Registry(type):
...   classes = []
...   def __init__(cls, name, bases, space, **kwargs):
...     Registry.classes.append(name)
...     super().__init__(name, bases, space, **kwargs)
>>> class PluginMeta(MetaType, Registry):
...   pass
>>> class Exporter(metaclass=PluginMeta):
...   pass
>>> Registry.classes
['Exporter']

```

`Object` is itself built by `MetaType`, so a class mixing an `Object`
class with one of another metaclass, such as `ABCMeta`, needs a
metaclass combining the two, as Python always requires.

A class `MetaType` builds keeps the namespace its body ran in as
`__namespace__`, which is where a worktoy metaclass keeps what it
learned from the body:

```
>>> class Settings(metaclass=MetaType):
...   width = 80
>>> Settings.__namespace__['width']
80

```

A metaclass of your own may give the body a namespace of its own from
`__prepare__`, a `dict` or a subclass of it. The entries worktoy adds
itself, `__namespace__` and `__annotations__`, never pass through its
`__setitem__`, so it sees the names of the class body alone. And the
`__annotations__` of a class are always its own: for an ordinary class
that is what Python gives anyway, and it matters when a metaclass
annotates its own body, where Python may report the annotations of the
metaclass instead.
