"""AbstractNamespace class provides a base class for custom namespace
objects used in custom metaclasses."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ..parse import maybe
from ..static import HistDict
from ..text import typeMsg, monoSpace, joinWords
from ..waitaminute import MissingVariable, HashError, TypeException
from . import Base, Types, Spaces
from .hooks import AbstractHook

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


class AbstractNamespace(HistDict):
  """AbstractNamespace class provides a base class for custom namespace
  objects used in custom metaclasses."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback variables
  __owner_hooks_list_name__ = '__hook_objects__'

  #  Reserved private names
  __meta_class__ = None
  __class_name__ = None
  __base_classes__ = None
  __base_spaces__ = None
  __key_args__ = None
  __hash_value__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  @classmethod
  def getHookListName(cls, ) -> str:
    """Getter-function for the name of the hook list. """
    if TYPE_CHECKING:
      assert isinstance(cls, dict)
    return cls.__owner_hooks_list_name__

  def getHooks(self, owner: type = None) -> list[AbstractHook]:
    """Getter-function for the AbstractHook classes. """
    pvtName = self.getHookListName()
    cls = type(self)
    hooks = getattr(cls, pvtName, [])
    out = []
    for hook in hooks:
      out.append(hook.__get__(self, cls))
    return out

  @classmethod
  def getLegacySpace(cls, self, ) -> Self:
    """
    Returns the namespace object of the base classes.
    """
    itemCalls = []
    mroClasses = [*reversed(self.getMRO(), )]
    for base in mroClasses:
      if base is self:
        continue
      space = getattr(base, '__namespace__', None)
      if space is None:
        continue
      if isinstance(space, HistDict):
        itemCalls.extend(space.getItemCalls())
        continue
    mcls = self.getMetaclass()
    name = self.getClassName()
    bases = self.getClassBases()
    kwargs = self.getKwargs()
    out = cls(mcls, name, (), **kwargs)
    for call in itemCalls:
      out = call.applyToNamespace(out)
    return out

  def getClassBases(self) -> tuple[type, ...]:
    """
    Getter-function for the given base classes.
    """
    return maybe(self.__base_classes__, ())

  def _computeHash(self, ) -> int:
    """
    Computes the hash value for the future class.
    """
    clsName = self.getClassName()
    baseNames = [base.__name__ for base in self.getClassBases()]
    mclsName = self.getMetaclass().__name__
    return hash((clsName, *baseNames, mclsName,))

  def getHash(self, **kwargs) -> int:
    """
    Resolves the hash value for the future class.
    """
    computedHash = self._computeHash()
    if self.__hash_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__hash_value__ = computedHash
      return self.getHash(_recursion=True)
    if not isinstance(self.__hash_value__, int):
      raise TypeException('__hash_value__', self.__hash_value__, int)
    if self.__hash_value__ != computedHash:
      raise HashError(self.__hash_value__, computedHash, )
    return self.__hash_value__

  def getMetaclass(self, ) -> type:
    """Returns the metaclass."""
    return self.__meta_class__

  def getClassName(self, ) -> str:
    """Returns the name of the class."""
    return self.__class_name__

  def getKwargs(self, ) -> dict:
    """Returns the keyword arguments passed to the class."""
    return {**self.__key_args__, **dict()}

  def getMRO(self, ) -> Types:
    """Returns the method resolution order of the class."""
    mcls = self.getMetaclass()
    name = self.getClassName()
    Space = type(self)
    space = Space(mcls, name, self.getClassBases(), **self.getKwargs())
    bases = self.getClassBases()
    tempClass = mcls('_', (*bases,), space)
    return tempClass.__mro__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def addHook(cls, hook: AbstractHook) -> None:
    """Adds a hook to the list of hooks. """
    if TYPE_CHECKING:
      assert isinstance(cls, dict)
    if not isinstance(hook, AbstractHook):
      raise TypeError(typeMsg('hook', hook, AbstractHook))
    existingHooks = getattr(cls, cls.getHookListName(), [])
    setattr(cls, cls.getHookListName(), [*existingHooks, hook])

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: type, name: str, bases: Base, **kwargs) -> None:
    self.__meta_class__ = mcls
    self.__class_name__ = name
    if len(bases) > 1:
      e = """The 'worktoy' package does not support multiple inheritance!"""
      raise TypeError(monoSpace(e))
    self.__base_classes__ = (*bases,)
    self.__key_args__ = kwargs or {}

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __setitem__(self, key: str, val: object, **kwargs) -> None:
    """Sets the value of the key."""
    try:
      oldVal = dict.__getitem__(self, key)
    except KeyError:
      oldVal = None
    for hook in self.getHooks():
      if TYPE_CHECKING:
        assert isinstance(hook, AbstractHook)
      if hook.setItemHook(self, key, val, oldVal):
        break
    else:
      dict.__setitem__(self, key, val)

  def _getStrComponents(self, ) -> dict:
    """
    Resolves the components of 'self' that is shared between __repr__ and
    __str__.
    """
    spaceClass = type(self).__name__
    className = self.getClassName()
    mclsName = self.getMetaclass().__name__
    baseNames = [base.__name__ for base in self.getClassBases()]

    kwargStr = []
    for key, value in self.getKwargs().items():
      kwargStr.append("""%s=%s""" % (key, repr(value),))
    kwargStr = ', '.join(kwargStr, )

    return dict(
        spaceClass=spaceClass,
        className=className,
        mclsName=mclsName,
        baseName=baseNames,
        kwargStr=kwargStr,
    )

  def __str__(self, ) -> str:
    """Returns the string representation of the namespace object."""
    infoSpec = """Namespace object of type: '%s' created by metaclass: 
    '%s' with bases: '%s' to create class: '%s'."""
    components = self._getStrComponents()
    spaceClass = components['spaceClass']
    className = components['className']
    mclsName = components['mclsName']
    baseName = joinWords(components['baseName'], )
    kwargStr = components['kwargStr']
    return infoSpec % (spaceClass, mclsName, baseName, className)

  def __repr__(self, ) -> str:
    """Returns the string representation of the namespace object."""
    infoSpec = """%s(%s, %s, %s, **%s)"""
    components = self._getStrComponents()
    spaceClass = components['spaceClass']
    className = components['className']
    mclsName = components['mclsName']
    baseName = joinWords(components['baseName'], )
    kwargStr = components['kwargStr']
    return infoSpec % (spaceClass, mclsName, className, baseName, kwargStr,)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def preCompile(self, ) -> dict:
    """The return value from this method is passed to the compile method.
    Subclasses can implement this method to provide special objects at
    particular names in the namespace. By default, an empty dictionary is
    returned. """
    namespace = dict()
    for hook in self.getHooks():
      if TYPE_CHECKING:
        assert isinstance(hook, AbstractHook)
      namespace = hook.preCompileHook(self, namespace)
    return namespace

  def compile(self, ) -> dict:
    """This method is responsible for building the final namespace object.
    Subclasses may reimplement preCompile or postCompile as needed,
    but must not reimplement this method."""
    namespace = self.preCompile()
    for (key, val) in dict.items(self, ):
      namespace[key] = val
    namespace['__metaclass__'] = self.getMetaclass()
    namespace['__namespace__'] = self
    return self.postCompile(namespace)

  def postCompile(self, namespace: dict) -> dict:
    """The object returned from this method is passed to the __new__
    method in the owning metaclass. By default, this method returns dict
    object created by the compile method after performing certain
    validations. Subclasses can implement this method to provide further
    processing of the compiled object. """
    for hook in self.getHooks():
      if TYPE_CHECKING:
        assert isinstance(hook, AbstractHook)
      namespace = hook.postCompileHook(self, namespace)
    if '__metaclass__' not in namespace:
      raise MissingVariable('__metaclass__', self.getMetaclass())
    if '__namespace__' not in namespace:
      raise MissingVariable('__namespace__', type(self))
    return namespace
