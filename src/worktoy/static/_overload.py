"""Function objects decorated with the @overload decorator may have same
name but different signatures. The overload decorator is used to"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.static import TypeSig


def func() -> None: pass


CallMeMaybe = type(func)


def overload(*types, **kwargs) -> CallMeMaybe:
  """Function objects decorated with the @overload decorator may have same
  name but different signatures. The overload decorator is used to
  create a function object that can be called with different argument
  types. """

  typeSig = TypeSig(*types)

  def hereIsMyNumber(callMeMaybe: CallMeMaybe) -> CallMeMaybe:
    """Here is my number"""
    existing = getattr(callMeMaybe, '__type_sigs__', ())
    setattr(callMeMaybe, '__type_sigs__', (*[*existing, typeSig],))
    setattr(callMeMaybe, '__is_overloaded__', True)

    return callMeMaybe

  return hereIsMyNumber
