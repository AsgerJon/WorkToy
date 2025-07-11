"""EZHook collects the field entries in EZData class bodies. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
import warnings
from warnings import warn

from ..core import Object
from ..mcls.space_hooks import AbstractSpaceHook, ReservedNames
from ..utilities import textFmt, maybe, stringList
from ..waitaminute import TypeException, attributeErrorFactory
from ..waitaminute.desc import ProtectedError
from ..waitaminute.ez import DeferredTypeException, UnorderedEZException, \
  UnfrozenHashException, FrozenEZException, EZDeleteException
from ..waitaminute.meta import ReservedName

from icecream import ic

ic.configureOutput(includeContext=True)

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Iterator, Callable, TypeAlias, Any, Never, Optional

  from worktoy.ezdata import EZData, EZMeta, EZSlot

  Slots: TypeAlias = tuple[str, ...]
  SlotTypes: TypeAlias = Callable[[EZData, str], type]
  SlotDefaults: TypeAlias = Callable[[EZData, str], Any]

  Dunder: TypeAlias = Callable[[Any], Any]
  Factory: TypeAlias = Callable[[], Dunder]
  Factories: TypeAlias = dict[str, Factory]
  __INIT__: TypeAlias = Callable[[EZData], None]
  __LT__: TypeAlias = Callable[[EZData, EZData], bool]
  __LE__: TypeAlias = Callable[[EZData, EZData], bool]
  __GT__: TypeAlias = Callable[[EZData, EZData], bool]
  __GE__: TypeAlias = Callable[[EZData, EZData], bool]
  __EQ__: TypeAlias = Callable[[EZData, EZData], bool]
  __HASH__: TypeAlias = Callable[[EZData], int]
  __STR__: TypeAlias = Callable[[EZData], str]
  __REPR__: TypeAlias = Callable[[EZData], str]
  __ITER__: TypeAlias = Callable[[EZData], Iterator]
  __LEN__: TypeAlias = Callable[[EZData], int]
  __GETITEM__: TypeAlias = Callable[[EZData, str], Any]
  __SETITEM__: TypeAlias = Callable[[EZData, str, Any], None]
  __GETATTR__: TypeAlias = Callable[[EZData, str], Any]
  __SETATTR__: TypeAlias = Callable[[EZData, str, Any], None]
  __DELATTR__: TypeAlias = Callable[[EZData, str], Never]
  AS_TUPLE: TypeAlias = Callable[[EZData], tuple[Any, ...]]
  AS_DICT: TypeAlias = Callable[[EZData], dict[str, Any]]


class EZSpaceHook(AbstractSpaceHook):
  """EZHook collects the field entries in EZData class bodies. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __bad_names__ = """__slots__, __init__, __eq__, 
    __iter__, __getitem__, __setitem__, __getattr__, __len__, __hash__"""
  __auto_names__ = """__slots__, __init__, __eq__, __str__, __repr__,
    __iter__, __getitem__, __setitem__, __getattr__, __len__, __hash__"""

  #  Private Variables
  __new_callables__ = None

  #  Public Variables
  reservedNames = ReservedNames()
  if TYPE_CHECKING:  # pragma: no cover
    from . import EZSpace
    space: EZSpace

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getAutoNameFactoryDict(self, ) -> Factories:
    """Returns a dictionary of auto-named methods."""
    return {
        '__init__'   : self.initFactory,
        '__eq__'     : self.eqFactory,
        '__hash__'   : self.hashFactory,
        '__str__'    : self.strFactory,
        '__repr__'   : self.reprFactory,
        '__iter__'   : self.iterFactory,
        '__len__'    : self.lenFactory,
        '__getitem__': self.getItemFactory,
        '__setitem__': self.setItemFactory,
        '__getattr__': self.getAttrFactory,
        'asTuple'    : self.asTupleFactory,
        'asDict'     : self.asDictFactory,
    }

  def _getBadNames(self) -> list[str]:
    """Returns a tuple of names that are reserved and should not be used."""
    return stringList(self.__bad_names__, )

  def _getNewCallables(self) -> list[Callable]:
    """Returns a list of callables introduced by the current class body. """
    return maybe(self.__new_callables__, [])

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _addNewCallable(self, callMeMaybe: Callable) -> None:
    """Adds a new callable to the list of new callables."""
    existing = self._getNewCallables()
    self.__new_callables__ = [*existing, callMeMaybe]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def slotsGen(self, ) -> list[EZSlot]:
    """Creates the '__slots__' tuple during the preCompilePhase."""
    mroSpace = [self.space, *self.space.getMRONamespaces(), ]
    ezSlots = []
    for space in reversed(mroSpace):
      if hasattr(space, 'getEZSlots', ):
        for ezSlot in space.getEZSlots():
          if ezSlot in ezSlots:
            continue
          ezSlots.append(ezSlot)
    return ezSlots

  def preCompilePhase(self, compiledSpace: dict) -> dict:
    """The preCompileHook method is called before the class is compiled."""
    ezSlots = self.slotsGen()
    for name, factory in self._getAutoNameFactoryDict().items():
      compiledSpace[name] = factory()
    return compiledSpace

  def postCompilePhase(self, compiledSpace: dict) -> dict:
    """The postCompileHook method is called after the class is compiled."""
    ezSlots = self.slotsGen()
    compiledSpace['__slot_objects__'] = ezSlots
    compiledSpace['__slots__'] = [ez.name for ez in ezSlots]
    return compiledSpace

  def setItemPhase(self, key: str, value: Any, oldValue: Any, ) -> bool:
    """
    Checks that 'key' is not the name of a method for which the hook
    provides an auto-generated factory. This may be bypassed by the
    '__is_root__' attribute on 'value'. Please note that while this does
    suppress the exception, the value will be overridden by the hook.

    The following cases are not handled by this hook:

    - If 'key' is a reserved name, the ReservedNameHook has already
    handled it, but still allowed it through. This means that it is a
    'write once' attribute, and that this key, value pair must be allowed
    through.

    - If 'value' is a callable or a descriptor. Please note that
    descriptors are identified by the presence of the '__instance_get__'
    or '__instance_set__' methods. These are present on all 'Object'
    subclasses. To use a descriptor class in a slot, use a type-hint,
    for example:

    class Foo(EZData):
      bar: MyDescriptor  # no instantiation

    Special note when using 'from __future__ import annotations':
    Support of forward references is not implemented as unlike methods,
    fields in data classes do require runtime resolution of types. This is
    in contrast to methods, which ignore type hints at runtime.
    """
    if key in self._getBadNames():
      if not hasattr(value, '__is_root__'):
        raise ReservedName(key)
      return True  # Ignores @_root decorated methods
    if key in self.reservedNames:
      return False  # Already handled by ReservedNameHook
    if callable(value):
      self._addNewCallable(value)
      return False
    for descName in ['__instance_get__', '__instance_set__']:
      descFunc = getattr(type(value), descName, None)
      if descFunc is not None:
        if descFunc is not getattr(Object, descName):
          return False  #
    self.space.addRegularSlot(key, value)
    return True

  def setAnnotationPhase(self, key: str, value: Any) -> Any:
    """Adds annotations to slots"""
    if isinstance(value, str):
      raise DeferredTypeException(key, value)
    self.space.addTypeOnlySlot(key, value)

  # \_____________________________________________________________________/ #
  #  Method factories
  # /¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨\ #
  @staticmethod
  def initFactory() -> __INIT__:
    """
    Creates the '__init__' method for the EZData class.
    """

    def __init__(self, *args, **kwargs) -> None:
      """
      The generated '__init__' method sets attributes on the instance
      based on given arguments. Keyword arguments take precedence.
      Positional arguments are applied in order.
      """
      posArgs = [*args, ]
      while len(posArgs) < len(self.__slot_objects__):
        posArgs.append(None)
      for (arg, slot) in zip(args, self.__slot_objects__):
        if arg is None:
          continue
        if not isinstance(arg, slot.typeValue):
          if slot.typeValue is not str:
            setattr(self, slot.name, slot.typeValue(arg))
            continue
          raise TypeException('arg', arg, slot.typeValue, )
        setattr(self, slot.name, arg)
      for key, val in kwargs.items():
        if key in self.__slots__:
          slot = self.__slot_objects__[self.__slots__.index(key)]
          if not isinstance(val, slot.typeValue):
            if slot.typeValue is not str:
              setattr(self, key, slot.typeValue(val))
              continue
            raise TypeException('val', val, slot.typeValue, )
          setattr(self, key, val)

    setattr(__init__, '__auto_generated__', True)
    return __init__

  @staticmethod
  def lessFactory(**kwargs) -> __LT__:
    """Creates the inequality methods for the EZData class."""

    def func(self, other: EZData) -> bool:
      """
      Instances of EZData are less than each other if their first data
      field is less than the other's first data field.
      """
      if type(self) is not type(other):
        return NotImplemented
      if not type(self).isOrdered:
        raise UnorderedEZException(self.space.getClassName(), )
      for slot in self.__slots__:
        try:
          if getattr(self, slot) < getattr(other, slot):
            return True
          if getattr(self, slot) > getattr(other, slot):
            return False
          if kwargs.get('equal', False):
            return False
        except TypeError as typeError:
          if 'not supported between instances of' in str(typeError):
            clsName = self.space.getClassName()
            fName = slot
            slotObject = None
            for slotObject in self.__slot_objects__:
              if slotObject.name == slot:
                break
            else:
              raise typeError
            fType = slotObject.typeValue
            raise UnorderedEZException(clsName, fName, fType) from typeError
          raise typeError
      return True if kwargs.get('equal', False) else False

    return func

  @classmethod
  def ltFactory(cls, ) -> __LT__:
    """Creates the '__lt__' method for the EZData class. """
    func = cls.lessFactory(equal=False)
    setattr(func, '__name__', '__lt__')
    setattr(func, '__qualname__', '__lt__')
    setattr(func, '__auto_generated__', True)
    return func

  @classmethod
  def leFactory(cls, ) -> __LE__:
    """Creates the '__le__' method for the EZData class. """
    func = cls.lessFactory(equal=True)
    setattr(func, '__name__', '__le__')
    setattr(func, '__qualname__', '__le__')
    setattr(func, '__auto_generated__', True)
    return func

  @staticmethod
  def gtFactory() -> __GT__:
    """Creates the '__gt__' method for the EZData class."""

    def __gt__(self, other: EZData) -> bool:
      if type(self) is not type(other):
        return NotImplemented
      return other < self  # Uses __lt__

    setattr(__gt__, '__auto_generated__', True)
    return __gt__

  @staticmethod
  def geFactory() -> __GE__:
    """Creates the '__ge__' method for the EZData class. """

    def __ge__(self, other: EZData) -> bool:
      if type(self) is not type(other):
        return NotImplemented
      return other <= self  # Uses __le__

    setattr(__ge__, '__auto_generated__', True)
    return __ge__

  @staticmethod
  def eqFactory() -> __EQ__:
    """
    Creates the '__eq__' method for the EZData class.
    """

    def __eq__(self, other: EZData) -> bool:
      """
      Instances of EZData are equal if each of their data fields are equal.
      """
      if type(self) is not type(other):
        return NotImplemented
      for slot in self.__slot_objects__:
        if getattr(self, slot.name) != getattr(other, slot.name):
          return False
      return True

    setattr(__eq__, '__auto_generated__', True)
    return __eq__

  @staticmethod
  def hashFactory() -> __HASH__:
    """Creates the '__hash__' method for the EZData class."""

    def __hash__(self) -> int:
      """The hash of an EZData instance is the hash of its data fields."""
      if not type(self).isFrozen:
        values = []
        for slot in self.__slots__:
          values.append(getattr(self, slot))
        return hash((*values,))
      raise UnfrozenHashException(self.space.getClassName())

    setattr(__hash__, '__auto_generated__', True)
    return __hash__

  @staticmethod
  def strFactory() -> __STR__:
    """The strFactory method is called when the class is created."""

    def __str__(self) -> str:
      """The __str__ method is called when the class is created."""
      clsName = type(self).__name__
      names = [ezSlot.name for ezSlot in self.__slot_objects__]
      vals = [str(getattr(self, name)) for name in names]
      keyVals = ['%s=%s' % (name, val) for name, val in zip(names, vals)]
      return """%s(%s)""" % (clsName, ', '.join(keyVals))

    setattr(__str__, '__auto_generated__', True)
    return __str__

  @staticmethod
  def reprFactory(*ezSlots) -> __REPR__:
    """The reprFactory method is called when the class is created."""

    def __repr__(self) -> str:
      """The __repr__ method is called when the class is created."""
      infoSpec = """%s(%s)"""
      clsName = type(self).__name__
      fieldNames = [ezSlot.name for ezSlot in self.__slot_objects__]
      fieldValues = [getattr(self, name) for name in fieldNames]
      fieldRepr = []
      for field in fieldValues:
        if isinstance(field, str):
          fieldRepr.append("""'%s'""" % field)
          continue
        fieldRepr.append(str(field))
      if fieldRepr:
        info = infoSpec % (clsName, ', '.join(fieldRepr))
      else:
        info = infoSpec % (clsName, '')
      return textFmt(info)

    setattr(__repr__, '__auto_generated__', True)
    return __repr__

  @staticmethod
  def iterFactory() -> __ITER__:
    """The iterFactory method is called when the class is created."""

    def __iter__(self, ) -> Iterator:
      """
      Implementation of the iteration protocol
      """
      for key in self.__slots__:
        yield getattr(self, key)

    setattr(__iter__, '__auto_generated__', True)
    return __iter__

  @staticmethod
  def lenFactory() -> __LEN__:
    """The lenFactory method is called when the class is created."""

    def __len__(self) -> int:
      """The __len__ method is called when the class is created."""
      return len(self.__slots__)

    setattr(__len__, '__auto_generated__', True)
    return __len__

  @staticmethod
  def getItemFactory() -> __GETITEM__:
    """The getItemFactory method is called when the class is created."""

    def __getitem__(self, identifier: str) -> Any:
      """The __getitem__ method is called when the class is created."""
      if isinstance(identifier, int):
        if identifier < 0:
          return self[identifier + len(self)]
        if identifier < len(self):
          #  Uses the 'int' valued identifier to retrieve the name from
          #  the '__slots__' tuple. Then this name is passed recursively
          #  back to '__getitem__' retrieving the value from 'str'.
          return self[self.__slots__[identifier]]
        infoSpec = """Index %d out of range for '%s' with %d slots."""
        clsName = type(self).__name__
        info = infoSpec % (identifier, clsName, len(self.__slots__))
        raise IndexError(textFmt(info))
      if isinstance(identifier, str):
        #  Uses the 'str' valued identifier to retrieve the value. The
        #  identifier may initially have been an 'int' value, resolved to
        #  a 'str' value as described above.
        if identifier in self.__slots__:
          try:
            value = getattr(self, identifier)
          except Exception as exception:
            raise exception
          else:
            if value is None:
              try:
                value = type(self).__getattr__(self, identifier)
              except Exception as exception:
                infoSpec = """Unable to retrieve value for attribute '%s' in 
                '%s' object!"""
                clsName = type(self).__name__
                info = infoSpec % (identifier, clsName)
                raise AttributeError(textFmt(info)) from exception
              else:
                return value
            return value
        raise attributeErrorFactory(type(self), identifier)
      if isinstance(identifier, slice):
        sliceKeys = self.__slots__[identifier]
        out = []
        for sliceKey in sliceKeys:
          out.append(self[sliceKey])
        return out
      raise TypeException('key', identifier, str, int, slice)

    setattr(__getitem__, '__auto_generated__', True)
    return __getitem__

  @staticmethod
  def setItemFactory() -> __SETITEM__:
    """The setItemFactory method is called when the class is created."""

    def __setitem__(self, key: str, value: object) -> None:
      """The __setitem__ method is called when the class is created."""
      if key in self.__slots__:
        return setattr(self, key, value)
      raise KeyError(key)

    setattr(__setitem__, '__auto_generated__', True)
    return __setitem__

  @staticmethod
  def getAttrFactory() -> __GETATTR__:
    """The getAttrFactory method is called when the class is created."""

    def __getattr__(self, key: str) -> Any:
      """If the given key is in one of the '__slots__', but this method
      still is invoked, it means that 'object.__getattribute__' was unable
      to retrieve a value for the given key. This method confirms that no
      value is present at 'self' nor in any base. In this case, the method
      attempts to set a default value at the given key for 'self'. """

      if key not in self.__slots__:  # Raises
        raise attributeErrorFactory(self, key)
      value = None
      exception = None
      for slot in self.__slot_objects__:
        if slot.name == key:
          if slot.defaultValue is not None:
            value = slot.defaultValue
            break
          if slot.typeValue is not None:
            value = slot.typeValue()
            break
          try:
            value = self.resolveSlotDefault(key)
          except Exception as e:
            exception = e
          else:
            break
      if value is None:
        infoSpec = """Unable to resolve default value for slot '%s' in 
        '%s' object!"""
        clsName = type(self).__name__
        info = infoSpec % (key, clsName)
        if exception is None:
          raise AttributeError(textFmt(info))
        raise AttributeError(textFmt(info)) from exception
      setattr(self, key, value)
      return value

    setattr(__getattr__, '__auto_generated__', True)
    return __getattr__

  @staticmethod
  def setAttrFactory(*dataFields) -> __SETITEM__:
    """The setAttrFactory method is called when the class is created."""

    def __setattr__(self, key: str, value: Any) -> None:
      """Sets the value of the given key in the EZData instance."""
      if type(self).isFrozen:
        clsName = self.space.getClassName()
        oldValue = getattr(self, key, )
        raise FrozenEZException(key, clsName, oldValue, value)
      if key in self.__slots__:
        return object.__setattr__(self, key, value)
      raise KeyError(key)

    setattr(__setattr__, '__auto_generated__', True)
    return __setattr__

  @staticmethod
  def delAttrFactory(*dataFields) -> __DELATTR__:
    """The delAttrFactory method is called when the class is created."""

    def __delattr__(self, key: str) -> Never:
      """Illegal deleter"""
      raise EZDeleteException(self.space.getClassName(), key, )

    setattr(__delattr__, '__auto_generated__', True)
    return __delattr__

  @staticmethod
  def asTupleFactory(*ezSlots) -> AS_TUPLE:
    """The asTupleFactory method is called when the class is created."""

    def asTuple(self, ) -> tuple:
      """Returns a tuple of the values of the EZData instance."""
      return tuple(getattr(self, key) for key in self.__slots__)

    setattr(asTuple, '__auto_generated__', True)
    return asTuple

  @staticmethod
  def asDictFactory(*ezSlots) -> AS_DICT:
    """The asDictFactory method is called when the class is created."""

    def asDict(self: EZData) -> dict:
      """Returns a dictionary of the values of the EZData instance."""
      return {key: getattr(self, key) for key in self.__slots__}

    setattr(asDict, '__auto_generated__', True)
    return asDict
