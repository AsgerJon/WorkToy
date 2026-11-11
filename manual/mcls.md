# worktoy manual: mcls

`worktoy.mcls` holds `BaseObject`, the base of a worktoy class, and the
metaclass machinery behind it. Most projects need `BaseObject` and
nothing else from here; the later sections are for giving a class
behaviour of its own and for writing namespace rules of your own.

Everything shown here is promised. The examples are checked against
every release, so they keep working in every update. Anything this
chapter does not show may change.

Contents:

1. `BaseObject`
2. A class that behaves as an object: the class hooks
3. `__class_init__` and `__subclasshook__`
4. Mistakes caught in the class body
5. Combining with another library's metaclass
6. Namespace hooks of your own


## 1. `BaseObject`

Base a class on `BaseObject` and it gets the overloads of the dispatch
chapter, the checks of section 4 and the class hooks of section 2 at
once. The layers underneath are for those building metaclasses:
`BaseMeta` is the metaclass of `BaseObject` and the one to base a
metaclass of your own on; `AbstractMetaclass` and `AbstractNamespace`
are its plainer parts, and `MetaType` of the core chapter is the
bottom.

A class with no initializer refuses constructor arguments, as a plain
class does:

```
>>> from worktoy.mcls import BaseObject
>>> class Point(BaseObject):
...   pass
>>> try:
...   Point(1)
... except TypeError:
...   print('Point takes no arguments')
Point takes no arguments

```

A plain base listed after `BaseObject`, as `threading.Thread`, is
initialized as in a plain class, without arguments; a base whose
`__init__` requires arguments goes before `BaseObject`.


## 2. A class that behaves as an object: the class hooks

In plain Python, making a class itself iterable, or giving it a length,
takes a metaclass of its own. A worktoy class defines it in its own
body, with classmethods named after the operation:

```
>>> class Planets(BaseObject):
...   __names__ = ('Mercury', 'Venus', 'Earth')
...   @classmethod
...   def __class_iter__(cls):
...     return iter(cls.__names__)
...   @classmethod
...   def __class_len__(cls):
...     return len(cls.__names__)
>>> list(Planets)
['Mercury', 'Venus', 'Earth']
>>> len(Planets), 'Venus' in Planets
(3, True)

```

The hooks are `__class_call__`, `__class_init__`,
`__class_instancecheck__`, `__class_subclasscheck__`, `__class_str__`,
`__class_repr__`, `__class_iter__`, `__class_next__`, `__class_bool__`,
`__class_contains__`, `__class_len__`, `__class_hash__`,
`__class_setitem__`, `__class_delitem__`, `__class_getattr__` for a
missing attribute, `__class_setattr__` and `__class_delattr__`. A
subscript of a class still goes to Python's own `__class_getitem__`.

- Each hook must be a classmethod; anything else raises
  `UnboundClassHook` as the class is created.
- An operation without a hook behaves as for a plain class: `len` and
  `iter` raise `TypeError`, `bool` answers from `__class_len__` or else
  `True`, and `in` searches what `__class_iter__` yields, one item at a
  time.
- A hook decides alone. `__class_instancecheck__` answering for `int`
  makes `isinstance(3, Whole)` True and leaves instances of `Whole`
  itself to whatever the hook says; `__class_call__` replaces making an
  instance.
- Hooks are inherited. A subclass sets one to `METACALL`, from the core
  chapter, to hand the operation back:

```
>>> from worktoy.core.sentinels import METACALL
>>> class Whole(BaseObject):
...   @classmethod
...   def __class_instancecheck__(cls, obj):
...     return isinstance(obj, int)
>>> class Ordinary(Whole):
...   __class_instancecheck__ = METACALL
>>> isinstance(3, Whole), isinstance(3, Ordinary)
(True, False)

```

`METACALL` at `__class_call__` likewise brings back ordinary
construction in a subclass.


## 3. `__class_init__` and `__subclasshook__`

`__class_init__` runs once a class exists, for the class declaring it
and for every subclass, with the name, the bases, the namespace and
the class keywords. A plugin registry is the usual use:

```
>>> registry = []
>>> class Plugin(BaseObject):
...   @classmethod
...   def __class_init__(cls, name, bases, space, **kwargs):
...     registry.append((name, kwargs))
>>> class Exporter(Plugin, format='csv'):
...   pass
>>> registry
[('Plugin', {}), ('Exporter', {'format': 'csv'})]

```

