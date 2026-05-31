"""
Sentinel is the base class for sentinel objects, built by the
'SentinelMeta' metaclass.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import maybe
from ...waitaminute.meta import IllegalInstantiation

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Never

  Bases = tuple[type, ...]


class SentinelMeta(type):
  """
  SentinelMeta is the metaclass for sentinel classes. It registers each
  sentinel by name, returns the existing sentinel when a name is reused,
  and prevents its classes from being instantiated.
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
  def _getNamedSentinel(cls, sentinelName: str, ) -> Self:
    """
    Returns registered sentinel having this name.
    """
    existing = cls._getRegisteredSentinels()
    for existingSentinel in existing:
      if existingSentinel.__name__ == sentinelName:
        return existingSentinel
    raise KeyError(sentinelName)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _registerSentinel(mcls, sentinel: Self) -> None:
    """Records 'sentinel' in the registry, so a later class statement reusing
    its name receives the existing sentinel instead of building a second one
    of the same name."""
    existing = mcls._getRegisteredSentinels()
    mcls.__registered_sentinels__ = [*existing, sentinel]

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    return dict()

  def __new__(mcls, name: str, bases: Bases, space: dict, **kwargs) -> Self:
    """Returns the sentinel class for 'name', building and registering it on
    first use and handing back the already-registered class whenever the name
    is reused."""
    try:
      cls = mcls._getNamedSentinel(name)
    except KeyError as keyError:
      if kwargs.get('_recursion', False):
        raise keyError from RecursionError
      namespace = dict()
      cls = super().__new__(mcls, name, (), namespace, **kwargs)
      mcls._registerSentinel(cls)
      return mcls.__new__(mcls, name, (), {}, _recursion=True)
    else:
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
  that only one sentinel of each name exists.
  """
