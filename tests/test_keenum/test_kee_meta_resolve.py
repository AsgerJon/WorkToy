"""
TestKeeMetaResolve subclasses 'KeeTest' and provides testing of different
resolution methods on the 'KeeMeta'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeMeta, KeeNum, Kee
from worktoy.waitaminute.keenum import KeeResolveError
from . import KeeTest
from .examples import CurrencyData, \
  CurrencyNum, \
  ElementData, \
  ElementNum, \
  PlanetData, PlanetNum

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Callable

  Contract: TypeAlias = Callable[[KeeMeta], None]


class TestKeeMetaResolve(KeeTest):
  """
  TestKeeMetaResolve subclasses 'KeeTest' and provides testing of different
  resolution methods on the 'KeeMeta'.
  """

  def _shuffleCase(self, text: str) -> str:
    self.randomInteger.colCount = len(text)
    c, C, X = str.lower(text), str.upper(text), self.randomInteger.row
    return ''.join((C if x % 2 else c for c, C, x in zip(c, C, X)))

  def nameContract(self, num: KeeMeta) -> None:
    """
    Resolve each member by its name in several case variants (exact,
    lower, shuffled, upper) via '_resolveFromName' and
    '_resolveMember', asserting both return that member. This checks
    that name resolution is case-insensitive.
    """
    self.assertIsInstance(num, KeeMeta)
    names = (*(m.name for m in num),)
    values = (*(m.value for m in num),)

    lowerCase = (*(str.lower(name) for name in names),)
    shuffleCase = (*(self._shuffleCase(name) for name in names),)
    upperCase = (*(str.upper(name) for name in names),)
    variants = (names, lowerCase, shuffleCase, upperCase)
    for variant in variants:
      for name, member in zip(variant, num):
        resolvedFromName = KeeMeta._resolveFromName(num, name)
        resolvedFromMember = KeeMeta._resolveMember(num, name)
        self.assertIs(resolvedFromName, member)
        self.assertIs(resolvedFromMember, member)

  def valueContract(self, num: KeeMeta) -> None:
    """
    Applying value based resolution testing to a 'KeeMeta' enumeration.
    """
    self.assertIsInstance(num, KeeMeta)
    names = (*(m.name for m in num),)
    values = (*(m.value for m in num),)

    for value, member in zip(values, num):
      resolvedFromValue = KeeMeta._resolveFromValue(num, value)
      self.assertIs(resolvedFromValue, member)

  def indexContract(self, num: KeeMeta) -> None:
    """
    Applying index based resolution testing to a 'KeeMeta' enumeration.
    """
    self.assertIsInstance(num, KeeMeta)
    for i, member in enumerate(num):
      resolvedFromIndex = KeeMeta.__getitem__(num, i)
      self.assertIs(resolvedFromIndex, member)

  def strRaisesContract(self, num: KeeMeta) -> None:
    """
    Applying 'str' resolution testing to a 'KeeMeta' enumeration, but
    expecting an error.
    """
    self.assertIsInstance(num, KeeMeta)
    realNames: tuple[str, ...] = (*(m.name for m in num),)
    realLower: tuple[str, ...] = (*(str.lower(name) for name in realNames),)
    self.randomWord.colCount = 2
    fakeNames: list[str] = [realNames[0], ]
    for _ in realNames:
      fakeName = str.join('_', (*self.randomWord.row,))
      list.append(fakeNames, fakeName)
    for fakeName in fakeNames:
      if fakeName.lower() in realLower:
        continue
      tried = KeeMeta._resolveFromName(num, fakeName)
      self.assertIs(tried, NotImplemented)
      with self.assertRaises(KeeResolveError) as context:
        _ = KeeMeta._resolveMember(num, fakeName)
      e = context.exception
      self.assertIs(e.keeNum, num)
      self.assertEqual(e.identifier, fakeName)

  def test_base_str_value_index(self, ) -> None:
    """
    This method applies 'str' resolution testing to all example
    enumerations.
    """

    contracts: tuple[Contract, Contract, Contract] = (
      self.nameContract,
      self.valueContract,
      self.indexContract,
    )
    nums = self.baseNums
    for num in nums:
      for contract in contracts:
        contract(num)

  def test_good_class_resolve(self, ) -> None:
    """
    This method tests the '__class_resolve__' method of 'KeeMeta' by
    creating a 'KeeMeta' enumeration with a custom resolver that always
    declines to resolve.
    """

    #  ________________
    #  Currency example
    #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

    currencyData = (
      CurrencyData('EUR', '€', 'Euro', 2),
      CurrencyData('DKK', 'kr', 'Krone', 2),
      CurrencyData('JPY', '¥', 'Yen', 0),
      CurrencyData('GBP', '£', 'Sterling', 2),
    )

    currencyNames = (
      'Euro',
      'Krone',
      'Yen',
      'Sterling',
    )

    for expectedData, name in zip(currencyData, currencyNames):
      resolvedMember = CurrencyNum(name)
      actualData = resolvedMember.value
      self.assertIsInstance(resolvedMember, CurrencyNum)
      self.assertIsInstance(actualData, CurrencyData)
      self.assertEqual(actualData, expectedData)

    #  _______________
    #  Element example
    #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

    elementData = (
      ElementData('hydrogen', 'H', 1, 1.008),
      ElementData('helium', 'He', 2, 4.0026),
      ElementData('lithium', 'Li', 3, 6.94),
      ElementData('beryllium', 'Be', 4, 9.0122),
      ElementData('boron', 'B', 5, 10.81),
      ElementData('carbon', 'C', 6, 12.011),
      ElementData('nitrogen', 'N', 7, 14.007),
      ElementData('oxygen', 'O', 8, 15.999),
      ElementData('fluorine', 'F', 9, 18.998),
      ElementData('neon', 'Ne', 10, 20.180),
    )

    elementSymbols = (
      'H',
      'He',
      'Li',
      'Be',
      'B',
      'C',
      'N',
      'O',
      'F',
      'Ne',
    )

    for expectedData, symbol in zip(elementData, elementSymbols):
      resolvedMember = ElementNum(symbol)
      actualData = resolvedMember.value
      self.assertIsInstance(resolvedMember, ElementNum)
      self.assertIsInstance(actualData, ElementData)
      self.assertEqual(actualData, expectedData)

    #  ______________
    #  Planet example
    #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨

    planetData = (
      PlanetData('mercury', 3.301e23, 2440.0, 0.39),
      PlanetData('venus', 4.867e24, 6052.0, 0.72),
      PlanetData('earth', 5.972e24, 6371.0, 1.00),
      PlanetData('mars', 6.417e23, 3390.0, 1.52),
      PlanetData('jupiter', 1.898e27, 69911.0, 5.20),
      PlanetData('saturn', 5.683e26, 58232.0, 9.58),
      PlanetData('uranus', 8.681e25, 25362.0, 19.22),
      PlanetData('neptune', 1.024e26, 24622.0, 30.05),
    )

    for data in planetData:
      resolved = PlanetNum(data)
      self.assertEqual(resolved.value, data)

  def test_bad_class_resolve(self, ) -> None:
    """
    This method tests the '__class_resolve__' method returning
    'NotImplemented'.
    """

    trollCurrencies = (
      CurrencyData('EXP', 'E', 'Exposure', 0),
      CurrencyData('CAP', 'Nuka', 'Bottle Cap', 0),
      CurrencyData('SCH', 'SB', 'Schrute Buck', 4),
      CurrencyData('STN', 'SN', 'Stanley Nickel', 0),
      CurrencyData('ZWD', '100T', 'Zimbabwe Dollar', 14),
      CurrencyData('USD', '$', 'US Dollar', 'yes'),
    )

    trollPlanets = (
      PlanetData('pluto', 1.309e22, 1188.3, 39.48),  # yeah I said it!
      PlanetData('themis', 1e25, 1e5, 1e5),
      PlanetData('Phaeton', 1e26, 1e4, 1e4),
      PlanetData('urmom', 1e30, 1e6, 1e6),
    )

    trollElements = (
      ElementData('trollium', 'Tr', 69, 420.69),
      ElementData('unobtainium', 'Uo', 420, 69.42),
      ElementData('Hesperium', 'Hp', 1337, 800.85),
      ElementData('Adamantium', 'Ad', 8008135, 6.7),
      ElementData('Nipponium', 'Np', 69, 420.69),
    )

    nums = (CurrencyNum, PlanetNum, ElementNum)
    trollData = (trollCurrencies, trollPlanets, trollElements)
    for num, data in zip(nums, trollData):
      for datum in data:
        resolved = num.__class_resolve__(datum)  # noqa
        self.assertIs(resolved, NotImplemented)

  def test_bad_str(self, ) -> None:
    """
    This method applies 'str' resolution testing to all example
    enumerations, but expects an error.
    """

    for num in self.baseNums:
      if num.valueType is str:
        continue
      self.strRaisesContract(num)

  def test_unhashable_value_num(self) -> None:
    """
    This method tests that a 'KeeNum' enumeration with unhashable values
    raises an error when trying to resolve from value.
    """

    testLists = [69, ], [69, 420, ], [69, 420, 1337, ]

    class UnhashableValueNum(KeeNum):
      A = Kee[list](testLists[0])
      B = Kee[list](testLists[1])
      C = Kee[list](testLists[2])

    type.__setattr__(UnhashableValueNum, '__valued_members__', None)
    with self.assertRaises(RecursionError):
      _ = UnhashableValueNum._getValuedMembers(_recursion=True)

    expectingNotImplemented = UnhashableValueNum._resolveFromValue([])
    self.assertIs(expectingNotImplemented, NotImplemented)

    for testList, member in zip(testLists, UnhashableValueNum):
      resolved = UnhashableValueNum(testList)
      self.assertIs(resolved, member)
      with self.assertRaises(TypeError):
        _ = UnhashableValueNum.valuedMembers[testList]
      with self.assertRaises(TypeError):
        _ = hash(member)
