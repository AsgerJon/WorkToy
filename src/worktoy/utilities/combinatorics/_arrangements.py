"""All unique arrangements of a ground tuple of items.

``Arrangements`` enumerates the distinct permutations of the
supplied items. Repeated items collapse: ``Arrangements('A', 'A',
'B')`` yields three arrangements, not six."""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

from . import Arrangement, indexPermutations
from .. import QuickDesc

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
  MaybeBool: TypeAlias = Optional[bool]


class Arrangements(Generic[ItemTypeT]):
  """All unique arrangements of a ground tuple of items.

  Iterating yields ``Arrangement`` instances. The set is
  deduplicated by arranged-value equality, so repeated items in the
  ground tuple collapse: ``Arrangements('A', 'A', 'B')`` yields
  three arrangements, not six.

  Examples
  --------
  >>> list(a.values for a in Arrangements('A', 'A', 'B'))
  [('A', 'A', 'B'), ('A', 'B', 'A'), ('B', 'A', 'A')]
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __ground_items__: MaybeItems[ItemTypeT] = None
  __cached__: tuple[Arrangement, ...] = None
  __is_hashable__: MaybeBool = None

  #  Public Variables
  items: QuickDesc[tuple[ItemTypeT, ...]] = QuickDesc('__ground_items__')
  permutations: QuickDesc[tuple[Arrangement, ...]] = QuickDesc('__cached__')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *items: Any) -> None:
    self.__ground_items__ = items
    self._buildCache()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createIsHashable(self, ) -> None:
    for item in self.items:
      try:
        _ = hash(item)
      except TypeError:
        break
      else:
        continue
    else:
      self.__is_hashable__ = True
      return
    self.__is_hashable__ = False

  def isHashable(self, **kwargs) -> bool:
    if self.__is_hashable__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createIsHashable()
      return self.isHashable(_recursion=True)
    return self.__is_hashable__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _buildCacheHashed(self, ) -> None:
    out: list[Arrangement] = []
    seen: set[Values] = set()
    for forward in indexPermutations(len(self.items)):
      arrangement = Arrangement(self.items, forward)
      values = arrangement.values
      if values in seen:
        continue
      seen.add(values)
      out.append(arrangement)
    self.__cached__ = (*out,)

  def _buildCacheNoHash(self) -> None:
    out: list[Arrangement] = []
    seen: list[Values] = []
    for forward in indexPermutations(len(self.items)):
      arrangement = Arrangement(self.items, forward)
      values = arrangement.values
      if values in seen:
        continue
      seen.append(values)
      out.append(arrangement)
    self.__cached__ = (*out,)

  def _buildCache(self, ) -> None:
    if self.isHashable():
      self._buildCacheHashed()
    else:
      self._buildCacheNoHash()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self) -> Iterator[Arrangement]:
    yield from self.permutations

  def __len__(self) -> int:
    return len(self.permutations)

  def __getitem__(self, index: int) -> Arrangement:
    return self.permutations[index]

  def __contains__(self, item: Any) -> bool:
    if isinstance(item, Arrangement):
      return item in self.permutations
    if isinstance(item, tuple):
      return item in (a.values for a in self.permutations)
    return False
