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

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Never

  Bases = tuple[type, ...]


class SentinelMeta(type):
  """
  SentinelMeta is the metaclass for sentinel classes. It registers each
  sentinel by name, refuses a second class statement at a registered name
  with 'DuplicateSentinel', and prevents its classes from being
  instantiated. A sentinel defines one concept for the whole process, so
  the registry holds one sentinel per name wherever it was declared, and
  the existing one is the one to import.
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
    """The sentinel classes registered so far, or an empty list when none
    have been registered yet."""
    return maybe(mcls.__registered_sentinels__, [])

  @classmethod
  def _getNamedSentinel(mcls, sentinelName: str, ) -> Self:
    """
    Returns the registered sentinel having this name, or raises 'KeyError'
    when none has it.
    """
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
    """Records 'sentinel' in the registry, so a later class statement at
    its name is refused instead of building a second sentinel of the
    name."""
    existing = mcls._getRegisteredSentinels()
    mcls.__registered_sentinels__ = [*existing, sentinel]

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    return dict()

  def __new__(mcls, name: str, bases: Bases, space: dict, **kwargs) -> Self:
    """Builds and registers the sentinel class for 'name'. A name a
    sentinel already holds is refused with 'DuplicateSentinel', naming the
    existing sentinel and the module of the refused class statement, since
    a sentinel defines one concept for the whole process."""
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
    Raises 'IllegalInstantiation'.
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
  Sentinel is the base class for all sentinel objects in the
  'worktoy.core.sentinels' package. It prevents instantiation and ensures
  that only one sentinel of each name exists: a sentinel defines one
  concept for the whole process, and a second class statement at a
  registered name raises 'DuplicateSentinel'.
  """
