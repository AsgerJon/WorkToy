"""
KeeFlagsSpace subclasses KeeSpace from the worktoy.keenum package
providing the namespace object required for KeeFlags.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeSpace, Kee
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeDuplicate

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class KeeFlagsSpace(KeeSpace):
  """
  KeeFlagsSpace subclasses KeeSpace from the worktoy.keenum package
  providing the namespace object required for KeeFlags.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __kee_flags__ = None
  __flag_type__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addNum(self, name: str, member: Kee, ) -> Any:
    """
    Returns the KeeFlags instance associated with this space.
    """
    if self.__kee_flags__ is None:
      self.__kee_flags__ = dict()
    member.name = name
    member.index = len(self.__kee_flags__)
    if self.__flag_type__ is None:
      self.__flag_type__ = member.type_
    elif self.__flag_type__ is not member.type_:
      raise TypeException('member', member, self.__flag_type__, )
    if name in self.__kee_flags__:
      raise KeeDuplicate(name, member)
    self.__kee_flags__[name] = member

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    KeeSpace.__init__(self, *args, **kwargs)
    if self.__enumeration_members__ is not None:
      self.__kee_flags__ = {**self.__enumeration_members__, }
      self.__enumeration_members__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def expandNum(self, ) -> Self:
    """Creates a num instance for each combination of flags. """
    if not self.__kee_flags__:
      raise NotImplementedError('No flags')
    N = 2 ** len(self.__kee_flags__)  # Number of combinations
    for i in range(N):
      included = []
      for j, (name, member) in enumerate(self.__kee_flags__.items()):
        if i & (1 << j):
          included.append(member)
      name = '_'.join(sorted([m.name for m in included])) or 'NULL'
      kee = Kee[set](set(included))
      KeeSpace.addNum(self, name, kee)
    return self
