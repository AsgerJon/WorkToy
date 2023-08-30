"""WorkToy - Core - CoreClass
Provides utilities accessible by subclassing this CoreClass or its
subclasses.
Typically, subclasses would inherit from DefaultClass and add mixin
classes as appropriate."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from warnings import warn

from icecream import ic

from worktoy.core import Function, Bases

ic.configureOutput(includeContext=True)


class CoreMeta(type):
  """Creates the __core_instance__ at the end of class initialization."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> dict:
    return dict()

  def __new__(mcls, name: str, bases: Bases, nameSpace: dict, **kw) -> type:
    return type.__new__(mcls, name, bases, nameSpace, **kw)

  def __init__(cls, *args, **kwargs) -> None:
    type.__init__(cls, *args, **kwargs)
    setattr(cls, '__core_instance__', cls.__call__())
  #
  # def __getattr__(cls, key: str) -> object:
  #   if key == '__core_instance__':
  #     return cls()
  #   raise AttributeError(key)
  #
  # def __getattribute__(cls, key: str) -> object:
  #   func = object.__getattribute__(cls, key)
  #   self = object.__getattribute__(cls, '__core_instance__')
  #   if not isinstance(func, Function):
  #     return func
  #   if isinstance(func, Function):
  #
  #     def wrapper(*args, **kwargs) -> object:
  #       """Wrapped version"""
  #       if args and isinstance(args[0], cls):
  #         return func(*args, **kwargs)
  #       return func(self, *args, **kwargs)
  #
  #     return wrapper
  #   raise TypeError(func)


