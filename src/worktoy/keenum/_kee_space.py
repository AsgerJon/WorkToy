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
  from typing import Any, TypeAlias

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
  which holds the name of every 'Kee' bound in the body to upper case,
  unless 'strictCase=False' holds for the class, refuses a name that
  'getNumsIgnoringCase' finds on record in any case, refuses a name a
  base or the metaclass holds where the upper-case rule does not hold,
  and hands the 'Kee' to 'addNum'. 'addNum' refuses a repeated name with
  'KeeDuplicate', a 'Kee' already named otherwise with
  'KeeNameConflict', and a value type other than the first member's
  through 'typeGuard', then records the member. The
  constructor registers a clone of every member of every base that is
  an enumeration, the bases in order, so the names and the value type
  are inherited before the body runs. A member reached through two
  bases, as in a diamond, is one member; two different members under
  one name, or under names that differ only by case, raise
  'KeeDuplicate', and bases of different value types
  'KeeTypeException'. 'postCompile' writes the pinned value type into
  the class dictionary as '__member_type__'; 'KeeMeta' reads the
  members off the namespace as the class is created.

  Attributes
  ----------

  __enumeration_members__ : dict
    The 'Kee' of each member by name, inherited clones first.

  __inherited_members__ : dict
    The member objects of the bases by name, in the order of the bases.

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
  __inherited_members__ = None
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
      raise KeeDuplicate(self.getClassName(), name, oldMember, member)
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

  def getNumsIgnoringCase(self, name: str) -> tuple[Kee, ...]:
    """
    A lookup by name ignores case, so two members whose names differ by
    case alone could not be told apart. Before a member is recorded, it
    must therefore be known whether another one has its name already, in
    any case.

    Implementation
    --------------

    The names on record are compared lower-cased, as the table of names
    of the finished class is keyed.

    Parameters
    ----------

    name : str
      The name asked about.

    Returns
    -------

    tuple[Kee, ...]
      The 'Kee' objects on record, declared in this body or inherited,
      under a name equal to 'name' when case is ignored; empty when there
      is none.
    """
    lowered = name.lower()
    out = []
    for held, member in self.__enumeration_members__.items():
      if held.lower() == lowered:
        out.append(member)
    return (*out,)

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
    self.__inherited_members__ = dict()
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
      for member in type.__getattribute__(base, '__registered_members__'):
        self._inheritMember(member)

  def _inheritMember(self, member: Any) -> None:
    """
    The '_inheritMember' method records one member of a base. A member
    the namespace holds already under its name is the same member,
    reached through another base, unless it is another object, which is
    refused with 'KeeDuplicate'. So is a member whose name differs by
    case alone from that of a member another base gave, since a lookup
    by name could not tell the two apart. The member's 'Kee' is
    registered as a clone, so the base's 'Kee', placed on the base, is
    never handed to this body: the class takes the member object itself
    as it is created, and the clone serves the name and type checks
    alone.
    """
    name = member.name
    clsName = self.getClassName()
    inherited = self.__inherited_members__
    if name in inherited:
      if inherited[name] is member:
        #  This branch is reached by the following:
        #  - A diamond: two bases hold the member of a common ancestor
        return
      raise KeeDuplicate(clsName, name, inherited[name].kee, member.kee)
    for held in self.getNumsIgnoringCase(name):
      #  This loop is entered by the following:
      #  - Another base gave a member whose name differs by case alone
      oldKee = inherited[held.name].kee
      raise KeeDuplicate(clsName, name, oldKee, member.kee)
    inherited[name] = member
    self.addNum(name, member.kee.clone())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def postCompile(self, namespace: dict) -> dict:
    namespace = BaseSpace.postCompile(self, namespace)
    namespace['__member_type__'] = self.__member_type__
    return namespace
