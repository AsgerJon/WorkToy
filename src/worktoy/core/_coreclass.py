"""WorkToy - Core - CoreClass
Provides utilities accessible by subclassing this CoreClass or its
subclasses.
The line of such utility classes begins at CoreClass inherited by:
  - CoreClass
  - StringAware
  - ExceptionClass
  ...
  - DefaultClass
Additionally, the core module provides a few optional mixin classes:
  - StateAware
  - TypeAware
Typically, subclasses would inherit from DefaultClass and add mixin
classes as appropriate."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from warnings import warn

from worktoy.core import Function


class CoreClass:
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
    out = []
    for arg in args:
      if isinstance(arg, cls):
        out.append(arg)
    while len(out) < kwargs.get('pad', 0):
      out.append(kwargs.get('padChar', None))
    if out:
      return out
    out = self.starWarning(self.maybeType, [cls, ], args, noKwargs=True)
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

    def parseKeyType(instance: CoreClass, *args, **kwargs) -> list:
      """Parses for keys and types given in positional arguments. Roughly
      speaking, then types are used to find positional arguments and
      strings are used to find keyword arguments:"""
      typeValues = self.maybeTypes(type, *args)
      keyValues = self.maybeTypes(str, *args)
      types = (*typeValues,) or (object,)
      out = []
      for arg in args:
        if isinstance(arg, types):
          out.append(arg)
      for key in keyValues:
        val = kwargs.get(key, None)
        if val is not None and isinstance(val, types):
          out.append(val)
      return out

    return parseKeyType
