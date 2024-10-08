"""InfoHandle encapsulates messages along with an InfoGroup permitting
grouping of messages. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy._WORK_IN_PROGRESS.info import InfoGroup, InfoField, BaseGroup
from worktoy.text import typeMsg

try:
  from typing import Callable, Any
except ImportError:
  Callable = object

from worktoy.parse import maybe


class InfoHandle:
  """LOL"""

  __info_instances__ = None

  @classmethod
  def _getInfoInstances(cls) -> list[InfoHandle]:
    """Getter-function for list of instances"""
    return maybe(cls.__info_instances__, [])

  @classmethod
  def _registerInfoInstance(cls, self: InfoHandle) -> None:
    """Registers the instance"""
    instances = cls._getInfoInstances()
    if self not in instances:
      cls.__info_instances__ = [*instances, self]

  @classmethod
  def _getGroupedInstances(cls, infoGroup: InfoGroup) -> list[InfoHandle]:
    """Returns the instances belonging to the given group"""
    print('_getGroupedInstances: ', infoGroup)
    base = cls._getInfoInstances()
    print('\n'.join([str(i) for i in base]))
    out = [i for i in base if i.grp == infoGroup]
    print(out)
    return out

  msg = InfoField('')
  grp = InfoField(BaseGroup)

  def __init__(self, *args) -> None:
    """The '__init__' method initializes the descriptor."""
    if not args:
      e = """The message is not set!"""
      raise ValueError(e)
    if len(args) == 1:
      self.msg = args[0]
    elif len(args) > 1:
      self.msg, self.grp = [*args, ][:2]
    self._registerInfoInstance(self)
    if self not in self._getInfoInstances():
      raise ValueError
    print("""lmao: %s = %s""" % (str(self.grp), self.msg))

  def __matmul__(self, other: object) -> InfoHandle:
    """The '__matmul__' method is invoked when the '@' operator is used."""
    if isinstance(other, InfoGroup):
      print(self)
      self.grp = other
      print(self)
      return self
    if isinstance(other, str):
      return self @ InfoGroup(other)
    return NotImplemented

  def __str__(self, ) -> str:
    """String representation"""
    return """InfoHandle('%s'): \n--<| %s""" % (str(self.grp), self.msg)

  def __repr__(self, ) -> str:
    """String representation"""
    return """InfoHandle('%s', %s)""" % (self.msg, self.grp)

  def __class_getitem__(cls, infoGroup: object, **kwargs) -> None:
    """The '__class_getitem__' method is invoked when the class is
    indexed."""
    if isinstance(infoGroup, InfoGroup):
      header = """Beginning Printout of group: '%s'""" % str(infoGroup)
      body = []
      for self in cls._getGroupedInstances(infoGroup):
        body.append(str(self))
      else:
        footer = """End of Printout"""
        lines = [header, *body, footer]
        n = max([len(i) for i in lines])
        header = header.center(n, '_').center(n + 4, '|')
        footer = footer.center(n, '¨').center(n + 4, '|')
        lines = [line.ljust(n, ' ').center(n + 4, '|') for line in
                 lines[1:-1]]
        print(header)
        for line in lines:
          print(line)
        print(footer)
        return
    elif isinstance(infoGroup, str):
      if kwargs.get('_recursion', False):
        raise RecursionError
      grp = getattr(InfoGroup, infoGroup, None)
      if grp is None:
        return cls.__class_getitem__(InfoGroup(infoGroup), _recursion=True)
      return cls.__class_getitem__(infoGroup, _recursion=True)
    e = typeMsg('infoGroup', infoGroup, InfoGroup)
    raise TypeError(e)
