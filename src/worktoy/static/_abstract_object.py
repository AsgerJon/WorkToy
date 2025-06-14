"""
AbstractObject reimplements certain functions on 'object':

  __init__
  __init_subclass__
  __setattr__
  __delattr__

The __init__ and __init_subclass__ methods remove arguments other than
'self' before calling the base class. This prevents errors caused by
arguments being passed up through base classes.

The __setattr__ and __delattr__ methods streamlines error handling. A
subclass wishing to indicate an illegal set or delete operation should
raise BadSet or BadDelete respectively. The __setattr__ and __delattr__
methods implemented here catch these errors and raise ReadOnlyError or
ProtectedError respectively.

"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import re

from ..text import monoSpace
from ..waitaminute import BadSet, BadDelete, ReadOnlyError, ProtectedError
from ..waitaminute import MissingVariable, TypeException
from ..parse import maybe

from .zeroton import THIS, OWNER, DELETED

from . import _CurrentInstance, _CurrentOwner, _CurrentClass, _CurrentModule

#  Below provides compatibility back to Python 3.7
try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Optional, Self, TypeAlias


class AbstractObject(object, metaclass=type):
  """
  AbstractObject reimplements certain functions on 'object':

  __init__
  __init_subclass__
  __setattr__
  __delattr__

  The __init__ and __init_subclass__ methods remove arguments other than
  'self' before calling the base class. This prevents errors caused by
  arguments being passed up through base classes.

  The __setattr__ and __delattr__ methods streamlines error handling. A
  subclass wishing to indicate an illegal set or delete operation should
  raise BadSet or BadDelete respectively. The __setattr__ and __delattr__
  methods implemented here catch these errors and raise ReadOnlyError or
  ProtectedError respectively.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __field_name__ = None
  __field_owner__ = None
  __pos_args__ = None
  __key_args__ = None
  __current_owner__ = None
  __current_instance__ = None

  #  Public variables
  instance = _CurrentInstance()
  owner = _CurrentOwner()
  cls = _CurrentClass()
  module = _CurrentModule()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getFieldName(self) -> str:
    """Get the field name."""
    if self.__field_name__ is None:
      raise MissingVariable('__field_name__', str)
    return self.__field_name__

  def getFieldOwner(self) -> type:
    """Get the field owner."""
    if self.__field_owner__ is None:
      raise MissingVariable('__field_owner__', type)
    return self.__field_owner__

  def _getPositionalArgs(self, **kwargs) -> tuple:
    """Get the positional arguments."""
    if self.__pos_args__ is None:
      return ()
    if isinstance(self.__pos_args__, (tuple, list)):
      instance = maybe(kwargs.get('THIS', self.instance), THIS)
      owner = maybe(kwargs.get('OWNER', self.owner), OWNER)
      posArgs = []
      for arg in self.__pos_args__:
        if arg is THIS:
          posArgs.append(instance)
        elif arg is OWNER:
          posArgs.append(owner)
        else:
          posArgs.append(arg)
      return (*posArgs,)
    raise TypeException('__pos_args__', self.__pos_args__, (tuple, list))

  def _getKeywordArgs(self, **kwargs) -> dict:
    """Get the keyword arguments."""
    if self.__key_args__ is None:
      return {}
    if isinstance(self.__key_args__, dict):
      instance = maybe(kwargs.get('THIS', self.instance), THIS)
      owner = maybe(kwargs.get('OWNER', self.owner), OWNER)
      keyArgs = {}
      for (key, val) in self.__key_args__.items():
        if val is THIS:
          keyArgs[key] = instance
        elif val is OWNER:
          keyArgs[key] = owner
        else:
          keyArgs[key] = val
      return {**keyArgs, }
    raise TypeException('__key_args__', self.__key_args__, dict)

  def getPrivateName(self, ) -> str:
    """Getter-function for the private name of the field."""
    fieldName = self.getFieldName()
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return '__%s__' % pattern.sub('_', fieldName).lower()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, fuckPycharm: str = None, *args, **kwargs) -> None:
    """Why are we still here?"""
    object.__init__(self, )  # Removed args and kwargs
    self.__pos_args__ = (fuckPycharm, *args,)
    self.__key_args__ = {**kwargs, }

  def __init_subclass__(cls, *args, **kwargs) -> None:
    """Just to suffer?"""
    object.__init_subclass__()  # Removed args and kwargs

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PYTHON API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    Provides the instance with awareness of the class, if any, owning it
    and by what name it does. This method is invoked by '__build_class__'
    which is implemented entirely in C.
    """
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    After updating the instance and owner, this method returns 'self' if
    accessed from the class (instance is None) or calls the
    '__instance_get__' method.
    """
    self.updateContext(instance, owner, **kwargs)
    if instance is None:
      return self
    return self.__instance_get__(**kwargs)

  def __set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    After updating the instance and owner, this method calls the
    '__instance_set__' method.
    """
    self.updateContext(instance, **kwargs)
    return self.__instance_set__(value, **kwargs)

  def __delete__(self, instance: Any, **kwargs) -> None:
    """
    After updating the instance and owner, this method calls the
    '__instance_delete__' method.
    """
    self.updateContext(instance, **kwargs)
    return self.__instance_delete__(**kwargs)

  #  Presentation
  def _getNames(self) -> tuple[str, str, str, str]:
    """
    Getter function for class name, owner name and field name. Convenience
    function for '__str__' and '__repr__' methods.
    """
    clsName = type(self).__name__
    modName = type(self).__module__
    if self.owner is None:
      ownerName = ''
      fieldName = ''
    else:
      ownerName = self.owner.__name__
      fieldName = self.__field_name__
    return modName, clsName, ownerName, fieldName

  def __str__(self, ) -> str:
    """
    String representation of the instance. This method should return a
    human-readable string.
    """
    modName, clsName, ownerName, fieldName = self._getNames()
    if ownerName and fieldName:
      infoSpec = """'%s.%s' object at '%s.%s'"""
    else:
      infoSpec = """'%s.%s' object%s%s"""
    return monoSpace(infoSpec % (modName, clsName, ownerName, fieldName))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def updateContext(self, *args, **kwargs) -> None:
    """Updates the current instance."""
    if len(args) == 1:  # __set__ and __delete__ methods
      self.__current_instance__ = args[0]
      self.__current_owner__ = type(args[0])
    elif len(args) == 2:
      ins, own = args
      if not isinstance(ins, own) and ins is not None:
        raise TypeException('instance', ins, own)
      self.__current_instance__ = ins  # even if None
      self.__current_owner__ = own
    else:
      print('__________________________________________________________')
      print("""updateContext problem! Received:""")
      for arg in args:
        print('type: %s, value: %s' % (type(arg), str(arg),))
      print('¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨')
      raise NotImplementedError('precise argument exception not ready')

  def __instance_get__(self, **kwargs, ) -> Any:
    """Subclasses may implement this method to specify the object to be
    returned from __get__. Since this method accepts only the self-argument,
    it should use the current instance and owner as appropriate to
    determine the return-object. By default, this method returns 'self'. """
    return self

  def __instance_set__(self, val: Any, oldVal: Any = None, **kwargs) -> None:
    """Subclasses may implement this method to enable setting of the
    descriptor. By default, this method raises 'ReadOnlyError'. """
    try:
      oldVal = self.__instance_get__()
    except Exception as exception:
      oldVal = exception
    raise ReadOnlyError(self.instance, self, oldVal, val)

  def __instance_delete__(self, oldVal: Any = None, **kwargs) -> None:
    """Subclasses may implement this method to enable deletion of the
    descriptor. By default, this method raises 'ProtectedError'. """
    try:
      oldVal = self.__instance_get__()
    except Exception as exception:
      oldVal = exception
    raise ProtectedError(self.instance, self, oldVal)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  UTILITIES  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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
