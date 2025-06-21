"""Function objects decorated with the @overload decorator may have same
name but different signatures. The overload decorator is used to"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import TypeSig

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, TypeAlias, Never


def overload(*types: object, **kwargs: object) -> Callable:
  """Function objects decorated with the @overload decorator may have same
  name but different signatures. The overload decorator is used to
  create a function object that can be called with different argument
  types. """
  if kwargs.get('verbose', False):
    typeNames = ', '.join([type_.__name__ for type_ in types])
    print("""Getting ready to overload: (%s)""" % typeNames)

  typeSig = TypeSig(*types)

  def hereIsMyNumber(callMeMaybe: Callable) -> Callable:
    """Here is my number"""
    if kwargs.get('verbose', False):
      print("""Overloading %s""" % callMeMaybe.__name__)
    existing = getattr(callMeMaybe, '__type_sigs__', ())
    setattr(callMeMaybe, '__type_sigs__', (*[*existing, typeSig],))
    setattr(callMeMaybe, '__is_overloaded__', True)

    return callMeMaybe

  return hereIsMyNumber
