"""TestEZData tests the functionality of EZData"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Self
except ImportError:
  Self = object

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.ezdata import EZData, IllegalInitException, \
  IllegalMethodException, NoDefaultError, AmbiguousDefaultError, \
  DefaultTypeMismatchError
from worktoy.text import monoSpace


class SomeData(EZData):
  """SomeData is a subclass of EZData. """

  a = AttriBox[int](0)
  b = AttriBox[int](0)
  c = AttriBox[int](0)
  d = AttriBox[int](0)


class TestEZData(TestCase):
  """TestEZData tests the functionality of EZData"""

  def setUp(self) -> None:
    """Sets up each test"""
    self.data0 = SomeData()
    self.data1 = SomeData(69)
    self.data2 = SomeData(69, 420)
    self.data3 = SomeData(69, 420, 1337)
    self.data4 = SomeData(69, 420, 1337, 80085)
    self.other4 = SomeData(69, 420, 1337, 80085)

  def test_init(self) -> None:
    """Tests that default values are used correctly"""
    self.assertEqual(self.data0.a, 0)
    self.assertEqual(self.data0.b, 0)
    self.assertEqual(self.data0.c, 0)
    self.assertEqual(self.data0.d, 0)

  def test_init1(self) -> None:
    """Tests that single values are used correctly"""
    self.assertEqual(self.data1.a, 69)
    self.assertEqual(self.data1.b, 0)
    self.assertEqual(self.data1.c, 0)
    self.assertEqual(self.data1.d, 0)

  def test_init2(self) -> None:
    """Tests that double values are used correctly"""
    self.assertEqual(self.data2.a, 69)
    self.assertEqual(self.data2.b, 420)
    self.assertEqual(self.data2.c, 0)
    self.assertEqual(self.data2.d, 0)

  def test_init3(self) -> None:
    """Tests that triple values are used correctly"""
    self.assertEqual(self.data3.a, 69)
    self.assertEqual(self.data3.b, 420)
    self.assertEqual(self.data3.c, 1337)
    self.assertEqual(self.data3.d, 0)

  def test_init4(self) -> None:
    """Tests that quadruple values are used correctly"""
    self.assertEqual(self.data4.a, 69)
    self.assertEqual(self.data4.b, 420)
    self.assertEqual(self.data4.c, 1337)
    self.assertEqual(self.data4.d, 80085)

  def test_str(self) -> None:
    """Tests that the string representation is correct"""
    expected = """SomeData(69, 420, 1337, 80085)"""
    self.assertEqual(str(self.data4), expected)

  def test_eq(self, ) -> None:
    """Testing that the equality operator works correctly"""
    self.assertEqual(self.data4, self.other4)

  def test_bad_init(self, ) -> None:
    """Subclasses of EZData are not allowed to define methods. If it
    attempts to define '__init__' a special exception is raised. This
    method tests that IllegalInitException raises correctly."""

    with self.assertRaises(IllegalInitException):
      class SusData(EZData):
        """SusData tries to implement __init__!"""

        def __init__(self, *__, **_) -> None:
          pass

  def test_bad_method(self) -> None:
    """Subclasses of EZData are not allowed to define any methods. For all
    other methods than __init__ the expected error type is
    IllegalMethodException."""

    with self.assertRaises(IllegalMethodException):
      class SusData(EZData):
        """SusData tries to implement a method!"""

        def createGlobalVariables(self, ) -> None:
          """Hey kids, u wanna try some global variables?"""
          pass

  def test_bad_attribox(self) -> None:
    """Subclasses of EZData must set their fields as instances of AttriBox
    and these must have exactly one positional argument to indicate
    default value. Not providing such a default value, will raise
    NoDefaultError. Providing more than one positional arguments to the
    AttriBox is not allowed either and should raise AmbiguousDefaultError.
    Finally, if the given default value is not an instance of the field
    class given, a DefaultTypeMismatchError is raised."""

    with self.assertRaises(NoDefaultError):
      class SusData(EZData):
        """SusData fails to provide default value!"""

        a = AttriBox[int]()  # The required default value is missing!

    with self.assertRaises(AmbiguousDefaultError):
      class SusData2(EZData):
        """SusData2 provides two default values!"""

        a = AttriBox[int](69, 420)

    with self.assertRaises(DefaultTypeMismatchError):
      class SusData3(EZData):
        """SusData3 sets a default value of the wrong type!"""

        a = AttriBox[int]('ur mom')
