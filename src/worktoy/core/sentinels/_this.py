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
from ...waitaminute.desc import DanglingAlias, ReferenceConflict
from ...waitaminute.desc import OverloadReference

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Optional, TypeVar, TypeAlias
  from ...desc import BaseDescriptor

  Descriptors: TypeAlias = dict[str, BaseDescriptor]

  #  A checker reads 'THIS[Parent]' as a '_SetParent' and 'THIS[Parent].x'
  #  as a '_SetDescriptorName', as the annotations below say. 'F' keeps a
  #  function decorated through such a reference its own type, which the
  #  roles below declare, and 'T' types the class named in the subscript.
  F = TypeVar('F', bound=Callable[..., Any])
  T = TypeVar('T')


class _SetDescriptorName:
  """
  'THIS[Parent].x' in the body of a subclass must stand for the
  descriptor 'x' as the subclass will hold it: a descriptor of its own,
  which callbacks may be added to while the base keeps its 'x' as it was.
  The subclass does not exist yet while its body runs, so the descriptor
  must be prepared now and handed over once the class exists. Decorating
  through the reference must work as decorating the descriptor itself
  would, its own decorators included.

  Implementation
  --------------

  The reference takes a clone of the descriptor at once, from the first
  class along the resolution order of 'Parent' that holds 'x' in its own
  dictionary, the holder. The seven notification decorators, and any
  other name read from the reference, act on the clone. The hook that
  'THIS' installs on the holder places the clone on the next subclass
  created, unless the body of that subclass binds the name to something
  else itself; see 'isDeclaredBy'. The name must hold an object with a
  'clone' method, such as a 'BaseDescriptor'.

  Attributes
  ----------

  __parent_class__ : type
    The holder.

  __descriptor_name__ : str
    The name of the descriptor.

  __new_descriptor__ : BaseDescriptor
    The clone the subclass receives.
  """
  __parent_class__: Optional[type] = None
  __descriptor_name__: Optional[str] = None
  __new_descriptor__: Optional[BaseDescriptor] = None

  @classmethod
  def newDescriptorsOnParent(cls, parent: type, **kwargs) -> Descriptors:
    """
    The references made through a holder wait on the holder until its next
    subclass is created. They must not be inherited: a subclass of the
    holder reading the record would otherwise see references meant for its
    sibling.

    Implementation
    --------------

    The record is read from the own dictionary of the holder under
    '__new_descriptors__', and an empty one is created there when missing.

    Parameters
    ----------

    parent : type
      The holder.

    Returns
    -------

    Descriptors
      A 'dict[str, BaseDescriptor]' from each referenced name to its
      reference.
    """
    key: str = """__new_descriptors__"""
    try:
      descriptors: Descriptors = parent.__dict__[key]
    except KeyError:
      if kwargs.get('_recursion', False):
        raise RecursionError
      type.__setattr__(parent, key, dict())
      return cls.newDescriptorsOnParent(
          parent, _recursion=True)  # pragma: no mutate
    else:
      return descriptors

  def _getParent(self) -> type:
    if self.__parent_class__ is None:
      raise MissingVariable(self, '__parent_class__', type)
    return self.__parent_class__

  def _getDescriptorName(self) -> str:
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
      return self.getNewDescriptor(_recursion=True)  # pragma: no mutate
    return self.__new_descriptor__

  def isDeclaredBy(self, sub: type) -> bool:
    """
    The clone must not replace a descriptor the body of the subclass
    declares at the same name, or that declaration would be lost without
    a word. Only what the body itself bound counts, not what a hook of its
    namespace added to the class. A body binding the very clone the
    reference gave, as a decorator of the descriptor that hands the
    descriptor back makes it do, declares nothing else.

    Implementation
    --------------

    The body is the namespace object 'MetaType' keeps under
    '__namespace__', whose dictionary holds the names the body bound and
    a hook did not claim; a class built by 'type' keeps none, and its own
    dictionary is the body. A name found there counts unless the class
    holds the clone itself at it.

    Parameters
    ----------

    sub : type
      The subclass being created.

    Returns
    -------

    bool
      Whether the body of 'sub' binds the name to something other than the
      clone.
    """
    name = self._getDescriptorName()
    body = sub.__dict__.get('__namespace__', None)
    if not isinstance(body, dict):
      body = sub.__dict__
    if name not in body:
      return False
    held = sub.__dict__.get(name, None)
    return False if held is self.getNewDescriptor() else True

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
    """
    A descriptor class of a project may define decorators beyond the seven
    of 'BaseDescriptor', and 'THIS[Parent].x' must offer them as well.

    Implementation
    --------------

    A name the reference lacks is read off the clone with
    'object.__getattribute__'.

    Raises
    ------

    AttributeError
      The clone has no such name either.
    """
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
  """
  'THIS[Parent]' must give an object from which 'THIS[Parent].x' is read,
  remembering which class the subscript named.

  Attributes
  ----------

  __parent_class__ : type
    The class named in the subscript.
  """
  __parent_class__: Optional[type] = None

  def _getParent(self) -> type:
    if self.__parent_class__ is None:
      raise MissingVariable(self, '__parent_class__', type)
    return self.__parent_class__

  def __init__(self, parent: type) -> None:
    self.__parent_class__ = parent

  def __getattr__(self, key: str) -> _SetDescriptorName:
    """
    'THIS[Parent].x' and 'THIS[GrandParent].x' must be one reference when
    'Parent' inherits 'x' from 'GrandParent', so that every decoration made
    through either reaches the one descriptor the subclass receives. A name
    that no class holds is a mistake in the class body and must fail at
    that line. So is a name holding an overloaded method: its clone would
    replace the dispatcher the namespace of the subclass builds, and with
    it the overloads the body declares.

    Implementation
    --------------

    The resolution order of the subscripted class is searched for the
    first class holding 'key' in its own dictionary, the holder, and the
    reference is kept on the holder, created on the first read. A name
    holding no value is refused with 'DanglingAlias', and one holding a
    value whose class sets '__no_this_reference__', as 'Dispatcher' does,
    with 'OverloadReference', both before anything is recorded. The marker
    is read with 'type.__getattribute__', so a class answering every name
    it lacks is not taken for a dispatcher. Both refusals are
    'SyntaxError's, so 'hasattr' and 'getattr' with a default raise for
    such a name rather than answer.

    Parameters
    ----------

    key : str
      The name of the descriptor.

    Returns
    -------

    _SetDescriptorName
      The reference.

    Raises
    ------

    DanglingAlias
      No class along the resolution order holds the name.

    OverloadReference
      The name holds an overloaded method.
    """
    parent = self._getParent()
    for holder in parent.__mro__:
      if key in holder.__dict__:
        break
    else:
      raise DanglingAlias(self, key, parent)
    heldType = type(holder.__dict__[key])
    try:
      refused = type.__getattribute__(heldType, '__no_this_reference__')
    except AttributeError:
      #  This branch is reached by the following:
      #  - The name holds a descriptor, as an 'AttriBox', or a plain value
      refused = False
    if refused:
      raise OverloadReference(parent.__name__, key)
    references = _SetDescriptorName.newDescriptorsOnParent(holder)
    if key not in references:
      references[key] = _SetDescriptorName(holder, key)
      THIS._installThese(holder)
    return references[key]


