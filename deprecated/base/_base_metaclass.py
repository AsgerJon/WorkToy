"""BaseMetaclass provides the metaclass for the BaseObject class. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace
from worktoy.abstract import AbstractFlag
from worktoy.base import LoadSpace
from worktoy.mcls import AbstractMetaclass, Base
from worktoy.waitaminute import AbstractInstantiationException

try:
  from typing import Any
except ImportError:
  Any = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Callable
except ImportError:
  Callable = object

if TYPE_CHECKING:
  FuncList = list[Callable]
else:
  FuncList = object


class BaseMetaclass(AbstractMetaclass):
  """BaseMetaclass provides the metaclass for the BaseObject class. """

  __abstract_methods__ = None

  isAbstract = AbstractFlag()

  def getAbstractMethods(cls, ) -> FuncList:
    """Return a list of abstract methods in the class."""
    out = getattr(cls, '__abstract_methods__', None)
    if out is None:
      e = """The attribute '__abstract_methods__' is not set on the 
      class: '%s'!""" % cls.__name__
      raise AttributeError(monoSpace(e))
    return [v for (k, v) in out.items()]

  @isAbstract.GET
  def _getIsAbstract(cls, ) -> bool:
    """Return the value of the isAbstract flag."""
    abstractMethods = cls.getAbstractMethods()
    return True if abstractMethods else False

  @classmethod
  def __prepare__(mcls, name: str, bases: Base, **kwargs) -> LoadSpace:
    """The '__prepare__' method is called before the class is created and
    returns the class namespace. """
    return LoadSpace(mcls, name, bases, **kwargs)

  def __call__(cls, *args, **kwargs) -> Any:
    """The '__call__' method is invoked when the class is called. """
    if cls._getIsAbstract():
      raise AbstractInstantiationException(cls, *args, **kwargs)
    return AbstractMetaclass.__call__(cls, *args, **kwargs)
