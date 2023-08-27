"""WorkToy - Core - TreeStructure
The class implements general representations of data structures as trees."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from worktoy.core import StringAware, FLAG, AbstractDescriptor


class Node(StringAware):
  """The class implements general representations of data structures as
  trees."""

  __is_root__ = FLAG[False,]
  __is_node__ = FLAG[False,]
  __is_leaf__ = FLAG[False,]
  __is_elemental__ = FLAG[False,]
  __parent_node__ = AbstractDescriptor[None, Node]

  def __init__(self, obj: object = None, *args, **kwargs) -> None:
    StringAware.__init__(self, *args, **kwargs)
    self._isRoot = None
    self._isNode = None
    self._isLeaf = None
    self._isElemental = None
    self._object = None
    self.setObject(obj)

  def setObject(self, obj: object, *args, **kwargs) -> None:
    """Setter function for the object. """
    self._isRoot = kwargs.get('_isRoot', True)
    if isinstance(obj, tuple):
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.setObject([*obj, ], _recursion=True)
    if isinstance(obj, list):
      for item in obj:
        pass

      raise NotImplementedError
    if not isinstance(obj, list):
      self.toLeaf(obj)

  def toLeaf(self, obj: object, **kwargs) -> None:
    """Sets this instance of Node as a leaf wrapping the given object."""
    parent = kwargs.get('_parent', None)
    if parent is None:
      self.toElemental(obj)

  def toElemental(self, obj) -> None:
    """Sets this instance of Node as an Elemental Node. """
    self._object = obj
    self._isRoot = True
    self._isNode = False
    self._isLeaf = True
    self._isElemental = True

  def setReady(self) -> bool:
    """Changes the state of the instance to ready. Notifies listeners."""


class TreeStructure(StringAware, metaclass=type):
  """The class implements general representations of data structures as
  trees."""

  def __init__(self, *args, **kwargs) -> None:
    StringAware.__init__(self, *args, **kwargs)
    self._wrappedObject = None
    self.setWrappedObject(*args, **kwargs)
    self._children = []

  @abstractmethod
  def setWrappedObject(self, *args, **kwargs) -> None:
    """Setter-function for the inner object"""

  @abstractmethod
  def getWrappedObject(self, ) -> object:
    """Setter-function for the inner object"""

  @abstractmethod
  def append(self, *args, **kwargs) -> None:
    """Appends a child to the structure."""

  def __eq__(self, other: object) -> bool:
    """Structures are equal if they have the same structure, even if the
    contents at their leaves are not the same. Subclass may implement the
    method to support other types, but by default, only other instances
    of TreeStructure support the equal operator."""
    if not isinstance(other, TreeStructure):
      return NotImplemented


class _Node(TreeStructure):
  """Subclass of TreeStructure wrapping iterables. """

  def __init__(self, *args, **kwargs) -> None:
    TreeStructure.__init__(self, *args, **kwargs)

  def setWrappedObject(self, obj: object, *args, **kwargs) -> None:
    """Requires a list or tuple."""
    if isinstance(obj, tuple):
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.setWrappedObject([*obj, ], _recursion=True)
    if not isinstance(obj, list):
      raise TypeError
    self._wrappedObject = obj