It runs for `Plugin` itself, so a registry wanting subclasses only
skips the base by hand. A class keyword reaches `__class_init__` and the
`__init_subclass__` of a plain base alike.

A base's `__subclasshook__` receives each new subclass as it is
created, and refuses it by raising whatever fits. Each direct base is
asked, its own hook or one it inherits, so a grandchild passes through
its parent's.

Mind the name. `abc` asks the same method inside `issubclass` and
expects `True`, `False` or `NotImplemented`. Under a metaclass combined
with `ABCMeta`, as in section 5, a hook that refuses by raising must
therefore return `NotImplemented` when it lets a class through.


## 4. Mistakes caught in the class body

Python lets some mistakes in a class body pass without a word. In a
worktoy class each fails at its line, with a `SyntaxError`:

- A known misspelling of a dunder, as `__setname__` for
  `__set_name__`, raises `QuestionableSyntax`, naming both. It checks
  a list of known misspellings, not every possible one.
- `__del__`, most often written where `__delete__` was meant, raises
  `DelException` unless the class statement says `trustMeBro=True`.
  Each class defining `__del__` says so itself.
- `__slots__` raises `SlotsRefused`: a worktoy instance always keeps a
  `__dict__`, where its boxes keep their values.
- Rebinding a name Python reserves for the class, as `__qualname__`,
  raises `ReservedName`.

```
>>> from worktoy.waitaminute.meta import QuestionableSyntax
>>> try:
...   class Placed(BaseObject):
...     def __setname__(self, owner, name):
...       pass
... except QuestionableSyntax as mistake:
...   print(mistake.derpName, 'should be', mistake.realName)
__setname__ should be __set_name__
>>> class Handle(BaseObject, trustMeBro=True):
...   def __del__(self):
...     pass

```


## 5. Combining with another library's metaclass

A class may have one metaclass, so a base built by another library's
metaclass, such as `abc.ABC`, cannot sit beside `BaseObject`: Python
raises its metaclass conflict. A metaclass based on both builds the
class with the features of both:

```
>>> import abc
>>> from worktoy.mcls import BaseMeta
>>> from worktoy.dispatch import overload
>>> class ABCBaseMeta(BaseMeta, abc.ABCMeta):
...   pass
>>> class Shape(BaseObject, metaclass=ABCBaseMeta):
...   @abc.abstractmethod
...   def area(self):
...     pass
...   @overload(int)
...   def scale(self, factor):
...     return factor
>>> class Square(Shape):
...   def area(self):
...     return 1.0
>>> Square().area(), Square().scale(2)
(1.0, 2)
>>> try:
...   Shape()
... except TypeError:
...   print('Shape is abstract')
Shape is abstract

```

The same pattern serves other libraries' metaclasses.


## 6. Namespace hooks of your own

A team rule for class bodies, such as "no single-underscore names",
can fail at the line breaking it. It takes three small classes: a hook,
a namespace holding it, and a metaclass returning that namespace.

```
>>> from worktoy.mcls import BaseSpace
>>> from worktoy.mcls.space_hooks import AbstractSpaceHook
>>> class NoSingleUnderscore(AbstractSpaceHook):
...   def setItemPhase(self, key, value, old=None):
...     if key.startswith('_') and not key.startswith('__'):
...       raise NameError('%s.%s' % (self.space.getClassName(), key))
...     return False
>>> class TeamSpace(BaseSpace):
...   noSingleUnderscore = NoSingleUnderscore()
>>> class TeamMeta(BaseMeta):
...   @classmethod
...   def __prepare__(mcls, name, bases, **kwargs):
...     return TeamSpace(mcls, name, bases, **kwargs)
>>> class TeamObject(BaseObject, metaclass=TeamMeta):
...   pass
>>> try:
...   class Report(TeamObject):
...     _cache = None
... except NameError as error:
...   print('refused', error)
refused Report._cache

```

`setItemPhase(key, value, old)` runs before each binding of a class
body. Raising refuses the binding at its line; returning `True` claims
it, and the class does not receive the name; returning `False` leaves it
alone. Inside a phase `self.space` is the namespace of the class
statement in progress. The other phases are `preparePhase`,
`getItemPhase`, `delItemPhase`, `preCompilePhase`, `postCompilePhase`
and `newClassPhase`.

The hook screens the class declaring the metaclass as well as its
subclasses, and worktoy's own checks of section 4 keep running beside
it. One hook object serves every class statement of its namespace, so
it keeps what it learns on `self.space`, never on itself.
