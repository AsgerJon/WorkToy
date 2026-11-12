"""
The 'fields' function returns the 'EZField' of each attribute declared on
an 'EZData' class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..utilities import textFmt
from ..waitaminute import WorkToyException
from . import EZMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


def fields(obj: Any) -> tuple:
  """
  Code handed a dataclass, or an instance of one, must be able to ask for
  its fields in declaration order without knowing the metaclass, as
  'dataclasses.fields' is asked.

  Implementation
  --------------

  The class of an instance is taken, and the 'fields' of a class built by
  'EZMeta' are returned. Anything else is refused, the message showing
  the object by its 'repr', cut as every message of the library cuts a
  value.

  Parameters
  ----------

  obj : Any
    An 'EZData' subclass or an instance of one.

  Returns
  -------

  tuple[EZField, ...]
    The fields of the class, own and inherited, in declaration order.

  Raises
  ------

  TypeError
    'obj' is neither an 'EZData' class nor an instance of one.
  """
  cls = obj if isinstance(obj, type) else type(obj)
  if not isinstance(cls, EZMeta):
    infoSpec = """'fields()' expects an 'EZData' class or instance,
    but received: %s of type '%s'."""
    shown = WorkToyException._reprOf(obj)
    info = infoSpec % (shown, type(obj).__name__)
    raise TypeError(textFmt(info))
  return cls.fields