class CoreClass(metaclass=CoreMeta):
  """WorkToy - Core - CoreClass
  Provides utilities accessible by subclassing this CoreClass or its
  subclasses."""

  def __init__(self, *args, **kwargs) -> None:
    self._args = args
    self._kwargs = kwargs

  def starWarning(self,
                  func: Function = None,
                  funcArgs: list = None,
                  args: tuple = None,
                  **kwargs) -> object:
    """This is method is called when one of the methods fails to find an
    argument. If 'args' is a tuple or list of length one, the function is
    repeated but with a star on the first element. Similar for keyword
    arguments. """
    if kwargs.get('singleTuple', False):
      warn('Received one positional argument of type tuple.')
      return None
    if kwargs.get('noKwargs', False) and len(args) == 1:
      if isinstance(args[0], (tuple, list)):
        warn('Missing stars?')
        return func(*funcArgs, *(*args[0],))
    if kwargs.get('noKwargs', False) and not args:
      return []
    if kwargs.get('emptyKwargs', False) and len(args) > 1:
      if isinstance(args[-1], dict):
        newArgs, newKwargs = (*args[:-1],), args[-1]
        return func(*funcArgs, *newArgs, **newKwargs)

  def maybe(self, *args, **_) -> object:
    """Returns the first argument different from None"""
    for arg in args:
      if arg is not None:
        return arg
    return self.starWarning(self.maybe, [], args, noKwargs=True)

  def maybeType(self, cls: type, *args) -> object:
    """Returns the first argument belonging to cls"""
    for arg in args:
      if isinstance(arg, cls):
        return arg
    return self.starWarning(self.maybeType, [cls, ], args, noKwargs=True)

  def maybeTypes(self, cls: type, *args, **kwargs) -> list:
    """Returns all arguments belonging to cls"""
    if not args:
      return []
    out = []
    for arg in args:
      if isinstance(arg, cls):
        out.append(arg)
    while len(out) < kwargs.get('pad', 0):
      out.append(kwargs.get('padChar', None))
    if out:
      return out
    out = self.starWarning(self.maybeTypes, [cls, ], args, noKwargs=True)
    if isinstance(out, list):
      return out

  def maybeKey(self, *args, **kwargs) -> object:
    """Finds the first object in kwargs that matches a given key. Provide
    keys as positional arguments of stringtype. Optionally provide a
    'type' in the positional arguments to return only an object of that
    type."""
    type_ = self.maybeType(type, *args)
    if not isinstance(type_, type):
      type_ = object
    keys = self.maybeTypes(str, *args)
    if not isinstance(type_, (tuple, list)):
      type_ = (type_,)
    if not isinstance(keys, (tuple, list)):
      keys = (keys,)
    if not kwargs:
      funcArgs = [*type_, *keys]
      newArgs = (*[arg for arg in args if arg not in funcArgs],)
      newKwargs = dict(emptyKwargs=True, )
      return self.starWarning(self.maybeKey, funcArgs, newArgs, **newKwargs)
    for key in keys:
      val = kwargs.get(key, None)
      if isinstance(val, type_) and val is not None:
        return val

  def maybeKeys(self, *args, **kwargs) -> list:
    """Same as maybeKey, but removes every value that matches a given key."""
    keyArgs, otherArgs = [], []
    for arg in args:
      if isinstance(arg, str):
        keyArgs.append(arg)
      else:
        otherArgs.append(arg)
    out = []
    for key in keyArgs:
      out.append(self.maybeKey(key, *otherArgs, **kwargs))
    return out

  def empty(self, *args) -> bool:
    """Returns True if every positional argument is None. The method
    returns True when receiving no positional arguments. Otherwise, the
    method returns True."""
    self.starWarning(singleTuple=True)
    if not args:
      return True
    for arg in args:
      if arg is not None:
        return False
    return True

  def plenty(self, *args) -> bool:
    """The method returns True if no positional argument is None.
    Otherwise, the method returns False. """
    self.starWarning(singleTuple=True)
    if not args:
      return True
    for arg in args:
      if arg is None:
        return False
    return True

  def pad(self, source: list, target: object = None, **kwargs) -> list:
    """The target argument indicates the desired shape. Elements from
    source replace from left to right in the target. If 'source' has more
    members than target, 'source' is returned. Setting an integer for
    target is taken to mean a 'None'-list of length given by the
    integer."""
    if source is None:
      raise TypeError('source argument is missing')
    if not target:
      return source
    if isinstance(target, (list, tuple)):
      if len(target) < len(source):
        return source
      out = []
      for (i, item) in enumerate(target):
        out.append(source[i] if i < len(source) else item)
      return out
    padChar = kwargs.get('padChar', None)
    if isinstance(target, int):
      return self.pad(source, [padChar for _ in range(target)], **kwargs)
    padLen = kwargs.get('padLen', 0)
    return self.pad(source, padLen, **kwargs)

  def parseFactory(self, type_: type, *keys) -> Function:
    """Creates a parsing function"""

    def parseKeyType(*args, **kwargs) -> list:
      """Parses for keys and types given in positional arguments. Roughly
      speaking, then types are used to find positional arguments and
      strings are used to find keyword arguments:"""
      keyArgs = []
      for key in keys:
        arg = kwargs.get(key, None)
        if arg is not None:
          keyArgs.append(arg)
      out = []
      for arg in keyArgs:
        out.append(arg)
      for arg in args:
        out.append(arg)
      return [arg for arg in out if isinstance(arg, type_)]

    return parseKeyType

  def getArgs(self) -> list:
    """Getter-function for the list of positional arguments."""
    return [arg for arg in self._args]

  def getKwargs(self) -> dict:
    """Getter-function for the dictionary of keyword arguments."""
    return self._kwargs

  def setArgs(self, *args) -> None:
    """Setter-function for the positional arguments"""
    self._args = [*args, ]

  def setKwargs(self, **kwargs) -> None:
    """Setter function for the keyword arguments"""
    self._kwargs = kwargs

  def setAllArgs(self, *args, **kwargs) -> None:
    """Setting both positional arguments and keyword arguments."""
    self._args, self._kwargs = self.setArgs(*args), self.setKwargs(**kwargs)
