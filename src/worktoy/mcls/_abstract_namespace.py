"""
AbstractNamespace class provides a base class for custom namespace
objects used in custom metaclasses.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from ..static import HistDict
from ..text import typeMsg, monoSpace
from ..waitaminute import HookException, DuplicateHookError
from ..waitaminute import HashError, TypeException
from . import Base
from .hooks import AbstractHook

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, TypeAlias

  Bases: TypeAlias = tuple[type, ...]
  Hooks: TypeAlias = list[AbstractHook]


class AbstractNamespace(HistDict):
  """
  AbstractNamespace defines the custom execution environment used by
  AbstractMetaclass during class construction. It provides a controlled
  and extensible context for evaluating class bodies, enabling advanced
  metaprogramming behavior.

  The core feature of AbstractNamespace is its support for modular
  hook-based behavior. Hooks are instances of subclasses of AbstractHook,
  declared directly within the body of the namespace class. Upon
  declaration, each hook registers itself with the namespace via the
  descriptor protocol.

  These hooks allow interception and transformation of key events during
  class construction, including symbol access, assignment, and final
  namespace compilation. For details on available hook methods and their
  intended usage, refer to the AbstractHook documentation.

  This design allows complex functionality, such as decorator-based
  overload resolution and placeholder replacement, to be cleanly
  separated into reusable components. By defining a namespace subclass
  with the desired combination of hooks, users can tailor the behavior of
  class construction without modifying the core metaclass logic.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __owner_hooks_list_name__ = '__hook_objects__'

  #  Private Variables
  __meta_class__ = None
  __class_name__ = None
  __base_classes__ = None
  __key_args__ = None
  __hash_value__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def getBases(self) -> Bases:
    """Returns the base classes of the class under creation."""
    return (*self.__base_classes__,)

  def _computeHash(self, ) -> int:
    """
    Computes the hash value for the future class.
    """
    clsName = self.getClassName()
    baseNames = [base.__name__ for base in self.getBases()]
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

  @classmethod
  def getHookListName(cls, ) -> str:
    """Getter-function for the name of the hook list. """
    if TYPE_CHECKING:
      assert isinstance(cls, dict)
    return cls.__owner_hooks_list_name__

  def getHooks(self, owner: type = None) -> Hooks:
    """Getter-function for the AbstractHook classes. """
    cls = type(self)
    hooks = self.classGetHooks()
    out = []
    for hook in hooks:
      out.append(hook.__get__(self, cls))
    return out

  @classmethod
  def classGetHooks(cls, ) -> Hooks:
    """
    Returns the hooks registered on this class or baseclasses.
    """
    pvtName = cls.getHookListName()
    out = []
    for base in cls.__mro__:
      if issubclass(base, dict):
        hooks = getattr(base, pvtName, [])
        for hook in hooks:
          if not isinstance(hook, AbstractHook):
            raise TypeError(typeMsg('hook', hook, AbstractHook))
          if hook in out:
            continue
          out.append(hook)
    return out

  def getMetaclass(self, ) -> type:
    """Returns the metaclass."""
    return self.__meta_class__

  def getClassName(self, ) -> str:
    """Returns the name of the class."""
    return self.__class_name__

  def getKwargs(self, ) -> dict:
    """Returns the keyword arguments passed to the class."""
    return {**self.__key_args__, **dict()}

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def addHook(cls, hook: AbstractHook) -> None:
    """Adds a hook to the list of hooks. """
    if not isinstance(hook, AbstractHook):
      raise TypeException('hook', hook, AbstractHook)
    existingHooks = cls.classGetHooks()
    for existingHook in existingHooks:
      existingName = existingHook.getFieldName()
      newName = hook.getFieldName()
      if existingName == newName:
        if existingHook is hook:
          return
        hooks = (existingHook, hook)
        raise DuplicateHookError(cls, hook.__name__, *hooks)
    pvtName = cls.getHookListName()
    setattr(cls, pvtName, [*existingHooks, hook])

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: type, name: str, bases: Base, **kwargs) -> None:
    self.__meta_class__ = mcls
    self.__class_name__ = name
    self.__base_classes__ = [*bases, ]
    self.__key_args__ = kwargs or {}

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getitem__(self, key: str, **kwargs) -> Any:
    """Returns the value of the key."""
    try:
      val = HistDict.__getitem__(self, key)
    except KeyError as keyError:
      val = keyError
    for hook in self.getHooks():
      if not isinstance(hook, AbstractHook):
        raise TypeError(typeMsg('hook', hook, AbstractHook))
      try:
        hook.getItemHook(key, val)
      except Exception as exception:
        print('hook exception: %s' % type(hook).__name__)
        print('  key: %s' % key)
        print('  value: %s' % val)
        print('  %s!\n%s' % (type(exception).__name__, str(exception)))
        raise HookException(exception, self, key, val, hook)
    if isinstance(val, KeyError):
      raise val
    return val

  def __setitem__(self, key: str, val: object, **kwargs) -> None:
    """Sets the value of the key."""
    try:
      oldVal = HistDict.__getitem__(self, key)
    except KeyError:
      oldVal = None
    for hook in self.getHooks():
      if TYPE_CHECKING:
        assert isinstance(hook, AbstractHook)
      if hook.setItemHook(key, val, oldVal):
        break
    else:
      HistDict.__setitem__(self, key, val)

  def __str__(self, ) -> str:
    """Returns the string representation of the namespace object."""
    bases = self.getBases()
    spaceName = type(self).__name__
    clsName = self.getClassName()
    baseNames = ', '.join([base.__name__ for base in bases])
    mclsName = self.getMetaclass().__name__
    info = """Namespace object of type: '%s' created by the '__prepare__' 
    method on metaclass: '%s' with base: %s to create class: '%s'."""
    return monoSpace(info % (spaceName, mclsName, baseNames, clsName))

  def __repr__(self, ) -> str:
    """Returns the string representation of the namespace object."""
    bases = self.getBases()
    spaceName = type(self).__name__
    clsName = self.getClassName()
    mclsName = self.getMetaclass().__name__
    baseNames = ', '.join([base.__name__ for base in bases])
    mclsName = self.getMetaclass().__name__
    args = """%s, %s, (%s,)""" % (mclsName, clsName, baseNames)
    kwargs = [(k, v) for (k, v) in self.getKwargs().items()]
    kwargStr = ', '.join(['%s=%s' % (k, str(v)) for (k, v) in kwargs])
    if kwargStr:
      kwargStr = ', %s' % kwargStr
    return """%s(%s%s)""" % (spaceName, args, kwargStr)

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
      namespace = hook.preCompileHook(namespace)
    return namespace

  def compile(self, ) -> dict:
    """This method is responsible for building the final namespace object.
    Subclasses may reimplement preCompile or postCompile as needed,
    but must not reimplement this method."""
    if self.__class_name__ == '_THIS_IS_WHY_WE_CANT_HAVE_NICE_THINGS':
      return dict()
    namespace = self.preCompile()
    for (key, val) in dict.items(self, ):
      namespace[key] = val
    namespace = self.postCompile(namespace)
    namespace['__metaclass__'] = self.getMetaclass()
    namespace['__namespace__'] = self
    return namespace

  def postCompile(self, namespace: dict) -> dict:
    """The object returned from this method is passed to the __new__
    method in the owning metaclass. By default, this method returns dict
    object created by the compile method after performing certain
    validations. Subclasses can implement this method to provide further
    processing of the compiled object. """
    for hook in self.getHooks():
      if TYPE_CHECKING:
        assert isinstance(hook, AbstractHook)
      namespace = hook.postCompileHook(namespace)
    return namespace
