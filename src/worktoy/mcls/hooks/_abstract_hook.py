"""
AbstractHook provides an abstract baseclass for hooks used by the
namespaces in the metaclass system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...static import AbstractObject, Alias

try:
  from typing import TYPE_CHECKING, Type
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable
  from worktoy.mcls import AbstractNamespace as ASpace

  AccessorHook = Callable[[ASpace, str, Any], Any]
  CompileHook = Callable[[ASpace, dict], dict]


class AbstractHook(AbstractObject):
  """
  AbstractHook is the abstract base class for defining hook objects
  used in conjunction with AbstractNamespace. These hooks enable modular,
  stage-specific interception during class body evaluation and namespace
  compilation within the metaclass system.

  ## Purpose

  Hooks allow custom behavior to be injected into the class construction
  pipeline without modifying the namespace or metaclass core logic. They
  are used to observe and/or alter how names are accessed, assigned, or
  compiled into the final class definition.

  ## Integration

  To activate a hook, simply instantiate a subclass of AbstractHook inside
  the body of a namespace class (i.e., a subclass of AbstractNamespace).
  The descriptor protocol (`__set_name__`) ensures the hook registers
  itself with the namespace automatically at definition time.

  Example:

      class MyNamespace(AbstractNamespace):
        overloadHook = OverloadHook()
        validationHook = ReservedNameHook()

  ## Lifecycle Hook Methods

  Subclasses may override any of the following methods to participate in
  different stages of the namespace lifecycle. All are optional.

  - `setItemHook(self, key, value, oldValue) -> bool`
    Called just before a name is set in the namespace.
    Returning True blocks the default behavior.

  - `getItemHook(self, key, value) -> bool`
    Called just before a name is retrieved from the namespace.
    Returning True blocks the default behavior.

  - `preCompileHook(self, compiled: dict) -> dict`
    Called after the class body finishes executing, but before the
    namespace is finalized. May transform or replace namespace contents.

  - `postCompileHook(self, compiled: dict) -> dict`
    Called immediately before the finalized namespace is handed off to the
    metaclass. Can be used for final transformations or validation.

  ## Descriptor Behavior

  AbstractHook implements the descriptor protocol. When accessed via a
  namespace class, it is bound with the following attributes:

  - `self.space` refers to the active namespace instance.
  - `self.spaceClass` refers to the namespace class itself.

  These attributes can be used to introspect the environment the hook is
  participating in.

  ## Extension Notes

  Subclasses are expected to override only the relevant hook methods.
  If none are overridden, the hook has no effect.

  The `addHook()` method of the namespace class is automatically invoked
  during registration. Hook authors do not need to call it manually.
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
