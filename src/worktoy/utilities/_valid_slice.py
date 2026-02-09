"""
ValidSlice is a special un-instantiable class that recognizes only valid
slice objects.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never


class _MetaSlice(type):

  def __instancecheck__(self, instance: Any) -> bool:
    if not isinstance(instance, slice):
      return False
    keys = ('start', 'stop', 'step',)
    for key in keys:
      val = getattr(instance, key)
      if val is None or isinstance(val, int):
        continue
      try:
        #  Check for '__index__' method
        valType = type(val)
        indexFunc = getattr(valType, '__index__', )

        #  Check  for '__index__' being callable
      except (AttributeError, TypeError):
        return False
      else:
        if not callable(indexFunc):
          return False
        continue
    return True

  def __call__(cls, *__, **_) -> Never:
    infoSpec = """%s cannot be instantiated. It is intended only for 
    validating 'slice' objects."""
    info = infoSpec % cls.__name__
    raise TypeError(textFmt(info))

  def __str__(cls, ) -> str:
    infoSpec = """<type '%s' | slice object validator>"""
    info = infoSpec % cls.__name__
    return textFmt(info)

  def __repr__(cls, ) -> str:
    infoSpec = """worktoy.utilities.%s"""
    info = infoSpec % cls.__name__
    return textFmt(info)


class ValidSlice(metaclass=_MetaSlice):
  """
  ValidSlice is a special un-instantiable class that recognizes only valid
  slice objects. Passing keyword arguments to the slice constructor does
  raise:
    'TypeError: slice() takes no keyword arguments'.
  Furthermore, passing no arguments at all likewise raises:
    'slice expected at least 1 argument, got 0'.
  Finally, passing arbitrary positional arguments raises:
    'slice indices must be integers or None or have an __index__ method'
  Or do they? Contrary to every other type and every reasonable expectation
  any *bonus pater familias* might have, slice objects waits until usage
  before raising the above exception. ValidSlice provides a special type,
  that recognizes slice objects as instances of itself, provided they are
  not malformed.

  For example:
  isinstance(slice('imma slice, trust me bro!'), ValidSlice) -> False
  isinstance(slice(0, 10, 'step'), ValidSlice) -> False
  isinstance(slice(1), ValidSlice) -> True
  isinstance(slice(None, None, None), ValidSlice) -> True
  """
  pass
