"""Shared helpers used by the per-class factory tests."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZSlot
from worktoy.ezdata import (
  makeAsDict,
  makeAsTuple,
  makeDelAttr,
  makeDelItem,
  makeEq,
  makeGetItem,
  makeHash,
  makeInit,
  makeIter,
  makeLen,
  makeOrderingOp,
  makeRepr,
  makeSetAttr,
  makeSetItem,
  makeStr,
)

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, List


def slot(name: str, fieldType: type, default: Any) -> EZSlot:
  """Construct an ``EZSlot`` with the given name, type, and default."""
  s = EZSlot(name)
  object.__setattr__(s, '__type_value__', fieldType)
  object.__setattr__(s, '__default_value__', default)
  object.__setattr__(s, '__owner_name__', 'TestOwner')
  return s


def build(fields: List[EZSlot], frozen: bool = False,
          ordered: bool = False
          ) -> type:
  """Construct an ad-hoc class wired up with the auto-generated dunders.

  The ``__slots__`` machinery is set up to match the field list so
  the generated ``object.__setattr__`` calls land in real slots.
  """
  slotNames = tuple(f.name for f in fields)
  if frozen:
    slotNames = slotNames + ('__ez_initialized__',)
  attrs = {
    '__slots__'  : slotNames,
    '__init__'   : makeInit(fields, frozen),
    '__eq__'     : makeEq(fields),
    '__hash__'   : makeHash(fields, frozen),
    '__repr__'   : makeRepr(fields),
    '__str__'    : makeStr(fields),
    '__iter__'   : makeIter(fields),
    '__len__'    : makeLen(fields),
    '__getitem__': makeGetItem(fields),
    '__setitem__': makeSetItem(fields),
    '__delitem__': makeDelItem(),
    '__setattr__': makeSetAttr(fields, frozen),
    '__delattr__': makeDelAttr(),
    '__lt__'     : makeOrderingOp(fields, '<', ordered),
    '__le__'     : makeOrderingOp(fields, '<=', ordered),
    '__gt__'     : makeOrderingOp(fields, '>', ordered),
    '__ge__'     : makeOrderingOp(fields, '>=', ordered),
    'asTuple'    : makeAsTuple(fields),
    'asDict'     : makeAsDict(fields)
  }
  return type('Synthetic', (), attrs)
