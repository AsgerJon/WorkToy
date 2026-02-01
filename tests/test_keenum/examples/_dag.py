"""
Dag is a simple class used by the 'Ugedag' example class. It serves to
facilitate testing of 'AttriBox'-like functionality of the 'Kee' helper
class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import Field
from worktoy.utilities import textFmt
from worktoy.waitaminute import MissingVariable, TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator, Optional


class _MetaDag(type):
  """
  The metaclass implements '__len__'.
  """

  __instance_registry__: Optional[tuple[Dag, ...]] = None

  def _createRegistry(cls, ) -> None:
    cls.__instance_registry__ = ()

  def resetRegistry(cls, ) -> None:
    cls.__instance_registry__ = None

  def getInstanceRegistry(cls, **kwargs) -> tuple[Dag, ...]:
    if cls.__instance_registry__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      cls._createRegistry()
      return cls.getInstanceRegistry(_recursion=True)
    if isinstance(cls.__instance_registry__, tuple):
      for dag in cls.__instance_registry__:
        if not isinstance(dag, cls):
          break
      else:
        return cls.__instance_registry__
      raise TypeException('dag', dag, cls)
    name, value = '__instance_registry__', cls.__instance_registry__
    raise TypeException(name, value, tuple)

  def registerInstance(cls, self: Dag) -> None:
    existing = cls.getInstanceRegistry()
    if self in existing:
      return
    cls.__instance_registry__ = (*existing, self)

  def __call__(cls, *args, **kwargs) -> Dag:
    self = super().__call__(*args, **kwargs)
    cls.registerInstance(self)
    return self

  def __iter__(cls, ) -> Iterator[object]:
    yield from cls.getInstanceRegistry()

  def __len__(cls, ) -> int:
    return len((*cls.getInstanceRegistry(),))

  def __contains__(cls, item: Any) -> bool:
    for instance in cls.getInstanceRegistry():
      if instance == item:
        return True
    return False

  def __int__(cls, ) -> int:
    return len(cls)


class Dag(metaclass=_MetaDag):
  """
  Dag is a simple class used by the 'Ugedag' example class. It serves to
  facilitate testing of 'AttriBox'-like functionality of the 'Kee' helper
  class.
  """
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __instance_registry__ = None

  #  Fallback Variables

  #  Private Variables
  __name_str__ = None

  #  Public Variables
  name = Field()

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @name.GET
  def _getName(self, ) -> str:
    if self.__name_str__ is None:
      raise MissingVariable(self, '__name_str__', str)
    if isinstance(self.__name_str__, str):
      return self.__name_str__
    raise TypeException('__name_str__', self.__name_str__, str)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __str__(self, ) -> str:
    infoSpec = """<%s: name='%s'>"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.name)
    return textFmt(info)

  def __repr__(self, ) -> str:
    infoSpec = """%s('%s')"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.name)
    return textFmt(info)

  def __hash__(self, ) -> int:
    clsName = type(self).__name__
    return hash((clsName, self.name))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    if args:
      self.__name_str__ = args[0]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
