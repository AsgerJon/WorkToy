"""
KeeFlagsSpace is the namespace 'KeeFlagsMeta' uses to build 'KeeFlags'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, cast
from collections.abc import Callable

from ..mcls import BaseSpace
from ..utilities import maybe
from ..waitaminute.keenum import KeeFlagDuplicate, KeeFlagNameError
from ..waitaminute.keenum import KeeCaseException
from . import KeeFlag, KeeFlagsHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Type, TypeAlias

  from . import KeeFlags
  from . import KeeFlagsMeta

  KFMType: TypeAlias = Type[KeeFlagsMeta]
  Bases: TypeAlias = tuple[Type, ...]


class KeeFlagsSpace(BaseSpace):
  """
  A 'KeeFlags' body declares its flags as 'KeeFlag' objects, and the
  class must receive them in declaration order, inherited flags first,
  each name once, upper case and free of the underscore that joins flag
  names into member names, with 'NULL' kept for the member with no flag
  high. The namespace of the body sees each binding and knows the
  bases, so the bookkeeping belongs there.

  Implementation
  --------------

  'KeeFlagsSpace' is a 'BaseSpace' with one hook of its own,
  'KeeFlagsHook', which hands every 'KeeFlag' bound in the body to
  'addKeeFlag'. 'addKeeFlag' refuses an underscore in the name or the
  name 'NULL' with 'KeeFlagNameError', a name that is not upper case
  with 'KeeCaseException' and a repeated or inherited name with
  'KeeFlagDuplicate', and records the flag under its name. The
  constructor records the flags of every base that is a flags class.
  'postCompile' writes the merged flags into the class dictionary as
  '__kee_flags__' and installs 'getKeeFlags', a classmethod that clones
  them onto the class with their bit indices; the root, declared with
  the class keyword '_root', gets neither.

  Attributes
  ----------

  __kee_flags__ : dict or None
    The flags the body declared, by name.

  __base_flags__ : dict or None
    The flags inherited from the bases, by name.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __kee_flags__ = None
  __base_flags__ = None

  #  Space Hooks
  keeFlagsHook = KeeFlagsHook()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getBaseFlags(self, ) -> dict[str, KeeFlag]:
    return maybe(self.__base_flags__, dict())

  def getKeeFlags(self, ) -> dict[str, KeeFlag]:
    """
    The 'getKeeFlags' method returns a new mapping of the inherited flags
    followed by the flags the class body declared, leaving both of those
    mappings as they are.
    """
    out = dict()
    for name, keeFlag in self._getBaseFlags().items():
      out[name] = keeFlag
    for name, keeFlag in maybe(self.__kee_flags__, dict()).items():
      out[name] = keeFlag
    return out

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def addBaseFlag(self, name: str, keeFlag: KeeFlag, **_) -> None:
    """
    The 'addBaseFlag' method records an inherited flag in the base-flags
    dict, so a subclass keeps the flags declared on its parents.
    """
    existing = self._getBaseFlags()
    existing[name] = keeFlag
    self.__base_flags__ = existing

  def addKeeFlag(self, name: str, keeFlag: KeeFlag, **_) -> None:
    """
    The 'addKeeFlag' method records a flag declared in the class body.
    A name containing '_' raises 'KeeFlagNameError', since the name of a
    combined member joins its flag names with '_', and so does the name
    'NULL', which the member with no flag high takes; a name that is not
    upper case raises 'KeeCaseException', as a 'KeeNum' member name does,
    and a name already declared in the body or inherited raises
    'KeeFlagDuplicate'.
    """
    if '_' in name or name == 'NULL':
      raise KeeFlagNameError(self.getClassName(), name)
    if not name.isupper():
      raise KeeCaseException(name)
    baseFlags = self._getBaseFlags()
    keeFlags = maybe(self.__kee_flags__, dict())
    if name in keeFlags:
      raise KeeFlagDuplicate(name, keeFlags[name], keeFlag)
    if name in baseFlags:
      raise KeeFlagDuplicate(name, baseFlags[name], keeFlag)
    #  The bit index is assigned later by 'getKeeFlags', which clones
    #  each flag with a fresh contiguous index in declaration order, so
    #  it is deliberately not set here.
    keeFlag.__member_name__ = name
    keeFlag.__field_name__ = name
    keeFlags[name] = keeFlag
    self.__kee_flags__ = keeFlags

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, mcls: KFMType, name: str, bases: Bases, **kw) -> None:
    """
    The '__init__' method records the flags of every flags class among
    the bases. Only a class built by 'KeeFlagsMeta' has flags; a plain
    mixin with an attribute named 'flags' contributes none.
    """
    BaseSpace.__init__(self, mcls, name, bases, **kw)
    #  Local import: 'KeeFlagsMeta' loads after this file in the package.
    from . import KeeFlagsMeta
    #  The root is marked by the '_root' keyword, never by its name.
    if not kw.get('_root', False):
      for base in bases:
        if not isinstance(base, KeeFlagsMeta):
          continue
        try:
          flags = type.__getattribute__(base, 'flags')
        except AttributeError:
          continue
        else:
          for flag in flags:
            self.addBaseFlag(flag.__member_name__, flag)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getKeeFlagsFactory(cls, ) -> Callable:
    """
    The '_getKeeFlagsFactory' classmethod builds the 'getKeeFlags'
    classmethod installed on each concrete 'KeeFlags' class, which clones
    the declared flags onto that class with fresh per-class indices.
    """

    def func(cls_: Type[KeeFlags]) -> dict[str, KeeFlag]:
      out = dict()
      for i, (name, flag) in enumerate(cls_.__kee_flags__.items()):
        out[name] = flag.clone(cls_, i)
      return out

    setattr(func, '__name__', 'getKeeFlags')
    docSpec = """Getter function for the flags dictionary."""
    setattr(func, '__doc__', docSpec)
    return func

  def postCompile(self, namespace: dict) -> dict:
    """
    The 'postCompile' method finalizes the namespace for a concrete
    'KeeFlags' subclass, recording the collected flags and installing the
    'getKeeFlags' classmethod. The 'KeeFlags' base itself is left
    unchanged.
    """
    namespace = BaseSpace.postCompile(self, namespace)
    if self.getKwargs().get('_root', False):
      return namespace
    namespace['__kee_flags__'] = self.getKeeFlags()
    flagsFactory = cast(Callable, self._getKeeFlagsFactory())
    namespace['getKeeFlags'] = classmethod(flagsFactory)
    return namespace
