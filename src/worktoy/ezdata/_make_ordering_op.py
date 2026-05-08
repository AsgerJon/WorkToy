"""``makeOrderingOp`` returns a single ordering operator
(``<`` / ``<=`` / ``>`` / ``>=``) parameterized by ``ordered``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..waitaminute.ez import UnorderedEZException
from ._ez_slot import EZSlot

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, List


def makeOrderingOp(
    fields: List[EZSlot], operator: str, ordered: bool,
) -> Callable:
  """Build a single ordering operator.

  ``operator`` is one of ``'<'``, ``'<='``, ``'>'``, ``'>='``.
  When ``ordered`` is false, the generated method always raises
  ``UnorderedEZException`` (regardless of the other operand's
  type). When ``ordered`` is true, comparisons against
  non-matching types also raise ``UnorderedEZException``;
  comparisons between same-type instances iterate the fields and
  return the first inequality, or a strict-vs-equal sentinel if
  all fields tie.
  """
  fieldNames = tuple(f.name for f in fields)
  ascending = operator in ('<', '<=')
  strict = operator in ('<', '>')
  opName = {'<': 'lt', '<=': 'le', '>': 'gt', '>=': 'ge'}[operator]

  def _op(self, other: Any) -> Any:
    if not ordered:
      raise UnorderedEZException(type(self).__name__)
    if type(self) is not type(other):
      raise UnorderedEZException(type(self).__name__)
    for name in fieldNames:
      a, b = getattr(self, name), getattr(other, name)
      if a == b:
        continue
      if ascending:
        return a < b
      return a > b
    return not strict

  _op.__name__ = '__%s__' % opName
  return _op
