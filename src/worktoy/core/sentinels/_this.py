"""
THIS is a sentinel placeholder for the enclosing class, resolved
contextually by the descriptor flow, and 'THIS[Parent].name' a deferred
reference to the descriptor 'name' that 'Parent' holds, as the class
being built will hold it.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from . import Sentinel
from ...waitaminute import TypeException, MissingVariable
from ...waitaminute.desc import DanglingAlias

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional, TypeVar, TypeAlias
  from ...desc import BaseDescriptor

  Descriptors: TypeAlias = dict[str, BaseDescriptor]

  #  'F' keeps a decorated function its own type for a checker, which
  #  the roles below declare; 'T' lets 'THIS[Parent]' resolve to
  #  'type[Parent]', so 'THIS[Parent].x' is 'Parent.x' statically.
  F = TypeVar('F', bound=Callable[..., Any])
  T = TypeVar('T')


class _SetDescriptorName:
  __parent_class__: Optional[type] = None
  __descriptor_name__: Optional[str] = None
  __new_descriptor__: Optional[BaseDescriptor] = None

  @classmethod
  def newDescriptorsOnParent(cls, parent: type, **kwargs) -> Descriptors:
    """
    Returns the record of references 'parent' holds itself, creating an
    empty one when it holds none.
    """
    key: str = """__new_descriptors__"""
    try:
      descriptors: Descriptors = parent.__dict__[key]
    except KeyError:
      if kwargs.get('_recursion', False):
        raise RecursionError
      type.__setattr__(parent, key, dict())
      return cls.newDescriptorsOnParent(parent, _recursion=True)
    else:
      return descriptors

  def _getParent(self) -> type:
    """
    Returns the parent class of this deferred THIS, or raises
    'MissingVariable' when it has not been set yet.
    """
    if self.__parent_class__ is None:
      raise MissingVariable(self, '__parent_class__', type)
    return self.__parent_class__

  def _getDescriptorName(self) -> str:
    """
    Returns the real name of this deferred THIS, or raises
    'MissingVariable' when it has not been set yet.
    """
    if self.__descriptor_name__ is None:
      raise MissingVariable(self, '__descriptor_name__', str)
    return self.__descriptor_name__

  def getParentDescriptor(self, ) -> BaseDescriptor:
    return self._getParent().__dict__[self._getDescriptorName()]

  def getNewDescriptor(self, **kwargs) -> BaseDescriptor:
    if self.__new_descriptor__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__new_descriptor__ = self.getParentDescriptor().clone()
      return self.getNewDescriptor(_recursion=True)
    return self.__new_descriptor__

  def __init__(self, parent: type, key: str) -> None:
    self.__parent_class__ = parent
    self.__descriptor_name__ = key
    self.getNewDescriptor()

  def preGet(self, func: F) -> F:
    return self.getNewDescriptor().preGet(func)

  def onGet(self, func: F) -> F:
    return self.getNewDescriptor().onGet(func)

  def preSet(self, func: F) -> F:
    return self.getNewDescriptor().preSet(func)

  def onSet(self, func: F) -> F:
    return self.getNewDescriptor().onSet(func)

  def preDelete(self, func: F) -> F:
    return self.getNewDescriptor().preDelete(func)

  def onDelete(self, func: F) -> F:
    return self.getNewDescriptor().onDelete(func)

  def setName(self, func: F) -> F:
    return self.getNewDescriptor().setName(func)

  def __getattr__(self, key: str) -> Any:
    newDescriptor = self.getNewDescriptor()
    try:
      decorator = object.__getattribute__(newDescriptor, key)
    except AttributeError:
      infoSpec = """'%s' has no attribute '%s'"""
      info = infoSpec % (type(newDescriptor).__name__, key,)
      raise AttributeError(info)
    else:
      return decorator


class _SetParent:
  __parent_class__: Optional[type] = None

  def _getParent(self) -> type:
    """
    Returns the parent class of this deferred THIS, or raises
    'MissingVariable' when it has not been set yet.
    """
    if self.__parent_class__ is None:
      raise MissingVariable(self, '__parent_class__', type)
    return self.__parent_class__

  def __init__(self, parent: type) -> None:
    self.__parent_class__ = parent

  def __getattr__(self, key: str) -> _SetDescriptorName:
    """
    THIS[Parent].x is a deferred reference to the descriptor 'x' that
    'Parent' holds, as the class being built will hold it. Reading it
    takes a clone of 'Parent.x' at once. The reference is recorded on the
    class that holds the descriptor, for the '__init_subclass__' installed
    there to place the clone on the subclass being created, and the next
    reading of 'x' through that class or any subclass of it returns the
    same reference: 'THIS[GrandParent].x' is 'THIS[Parent].x' for an 'x'
    that 'Parent' inherits, one reference with one clone. The base is
    named for a static checker as well.
    """
    parent = self._getParent()
    for holder in parent.__mro__:
      if key in holder.__dict__:
        break
    else:
      raise DanglingAlias(self, key, parent)
    references = _SetDescriptorName.newDescriptorsOnParent(holder)
    if key not in references:
      references[key] = _SetDescriptorName(holder, key)
      THIS._installThese(holder)
    return references[key]


class THIS(Sentinel):
  """
  THIS is a sentinel placeholder for the enclosing class, used inside
  a class body before that class exists.

  In a deferred 'AttriBox' constructor argument, THIS is replaced at
  access time by the 'instance' passed to '__get__' (the object the
  attribute is read from). In an '@overload(...)' signature it stands
  for the enclosing class, so the overload matches instances of that
  class, analogous to 'typing.Self'.

  'THIS[Parent].name' in a class body is a deferred reference to the
  descriptor 'name' that 'Parent' holds, as the class being built will
  hold it, so a subclass may expand on the notifiers of a descriptor it
  inherits without touching the base's:

    class Child(Parent):

      @THIS[Parent].x.onGet
      @THIS[Parent].x.onSet
      def _watchX(self, value) -> None:
        ...

  The decorators hand the function back as the descriptor's own decorators
  return it; the subclass takes a clone of the base's descriptor, decorated
  with the callback, as it is created, through an '__init_subclass__'
  installed on the base, and the base keeps its descriptor as it was.
  Naming the base is what lets a static checker resolve the reference to
  'Parent.x'.

  'THIS[GrandParent].x' is 'THIS[Parent].x' when 'Parent' inherits 'x'
  from 'GrandParent': one reference with one clone, so every decoration
  made through either applies to the 'x' the subclass takes.

  A decorator may hold a subscript only from Python 3.9 on (PEP 614). On
  3.7 and 3.8 the same decoration is written as a call after the method:

    class Child(Parent):

      def _watchX(self, value) -> None:
        ...

      _watchX = THIS[Parent].x.onGet(_watchX)
      _watchX = THIS[Parent].x.onSet(_watchX)

  Like the decorator, the call is written only inside the body of a
  subclass of 'Parent'.

  The clone goes to the next subclass created of the class holding the
  descriptor, which is the class whose body made the reference only when
  no other such subclass is created before that body ends. A subclass of
  'Parent' nested in the body is created first and takes the clone, so
  the enclosing class is left without the decoration. 'worktoy' is
  designed around custom metaclasses rather than nested classes; see the
  package docstring of 'worktoy'.

  Use 'OWNER' for the 'owner' class passed to '__get__'; OWNER has no
  role in overload signatures.
  """

  @classmethod
  def __class_getitem__(cls, parent: type[T], ) -> _SetParent:
    """
    THIS[Parent] names the base holding the descriptors a class body
    expands on, and installs on 'Parent' the '__init_subclass__' that
    places the clones taken through the reference on the subclass being
    created; see '_installThese'. 'Parent' is therefore a base of the
    class being built. Naming it is also what lets a static checker
    resolve 'THIS[Parent].x' to 'Parent.x'. Anything but a class is
    refused with 'TypeException'.
    """
    if not isinstance(parent, type):
      raise TypeException('parent', parent, type)
    cls._installThese(parent)
    return _SetParent(parent)

  @classmethod
  def _installThese(cls, parent: type) -> None:
    """
    Installs on 'parent', once, the '__init_subclass__' that places the
    descriptors recorded on 'parent' onto the subclass being created.
    Whether it is installed is read off 'parent' itself: a hook a base
    of 'parent' holds serves that base alone, placing the descriptors
    recorded on the base, so 'parent' takes a hook of its own beside it.
    The hook first hands over to what 'parent' held under the name, or,
    when 'parent' held nothing of its own, to the next '__init_subclass__'
    along the resolution order of the subclass, found as the hook runs,
    so a hook a base takes after this one is not passed over.
    """
    name: str = """__init_subclass__"""
    own: Optional[Callable] = parent.__dict__.get(name, None)
    try:
      installed = object.__getattribute__(own, '__this_new_desc__')
    except AttributeError:
      installed = False
    if installed:
      return

    @classmethod
    def __init_subclass__(sub, **kwargs) -> None:
      if own is None:
        super(parent, sub).__init_subclass__(**kwargs)
      else:
        own.__get__(None, sub)(**kwargs)
      references = _SetDescriptorName.newDescriptorsOnParent(parent)
      for descName, reference in references.items():
        newDesc = reference.getNewDescriptor()
        type.__setattr__(sub, descName, newDesc)
        newDesc.__set_name__(sub, descName)
      type.__delattr__(parent, '__new_descriptors__')

    object.__setattr__(__init_subclass__, '__this_new_desc__', True)

    type.__setattr__(parent, name, __init_subclass__)
