"""
AbstractHook provides an abstract baseclass for hooks used by the
namespaces in the metaclass system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func

from ...static import AbstractObject, Alias
from ...waitaminute import MissingVariable, ReadOnlyError

try:
  from typing import TYPE_CHECKING, Type
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self, Callable, Self, Never
  from worktoy.mcls import AbstractNamespace as ASpace

  AccessorHook = Callable[[ASpace, str, Any], Any]
  CompileHook = Callable[[ASpace, dict], dict]


class AbstractHook(AbstractObject):
  """
  AbstractHook provides an abstract baseclass for hooks used by the
  namespaces in the metaclass system. These hooks allow modification of the
  class creation process. The following static methods are expected from the
  hooks:
  - setItem: called before calls to __setitem__ on the namespace object.
  - getItem: called before calls to __getitem__ on the namespace object.
  - preCompile: called before the final namespace object is populated with
    the conventional key, value pairs.
  - postCompile: called after the final namespace object is populated with
    the conventional key, value pairs.

  Subclasses may implement either of the above methods. The default
  implementations have no effect, so subclasses need only implement the
  methods they are interested in.

  AbstractHook implements the descriptor protocol such that calls to
  '__get__' receive:
  - instance: The current instance of the namespace object.
  - owner: The current namespace class

  Subclasses should be made available as attributes on the namespace
  subclass.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables
  space = Alias('instance')
  spaceClass = Alias('owner')

  #  TYPE_CHECKING
  if TYPE_CHECKING:
    from . import AbstractHook
    from .. import AbstractNamespace
    assert isinstance(AbstractHook.space, AbstractNamespace)
    assert issubclass(AbstractHook.spaceClass, AbstractNamespace)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def getItemHook(self, key: str, value: Any, ) -> bool:
    """Hook for getItem. This is called before the __getitem__ method of
    the namespace object is called. The default implementation does nothing
    and returns False. """

  def setItemHook(self, key: str, value: Any, oldValue: Any, ) -> bool:
    """Hook for setItem. This is called before the __setitem__ method of
    the namespace object is called. The default implementation does nothing
    and returns False. """

  def preCompileHook(self, compiledSpace: dict) -> dict:
    """Hook for preCompile. This is called before the __init__ method of
    the namespace object is called. The default implementation does nothing
    and returns the contents unchanged. """
    return compiledSpace

  def postCompileHook(self, compiledSpace: dict) -> dict:
    """Hook for postCompile. This is called after the __init__ method of
    the namespace object is called. The default implementation does nothing
    and returns the contents unchanged. """
    return compiledSpace

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    After the super call, adds one self to the namespace class as a hook
    class.
    """
    super().__set_name__(owner, name, **kwargs)
    self.spaceClass.addHook(self)
