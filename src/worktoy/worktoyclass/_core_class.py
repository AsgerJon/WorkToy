"""WorkToy - Core - CoreClass
Provides utilities accessible by subclassing this CoreClass or its
subclasses.
Typically, subclasses would inherit from DefaultClass and add mixin
classes as appropriate."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Optional


class CoreClass:
  """WorkToy - Core - CoreClass
  Provides utilities accessible by subclassing this CoreClass or its
  subclasses."""

  def __init__(self, *args, **kwargs) -> None:
    self._args = args
    self._kwargs = kwargs

  def maybe(self, *args, ) -> Any:
    """
  The maybe function returns the first argument that is not None.

  :param *args: Pass in a tuple of arguments to the function
  :return: The first argument that is not 'None'
  """
    for arg in args:
      if arg is not None:
        return arg

  def maybeType(self, cls: type, *args) -> Any:
    """
    Returns the first positional argument belonging to the type given in
    the 'cls' argument.

    :param cls: type: Specify that the first parameter is a type
    :param *args: Pass a variable number of arguments to the function
    :return: The first argument that is an instance of 'cls'
    """
    for arg in args:
      if isinstance(arg, cls):
        return arg

  def maybeTypes(self, cls: type, *args, **kwargs) -> list:
    """
    Returns each positional argument belonging to the type given in the
    'cls' argument. Use keyword arguments 'pad' and 'padChar' to set a
    padding and a padding character. For example:
      maybeTypes(int, 'a', 1, 1.5, 2, pad=4, padChar=-1)
      >>> [1, 2, -1, -1]
    :param cls: type: Specify the type of class that we are looking for
    :param *args: Pass in a list of arguments
    :param **kwargs: Pass keyword arguments to the function
    :return: A list of all the arguments that are instances
    """
    out = [arg for arg in args if isinstance(arg, cls)]
    while len(out) < kwargs.get('pad', 0):
      out.append(kwargs.get('padChar', None))
    return out

  def searchKey(self, *keys, **kwargs) -> Any:
    """
    This method searches the positional arguments for an argument at each
    given key.
    :param *keys: Pass in a list of keys to search for
    :param **kwargs: Pass in keyword arguments to the function
    :return: The first value that is not none
    """
    for key in keys:
      val = kwargs.get(key, None)
      if val is not None:
        return val

  def searchKeys(self, *keys, **kwargs) -> Optional[list]:
    """Returns a list of 'kwargs' matching a key."""
    out = []
    if not keys:
      return None
    for key in keys:
      val = kwargs.get(key, None)
      if val is not None:
        out.append(val)
    return out or None

  def _maybeKey(self, allInstances: bool, *args, **kwargs) -> Any:
    """Finds the first object in kwargs that matches a given key. Provide
    keys as positional arguments of stringtype. Optionally provide a
    'type' in the positional arguments to return only an object of that
    type."""
    out = []
    if not kwargs:
      return out
    types = [arg for arg in args if isinstance(arg, type)]
    keys = [arg for arg in args if isinstance(arg, str)]
    keyVals = self.searchKeys(*keys, **kwargs)
    if keyVals is None:
      return keyVals
    if not types:
      return keyVals if allInstances else keyVals[0]
    out = []
    for cls in types:
      for val in keyVals:
        if isinstance(val, cls):
          if not allInstances:
            return val
          out.append(val)
    if allInstances:
      return out

  def maybeKey(self, *args, **kwargs) -> Any:
    """Finds the first object in kwargs that matches a given key and
    belongs to a given type."""
    return self._maybeKey(False, *args, **kwargs) or None

  def maybeKeys(self, *args, **kwargs) -> Any:
    """Finds all objects in kwargs matching any of the given keys and
    belonging to any given types. If no types are given, no type check is
    performed."""
    return self._maybeKey(True, *args, **kwargs) or None

  def empty(self, *args) -> bool:
    """Returns True if every positional argument is None. The method
    returns True when receiving no positional arguments. Otherwise, the
    method returns True."""
    if not args:
      return True
    for arg in args:
      if arg is not None:
        return False
    return True

  def plenty(self, *args) -> bool:
    """The method returns True if no positional argument is None.
    Otherwise, the method returns False. """
    if not args:
      return True
    for arg in args:
      if arg is None:
        return False
    return True

  def getArgs(self) -> list:
    """Getter-function for the list of positional arguments."""
    if self._args is None:
      return []
    return [arg for arg in self._args]

  def getKwargs(self) -> dict:
    """Getter-function for the dictionary of keyword arguments."""
    return self._kwargs

  def setArgs(self, *args) -> None:
    """Setter-function for the positional arguments"""
    self._args = args

  def setKwargs(self, **kwargs) -> None:
    """Setter function for the keyword arguments"""
    self._kwargs = kwargs

  def setAllArgs(self, *args, **kwargs) -> None:
    """Setting both positional arguments and keyword arguments."""
    self._args, self._kwargs = self.setArgs(*args), self.setKwargs(**kwargs)
