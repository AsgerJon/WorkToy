"""
Arrangement is a single permutation of a ground tuple of items.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

from .. import QuickDesc, textFmt

T = TypeVar('T')
ItemTypeT = TypeVar('ItemTypeT')

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Any, Iterator, Optional

  Values: TypeAlias = tuple[Any, ...]
  MaybeValues: TypeAlias = Optional[Values]
  Indices: TypeAlias = tuple[int, ...]
  MaybeIndices: TypeAlias = Optional[Indices]
  Items: TypeAlias = tuple[T, ...]
  MaybeItems: TypeAlias = Optional[Items[T]]


class Arrangement(Generic[ItemTypeT]):
  """A single permutation of a ground tuple of items.

  Holds two index recipes that are inverses of each other as
  permutations of 'range(len(items))':

  - 'forward[k]' is the position in 'items' that contributes slot
    'k' of the arranged values. Satisfies
    'self.values[k] is self.items[self.forward[k]]'.
  - 'inverse[k]' is the slot in the arranged values where
    'items[k]' has been placed. Satisfies
    'self.values[self.inverse[k]] is self.items[k]'.

  These are not interchangeable. Prefer 'applyTo' and
  'restoreFrom' over reaching for the recipes directly; the method
  names commit to the call direction and rule out the bug class
  where 'forward' is used where 'inverse' is needed (or vice
  versa), which fails silently on every involution and only
  surfaces on 3-cycles and longer.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __ground_items__: MaybeItems[ItemTypeT] = None
  __forward_indices__: MaybeIndices = None
  __inverse_indices__: MaybeIndices = None
  __current_order__: MaybeItems[ItemTypeT] = None

  #  Public Variables
  items: QuickDesc[tuple[ItemTypeT, ...]] = QuickDesc('__ground_items__')
  forward: QuickDesc[tuple[int, ...]] = QuickDesc('__forward_indices__')
  inverse: QuickDesc[tuple[int, ...]] = QuickDesc('__inverse_indices__')
  values: QuickDesc[tuple[ItemTypeT, ...]] = QuickDesc('__current_order__')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, items: Items, forward: Indices) -> None:
    if len(forward) != len(items):
      infoSpec = """'forward' recipe of length '%d' does not match 
      'items' tuple of length '%d'"""
      info = infoSpec % (len(forward), len(items))
      raise ValueError(textFmt(info))
    self.__ground_items__ = items
    self.__forward_indices__ = forward
    self.__current_order__ = (*(items[i] for i in forward),)
    inverse = [0] * len(forward)
    for slot, origin in enumerate(forward):
      inverse[origin] = slot
    self.__inverse_indices__ = (*inverse,)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __len__(self) -> int:
    return len(self.items)

  def __iter__(self) -> Iterator[Any]:
    yield from self.values

  def __eq__(self, other: Any) -> bool:
    if isinstance(other, Arrangement):
      return self.values == other.values
    if isinstance(other, tuple):
      return self.values == other
    return NotImplemented

  def __hash__(self) -> int:
    return hash(self.values)

  def __str__(self) -> str:
    infoSpec = '<%s: %s>'
    clsName = type(self).__name__
    orderStr = ', '.join(str(value) for value in self.values)
    return infoSpec % (clsName, orderStr)

  def __repr__(self) -> str:
    infoSpec = '%s(%s, %s)'
    clsName = type(self).__name__
    itemsStr = ', '.join(str(item) for item in self.items)
    forwardStr = ', '.join(str(index) for index in self.forward)
    return infoSpec % (clsName, itemsStr, forwardStr)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def applyTo(self, *values: Any) -> Values:
    """Permute 'values' into this arrangement's order.

    Given a parallel tuple supplied in the same order as
    'self.items', return the corresponding tuple in the same order
    as 'self.values'. Inverse of 'restoreFrom'.

    Parameters
    ----------
    *values : Any
        One value per ground item, supplied in 'self.items' order.

    Returns
    -------
    tuple
        The values reordered to match 'self.values'.

    Raises
    ------
    ValueError
        If 'len(values)' does not match the length of the
        arrangement.
    """
    if len(values) != len(self):
      infoSpec = """'applyTo' received '%d' values but arrangement has
      length '%d'"""
      info = infoSpec % (len(values), len(self))
      raise ValueError(textFmt(info))
    return (*(values[i] for i in self.forward),)

  def restoreFrom(self, *values: Any) -> Values:
    """Permute 'values' back to canonical order.

    Given a parallel tuple supplied in the same order as
    'self.values', return the corresponding tuple in the same
    order as 'self.items'. Inverse of 'applyTo'.

    Parameters
    ----------
    *values : Any
        One value per arranged slot, in 'self.values' order.

    Returns
    -------
    tuple
        The values reordered to match 'self.items'.

    Raises
    ------
    ValueError
        If 'len(values)' does not match the length of the
        arrangement.
    """
    if len(values) != len(self):
      infoSpec = """'restoreFrom' received '%d' values but arrangement
      has length '%d'"""
      info = infoSpec % (len(values), len(self))
      raise ValueError(textFmt(info))
    return (*(values[i] for i in self.inverse),)
