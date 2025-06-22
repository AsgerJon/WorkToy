"""
HistDict is a subclass of dict that keeps track of all accessor calls made
to either of its '__getitem__', '__setitem__', and '__delitem__' methods.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ..parse import maybe
from . import ItemCall
from ..waitaminute import TypeException

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class HistDict(dict):
  """
  HistDict is a subclass of dict that keeps track of all accessor calls made
  to either of its '__getitem__', '__setitem__', and '__delitem__' methods.
  """
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __item_calls__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getItemCalls(self) -> list[ItemCall]:
    """
    Returns a list of all item calls made to the namespace.
    """
    return maybe(self.__item_calls__, [])

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addItemCall(self, *args) -> None:
    """
    Adds an item call to the namespace.
    """
    if len(args) == 1 and isinstance(args[0], ItemCall):
      itemCall = args[0]
    else:
      itemCall = ItemCall(*args)
    existing = self.getItemCalls()
    self.__item_calls__ = [*existing, itemCall]

  def extendItemCalls(self, *args, **kwargs) -> None:
    """
    Extends the item calls with the provided list of ItemCall objects.
    """
    cls = type(self)
    itemCalls = []
    other = None
    for arg in args:
      if isinstance(arg, cls):
        other = arg
        break
      elif isinstance(arg, ItemCall):
        itemCalls.append(arg)
    else:
      for itemCall in itemCalls:
        if isinstance(itemCall, ItemCall):
          self.addItemCall(itemCall)
      else:
        return None
    if kwargs.get('_recursion', False):
      raise RecursionError  # pragma: no cover
    return self.extendItemCalls(*other.getItemCalls(), _recursion=True)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __getitem__(self, key: str, **kwargs) -> Any:
    """
    Gets the value associated with the key in the namespace.
    """
    try:
      value = dict.__getitem__(self, key)
    except KeyError as keyError:
      self.addItemCall(key, keyError, dict.__getitem__)
      raise keyError
    else:
      self.addItemCall(key, value, dict.__getitem__)
      return value
    finally:
      pass

  def __setitem__(self, key: str, value: Any, **kwargs) -> None:
    """
    Sets the value associated with the key in the namespace.
    """
    self.addItemCall(key, value, dict.__setitem__)
    return dict.__setitem__(self, key, value)

  def __delitem__(self, key: str, **kwargs) -> None:
    """
    Deletes the value associated with the key in the namespace.
    """
    try:
      value = dict.__getitem__(self, key)
    except KeyError as keyError:
      self.addItemCall(key, keyError, dict.__delitem__)
    else:
      self.addItemCall(key, value, dict.__delitem__)
      return dict.__delitem__(self, key)
    finally:
      pass

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    """
    Initializes the HistDict instance and sets up the item calls list.
    """
    dict.__init__(self, )
    for key, val in kwargs.items():
      if isinstance(key, str):
        raise TypeException('key', key, str)
      self[key] = val
