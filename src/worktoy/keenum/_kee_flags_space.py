"""
KeeFlagsSpace is the namespace 'KeeFlagsMeta' uses to build 'KeeFlags'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..mcls import BaseSpace
from ..waitaminute.keenum import KeeFlagDuplicate, KeeFlagNameError
from ..waitaminute.keenum import KeeCaseException
from . import KeeFlag, KeeFlagsHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Type, TypeAlias, Union

  from . import Kee, KeeFlags, KeeFlagsMeta

  KFMType: TypeAlias = Type[KeeFlagsMeta]
  Bases: TypeAlias = tuple[Type, ...]
  Declaration: TypeAlias = Union[Kee, KeeFlag]


class KeeFlagsSpace(BaseSpace):
  """
  A 'KeeFlags' body declares its flags with 'Kee', or with the
  deprecated 'KeeFlag', and the class must receive the flags of its
  bases first, in the order of the bases, then those of the body in the
  order declared, each name once, upper case and free of the underscore
  that joins flag names into member names, with 'NULL' kept for the
  member with no flag high. The namespace of the body sees each binding
  and knows the bases, so the bookkeeping belongs there.

  Implementation
  --------------

  'KeeFlagsSpace' is a 'BaseSpace' with one hook of its own,
  'KeeFlagsHook', which hands every declaration bound in the body to
  'addKeeFlag'. 'addKeeFlag' refuses an underscore in the name or the
  name 'NULL' with 'KeeFlagNameError', a name that is not upper case
  with 'KeeCaseException', and a name declared twice or declared over an
  inherited flag with 'KeeFlagDuplicate', then names the declaration and
  records it. The constructor records the flags of every base that is a
  flags class through 'addBaseFlag', which keeps a flag reached through
  two bases once and refuses two different flags of one name with
  'KeeFlagDuplicate'. The root, declared with the class keyword '_root',
  records no base flags. 'KeeFlagsMeta' reads both records as the class
  is created.

  Attributes
  ----------

  __declared_flags__ : dict or None
    The declarations of the body, by name.

  __base_flags__ : dict or None
    The flags of the bases, the flag members themselves, by name.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __declared_flags__ = None
  __base_flags__ = None

  #  Space Hooks
  keeFlagsHook = KeeFlagsHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def getBaseFlags(self, ) -> dict[str, KeeFlags]:
    """
    The 'getBaseFlags' method gives a new mapping of the flags of the
    bases, the flag members themselves, by name, in the order of the
    bases.
    """
    if self.__base_flags__ is None:
      return dict()
    return {**self.__base_flags__, }

  def getDeclaredFlags(self, ) -> dict[str, Declaration]:
    """
    The 'getDeclaredFlags' method gives a new mapping of the declarations
    of the body by name, in the order declared.
    """
    if self.__declared_flags__ is None:
      return dict()
    return {**self.__declared_flags__, }

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addBaseFlag(self, flag: KeeFlags) -> None:
    """
    The 'addBaseFlag' method records a flag of a base. The flag under its
    name already is the same flag, reached through another base, unless
    it is another object, which is refused with 'KeeFlagDuplicate'.
    """
    existing = self.getBaseFlags()
    if flag.name in existing:
      if existing[flag.name] is flag:
        #  This branch is reached by the following:
        #  - A diamond: two bases hold the flag of a common ancestor
        return
      raise KeeFlagDuplicate(flag.name, existing[flag.name], flag)
    existing[flag.name] = flag
    self.__base_flags__ = existing

  def addKeeFlag(self, name: str, declaration: Declaration) -> None:
    """
    The 'addKeeFlag' method records a flag declared in the class body.
    A name containing '_' raises 'KeeFlagNameError', since the name of a
    combined member joins its flag names with '_', and so does the name
    'NULL', which the member with no flag high takes; a name that is not
    upper case raises 'KeeCaseException', as a 'KeeNum' member name
    does, and a name declared already in the body or inherited raises
    'KeeFlagDuplicate'. The declaration then receives the name.
    """
    if '_' in name or name == 'NULL':
      raise KeeFlagNameError(self.getClassName(), name)
    if not name.isupper():
      raise KeeCaseException(name)
    declared = self.getDeclaredFlags()
    if name in declared:
      raise KeeFlagDuplicate(name, declared[name], declaration)
    inherited = self.getBaseFlags()
    if name in inherited:
      raise KeeFlagDuplicate(name, inherited[name], declaration)
    if isinstance(declaration, KeeFlag):
      declaration.__member_name__ = name
      declaration.__field_name__ = name
    else:
      declaration.name = name
    declared[name] = declaration
    self.__declared_flags__ = declared

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: KFMType, name: str, bases: Bases, **kw) -> None:
    """
    The '__init__' method records the flags of every flags class among
    the bases, in their order. Only a class built by 'KeeFlagsMeta' has
    flags; a plain mixin with an attribute named 'flags' contributes
    none.
    """
    BaseSpace.__init__(self, mcls, name, bases, **kw)
    #  Local import: 'KeeFlagsMeta' loads after this file in the package.
    from . import KeeFlagsMeta
    #  The root is marked by the '_root' keyword, never by its name.
    if kw.get('_root', False):
      return
    for base in bases:
      if isinstance(base, KeeFlagsMeta):
        for flag in base.flags:
          self.addBaseFlag(flag)
