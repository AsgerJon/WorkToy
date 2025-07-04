"""
Object provides the most basic object used by the 'worktoy' library. It
stands in for the 'object' type by adding functionality that must be
shared by every object in the library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ..utilities import Directory, maybe
from . import ContextInstance, ContextOwner, ContextCaller, MetaType
from .sentinels import THIS, DESC, OWNER, DELETED, LOCKED
from ..waitaminute import TypeException, MissingVariable, \
  attributeErrorFactory
from ..waitaminute.desc import AccessError

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Optional, Type, TypeAlias
  from types import TracebackType

  ExcType: TypeAlias = Optional[Type[Exception]]
  ExcVal: TypeAlias = Optional[Exception]
  Trace: TypeAlias = Optional[TracebackType]


class Object(object, metaclass=MetaType):
  """
  Object provides the most basic object used by the 'worktoy' library. It
  stands in for the 'object' type by adding functionality that must be
  shared by every object in the library.

  The class implements '__init__' that collects and holds references to
  the positional and keyword arguments passed to the constructor. These
  are later available through the 'getPosArgs' and 'getKeyArgs' methods.
  The class also implements '__set_name__' used by the descriptor protocol
  to inform instances defined in class bodies when the owning class is
  created and the name by which they appear in the class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Private Variables
  __field_owner__ = None
  __field_name__ = None
  __pos_args__ = None
  __key_args__ = None
  __context_instance__ = None
  __context_owner__ = None
  __call_chain__ = []

  #  Public Variables
  directory = Directory()
  instance = ContextInstance()
  owner = ContextOwner()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getFieldOwner(self) -> Optional[type]:
    """Getter for the field owner of the descriptor object"""
    if self.__field_owner__ is None:
      from ..waitaminute import MissingVariable
      raise MissingVariable('__field_owner__', type)
    return self.__field_owner__

  def getFieldName(self) -> Optional[str]:
    """Getter for the field name of the descriptor object"""
    if self.__field_name__ is None:
      from ..waitaminute import MissingVariable
      raise MissingVariable('__field_name__', str)
    return self.__field_name__

  def getPosArgs(self, **kwargs) -> tuple[Any, ...]:
    """Getter for the positional arguments of the object."""
    if self.__pos_args__ is None:
      return ()
    if not isinstance(self.__pos_args__, (list, tuple)):
      from ..waitaminute import TypeException
      raise TypeException('__pos_args__', self.__pos_args__, list, tuple, )
    thisObj = maybe(kwargs.get('THIS', self.__context_instance__), THIS)
    ownerObj = maybe(kwargs.get('OWNER', self.__context_owner__), OWNER)
    descObj = maybe(kwargs.get('DESC', self), )
    out = []
    for arg in self.__pos_args__:
      if arg is THIS:
        out.append(thisObj)
        continue
      if arg is OWNER:
        out.append(ownerObj)
        continue
      if arg is DESC:
        out.append(descObj)
        continue
      out.append(arg)
    return (*out,)

  def getKeyArgs(self, **kwargs) -> dict[str, Any]:
    """Getter for the keyword arguments of the object."""
    if self.__key_args__ is None:
      return dict()
    if not isinstance(self.__key_args__, dict):
      from ..waitaminute import TypeException
      raise TypeException('__key_args__', self.__key_args__, dict, )
    thisObj = maybe(kwargs.get('THIS', self.__context_instance__), THIS)
    ownerObj = maybe(kwargs.get('OWNER', self.__context_owner__), OWNER)
    descObj = maybe(kwargs.get('DESC', self), )
    out = dict()
    for key, value in self.__key_args__.items():
      if value is THIS:
        out[key] = thisObj
        continue
      if value is OWNER:
        out[key] = ownerObj
        continue
      if value is DESC:
        out[key] = descObj
        continue
      out[key] = value
    return {**out, }

  def getContextInstance(self) -> Any:
    """Returns the contextual instance or raises 'WithoutException'"""
    if self.hasContext():
      return self.__context_instance__
    from ..waitaminute.desc import WithoutException
    raise WithoutException(self)

  def hasContext(self) -> bool:
    """
    Returns True if the descriptor has a context, i.e. if it has been
    created with 'createContext' and not exited with 'exitContext'.
    """
    own = self.__context_owner__
    ins = self.__context_instance__
    if own is LOCKED or own is None:
      return False
    return True

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    object.__init__(self)
    self.__pos_args__ = args
    self.__key_args__ = kwargs
    self.__context_instance__ = LOCKED
    self.__context_owner__ = LOCKED

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: Type[object], name: str) -> None:
    self.__field_owner__ = owner
    self.__field_name__ = name

  def __get__(self, instance: Any, owner: type) -> Any:
    """
    Returns the root of the descriptor owning the hook.
    """
    if instance is None:
      return self
    with self.createContext(instance, owner) as context:
      value = context.__instance_get__()
    return self._deletedGuard(instance, value)

  def __set__(self, instance: Any, newValue: Any, **kwargs) -> None:
    """
    Sets the value of the descriptor in the instance. If accessing an
    attribute would raise an exception, it should not prevent setting a
    value on that attribute. Since the 'setter' control flow
    """
    with self.createContext(instance, type(instance)) as context:
      context.__instance_set__(newValue, **kwargs)

  def __delete__(self, instance: Any, **kwargs) -> None:
    """
    Deletes the value of the descriptor in the instance.
    """
    try:
      with self.createContext(instance, type(instance)) as context:
        oldVal = self._deletedGuard(instance, context.__instance_get__())
        context.__instance_delete__(oldVal, **kwargs)
    except AccessError as accessError:
      ownerName = type(instance).__name__
      fieldName = getattr(self, '__field_name__', 'Unknown')
      attributeError = attributeErrorFactory(ownerName, fieldName)
      raise attributeError from accessError

  def __enter__(self, ) -> Self:
    """
    Must be used with along with 'enterContext(instance, owner)'.
    """
    if self.hasContext():
      return self
    from ..waitaminute.desc import WithoutException
    raise WithoutException(self)

  def __exit__(self, _, exception: BaseException, __) -> None:
    """
    Must be used with along with 'exitContext'.
    """
    try:
      if exception is not None:
        raise exception
    except MissingVariable as missingVariable:
      raise AttributeError from missingVariable
    finally:
      self.exitContext()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, *args, **kwargs) -> Any:
    """
    Subclasses should implement this method to define the
    instance-specific getter. The root instance is accessed through the
    'root' attribute.
    """
    return self

  def __instance_set__(self, value: Any, *args, **kwargs) -> None:
    """
    Subclasses should implement this method to define the
    instance-specific setter. The root instance is accessed through the
    'root' attribute.
    """
    from ..waitaminute.desc import ReadOnlyError
    raise ReadOnlyError(self, value)

  def __instance_delete__(self, oldVal: Any, *args, **kwargs) -> None:
    """
    Subclasses should implement this method to define the
    instance-specific deleter. The root instance is accessed through the
    'root' attribute.
    """
    from ..waitaminute.desc import ProtectedError
    raise ProtectedError(self.instance, self, oldVal)

  def createContext(self, instance: Any, owner: type, ) -> Self:
    """
    Creates a context for the descriptor. The context is used to
    store the instance and owner of the descriptor.
    """
    self.__context_instance__ = instance
    self.__context_owner__ = owner
    return self

  def exitContext(self) -> Self:
    """
    Exits the context of the descriptor. The method restores the
    descriptor to its previous state.
    """
    self.__context_instance__ = LOCKED
    self.__context_owner__ = LOCKED
    return self

  def _deletedGuard(self, instance: Any, value: Any) -> Any:
    """
    A guard that raises an exception if the value is 'DELETED'. This is
    used to prevent accessing deleted attributes.
    """
    if value is DELETED:
      infoSpec = """%s: '%s' object has no attribute '%s'."""
      eType = 'AttributeError'
      ownerName = type(instance).__name__
      fieldName = getattr(self, '__field_name__', 'object')
      info = infoSpec % (eType, ownerName, fieldName)
      raise AttributeError(info)
    return value

  def getPrivateName(self, ) -> str:
    """
    Returns the name chain of the descriptor. This is used to access
    the name of the descriptor in the context of the instance.
    """
    fieldName = self.__field_name__
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return '__%s__' % pattern.sub('_', fieldName).lower()

  @classmethod
  def parseKwargs(cls, *args, **kwargs) -> tuple[Any, dict]:
    """
    Parses the keyword arguments for value matching keys and types given
    in positional arguments. The return value is a tuple of the value
    found and the remaining keyword arguments. If no value is found,
    the returned tuple will be 'None' and all the keyword arguments
    received. If no types are given, the type of the value is ignored.
    """
    typeArgs, keys = [], []
    for arg in args:
      if isinstance(arg, type):
        typeArgs.append(arg)
        continue
      if isinstance(arg, str):
        keys.append(arg)
        continue
    if not keys:
      return None, {**kwargs, }
    typeArgs = typeArgs or [object, ]
    if complex in typeArgs:
      if float not in typeArgs:
        typeArgs.append(float)
      if int not in typeArgs:
        typeArgs.append(int)
    elif float in typeArgs:
      if int not in typeArgs:
        typeArgs.append(int)
    for key in keys:
      if key in kwargs:
        value = kwargs[key]
        for type_ in typeArgs:
          if isinstance(value, type_):
            del kwargs[key]
            return value, {**kwargs, }
        else:
          raise TypeException(key, value, *typeArgs, )
    else:
      return None, {**kwargs, }
