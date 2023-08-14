"""Args is a subclass of list organizing the positional arguments"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic

ic.configureOutput(includeContext=True)


class Args(list):
  """Args is a subclass of list organizing the positional arguments. To
  extract all members of a particular type, use args @ type. To extract
  only the first such element, use args * type."""

  def __init__(self, *args) -> None:
    list.__init__(self, )
    for arg in args:
      self.append(arg)

  def __matmul__(self, other: type) -> Args:
    """Returns a new instance containing the members of this instance that
    belong to this type. Please note that this method removes those
    elements from the original list structure."""
    out = Args()
    keep = []
    for (i, arg) in enumerate(self):
      if isinstance(arg, other):
        out.append(arg)
      else:
        keep.append(arg)
    self.clear()
    for arg in keep:
      self.append(arg)
    return out

  def __rmatmul__(self, other: type) -> Args:
    """Same as __matmul__"""
    return self @ other

  def __mul__(self, other: type) -> Any:
    """Returning the first element of type other"""
    for (i, arg) in enumerate(self):
      if isinstance(arg, other):
        return self.pop(i)

  def __rmul__(self, other: type) -> Any:
    """Same as __mul__"""
    return self * other

  def __rlshift__(self, other: list) -> Any:
    """Transforms all elements of self to other by repeatedly calling the
    append method."""
    while self:
      other.append(self.pop(0))
    return other

  def __sub__(self, other: Any) -> Args:
    """If other is of an iterable type a new instance of Args is returned
    containing elements that are members of self but not members of other.
    If other is not iterable, it is treated as a list having one member."""
    try:
      iter(other)
    except TypeError:
      return self - [other]
    out = Args()
    other = list(other)
    for arg in self:
      if arg in other:
        other.remove(arg)
      else:
        out.append(arg)
    return out

  def __isub__(self, other: Any) -> Args:
    """Removes instances in other from self and returns self. If others is
    not iterable a list containing it is created."""
    try:
      iter(other)
    except TypeError:
      return self - [other]
    for arg in other:
      if arg in self:
        list.remove(self, arg)
    return self

  def __mod__(self, other: Any) -> Args:
    """Pads this instance to achieve a length defined by other. For
    example, if other is an integer, this instance has None appended until
    the length of this instance is equal to other. If other is an iterable
    containing an integer and any other object, then padding uses the
    other object. If both are integers the first is understood to be the
    padding target. If no integer is found or if the length of other is
    longer than two, then the padding target is taken as the length of
    other popping an element from the beginning as the padding object.

    Example:
      Let array = Args(1, 2)
      array % 4 = Args(1, 2, None, None)
      array % (4, 0) = Args(1, 2, 0, 0)
      array % ('never', 'gonna', 'give', 'you', 'up')
        = Args(1, 2, 'give', 'you', 'up')
    """

  def _toStr(self) -> list[str]:
    """Returns a list of string representations of each member"""
    return [str(e) for e in self]

  def __repr__(self) -> str:
    """Code Representation"""
    contents = ', '.join(self._toStr())
    return '%s((%s))' % (self.__class__.__name__, contents)

  def __str__(self) -> str:
    """String Representation"""
    msg = """**Instance of Args.** <br>Args is a subclass of list providing 
    methods convenient for use with positional arguments.<br>This present 
    instance contain the following elements:<br>"""
    elements = []
    maxLen = max([*[len(e) for e in self._toStr()], 0]) + 2
    fmtSpec = ('Index: %%03d - %%%ds - %%s' % (maxLen))
    for (i, arg) in enumerate(self):
      elements.append(fmtSpec % (i, arg, type(arg)))
    contents = '<br>'.join(elements)
    from worktoy.stringtools import monoSpace
    return '\n%s\n%s' % (monoSpace(msg), monoSpace(contents))
