"""
AbstractSpaceHook is the base class for the namespace hooks.
"""
#  Apache-2.0 license
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
    """
    The 'preparePhase' method runs during the namespace object's
    '__init__'. This phase does not allow changes to the namespace;
    raise an exception to interrupt the flow. The default does nothing.
    """

  def getItemPhase(self, key: str, value: Any, ) -> bool:
    """
    The 'getItemPhase' method runs during '__getitem__', after the value
    is fetched and before it is returned. Its return value is ignored
    (unlike 'setItemPhase'); raise an exception to interrupt. The default
    does nothing.
    """

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    The 'setItemPhase' method runs before a name is bound in the
    namespace. Returning True blocks the namespace's own assignment. The
    default does nothing and returns False.
    """

  def preCompilePhase(self, compiledSpace: dict) -> dict:
    """
    The 'preCompilePhase' method runs during 'compile()', before the
    class-body names are merged into the namespace dict. It receives that
    dict and must return it; the default returns it unchanged.
    """
    return compiledSpace

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """
    The 'postCompilePhase' method runs during 'compile()', after the
    class-body names are merged into the namespace dict. It receives the
    assembled dict and must return it; the default returns it unchanged.
    """
    return compiledSpace

  def newClassPhase(self, cls: Meta, ) -> Meta:  # NOQA
    """
    The 'newClassPhase' method is the final phase, invoked by the
    metaclass after it has created the new class object but before
    returning it, ahead of the normal post-class-creation flow. The
    default returns the class unchanged.
    """
    return cls

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: Space, name: str, **kwargs) -> None:
    """
    The '__set_name__' method runs the 'Object' registration and then
    registers this hook with the owning namespace class via 'addHook',
    so hook authors never call 'addHook' by hand.
    """
    super().__set_name__(owner, name, )
    owner.addHook(self)

  def __get__(self, instance: ASpace, owner: Space, **kwargs) -> Any:
    """
    Accessed on a namespace instance, '__get__' binds
    '__space_object__' to that instance and returns the hook, so the
    'space' property resolves to the active namespace during the hook's
    calls.
    """
    self.__space_object__ = instance
    return self
