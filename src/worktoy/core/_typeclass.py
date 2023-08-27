"""WorkToy - Core - TypeClass
Alternative to GenericAlias supporting instance checking."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import Function, ParsingClass

ic.configureOutput(includeContext=True)


class TypeClass(ParsingClass):
  """WorkToy - Core - TypeClass
  Alternative to GenericAlias supporting instance checking."""

  def __init__(self, *args, **kwargs) -> None:
    ParsingClass.__init__(self, *args, **kwargs)
    self._signature = self.collectSignature(*args)
    self._nestFactor = 4

  def __eq__(self, other: TypeClass) -> bool:
    """If both nested level and type are the same in self and other for
    each entry, self and other are considered equal. """
    if len(self.getFlatSignature()) - len(other.getFlatSignature()):
      return False
    return True if self._signature == other._signature else False

  def getFlatSignature(self) -> list:
    """Getter-function for the flattened signature"""
    return self.flatten(self.getSignature())

  def getSignature(self) -> list:
    """Getter-function for the signature"""
    return self._signature

  def collectSignature(self, *args) -> list:
    """Collects the signature from the arguments"""

  def nestedTypes(self, callBack: Function, entries: list, **kwargs) -> list:
    """Returns the nested list or type"""
    out = []
    r = kwargs.get('r', -1) + 1
    for arg in entries:
      if isinstance(arg, list):
        entry = self.nestedTypes(callBack, arg, r=r)
      else:
        entry = callBack(arg, r)
      out.append(entry)
    return out

  def collectTypes(self, *args) -> list:
    """Collects the arguments of list or type."""
    out = []
    for arg in args:
      if isinstance(arg, (list, type)):
        out.append(arg)
    return out

  def typeString(self, element: dict, fmtSpec: Function = None) -> str:
    """Prints out the entry"""
    if fmtSpec is None:
      fmtSpec = lambda x: x.upper()
    try:
      numTabs = element.get('nestLevel') * self._nestFactor
      tab = numTabs * ' '
      name = fmtSpec(element.get('name'))
      return '%s%s' % (tab, name)
    except AttributeError as e:
      ic(element)
      raise e

  def __str__(self) -> str:
    """String Representation"""
    lines = [self.typeString(e) for e in self.getFlatSignature()]
    return '\n'.join(lines)

  def __repr__(self) -> str:
    """Code Representation"""
    flat = self.getFlatSignature()
    r = -1
    stringList = []
    for element in flat:
      r0 = r
      r = element.get('nestLevel')
      nestStep = r - r0  # positive more nested
      delim = '[ ' if nestStep > 0 else ('] ' if nestStep < 0 else '')
      member = element.get('name')
      entry = '%s<%s>, ' % (delim, member)
      stringList.append(entry)
    while r + 1:
      stringList.append('], ')
      r -= 1
    stringList[-1] = stringList[-1].replace(', ', '')
    return ''.join(stringList)
