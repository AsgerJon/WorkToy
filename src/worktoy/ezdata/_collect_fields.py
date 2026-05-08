"""``collectFields`` is the EZData field-collection routine."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._ez_slot import EZSlot
from ._is_field_candidate import isFieldCandidate
from ._resolve_annotation import resolveAnnotation

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Dict, List


def collectFields(
    compiled: dict, bases: tuple, annotations: dict, ownerName: str,
) -> List[EZSlot]:
  """Gather inherited and class-body fields in declaration order.

  Three passes:

  1. Inherited slots from ``base.__slot_objects__`` for each base.
  2. Class-body annotated names: each entry in ``annotations`` is
     a field. Default comes from ``compiled[name]`` if present,
     otherwise ``None``. The compiled entry is removed.
  3. Class-body defaulted-without-annotation names: any remaining
     entry in ``compiled`` for which ``isFieldCandidate(name,
     value)`` is true. The compiled entry is removed.

  Later declarations override an inherited slot's type and default
  but keep the inherited position.
  """
  out: List[EZSlot] = []
  byName: Dict[str, int] = {}
  for base in bases:
    for slot in getattr(base, '__slot_objects__', ()):
      if slot.name not in byName:
        copy = EZSlot(slot.name)
        object.__setattr__(copy, '__type_value__', slot.typeValue)
        object.__setattr__(copy, '__default_value__', slot.defaultValue)
        object.__setattr__(copy, '__owner_name__', slot.ownerName)
        byName[slot.name] = len(out)
        out.append(copy)
  for name, annotation in annotations.items():
    if name.startswith('__') and name.endswith('__'):
      continue
    default = compiled.pop(name, None)
    fieldType = resolveAnnotation(annotation)
    if fieldType is None:
      fieldType = type(default) if default is not None else object
    if name in byName:
      slot = out[byName[name]]
    else:
      slot = EZSlot(name)
      byName[name] = len(out)
      out.append(slot)
    object.__setattr__(slot, '__type_value__', fieldType)
    object.__setattr__(slot, '__default_value__', default)
    object.__setattr__(slot, '__owner_name__', ownerName)
  for name in list(compiled.keys()):
    value = compiled[name]
    if not isFieldCandidate(name, value):
      continue
    del compiled[name]
    if name in byName:
      slot = out[byName[name]]
    else:
      slot = EZSlot(name)
      byName[name] = len(out)
      out.append(slot)
    object.__setattr__(slot, '__type_value__', type(value))
    object.__setattr__(slot, '__default_value__', value)
    object.__setattr__(slot, '__owner_name__', ownerName)
  return out
