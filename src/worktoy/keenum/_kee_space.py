"""
KeeSpace is the namespace 'KeeMeta' uses to build 'KeeNum' classes.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls import BaseSpace
from ..waitaminute.keenum import KeeDuplicate, KeeTypeException
from ..waitaminute.keenum import KeeNameConflict
from . import KeeSpaceHook, Kee

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Dict, TypeAlias

  Members: TypeAlias = Dict[str, Kee]
  Bases: TypeAlias = tuple[type, ...]


class KeeSpace(BaseSpace):
  """
  A 'KeeNum' body declares its members as 'Kee' objects, one per name,
  and the class must receive them as members in the order declared,
  inherited members first, every name once, every value of one type,
  and never as plain attributes the members would then replace. The
  namespace of the body is where that bookkeeping belongs, since it
  sees each binding as it is made and knows the bases before the body
  runs.

  Implementation
  --------------

  'KeeSpace' is a 'BaseSpace' with one hook of its own, 'KeeSpaceHook',
  which hands every 'Kee' bound in the body to 'addNum'. 'addNum'
  refuses a repeated name with 'KeeDuplicate', a 'Kee' already named
  otherwise with 'KeeNameConflict', a name that is not upper case
  through the 'Kee' setter, and a value type other than the first
  member's through 'typeGuard', then records the member. The
  constructor registers a clone of every member of each base that is an
  enumeration, so the names and the value type are inherited before the
  body runs. 'postCompile' writes the pinned value type into the class
  dictionary as '__member_type__'; 'KeeMeta' reads the members off the
  namespace as the class is created.

  Attributes
  ----------

  __enumeration_members__ : dict
    The 'Kee' of each member by name, inherited clones first.

  __member_type__ : type or None
    The value type pinned by the first member, or 'None' before any.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  keeSpaceHook = KeeSpaceHook()

  #  Private Variables
  __enumeration_members__ = None
  __member_type__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addNum(self, name: str, member: Kee) -> None:
    """
    The 'addNum' method registers one 'Kee' member under 'name', raising
    'KeeDuplicate' on a repeated name and 'KeeNameConflict' if the member
    already carries a different name. It runs the member through
    'typeGuard' before storing it; the index is assigned as the class is
    created, by 'KeeMeta._createMembers', once the 'Kee' is placed.
    """
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
    member = self.typeGuard(member)
    self.__enumeration_members__[name] = member

  def hasNum(self, name: str) -> bool:
    """
    The 'hasNum' method reports whether a member, declared in this body
    or inherited, is registered under 'name'.
    """
    return True if name in self.__enumeration_members__ else False

  def typeGuard(self, member: Kee) -> Kee:
    """
    The 'typeGuard' method pins the enumeration to the value type of its
    first member and rejects any later member of a different type with
    'KeeTypeException'.
    """
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
    for base in bases:
      try:
        space = type.__getattribute__(base, '__namespace__')
      except AttributeError:
        #  This branch is reached by the following:
        #  - The base was built by no worktoy metaclass, as a plain mixin
        continue
      if not isinstance(space, KeeSpace):
        #  This branch is reached by the following:
        #  - The base is a worktoy class that is no enumeration, as a
        #    'BaseObject' mixin
        continue
      self.__member_type__ = space.__member_type__
      for key, val in space.__enumeration_members__.items():
        if key in self.__enumeration_members__:
          oldMember = self.__enumeration_members__[key]
          raise KeeDuplicate(key, oldMember, val)
        #  The inherited member is registered as a clone, so the base's
        #  'Kee', placed on the base, is never handed to this body: the
        #  class takes the base's member object itself as it is created,
        #  and the clone serves the name checks alone.
        self.addNum(key, val.clone())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def postCompile(self, namespace: dict) -> dict:
    namespace = BaseSpace.postCompile(self, namespace)
    namespace['__member_type__'] = self.__member_type__
    return namespace