class THIS(Sentinel):
  """
  A class body sometimes needs to refer to the class it defines, which
  does not exist until the body ends. A method may take another instance
  of the same class, and its overload signature must say so. The value of
  an 'AttriBox' may need to be built with the instance it belongs to. And
  a subclass may need to add notifiers to a descriptor it inherits,
  without changing the descriptor of the base, which other subclasses
  share.

  Implementation
  --------------

  In an overload signature, as in '@overload(THIS)', 'THIS' stands for
  the class, and the dispatcher replaces it once the class exists. In the
  arguments of an 'AttriBox', an argument that is 'THIS' is replaced at
  the first read by the instance read through. 'THIS[Parent].name' is a
  reference to the descriptor 'name' as the subclass will hold it:

    class Child(Parent):

      @THIS[Parent].x.onGet
      @THIS[Parent].x.onSet
      def _watchX(self, value) -> None:
        ...

  The reference takes a clone of 'Parent.x', the decorators add their
  callbacks to the clone and return the function, and an
  '__init_subclass__' that the subscript installs on the base places the
  clone on 'Child' as it is created. 'THIS[GrandParent].x' is
  'THIS[Parent].x' when 'Parent' inherits 'x'. A decorator may hold a
  subscript only from Python 3.9 on, so on 3.7 and 3.8 the decoration is
  written as a call after the method:

    _watchX = THIS[Parent].x.onGet(_watchX)

  The clone goes to the next subclass created of the class holding the
  descriptor. The decoration therefore belongs in the body of a subclass
  of 'Parent' and nowhere else, and no other subclass of the holder may
  be created before that body ends: a subclass of 'Parent' nested in the
  body would take the clone. A body that declares 'x' itself decorates
  that 'x' directly, as in '@x.onGet'; decorating 'THIS[Parent].x' as
  well would replace the declaration with the clone, and the class
  statement is refused with 'ReferenceConflict'. A name holding an
  overloaded method is refused at the line with 'OverloadReference': a
  subclass declares its own overloads of an inherited name with
  '@overload' in its body. The owner class has its own placeholder,
  'OWNER', which has no meaning in an overload signature.
  """

  @classmethod
  def __class_getitem__(cls, parent: type[T], ) -> _SetParent:
    """
    'THIS[Parent]' names the base whose descriptors the class body expands
    on.

    Implementation
    --------------

    The subscript installs on 'Parent' the hook that hands the clones over
    (see '_installThese') and returns the object the references are read
    from. A builtin class such as 'int' cannot take the hook, and fails
    with Python's own 'TypeError'.

    Parameters
    ----------

    parent : type
      A base of the class being built.

    Returns
    -------

    _SetParent
      The object 'THIS[Parent].name' is read from.

    Raises
    ------

    TypeException
      'parent' is not a class.
    """
    if not isinstance(parent, type):
      raise TypeException('parent', parent, type)
    cls._installThese(parent)
    return _SetParent(parent)

  @classmethod
  def _installThese(cls, parent: type) -> None:
    """
    The clones taken through 'THIS[Parent].x' must reach the subclass as it
    is created, after the class exists but before anything uses it, and
    the base must go on creating subclasses as before: its own
    '__init_subclass__', and those along the resolution order, must still
    run with every class keyword.

    Implementation
    --------------

    An '__init_subclass__' is set on the class, once, marked with
    '__this_new_desc__' and read off the own dictionary, so a hook on a
    base does not count. When it runs, it calls what the class held under
    the name before, or else the next '__init_subclass__' along the
    resolution order of the subclass, with every keyword. With no record
    on the class it ends there, writing nothing. Otherwise it removes the
    record, so only the first subclass created receives the clones, even
    when its class statement is refused, and sets each recorded clone
    on the subclass and calls its '__set_name__', which Python has already
    run for the rest of the body. A clone whose name the body of the
    subclass binds to something else itself is refused with
    'ReferenceConflict' instead of replacing that declaration; see
    '_SetDescriptorName.isDeclaredBy'. The refusal comes from an
    '__init_subclass__', so no 'RuntimeError' wraps it on any version.

    Parameters
    ----------

    parent : type
      The class to install the hook on.
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
      try:
        references = parent.__dict__['__new_descriptors__']
      except KeyError:
        #  This branch is reached by the following:
        #  - No reference through 'THIS' is pending on the class, as for
        #    every subclass created after the one that received the clones
        return
      #  The record goes first, so the clones of a refused body never
      #  reach the next subclass.
      type.__delattr__(parent, '__new_descriptors__')
      for descName, reference in references.items():
        if reference.isDeclaredBy(sub):
          raise ReferenceConflict(sub.__name__, descName, parent.__name__)
        newDesc = reference.getNewDescriptor()
        type.__setattr__(sub, descName, newDesc)
        newDesc.__set_name__(sub, descName)

    object.__setattr__(__init_subclass__, '__this_new_desc__', True)

    type.__setattr__(parent, name, __init_subclass__)
