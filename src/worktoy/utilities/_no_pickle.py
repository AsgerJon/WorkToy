"""
NoPickle is the mixin through which the classes of 'worktoy' refuse the
pickle protocol while staying copyable.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Iterator, Never, Self


def _refusal(obj: Any, action: str) -> Exception:
  """Build a 'PickleException'.

  The import is deferred so 'utilities' does not pull in
  'waitaminute' at module load time.
  """
  from ..waitaminute import PickleException
  return PickleException(obj, action)


def _blank(cls: type) -> Any:
  """Make an instance of 'cls' without calling any Python code of the
  class: the nearest '__new__' along the method resolution order that is
  not defined in Python, which is that of 'object', 'dict' or
  'BaseException' for the classes of 'worktoy'. A '__new__' written in
  Python may expect arguments or return something else entirely, as that
  of 'overload' does. The walk always ends at 'object', whose '__new__'
  qualifies."""
  mro = cls.__mro__
  news = [k.__dict__['__new__'] for k in mro if '__new__' in k.__dict__]
  native = [new for new in news if not isinstance(new, staticmethod)]
  return native[0](cls)


def _mangled(klass: type, name: str) -> str:
  """The name under which instances store the slot 'name' that 'klass'
  declares. Python mangles a private name, one with two leading
  underscores and not two trailing ones, by prefixing an underscore and
  the name of the class without its own leading underscores; a class
  named with underscores alone mangles nothing."""
  if not name.startswith('__') or name.endswith('__'):
    return name
  owner = klass.__name__.lstrip('_')
  return '_%s%s' % (owner, name) if owner else name


def _slotNames(cls: type) -> Iterator[str]:
  """The names under which instances of 'cls' store the slots the
  classes along its method resolution order declare, the '__dict__' and
  '__weakref__' slots aside."""
  for klass in cls.__mro__:
    slots = klass.__dict__.get('__slots__', ())
    if isinstance(slots, str):
      slots = (slots,)
    for name in slots:
      if name not in ('__dict__', '__weakref__'):
        yield _mangled(klass, name)


def _fill(source: Any, target: Any, copier: Callable) -> None:
  """Give 'target' the state of 'source', each value passed through
  'copier': the arguments of an exception, the slot values, the instance
  dict and the items of a 'dict'. The values are written past any
  '__setattr__' or '__setitem__' of the class."""
  if isinstance(source, BaseException):
    object.__setattr__(target, 'args', copier(source.args))
  for name in _slotNames(type(source)):
    try:
      value = object.__getattribute__(source, name)
    except AttributeError:
      continue
    object.__setattr__(target, name, copier(value))
  try:
    sourceDict = object.__getattribute__(source, '__dict__')
  except AttributeError:
    pass
  else:
    targetDict = object.__getattribute__(target, '__dict__')
    for key, value in sourceDict.items():
      targetDict[key] = copier(value)
  if isinstance(source, dict):
    for key, value in dict.items(source):
      dict.__setitem__(target, copier(key), copier(value))


def _same(value: Any) -> Any:
  """The copier of a shallow copy, which keeps each value itself."""
  return value


class NoPickle:
  """
  NoPickle is the mixin through which the classes of 'worktoy' refuse to be
  pickled. Unpickling rebuilds an object from the state stored with it,
  without calling its class, so every check the class and its metaclass
  perform on construction and on assignment is skipped: an enumeration
  member comes back as a second member that equals none of the real ones,
  and a frozen or type-enforced object holds whatever the stream says.
  Pickling an object, by any protocol, raises 'PickleException', and so
  does a stream trying to restore state into one.

  The 'copy' module falls back on the same reduce protocol, so the
  refusal alone would stop every copy as well. 'NoPickle' therefore copies
  by itself, the way that protocol did: a new instance, made without
  calling '__init__', holding the arguments of an exception, the slot
  values, the instance dict and the items of a 'dict' of the original,
  shallow or deep, written past '__setattr__'. A class whose instances a
  copy must not duplicate defines its own '__copy__' and '__deepcopy__'
  returning 'self': an enumeration, whose members are unique, and the
  boxes of 'worktoy.desc' ('AttriBox' and the classes based on it), each
  of which belongs to the class it is declared on.

  The mixin declares 'NoPickle.__slots__ = ()', which adds nothing to an
  instance and restricts nothing. Python gives the instances of a class an
  instance dict unless every class along its method resolution order,
  'object' aside, declares '__slots__'. A class based on 'NoPickle' that
  declares no slots of its own therefore gets its instance dict, and its
  '__weakref__', exactly as it would without the mixin, and takes any
  attribute; this is the case of 'Object' and every 'BaseObject'. A class
  that does declare slots, such as 'ExceptionInfo', stays slot-only, since
  the empty slots of the mixin leave its layout as the class declares it.
  A mixin without '__slots__' would instead hand an instance dict to every
  class it is mixed into, and quietly undo the slots of such a class.

  One consequence reads oddly: every class based on 'NoPickle' has a
  '__slots__' attribute, inherited from the mixin, whether or not its
  instances have an instance dict. Whether a class declares '__slots__'
  therefore says nothing about its instances; whether an instance has an
  instance dict is found on the instance itself.
  """

  __slots__ = ()

  def __reduce_ex__(self, protocol: int) -> Never:
    raise _refusal(self, 'pickled')

  def __reduce__(self) -> Never:
    raise _refusal(self, 'pickled')

  def __getstate__(self) -> Never:
    raise _refusal(self, 'pickled')

  def __setstate__(self, state: Any) -> Never:
    raise _refusal(self, 'unpickled')

  def __copy__(self) -> Self:
    copied = _blank(type(self))
    _fill(self, copied, _same)
    return copied

  def __deepcopy__(self, memo: dict) -> Self:
    copied = _blank(type(self))
    memo[id(self)] = copied

    def copier(value: Any) -> Any:
      return deepcopy(value, memo)

    _fill(self, copied, copier)
    return copied
