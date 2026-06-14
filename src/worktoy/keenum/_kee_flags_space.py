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
from ..waitaminute.keenum import KeeFlagDuplicate
from . import KeeFlag, KeeFlagsHook

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type, TypeAlias

  from . import KeeFlags
  from . import KeeFlagsMeta

  KFMType: TypeAlias = Type[KeeFlagsMeta]
  Bases: TypeAlias = tuple[Type, ...]


class KeeFlagsSpace(BaseSpace):
  """
  KeeFlagsSpace subclasses KeeSpace from the worktoy.keenum package
  providing the namespace object required for KeeFlags.
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
    baseFlags = self._getBaseFlags()
    keeFlags = maybe(self.__kee_flags__, dict())
    for name, keeFlag in keeFlags.items():
      baseFlags[name] = keeFlag
    return baseFlags

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
    baseFlags = self._getBaseFlags()
    keeFlags = self.getKeeFlags()
    if name in maybe(self.__kee_flags__, dict()):
      oldFlag = self.__kee_flags__[name]
      raise KeeFlagDuplicate(name, oldFlag, keeFlag)
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
    BaseSpace.__init__(self, mcls, name, bases, **kw)
    if name != 'KeeFlags':
      for base in bases:
        try:
          flags = getattr(base, 'flags')
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
    if self.getClassName() == 'KeeFlags':
      return namespace
    namespace['__kee_flags__'] = self.getKeeFlags()
    flagsFactory = cast(Callable, self._getKeeFlagsFactory())
    namespace['getKeeFlags'] = classmethod(flagsFactory)
    return namespace
