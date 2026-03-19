"""
BaseSample provides the base class for sample classes in the
'worktoy.work_test.samples' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...utilities import maybe
from ...desc import Field, Alias
from ...mcls import BaseObject
from ...waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union, Iterator

  MaybeInt: TypeAlias = Optional[int]
  IntField: TypeAlias = Union[int, Field]

  TypeField: TypeAlias = Union[type, Field]
  ValueTuple: TypeAlias = tuple[Any, ...]
  ValueTuples: TypeAlias = tuple[ValueTuple, ...]

  Item: TypeAlias = Any
  Row: TypeAlias = tuple[Item, ...]
  Table: TypeAlias = tuple[Row, ...]

  ItemField: TypeAlias = Union[Item, Field]
  RowField: TypeAlias = Union[Row, Field]
  TableField: TypeAlias = Union[Table, Field]

  from abc import ABC, abstractmethod
else:
  ABC, abstractmethod = object, lambda x: x


class BaseSample(BaseObject, ABC):
  """
  BaseSample provides the base class for sample classes in the
  'worktoy.work_test.samples' module.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Fallback Variables
  __fallback_col_count__: int = 1
  __fallback_row_count__: int = 1

  #  Private Variables
  __col_count__: MaybeInt = None
  __row_count__: MaybeInt = None

  #  Public Variables
  valueType: TypeField = Field()
  # --#  Settings
  colCount: IntField = Field()
  rowCount: IntField = Field()

  #  Virtual Variables
  # --#  Samples
  item: ItemField = Field()
  row: RowField = Field()
  table: TableField = Field()

  #  Aliases
  width = Alias('colCount')
  height = Alias('rowCount')
  size = Alias('colCount')
  count = Alias('rowCount')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @colCount.GET
  def _getCount(self) -> int:
    return maybe(self.__col_count__, self.__fallback_col_count__)

  @rowCount.GET
  def _getTupleCount(self) -> int:
    return maybe(self.__row_count__, self.__fallback_row_count__)

  @item.GET
  def _getItem(self, ) -> Any:  # Should return value type.
    return self.gen()

  @row.GET
  def _getRow(self, ) -> Row:
    return self.genTuple()

  @table.GET
  def _getTable(self, ) -> Table:
    return self.genTuples()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @colCount.SET
  def _setColCount(self, colCount: int) -> None:
    if colCount < 1:
      raise ValueError("""Column count must be a positive integer.""")
    self.__col_count__ = colCount

  @rowCount.SET
  def _setRowCount(self, rowCount: int) -> None:
    if rowCount < 1:
      raise ValueError("""Row count must be a positive integer.""")
    self.__row_count__ = rowCount

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  REQUIRED METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @abstractmethod
  @valueType.GET
  def _getValueType(self, **kwargs) -> type:
    """
    Subclasses must implement this method to return the type of the sample
    values.
    """

  @abstractmethod
  @item.GET
  def _getItem(self, ) -> Any:
    """
    Subclasses must implement this method to specify how it generates a
    single sample value. Please note that the method cannot accept any
    arguments other than the bound instance.

    Returns
    -------
    Any
      A single sample value of the type specified by the '_getValueType'
      method.
    """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  OPTIONAL METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @row.GET
  def _getRow(self, ) -> Row:
    """
    This method generates a tuple of 'n' sample values with 'n' specified
    by the 'self.count' variable. Subclasses reimplementing this method
    are responsible for ensuring that the correct number of sample values
    are included in the generated tuple.

    Returns
    -------
    Row
      A tuple of sample values of the type specified by the '_getValueType'
      method.
    """
    out = []
    for _ in range(self.colCount):
      value = self._getItem()
      if not isinstance(value, self.valueType):
        raise TypeException('value', value, self.valueType)
      out.append(value)
    return (*out,)

  @table.GET
  def _getTable(self, *args, **kwargs) -> ValueTuples:
    """
    This method generates 'N' tuples each with 'n' sample values where 'N'
    and 'n' are specified by the 'self.count' and 'self.tupleCount'
    variables, respectively. Subclasses reimplementing this method are
    responsible for ensuring that the correct number of tuples and sample
    values are included in the generated tuples.

    Returns
    -------
    ValueTuples
      A tuple of tuples of sample values of the type specified by the
      '_getValueType' method.
    """
    out = []
    while len(out) < self.rowCount:
      out.append(self._getRow(*args, **kwargs))
    return (*out,)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, ) -> Any:
    """
    This method generates a single sample value by calling the 'gen' method.
    """
    return self._getItem()

  def __iter__(self) -> Iterator[Any]:
    """
    This method generates an infinite stream of sample values by repeatedly
    calling the 'gen' method.
    """
    _c = int(self.rowCount)
    while _c:
      _c -= 1
      yield self._getRow()

  def __str__(self, ) -> str:
    infoSpec = """<%s: '%s' (%d, %d)>"""
    clsName = type(self).__name__
    typeName = self.valueType.__name__
    count, tupleCount = self.colCount, self.rowCount
    return infoSpec % (clsName, typeName, count, tupleCount)

  def __repr__(self, ) -> str:
    infoSpec = """%s(count=%d, tupleCount=%d)"""
    clsName = type(self).__name__
    count, tupleCount = self.colCount, self.rowCount
    return infoSpec % (clsName, count, tupleCount)
