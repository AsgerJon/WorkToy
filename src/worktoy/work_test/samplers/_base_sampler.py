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

  The settings are boxes, apart from 'seed'. 'colCount' and 'rowCount',
  one each unless set, size a row and a table, with 'width', 'size',
  'height' and 'count' as aliases and as keywords, and a count below
  one is refused with 'ValueError'; a subclass declares its own
  settings the same way. The keyword constructor takes every setting
  by the synonyms '__key_groups__' lists, merged along the resolution
  order so that a subclass adds its own groups, assigns the first
  synonym present of each, and refuses a keyword that names no setting
  with the 'TypeError' Python raises for an unexpected keyword
  argument. A box casts the value assigned when it converts without
  loss and refuses it otherwise with 'TypeException' naming the
  setting. '_applySettings' receives the values found, so a subclass
  holding a pair of settings may write them together. Every draw goes
  to 'random', a 'random.Random' built for each sampler apart. 'seed'
  is a field over the seed last given, 'None' until an 'int' is given,
  by keyword or by assignment, which seeds that generator, so two
  samplers seeded alike draw alike whatever else draws in between; it
  takes an 'int' alone and casts nothing. 'item', 'row' and 'table'
  draw one value, a row of 'colCount' values and a table of 'rowCount'
  rows; 'row', and 'table' through it, check each value against
  'valueType', while 'item' and a call of the sampler hand out what
  '_getItem' gives as it is. Iterating the sampler yields 'rowCount'
  rows. The two hooks are abstract, and a class that leaves either out
  cannot be instantiated.

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
    A sampler class declares the settings it adds and inherits the rest,
    so the keyword constructor needs the synonyms of every setting along
    the resolution order, and a subclass must be able to give a setting
    it inherits other synonyms.

    Implementation
    --------------

    '__key_groups__' is read from the own dictionary of each class
    along the resolution order, and the nearest class declaring a
    setting answers for it.

    Returns
    -------

    KeyGroups
      A 'dict[str, tuple[str, ...]]' from each setting to its synonyms,
      the settings of the nearest class first.
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
    A sampler is sized, narrowed and seeded in the expression that
    creates it, each setting under whichever of its usual names the test
    writes, and a name that is no setting, most often a misspelled one,
    must not pass in silence.

    Implementation
    --------------

    A keyword naming no setting is refused first, as Python refuses an
    unexpected keyword argument. Each setting then takes the first of
    its synonyms present, by assignment. A box casts what converts
    without loss, so an 'int' bound suits a float sampler, and refuses a
    lossy value with 'TypeException' naming the setting; 'seed' takes an
    'int' alone.

    Parameters
    ----------

    **kwargs
      The settings, each under any of its synonyms.

    Raises
    ------

    TypeError
      A keyword names no setting.

    TypeException
      A setting refuses its value.

    ValueError
      A count is below one.
    """
    self._refuseUnknown(**kwargs)
    self._applySettings(self._collectSettings(**kwargs))

  def _refuseUnknown(self, **kwargs) -> None:
    """
    A keyword the sampler does not know, most often a misspelled
    setting, must not pass in silence: the test would run on a default
    it believes it replaced.

    Implementation
    --------------

    A keyword among the synonyms of no setting raises, worded as Python
    words an unexpected keyword argument.

    Raises
    ------

    TypeError
      A keyword names no setting.
    """
    groups = self._getKeyGroups()
    accepted = [key for keys in groups.values() for key in keys]
    for key in kwargs:
      if key not in accepted:
        infoSpec = """%s() got an unexpected keyword argument '%s'"""
        raise TypeError(infoSpec % (type(self).__name__, key))

  def _collectSettings(self, **kwargs) -> Settings:
    """
    A setting may be written under several names, and the constructor
    needs each setting once, under its own name, whichever synonym the
    caller used.

    Implementation
    --------------

    For each setting the synonyms are tried in the order
    '__key_groups__' lists them, and the first one present gives the
    value; a further synonym of the same setting is passed over.

    Returns
    -------

    Settings
      A 'dict[str, Any]' from the name of each setting found to its
      value.
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
    The settings found among the keywords must reach the sampler, and a
    subclass whose settings belong together, as two bounds do, must be
    able to write them in one step, so that neither is checked against
    a value of the other that is about to be replaced.

    Implementation
    --------------

    Each setting is assigned under its own name: a box casts or refuses
    the value, and 'seed' takes an 'int' alone. A subclass holding such
    a pair reimplements the method, takes the pair out of the settings,
    writes it, and hands the rest on to this one.

    Parameters
    ----------

    settings : Settings
      A 'dict[str, Any]' from the name of each setting found to its
      value.
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
    A test often wants several values at once, and wants to trust that
    every one of them is of the type the sampler names.

    Implementation
    --------------

    'colCount' values are drawn through '_getItem', and each is checked
    against 'valueType'. A subclass reimplementing the method sees to
    the number of values, and to their type, itself.

    Returns
    -------

    Row
      A 'tuple[Any, ...]' of 'colCount' values.

    Raises
    ------

    TypeException
      '_getItem' gave a value that is no instance of 'valueType'.
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
    A test of anything laid out in rows wants a whole table of values
    from one read.

    Implementation
    --------------

    'rowCount' rows are drawn through '_getRow'. A subclass
    reimplementing the method sees to the number of rows itself.

    Returns
    -------

    Table
      A 'tuple[tuple[Any, ...], ...]' of 'rowCount' rows, each of
      'colCount' values.
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
    A sampler handed over where a function of no arguments is expected,
    as a factory of values, must give one value at each call.

    Implementation
    --------------

    The call returns what '_getItem' gives, unchecked, as 'item' does.
    """
    return self._getItem()

  def __iter__(self) -> Iterator[Any]:
    """
    A loop over a sampler must end, so iterating one is a loop over a
    table of its rows, not over values without end.

    Implementation
    --------------

    'rowCount' is read once, as the iteration starts, and that many rows
    are yielded, each drawn by '_getRow' when the loop asks for it.

    Yields
    ------

    Row
      A 'tuple[Any, ...]' of 'colCount' values.
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
    A sampler shown in a failure message should say how it is set, so
    that the data of the failing test can be drawn again.

    Implementation
    --------------

    Every setting of the key groups is named with its value, the
    settings of the nearest class first, as 'IntSampler(minVal=0,
    maxVal=255, colCount=1, rowCount=1, seed=None)'.
    """
    parts = []
    for name in self._getKeyGroups():
      value = object.__getattribute__(self, name)
      parts.append('%s=%r' % (name, value))
    return '%s(%s)' % (type(self).__name__, ', '.join(parts))
