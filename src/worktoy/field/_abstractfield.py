"""Field quickly provides a property to a class. Specify default value,
permission levels and name at creation time."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Never, Any, TYPE_CHECKING
from warnings import warn

from icecream import ic

from worktoy.field import PermissionLevel as PermLvl
from worktoy.stringtools import monoSpace
from worktoy.waitaminute import SecretPropertyError
from worktoy.waitaminute import ReadOnlyError
from worktoy.waitaminute import ProtectedPropertyError

if TYPE_CHECKING:
  from worktoy.core import WorkType

ic.configureOutput(includeContext=True)
DEBUG = False


class AbstractField:
  """Abstract base class for the descriptor implementation.

  Nomenclature:
    FieldClass: The subclass of the AbstractField
    field: Instance of FieldClass
    WorkTypeMeta: The metaclass customizing class creation
    WorkType: Intermediary class having metaclass=WorkTypeMeta. Implements
              only the metaclass and should not be relied upon for any
              additional logic.
    OwnerClass: Inherits WorkType for the purpose of applying the metaclass
    ownerObject: Instance of OwnerClass.
    The FieldClass provides the following variables:
     - fieldType: The type of the value returned by the descriptor.
     - fieldName: The key in the __dict__ of the OwnerClass mapping field.
                  instance variable 'name' on the OwnerClass gets set to this
                  name automatically when the OwnerClass is created. This
                  happens through implementing the __set_item__ method.
     - fieldOwner: points to the ownerObject
     - fieldObject: points to the ownerObject
     The FieldClass provides the following methods:
      - _getPermLevel(self: fieldInstance, ) -> PermissionLevel:
        - The permission level defined on the FieldClass must immutable.
        If override is necessary in some case, for example during some
        error handling, the explicit accessor functions defined below
        provide access circumventing the permission check of the public
        interface.


    Accessors: explicitGetter, explicitSetter, explicitDeleter
      The __get__, __set__ and __del__ methods provide the logic from
      the FieldClass based on the permission level.



  Order of events:
  0. Prerequisites - The following classes are imported by the
  WorkTypeMeta metaclass implementation:
    - NameSpace (Orphan class inheriting only from builtins)
    -
  1. Creation of the metaclass.
  """

  @classmethod
  @abstractmethod
  def _getPermissionLevel(cls) -> PermLvl:
    """Getter-function for the permission level. This is an abstract
    method that should be implemented by subclasses."""

  def __init__(self, *args, **kwargs) -> None:
    self._type = None
    self._name = None
    self._owner = None
    self._object = None
    try:
      self._root = kwargs['_root']
    except KeyError:
      self._root = None
    if self._root is not None:
      w = """Created rooted instance of class Field. This allows this 
      instance to change its permission level at runtime. """
      warn(monoSpace(w))

  def _getPermission(self, ) -> PermLvl:
    """Getter-function for permissions"""
    return self._getPermissionLevel()

  def _setPermission(self, *_) -> Never:
    """Setter-function for permissions"""
    e = """Unauthorized attempt at changing permission level!"""
    raise PermissionError(e)

  def _delPermission(self) -> Never:
    """Illegal delete function"""
    e = """LOL, you tried to delete the delete permission level on 
    Field %s LMAO!""" % self.name
    raise ProtectedPropertyError(monoSpace(e))

  def _getName(self) -> str:
    """Getter-function for name"""
    if isinstance(self._name, str):
      return self._name
    raise TypeError

  def _setName(self, name: str) -> None:
    """Illegal-setter function for name"""
    raise ReadOnlyError('name')

  def _delName(self, ) -> Never:
    """Illegal delete function for name"""
    raise ProtectedPropertyError('name')

  def _getType(self) -> type:
    """Getter-function for the type"""
    if isinstance(self._type, type):
      return self._type
    raise TypeError

  def _setType(self, type_: type) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('type_')

  def _delType(self, ) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('type')

  def _getOwner(self, ) -> type:
    """Getter-function for owner class"""
    if self._owner is None:
      raise TypeError
      # raise ProceduralError
    if not isinstance(self._owner, type):
      raise TypeError
    return self._owner

  def _setOwner(self, owner: type) -> None:
    """Setter-function for the owner class"""
    if self._owner is not None:
      raise ReadOnlyError('owner')
    if not isinstance(owner, type):
      raise TypeError
    self._owner = owner

  def _delOwner(self) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('owner')

  def _getObject(self) -> Any:
    """Getter-function for the object this instance"""
    return self._object

  def _setObject(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('object')

  def _delObject(self, ) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('object')

  permLevel = property(_getPermission, _setPermission, _delPermission)
  name = property(_getName, _setName, _delName)
  owner = property(_getOwner, _setOwner, _delOwner)
  type_ = property(_getType, _setType, _delType)
  obj = property(_getType, _setType, _delType)

  def __get__(self, obj: object, cls: type) -> Any:
    if self.permLevel.canGet:
      return self._explicitGetter(obj, cls)
    raise SecretPropertyError(self.name)

  def __set__(self, obj: object, value: Any) -> None:
    if not self.permLevel.canSet:
      raise ReadOnlyError(self.name)
    self._explicitSetter(obj, value)

  def __delete__(self, obj: object) -> None:
    if self.permLevel.canDel:
      return self._explicitDeleter(obj)
    else:
      raise ProtectedPropertyError(self.name)

  def __set_object__(self, obj: WorkType) -> None:
    self._object = obj

  def __set_name__(self, cls: type, name: str) -> None:
    """This method gets invoked when the class owning this instance is
    created. It receives the class and the name of this instance as it is
    set in the owner class."""
    self._owner = name
    self._name = name

  @abstractmethod
  def _explicitGetter(self, obj: object, cls: type) -> Any:
    """This abstract method defines how the field value on the given
    object of the given type is to be calculated. Typically, it will
    return the value of an instance variable, subclasses may also
    implement a computation at call time.

    **Regarding Accessor Functions**
    Please note that the three accessor operations used in this descriptor
    implementation, requires subclasses to define their behaviour by
    reimplementing the private methods:
     - _explicitGetter(self, obj: object, cls: type)  # This method
     - _explicitSetter(self, obj: object, newValue: Any)
     - _explicitDeleter(self, obj: object)
     (This note is not repeated on the other two explicit accessor)."""

  @abstractmethod
  def _explicitSetter(self, obj: object, newValue: Any) -> None:
    """This abstract method defines how the __set__ method updates the
    given object """

  @abstractmethod
  def _explicitDeleter(self, obj: object) -> None:
    """Explicitly deletes the value."""
