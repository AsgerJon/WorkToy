"""The EZMeta class provides the metaclass for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy._WORK_IN_PROGRESS.ezdata import EZSpace
from worktoy.meta import BaseMetaclass, Bases


class EZMeta(BaseMetaclass):
  """The EZMeta class provides the metaclass for the EZData class."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> EZSpace:
    return EZSpace(mcls, name, bases, **kwargs)

  def __new__(mcls,
              name: str,
              bases: Bases,
              space: EZSpace,
              **kwargs) -> type:
    newInit = space.ezInitFactory()
    newStr = space.ezStrFactory()
    newEq = space.ezEqFactory()
    EZSpace.__setitem__(space, '__init__', newInit, __trust_me_bro__=True)
    EZSpace.__setitem__(space, '__str__', newStr, __trust_me_bro__=True)
    EZSpace.__setitem__(space, '__repr__', newStr, __trust_me_bro__=True)
    EZSpace.__setitem__(space, '__eq__', newEq, __trust_me_bro__=True)
    return BaseMetaclass.__new__(mcls, name, bases, space, **kwargs)
