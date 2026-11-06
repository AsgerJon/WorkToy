"""
Sentinel is the base class for sentinel objects, built by the
'SentinelMeta' metaclass.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import maybe
from ...waitaminute.meta import IllegalInstantiation, DuplicateSentinel
from .. import MetaType

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Self, Never

  Bases = tuple[type, ...]


class SentinelMeta(MetaType, metaclass=MetaType):
  """
  Code often needs a marker that no real value can be mistaken for: a
  value meaning deleted, not given, or the class being defined. Such a
  marker must be unique, compared by identity, readable in a traceback,
  and impossible to instantiate, since an instance would be a second
  object claiming the same meaning. A marker also means one thing in the
  whole process: two files declaring a marker of the same name must not
  end up with two objects of one meaning, nor share one object without
  knowing it. A project building on worktoy must be able to declare
  markers of its own, and families of markers that carry behaviour.

  Implementation
  --------------

  A sentinel is a class whose metaclass is 'SentinelMeta', and the class
  object itself is the marker. '__new__' refuses a name the registry
  already holds with 'DuplicateSentinel' and registers every new
  sentinel, the family bases included, in one registry kept on
  'SentinelMeta' itself and shared by every metaclass based on it.
  '__call__' raises 'IllegalInstantiation'; a family whose members must
  be instantiable, as that of 'ARGS', reimplements it. Equality is
  identity, the hash is taken from the modules and names of the sentinel
  and its metaclass, and the text reads "<Sentinel: 'NAME'>".
  'SentinelMeta' is a subclass and an instance of 'MetaType', so a
  sentinel declared with a class keyword has the keyword absorbed by
  '_Chill'.

  Attributes
  ----------

  __registered_sentinels__ : list or None
    The registry of sentinel classes, created on the first registration.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __registered_sentinels__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getRegisteredSentinels(mcls) -> list[Self]:
    """
    Every family of sentinels must share one registry, or two families
    could hold one name between them.

    Implementation
    --------------

    The registry is read off 'SentinelMeta' by name, not off 'mcls', so a
    metaclass based on 'SentinelMeta' reads the same list.

    Returns
    -------

    list[SentinelMeta]
      The registered sentinels, or an empty list.
    """
    return maybe(SentinelMeta.__registered_sentinels__, [])

  @classmethod
  def _getNamedSentinel(mcls, sentinelName: str, ) -> Self:
    existing = mcls._getRegisteredSentinels()
    for existingSentinel in existing:
      if existingSentinel.__name__ == sentinelName:
        return existingSentinel
    raise KeyError(sentinelName)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _registerSentinel(mcls, sentinel: Self) -> None:
    existing = mcls._getRegisteredSentinels()
    SentinelMeta.__registered_sentinels__ = [*existing, sentinel]

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    return dict()

  def __new__(mcls, name: str, bases: Bases, space: dict, **kwargs) -> Self:
    """
    A sentinel name stands for one meaning in the whole process, so a
    second class statement at a name already taken is a mistake, wherever
    it is written: the existing sentinel is the one to import.

    Implementation
    --------------

    The name is checked before the class is built and registered after,
    so a class statement failing in between leaves no trace.

    Parameters
    ----------

    name : str
      The name of the sentinel.

    bases : Bases
      A 'tuple[type, ...]' of the bases.

    space : dict
      The class body.

    **kwargs
      Class keywords, passed on to 'MetaType.__new__'.

    Returns
    -------

    SentinelMeta
      The new sentinel.

    Raises
    ------

    DuplicateSentinel
      A sentinel of the name is already registered.
    """
    try:
      existing = mcls._getNamedSentinel(name)
    except KeyError:
      pass
    else:
      raise DuplicateSentinel(name, existing, space.get('__module__', None))
    cls = super().__new__(mcls, name, bases, space, **kwargs)
    mcls._registerSentinel(cls)
    return cls

  def __call__(cls, *__, **_) -> Never:
    """
    A sentinel is the class object itself, and an instance would be a
    second object claiming its meaning.

    Implementation
    --------------

    Every call is refused.

    Raises
    ------

    IllegalInstantiation
      Always.
    """
    raise IllegalInstantiation(cls)

  def __hash__(cls, ) -> int:
    mcls = type(cls)
    mclsModule = getattr(mcls, '__module__')
    clsModule = getattr(cls, '__module__')
    mclsName = mcls.__name__
    clsName = cls.__name__
    return hash((mclsModule, mclsName, clsModule, clsName,))

  def __str__(cls) -> str:
    return """<Sentinel: '%s'>""" % cls.__name__

  __repr__ = __str__


class Sentinel(metaclass=SentinelMeta):
  """
  A project declaring a sentinel of its own needs a base to declare it
  on, as in 'class PENDING(Sentinel)', with a docstring and nothing else.

  Implementation
  --------------

  'Sentinel' has no body; 'SentinelMeta' gives every subclass its
  behaviour. The name 'Sentinel' is itself registered, so no sentinel may
  take it.
  """
