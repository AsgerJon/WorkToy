"""
TestKeeNumBase tests the KeeNumBase class. This class provides a base for
the KeeNum class, but this class creation process if quite unconventional.
For this reason, much of this test code bypasses the normal KeeNum process
to target the _KeeNumBase class directly.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import KeeTest
from typing import TYPE_CHECKING

from worktoy.desc import Field
from worktoy.keenum import KeeMeta
from worktoy.utilities import maybe
from worktoy.waitaminute import TypeException, MissingVariable
from worktoy.waitaminute.meta import IllegalInstantiation

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestKeeNumBase(KeeTest):
  """
  TestKeeNumBase tests the KeeNumBase class. This class provides a base for
  the KeeNum class, but this class creation process if quite unconventional.
  For this reason, much of this test code bypasses the normal KeeNum process
  to target the _KeeNumBase class directly.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __core_keenum__ = None

  #  Public Variables
  coreNum = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @coreNum.GET
  def _getCoreNum(self, ) -> Any:
    """
    Returns the core KeeNum class.
    """

    def wrapper(name: str, ind: int, val: Any = None, **kwargs, ) -> Any:
      """
      Wrapper function to return the core KeeNum class.
      """
      num = self.__core_keenum__(_root=True)
      setattr(num, '__member_name__', name)
      setattr(num, '__member_index__', ind)
      setattr(num, '__member_value__', maybe(val, ind))
      setattr(num, '__value_type__', type(maybe(val, ind)))
      return num

    return wrapper

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def setUpClass(cls) -> None:
    """
    Collects the core KeeNum class from the KeeMeta metaclass.
    """
    cls.__core_keenum__ = KeeMeta.getCoreKeeNum()

  def setUp(self) -> None:
    """
    Sets up each test, but creating instances of _KeeNumBase. This
    requires unconventional instantiation as described in the documentation.
    """
    self.testNum1 = self.coreNum('test1', 0, 69, )
    self.testNum2 = self.coreNum('test2', 1, 420, )
    self.testNum3 = self.coreNum('test3', 2, 1337, )
    self.testNum4 = self.coreNum('test4', 3, 80085, )

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  TESTS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_missing_member_name(self) -> None:
    """
    Testing the errors raised when a member name is missing.
    """
    sus = self.__core_keenum__(_root=True)
    with self.assertRaises(AttributeError) as context:
      _ = sus.name
    e = context.exception
    c = e.__cause__
    self.assertIsInstance(c, MissingVariable)
    self.assertEqual(str(c), repr(c))
    self.assertEqual(c.varName, '__member_name__')
    self.assertEqual(c.varType, str, )

  def test_bad_member_name_type(self) -> None:
    """
    Testing the errors raised when a member name is of the wrong type.
    """
    sus = self.__core_keenum__(_root=True)
    sus.__member_name__ = 42
    with self.assertRaises(TypeException) as context:
      _ = sus.name
    e = context.exception
    self.assertEqual(e.varName, '__member_name__')
    self.assertEqual(e.actualObject, 42)
    self.assertEqual(e.actualType, int)
    self.assertEqual(e.expectedTypes, (str,))

  def test_missing_member_index(self) -> None:
    """
    Testing the errors raised when a member index is missing.
    """
    sus = self.__core_keenum__(_root=True)
    with self.assertRaises(AttributeError) as context:
      _ = sus.index
    e = context.exception
    c = e.__cause__
    self.assertIsInstance(c, MissingVariable)
    self.assertEqual(c.varName, '__member_index__')
    self.assertEqual(c.varType, int)

  def test_bad_member_index_type(self) -> None:
    """
    Testing the errors raised when a member index is of the wrong type.
    """
    sus = self.__core_keenum__(_root=True)
    sus.__member_index__ = """i'm an int, trust!"""
    with self.assertRaises(TypeException) as context:
      _ = sus.index
    e = context.exception
    self.assertEqual(e.varName, '__member_index__')
    self.assertEqual(e.actualObject, """i'm an int, trust!""")
    self.assertEqual(e.actualType, str)
    self.assertEqual(e.expectedTypes, (int,))

  def test_missing_member_value(self) -> None:
    """
    Testing the errors raised when a member value is missing.
    """
    sus = self.__core_keenum__(_root=True)
    setattr(sus, '__member_name__', """I'm not sus!""")
    self.assertEqual(sus.value, """I'M NOT SUS!""")

  def test_missing_value_type(self) -> None:
    """
    Testing the errors raised when a member value type is missing.
    """
    sus = self.__core_keenum__(_root=True)
    with self.assertRaises(AttributeError) as context:
      _ = sus.valueType
    e = context.exception
    self.assertIsInstance(e.__cause__, MissingVariable)
    self.assertEqual(e.__cause__.varName, '__value_type__')
    self.assertEqual(e.__cause__.varType, type, )

  def test_bad_value_type(self) -> None:
    """
    Testing the errors raised when a member value type is of the wrong type.
    """
    sus = self.__core_keenum__(_root=True)
    susType = """I'm a type, trust!"""
    setattr(sus, '__value_type__', susType)
    with self.assertRaises(TypeException) as context:
      _ = sus.valueType
    e = context.exception
    self.assertEqual(e.varName, '__value_type__')
    self.assertEqual(e.actualObject, susType)
    self.assertEqual(e.actualType, str)
    self.assertEqual(e.expectedTypes, (type,))

  def test_str_repr(self) -> None:
    """
    Testing the string representation of the KeeNumBase class.
    """
    self.assertEqual(str(self.testNum1), 'KeeNum.TEST1')
    self.assertEqual(repr(self.testNum1), """<KeeNum.TEST1[int]: 69>""")
    long = self.coreNum('LONG', 4, 'tro%s' % (69 * 'lo'))
    self.assertTrue(str.endswith(repr(long), '...'))

  def test_hashing(self, ) -> None:
    """
    Testing the hashing of the KeeNumBase class.
    """
    data = dict()
    data[self.testNum1] = '69'
    data[self.testNum2] = '420'
    data[self.testNum3] = '1337'
    data[self.testNum4] = '80085'

    testNums = [self.testNum1, self.testNum2, self.testNum3, self.testNum4]

    for num, (key, val) in zip(testNums, data.items()):
      self.assertIs(key, num)
      self.assertEqual(data[num], val)

  def test_eq(self, ) -> None:
    """
    Testing the equality of the KeeNumBase class.
    """
    self.assertEqual(self.testNum1, self.testNum1)
    left = self.coreNum('LEFT', 0, (69, 420))
    right = self.coreNum('RIGHT', 1, (69, 420))
    self.assertEqual(left, right)
    self.assertIs(left.__eq__('breh'), NotImplemented)

  def test_bad_init(self, ) -> None:
    """
    Testing the errors raised when the KeeNumBase class is initialized
    incorrectly.
    """
    with self.assertRaises(IllegalInstantiation) as context:
      _ = self.__core_keenum__()  # without _root=True
    e = context.exception
    self.assertIs(e.cls, self.__core_keenum__)

    from worktoy.keenum._keenum_base import _KeeNumBase

    with self.assertRaises(IllegalInstantiation) as context:
      _ = _KeeNumBase()
    e = context.exception
    self.assertIs(e.cls, _KeeNumBase)
