"""This file contains Enum classes with convenient functionalities
relating to the Fielf decorator class."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from enum import IntEnum
import os

from worktoy.core import extractArg, Extracted
from worktoy.stringtools import stringList, justify


class Perm(IntEnum):
  """Enum defining permission profiles"""
  SECRET = 0
  READONLY = 1
  READSET = 2
  FULL = 3

  @classmethod
  def parseArg(cls, *args, **kwargs) -> Extracted:
    """Parses from arguments the appropriate permission profile"""
    readKeys = stringList('read, readable, allowRead')
    setKeys = stringList('set, allowSet, canSet, editable')
    delKeys = stringList('del, allowDel, erase, deletable')
    read, args, kwargs = extractArg(bool, readKeys, *args, **kwargs)
    set_, args, kwargs = extractArg(bool, setKeys, *args, **kwargs)
    del_, args, kwargs = extractArg(bool, delKeys, *args, **kwargs)
    if del_:
      return Extracted(Perm.FULL, args, kwargs)
    if set_:
      return Extracted(Perm.READSET, args, kwargs)
    if read:
      return Extracted(Perm.READONLY, args, kwargs)
    return Extracted(Perm.SECRET, args, kwargs)


class NameF(IntEnum):
  """For a variable, the name can take different styles:"""

  @staticmethod
  def noChange(name: str) -> str:
    """Returns name with no change"""
    return name

  @staticmethod
  def dash(name: str) -> str:
    """Returns name with dash in front"""
    return '_%s' % (name)

  @staticmethod
  def cap(name: str) -> str:
    """Returns name with first letter capitalised"""
    return '%s%s' % (name[0].upper(), name[1:])

  @staticmethod
  def _all(name: str) -> list[str]:
    """Returns a list of name in all formats"""
    return [
      NameF.noChange(name),
      NameF.cap(name),
      NameF.dash(name),
    ]

  @staticmethod
  def privateVariableName(name: str) -> str:
    """Suggests a private variable name for field of given name"""
    return NameF.DASH @ name

  NAME = 0
  CAP = 1
  DASH = 2

  def __matmul__(self, name: str) -> str:
    return self._all(name)[self]

  def __rmatmul__(self, name: str) -> str:
    return self @ name


class Accessor(IntEnum):
  """Enum defining access types"""

  @staticmethod
  def _loadDocs() -> str:
    """Loads the docs"""
    here = os.getcwd()
    name = '_config.inf'
    fullPath = os.path.join(here, name)
    with open(fullPath, 'r', encoding='utf-8') as f:
      out = f.read()
    return out

  @staticmethod
  def _baseDoc() -> str:
    lines = [
      """The field was created with the Field decorator from 
the worktoy.field module. """, """For more information, visit:""",
      """https://github.com/AsgerJon/WorkToy""",
      """Or simply: pip install worktoy""",
      """For contact, please visit my open linkedin:""",
      """https://www.linkedin.com/in/asgerjonvistisen/"""]
    lines = [justify(line) for line in lines]
    sig = Accessor._loadDocs()
    return '%s\n%s' % ('\n'.join(lines), sig)

  READ = 0
  SET = 1
  DEL = 2

  def _shortDash(self) -> str:
    """Returns a short and dashed version of this accessor"""
    return stringList('_get, _set, _del')[self]

  def denyDoc(self) -> str:
    """Suggests a docstring for an illegal accessor function"""
    return 'Illegal %s-function!\n%s' % (self, self._baseDoc())

  def allowDoc(self, name: str, type_: type, cls: type) -> str:
    """Docstring!"""
    typeName, className = type_.__name__, cls.__name__
    msg = """%s-function for field named %s of type %s 
    belonging to class %s.""" % (self, name, typeName, className)
    infoLine = msg
    return '%s\n%s' % (infoLine, Accessor._baseDoc())

  def functionName(self, name: str) -> str:
    """Suggests a name for an accessor function for variable of given
    name."""
    return '%s%s' % (self._shortDash(), NameF.CAP @ name)

  def __str__(self) -> str:
    """String representation"""
    return stringList('getter, setter, deleter')[self]
