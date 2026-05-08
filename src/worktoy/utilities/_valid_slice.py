"""Validator type for well-formed ``slice`` objects.

``ValidSlice`` is an un-instantiable class whose ``isinstance``
check returns ``True`` only for ``slice`` objects whose ``start``,
``stop``, and ``step`` are ``None``, ``int``, or values supporting
``__index__``."""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import textFmt

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never


class _MetaSlice(type):
  """Metaclass implementing ``ValidSlice``'s isinstance hook."""

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
  """Un-instantiable validator for ``slice`` objects.

  The built-in ``slice`` constructor accepts arbitrary positional
  arguments and only complains at usage time, when CPython tries to
  call ``__index__`` on each component. ``ValidSlice`` short-circuits
  that lazy check: ``isinstance(s, ValidSlice)`` is ``True`` iff
  every component of ``s`` is ``None``, an ``int``, or an object
  whose type defines ``__index__``.

  Instantiating ``ValidSlice`` raises ``TypeError``; the class is a
  pure type-level predicate.

  Examples
  --------
  >>> isinstance(slice('not a slice'), ValidSlice)
  False
  >>> isinstance(slice(0, 10, 'step'), ValidSlice)
  False
  >>> isinstance(slice(1), ValidSlice)
  True
  >>> isinstance(slice(None, None, None), ValidSlice)
  True
  """
  pass
