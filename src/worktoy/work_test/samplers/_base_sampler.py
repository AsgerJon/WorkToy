"""
BaseSampler is the base class of the sample-data generators.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from random import Random
from typing import TYPE_CHECKING, Any

from ...dispatch import overload
from ...desc import Field, Alias, AttriBox
from ...mcls import BaseObject
from ...waitaminute import TypeException
from . import SamplerMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias, Optional, Iterator

  Item: TypeAlias = Any
  Row: TypeAlias = tuple[Item, ...]
  Table: TypeAlias = tuple[Row, ...]
  KeyGroups: TypeAlias = dict[str, tuple[str, ...]]
  Settings: TypeAlias = dict[str, Any]


class BaseSampler(BaseObject, metaclass=SamplerMeta):
  """
  A test that needs random data wants a sampler it can size, narrow and
  seed in one expression, draw from one value, one row or one table at
  a time, and trust to give values of one type; and a sampler for a new
  kind of value should take a value type and a single-sample recipe and
  nothing more. 'BaseSampler' is that base. 'IntSampler' and the other
  samplers of the package supply the two hooks, and a sampler of a
  project does the same:

    class DieSampler(BaseSampler):

      sides = AttriBox[int](6)

      def _getValueType(self, **kwargs) -> type:
        return int

      def _getItem(self, *args, **kwargs) -> int:
        return self.random.randint(1, self.sides)

  Implementation
  --------------

  The settings are boxes. 'colCount' and 'rowCount', one each unless
  set, size a row and a table, with 'width', 'size', 'height' and
  'count' as aliases and as keywords, and a count below one is refused
  with 'ValueError'; a subclass declares its own settings the same way.
  The keyword constructor takes every setting by the synonyms
  '__key_groups__' lists, merged along the resolution order so that a
  subclass adds its own groups, writes the first synonym present of
  each through its box, which casts what converts without loss and
  refuses the rest with 'TypeException' naming the setting, and refuses
  a keyword that names no setting with the 'TypeError' Python raises
  for an unexpected keyword argument. '_applySettings' receives the
  values found, so a subclass holding a pair of settings may write them
  together. Every draw goes to 'random', a 'random.Random' built for
  each sampler apart; 'seed' is 'None' until an 'int' is given, by
  keyword or by assignment, which seeds that generator, so two samplers
  seeded alike draw alike whatever else draws in between. 'item', 'row'
  and 'table' draw one value, a row of 'colCount' values and a table of
  'rowCount' rows, each value checked against 'valueType'; calling the
  sampler draws one value and iterating it yields 'rowCount' rows. The
  two hooks are abstract, and 'SamplerMeta' refuses a sampler without
  both.

  Attributes
  ----------

  colCount, rowCount : int
    The values in a row and the rows in a table.

  random : random.Random
    The generator of this sampler.

  seed : int or None
    The seed the generator was last given, 'None' when never seeded.

  valueType : type
    The class of every value drawn.

  item, row, table
    One value, one row and one table, drawn afresh at each read.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __key_groups__: KeyGroups = dict(
      colCount=('colCount', 'width', 'size'),
      rowCount=('rowCount', 'height', 'count'),
      seed=('seed', 'randomSeed'),
  )

  #  Private Variables
  __seed_value__: Optional[int] = None

  #  Public Variables
  colCount = AttriBox[int](1)
  rowCount = AttriBox[int](1)
  random = AttriBox[Random]()
  seed: Field[Optional[int]] = Field()
  valueType: Field[type] = Field()

  #  Virtual Variables
  item: Field[Any] = Field()
  row: Field[Row] = Field()
  table: Field[Table] = Field()

  #  Aliases
  width = Alias('colCount')
  height = Alias('rowCount')
  size = Alias('colCount')
  count = Alias('rowCount')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @seed.GET
  def _getSeed(self) -> Optional[int]:
    return self.__seed_value__

  @classmethod
  def _getKeyGroups(cls) -> KeyGroups:
    """
    The '_getKeyGroups' method returns the synonyms of every setting the
    class and its bases declare in '__key_groups__', the nearest class
    answering for a setting declared more than once, so a subclass may
    redeclare the synonyms of a setting it inherits.
    """
    out = dict()
    for base in cls.__mro__:
      if '__key_groups__' not in vars(base):
        continue
      for name, keys in vars(base)['__key_groups__'].items():
        if name in out:
          continue
        out[name] = keys
    return out

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @seed.SET
  def _setSeed(self, seed: int) -> None:
    if not isinstance(seed, int):
      raise TypeException('seed', seed, int)
    self.__seed_value__ = seed
    self.random.seed(seed)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NOTIFIERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @colCount.preSet
  def _refuseColCount(self, value: Any) -> None:
    if isinstance(value, (int, float)) and value < 1:
      raise ValueError("""Column count must be a positive integer.""")

  @rowCount.preSet
  def _refuseRowCount(self, value: Any) -> None:
    if isinstance(value, (int, float)) and value < 1:
      raise ValueError("""Row count must be a positive integer.""")

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload()
  def __init__(self, **kwargs) -> None:
    """
    The keyword constructor sets each setting from the first of its
    synonyms present, through its box, so an 'int' bound suits a float
    sampler and a lossy value is refused with 'TypeException' naming the
    setting. A keyword naming no setting raises the 'TypeError' Python
    raises for an unexpected keyword argument.
    """
    self._refuseUnknown(**kwargs)
    self._applySettings(self._collectSettings(**kwargs))

  def _refuseUnknown(self, **kwargs) -> None:
    """
    The '_refuseUnknown' method raises 'TypeError' for a keyword that is
    none of the synonyms of any setting, such as a misspelled one.
    """
    groups = self._getKeyGroups()
    accepted = [key for keys in groups.values() for key in keys]
    for key in kwargs:
      if key not in accepted:
        infoSpec = """%s() got an unexpected keyword argument '%s'"""
        raise TypeError(infoSpec % (type(self).__name__, key))

  def _collectSettings(self, **kwargs) -> Settings:
    """
    The '_collectSettings' method returns the value of each setting from
    the first of its synonyms present in the keywords, by the name of
    the setting.
    """
    out = dict()
    for name, keys in self._getKeyGroups().items():
      for key in keys:
        if key in kwargs:
          out[name] = kwargs[key]
          break
    return out

  def _applySettings(self, settings: Settings) -> None:
    """
    The '_applySettings' method writes each setting found through its
    box, which casts or refuses the value. A subclass holding a pair of
    settings that belong together overrides it to write the pair at
    once and hands the rest on.
    """
    for name, value in settings.items():
      setattr(self, name, value)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  REQUIRED METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @abstractmethod
  @valueType.GET
  def _getValueType(self, **kwargs) -> type:
    """
    A sampler returns here the class of every value it draws; 'row'
    checks each value against it.
    """

  @abstractmethod
  @item.GET
  def _getItem(self, *args, **kwargs) -> Any:
    """
    A sampler draws here one value of its value type from 'self.random',
    the generator of the sampler, so that a seeded sampler draws the
    same values again.

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
    The 'row' getter generates a tuple of 'n' sample values, with 'n'
    given by the 'self.colCount' variable. Subclasses reimplementing this
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
  def _getTable(self, ) -> Table:
    """
    The 'table' getter generates 'N' tuples each with 'n' sample values,
    where 'N' and 'n' are given by the 'self.rowCount' and 'self.colCount'
    variables respectively. Subclasses reimplementing this are
    responsible for ensuring that the correct number of tuples and sample
    values are included in the generated tuples.

    Returns
    -------
    Table
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
    Calling a sampler draws a single sample value through '_getItem'.
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
    """
    The 'repr' of a sampler names every setting of its key groups with
    its value, as 'IntSampler(minVal=0, maxVal=255, colCount=1,
    rowCount=1, seed=None)'.
    """
    parts = []
    for name in self._getKeyGroups():
      value = object.__getattribute__(self, name)
      parts.append('%s=%r' % (name, value))
    return '%s(%s)' % (type(self).__name__, ', '.join(parts))
