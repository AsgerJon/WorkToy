"""
AbstractSpaceHook provides an abstract baseclass for hooks used by the
namespaces in the metaclass system.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import SpaceDesc
from ...core import Object

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias, Type, Union, Optional
  from .. import AbstractNamespace as ASpace

  AccessorHook = Callable[[ASpace, str, Any], Any]
  CompileHook = Callable[[ASpace, dict], dict]
  Space: TypeAlias = Type[ASpace]
  Desc: TypeAlias = Union[ASpace, SpaceDesc]
  MaybeSpace: TypeAlias = Optional[ASpace]
  Meta: TypeAlias = Type[type]
  from .. import AbstractNamespace


class AbstractSpaceHook(Object):
  """
  AbstractSpaceHook is the abstract base class for defining hook objects
  used in conjunction with 'AbstractNamespace'. These hooks enable
  modular, stage-specific interception during class body evaluation and
  namespace compilation within the metaclass system.

  Purpose
  -------
  Hooks allow custom behavior to be injected into the class construction
  pipeline without modifying the namespace or metaclass core logic. They
  observe and alter how names are accessed, assigned, or compiled into
  the final class definition.

  Integration
  -----------
  To activate a hook, instantiate a subclass of 'AbstractSpaceHook'
  inside the body of a namespace class (a subclass of
  'AbstractNamespace'). The descriptor protocol ('__set_name__') ensures
  the hook registers itself with the namespace automatically at
  definition time:

      class MyNamespace(AbstractNamespace):
        nameHook = NamespaceHook()
        reservedNameHook = ReservedNamespaceHook()

  Lifecycle hook methods
  ----------------------
  Subclasses may override any of the following methods to participate in
  different stages of the namespace lifecycle. All are optional.

  - 'preparePhase(self, space) -> None'
    Called during '__init__' of the namespace object. This phase does
    not allow changes to the namespace. Raise an exception to interrupt.

  - 'setAnnotationPhase(self, key, value) -> Any'
    Called when the namespace encounters an annotation. With
    'from __future__ import annotations' enabled, this method may be
    called with a string naming an as-yet unavailable type. The return
    value is ignored.

  - 'setItemPhase(self, key, value, oldValue) -> bool'
    Called just before a name is set in the namespace. Returning True
    blocks the default behavior.

  - 'getItemPhase(self, key, value) -> bool'
    Called just before a name is retrieved from the namespace.

  - 'preCompilePhase(self, compiled: dict) -> dict'
    Called after the class body finishes executing, but before the
    namespace is finalized. May transform or replace namespace contents.

  - 'postCompilePhase(self, compiled: dict) -> dict'
    Called immediately before the finalized namespace is handed off to
    the metaclass. Used for final transformations or validation.

  - 'newClassPhase(self, cls) -> type'
    Called after the metaclass has created the new class object, but
    before returning it.

  Descriptor behavior
  -------------------
  'AbstractSpaceHook' implements the descriptor protocol. When accessed
  via a namespace instance, the descriptor returns the hook with its
  '__space_object__' attribute bound to that namespace. The 'space'
  property exposes this binding so subclasses can introspect the active
  namespace.

  Extension notes
  ---------------
  Subclasses are expected to override only the relevant hook methods.
  If none are overridden, the hook has no effect.

  The 'addHook' method of the namespace class is automatically invoked
  during registration via '__set_name__'. Hook authors do not need to
  call it manually.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __space_object__: Optional[AbstractNamespace] = None

  #  Public variables
  space: SpaceDesc[AbstractNamespace] = SpaceDesc()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preparePhase(self, space: ASpace, ) -> None:
    """Hook for prepare. This runs during the __init__ method of the
    namespace object. This phase does not allow changes to the namespace,
    to interrupt the flow, raise an exception. """

  def setAnnotationPhase(self, key: str, value: Any, ) -> Any:
    """Hook for setAnnotation. This is called when the namespace encounters
    an annotation. The default implementation does nothing and returns the
    value unchanged. If you want to block the annotation, raise an exception.
    """

  def getItemPhase(self, key: str, value: Any, ) -> bool:
    """Hook for getItem. This is called before the __getitem__ method of
    the namespace object is called. The default implementation does nothing
    and returns False. """

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """Hook for setItem. This is called before the __setitem__ method of
    the namespace object is called. The default implementation does nothing
    and returns False. """

  def preCompilePhase(self, compiledSpace: dict) -> dict:
    """Hook for preCompile. This is called before the __init__ method of
    the namespace object is called. The default implementation does nothing
    and returns the contents unchanged. """
    return compiledSpace

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """Hook for postCompile. This is called after the __init__ method of
    the namespace object is called. The default implementation does nothing
    and returns the contents unchanged. """
    return compiledSpace

  def newClassPhase(self, cls: Meta, ) -> Meta:  # NOQA
    """
    Final phase invoked by the metaclass after it has created the new
    class object, but before returning it. This phase occurs before the
    normal post class creation flow continues.
    """
    return cls

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: Space, name: str, **kwargs) -> None:
    """
    After the super call, adds one self to the namespace class as a hook
    class.
    """
    super().__set_name__(owner, name, )
    owner.addHook(self)

  def __get__(self, instance: ASpace, owner: Space, **kwargs) -> Any:
    """
    Descriptor protocol method. Returns the bound hook instance with
    `space` and `spaceClass` attributes set to the current namespace
    instance and its class.
    """
    self.__space_object__ = instance
    return self
