"""
'fields' returns the tuple of 'EZField' descriptors declared on an
'EZData' class, mirroring 'dataclasses.fields' for callers who
prefer a module-level free function over the metaclass property
'cls.fields'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from . import EZMeta

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def fields(obj: Any) -> tuple:
  """
  Returns the tuple of 'EZField' descriptors declared on an
  'EZData' class, in declaration order. Accepts either the
  class itself or an instance of it. Raises 'TypeError' when
  passed anything else.

  Parameters
  ----------
  obj : Any
    An 'EZData' subclass or an instance of one.

  Returns
  -------
  tuple[EZField, ...]
    The fields declared on the class, in declaration order.

  Raises
  ------
  TypeError
    If 'obj' is neither an 'EZData' class nor an instance of one.
  """
  cls = obj if isinstance(obj, type) else type(obj)
  if not isinstance(cls, EZMeta):
    infoSpec = """'fields()' expects an 'EZData' class or instance,
    but received '%s' of type '%s'."""
    info = infoSpec % (obj, type(obj).__name__)
    raise TypeError(textFmt(info))
  return cls.fields
