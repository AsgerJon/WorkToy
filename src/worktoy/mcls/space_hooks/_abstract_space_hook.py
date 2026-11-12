"""
AbstractSpaceHook is the base class for the namespace hooks.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import SpaceDesc
from ...core import Object, MetaType

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, TypeAlias, Union, Optional
  from .. import AbstractMetaclass
  from .. import AbstractNamespace as ASpace

  MaybeSpace: TypeAlias = Optional[ASpace]
  Meta: TypeAlias = Union[MetaType, AbstractMetaclass, type]
  from .. import AbstractNamespace


class AbstractSpaceHook(Object):
  """
  A worktoy namespace must be able to screen and transform the class
  body as it runs and as it is compiled: refuse a misspelled dunder at
  its line, claim '@overload' declarations so one name may be bound
  several times, turn declarations into dispatchers. Each such job must
  be a separate piece, declared in the body of a namespace class, so a
  namespace is assembled from the jobs it needs, and a project may write
  a job of its own.

    class MySpace(AbstractNamespace):
      nameHook = NamespaceHook()

  Implementation
  --------------

  A hook registers itself with its namespace class in '__set_name__'.
  The namespace calls each hook at each phase, and a hook reimplements
  the phases it needs; the defaults do nothing:

  - 'preparePhase(space)' as the namespace is created; it may refuse by
    raising, not change anything.
  - 'setItemPhase(key, value, old)' before a binding; 'True' claims it,
    and the namespace does not store it.
  - 'getItemPhase(key, value)' on a read; it may refuse by raising.
  - 'delItemPhase(key, value)' before a deletion; 'True' claims it.
  - 'preCompilePhase(compiled)' and 'postCompilePhase(compiled)' before
    and after the names of the body are merged into the dictionary for
    'type.__new__'; each returns the dictionary.
  - 'newClassPhase(cls)' after the class is created, returning it.

  Inside a phase, 'self.space' is the namespace. One hook object serves
  every class its namespace class builds, so it keeps the state of a
  class body on the namespace, not on itself.

  Attributes
  ----------

  space : AbstractNamespace
    The namespace the hook is working for.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public variables
  space: SpaceDesc[AbstractNamespace] = SpaceDesc()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preparePhase(self, space: ASpace, ) -> None:
    """
    A hook may need to refuse a class before its body runs.

    Implementation
    --------------

    The default does nothing.

    Parameters
    ----------

    space : AbstractNamespace
      The new namespace.
    """

  def getItemPhase(self, key: str, value: Any, ) -> None:
    """
    A hook may need to refuse a read in the class body.

    Implementation
    --------------

    The default does nothing; a return value is ignored.

    Parameters
    ----------

    key : str
      The name read.

    value : Any
      The value found, or the 'KeyError' of a miss.
    """

  def delItemPhase(self, key: str, val: Any = None, ) -> bool:
    """
    A hook that claimed a binding may need to take care of its deletion.

    Implementation
    --------------

    The default claims nothing.

    Parameters
    ----------

    key : str
      The name deleted.

    val : Any
      The value removed.

    Returns
    -------

    bool
      'True' to claim the deletion.
    """
    return False

  def setItemPhase(self, key: str, val: Any, old: Any = None, ) -> bool:
    """
    A hook may need to refuse a binding in the class body, or take the
    value for itself instead of the namespace storing it.

    Implementation
    --------------

    The default claims nothing. The first hook claiming a binding hides it
    from the hooks after it.

    Parameters
    ----------

    key : str
      The name bound.

    val : Any
      The value bound.

    old : Any, optional
      The value the name held, or 'None'.

    Returns
    -------

    bool
      'True' to claim the binding.
    """
    return False

  def preCompilePhase(self, compiledSpace: dict) -> dict:
    """
    A hook may need to give the class a default that the class body can
    still override.

    Implementation
    --------------

    The names of the body are merged in after this phase, so they replace
    what it added. The default changes nothing.

    Parameters
    ----------

    compiledSpace : dict
      The dictionary being assembled.

    Returns
    -------

    dict
      The dictionary.
    """
    return compiledSpace

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """
    A hook may need to transform what the class body bound, as building
    the dispatchers of overloaded names.

    Implementation
    --------------

    The names of the body are merged in before this phase, so what it
    writes replaces them. The default changes nothing.

    Parameters
    ----------

    compiledSpace : dict
      The dictionary being assembled.

    Returns
    -------

    dict
      The dictionary.
    """
    return compiledSpace

  def newClassPhase(self, cls: Meta, ) -> Meta:  # NOQA
    """
    A hook may need to act on the finished class before the metaclass
    returns it.

    Implementation
    --------------

    The default returns the class unchanged.

    Parameters
    ----------

    cls : Meta
      The new class.

    Returns
    -------

    Meta
      The class.
    """
    return cls

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    A hook declared in a namespace class body must take part without
    further code.

    Implementation
    --------------

    The hook is registered with 'owner.addHook'. Placed in a class that is
    not a namespace class, it fails for want of 'addHook'.
    """
    super().__set_name__(owner, name, **kwargs)
    if TYPE_CHECKING:  # pragma: no cover, no mutate
      assert isinstance(owner, type)
      assert issubclass(owner, AbstractNamespace)
    owner.addHook(self)

  def __get__(self, instance: MaybeSpace, owner: type, **kwargs) -> Any:
    """
    A hook read through a namespace must work on that namespace.

    Implementation
    --------------

    The namespace is recorded as the one 'self.space' gives, and the hook
    returned. Through the namespace class, the hook is returned as it is.
    """
    if instance is None:
      return self
    self.space = instance
    return self
