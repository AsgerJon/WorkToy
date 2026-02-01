"""
KeeSpace provides the namespace class used by the 'worktoy.keenum' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls import BaseSpace
from ..waitaminute.keenum import KeeDuplicate, KeeTypeException
from ..waitaminute.keenum import KeeNameConflict
from . import KeeSpaceHook, Kee

if TYPE_CHECKING:  # pragma: no cover
  from typing import Dict, TypeAlias

  Members: TypeAlias = Dict[str, Kee]
  Bases: TypeAlias = tuple[type, ...]


class KeeSpace(BaseSpace):
  """KeeSpace provides the namespace class used by the 'worktoy.keenum'
  module. """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  keeSpaceHook = KeeSpaceHook()

  #  Private Variables
  __enumeration_members__ = None
  __member_type__ = None
  __num_list__ = None
  __null_value__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addNum(self, name: str, member: Kee) -> None:
    """Adds the member to the enumeration dict. """
    if name in self.__enumeration_members__:
      oldMember = self.__enumeration_members__[name]
      raise KeeDuplicate(name, oldMember, member)
    try:
      oldName = member.name
    except AttributeError:
      member.name = name
    else:
      if oldName != name:
        raise KeeNameConflict(member, oldName, name)
    member.__num_index__ = len(self.__enumeration_members__)
    member = self.typeGuard(member)
    self.__enumeration_members__[name] = member

  def typeGuard(self, member: Kee) -> Kee:
    """Ensures that the member is an instance of KeeNum. """
    if self.__member_type__ is None:
      self.__member_type__ = member.__field_type__
      return member
    if self.__member_type__ is member.__field_type__:
      return member
    name, val, type_ = member.name, member.getValue(), self.__member_type__
    raise KeeTypeException(name, val, type_, )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: type, name: str, bases: Bases, **kwargs) -> None:
    self.__enumeration_members__ = dict()
    super().__init__(mcls, name, bases, **kwargs)
    cls = type(self)

    for base in bases:
      try:
        space = getattr(base, '__namespace__')
      except AttributeError:
        continue
      else:
        try:
          memberType = space.__member_type__
        except AttributeError:
          continue
        else:
          self.__member_type__ = memberType
        try:
          members = getattr(space, '__enumeration_members__')
        except AttributeError:
          continue
        else:
          for i, (key, val) in enumerate(members.items()):
            if key in self.__enumeration_members__:
              oldMember = self.__enumeration_members__[key]
              raise KeeDuplicate(key, oldMember, val)
            self.addNum(key, val)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
