"""
BaseSampler is the base class for the sample-data generators.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ...dispatch import overload
from ...utilities import maybe
from ...desc import Field, Alias
from ...mcls import BaseObject
from ...waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Iterator

  MaybeInt: TypeAlias = Optional[int]

  ValueTuple: TypeAlias = tuple[Any, ...]
  ValueTuples: TypeAlias = tuple[ValueTuple, ...]

  Item: TypeAlias = Any
  Row: TypeAlias = tuple[Item, ...]
  Table: TypeAlias = tuple[Row, ...]

  from abc import ABC, abstractmethod
else:
  ABC, abstractmethod = object, lambda x: x


class BaseSampler(BaseObject, ABC):
  """
  BaseSampler provides the base class for sample classes in the
  'worktoy.work_test.samplers' package.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __key_groups__: dict[str, tuple[str, ...]] = dict()
  __key_types__: dict[str, type] = dict()
  __key_defaults__: dict[str, Any] = dict()

  #  Fallback Variables
  __fallback_col_count__: int = 1
  __fallback_row_count__: int = 1

  #  Private Variables
  __col_count__: MaybeInt = None
  __row_count__: MaybeInt = None

  #  Public Variables
  valueType: Field[type] = Field()
  # --#  Settings
  colCount: Field[int] = Field()
  rowCount: Field[int] = Field()

  #  Virtual Variables
  # --#  Samples
  item: Field[Any] = Field()
  row: Field[tuple[Any, ...]] = Field()
  table: Field[tuple[tuple[Any, ...], ...]] = Field()

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

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @colCount.SET
  def _setColCount(self, colCount: int) -> None:
    if not isinstance(colCount, int):
      raise TypeException('colCount', colCount, int)
    if colCount < 1:
      raise ValueError("""Column count must be a positive integer.""")
    self.__col_count__ = colCount

  @rowCount.SET
  def _setRowCount(self, rowCount: int) -> None:
    if not isinstance(rowCount, int):
      raise TypeException('rowCount', rowCount, int)
    if rowCount < 1:
      raise ValueError("""Row count must be a positive integer.""")
    self.__row_count__ = rowCount

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload()
  def __init__(self, **kwargs) -> None:
    defaults = self.__key_defaults__
    valTypes = self.__key_types__
    keys = (*(k for k, v in self.__key_groups__.items()),)
    cls = type(self)
    fields = {k: getattr(cls, k) for k in keys}
    getterKeys = {k: getattr(f, '__get_key__') for k, f in fields.items()}
    getters = {k: getattr(cls, g) for k, g in getterKeys.items()}
    existing = dict()
    for name, default in defaults.items():
      try:
        value = getters[name](self, _recursion=True)
      except RecursionError:
        existing[name] = default
      else:
        existing[name] = value
    for name, keys in self.__key_groups__.items():
      type_ = valTypes[name]
      default = existing[name]
      for key in keys:
        if key in kwargs:
          value = kwargs[key]
          if not isinstance(value, type_):
            raise TypeException(name, value, type_)
          setattr(self, name, value)
          break
      else:
        setattr(self, name, default)

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
    This method generates a tuple of 'n' sample values with 'n' given
    by the 'self.colCount' variable. Subclasses reimplementing this
    method are responsible for ensuring that the correct number of
    sample values are included in the generated tuple.

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
    and 'n' are specified by the 'self.rowCount' and 'self.colCount'
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
      out.append(self._getRow())
    return (*out,)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, ) -> Any:
    """
    Generates a single sample value by calling '_getItem'.
    """
    return self._getItem()

  def __iter__(self) -> Iterator[Any]:
    """
    Yields exactly 'self.rowCount' rows. Each yielded value is a row
    tuple produced by '_getRow', not a single sample value.
    """
    _c = int(self.rowCount)
    while _c:
      _c -= 1
      yield self._getRow()

  def __str__(self, ) -> str:
    infoSpec = """<%s: '%s' (%d, %d)>"""
    clsName = type(self).__name__
    typeName = self.valueType.__name__
    return infoSpec % (clsName, typeName, self.colCount, self.rowCount)

  def __repr__(self, ) -> str:
    infoSpec = """%s(colCount=%d, rowCount=%d)"""
    return infoSpec % (type(self).__name__, self.colCount, self.rowCount)
