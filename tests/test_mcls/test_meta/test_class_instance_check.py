"""
TestClassInstanceCheck tests the functionality of the
'__class_instancecheck__' hook.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import MCLSTest
from worktoy.mcls import AbstractMetaclass
from worktoy.utilities import stringList
from worktoy.waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestClassInstanceCheck(MCLSTest):
  """
  TestClassInstanceCheck tests the functionality of the
  '__class_instancecheck__' hook.
  """

  @classmethod
  def setUpClass(cls) -> None:
    """
    unittest imports system is cancer
    """

    class NumberClass(metaclass=AbstractMetaclass):
      """
      self.Number is a simple class that can be used to test the
      '__class_instancecheck__' hook.
      """

      __test_number__ = True

      @classmethod
      def __class_instancecheck__(cls, instance: Any) -> bool:
        """
        Check if the instance is an instance of the class.
        """
        if isinstance(instance, (int, float, complex)):
          return True
        return False

      @classmethod
      def __class_subclasscheck__(cls, other: type) -> bool:
        """
        Check if the other class is a subclass of the class.
        """
        if not isinstance(other, type):
          raise TypeException('other', other, type)
        if other is cls:
          return True
        numberMethods = stringList("""__int__, __float__, __complex__""")
        for method in numberMethods:
          if hasattr(other, method):
            return True
        return False

    cls.Number = NumberClass

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def testDirectInstance(self) -> None:
    """
    Tests that a direct instance of self.Number passes isinstance.
    """
    number = self.Number()
    self.assertTrue(isinstance(number, self.Number))

  def testBuiltinInt(self) -> None:
    """
    Tests that a built-in int passes as instance of self.Number.
    """
    self.assertTrue(isinstance(7, self.Number))

  def testBuiltinFloat(self) -> None:
    """
    Tests that a built-in float passes as instance of self.Number.
    """
    self.assertTrue(isinstance(3.14, self.Number))

  def testBuiltinComplex(self) -> None:
    """
    Tests that a built-in complex passes as instance of self.Number.
    """
    self.assertTrue(isinstance(1 + 2j, self.Number))

  def testFakeNumber(self) -> None:
    """
    Tests that a non-numeric class does not pass as instance of self.Number.
    """
    self.assertFalse(isinstance((69,), self.Number))

  def testWrongTypeSubclass(self) -> None:
    """
    Tests that passing a non-type to issubclass raises.
    """
    with self.assertRaises(TypeException):
      issubclass(3.14, self.Number)

  def testBuiltinIntSubclass(self) -> None:
    """
    Tests that int is accepted as subclass of self.Number.
    """
    self.assertTrue(issubclass(int, self.Number))

  def testDuckTypedSubclass(self) -> None:
    """
    Tests that a class with __float__ counts as a self.Number subclass.
    """

    class Bad:
      def __floating_trust_me_bro__(self) -> float:
        return '1337 here bro!'

    class Good:
      def __float__(self) -> float:
        return .1337

      def __int__(self) -> int:
        return 80085

      def __complex__(self) -> complex:
        return 69 + 420j

    self.assertFalse(issubclass(Bad, self.Number))
    self.assertTrue(issubclass(Good, self.Number))
    with self.assertRaises(TypeError) as context:
      _ = float(Bad())
    self.assertEqual(int(Good()), 80085)
    self.assertAlmostEqual(float(Good()), 0.1337)
    self.assertAlmostEqual(complex(Good()).real, 69)
    self.assertAlmostEqual(complex(Good()).imag, 420)
    self.assertIsInstance(Bad().__floating_trust_me_bro__(), str)

  def testSelfSubclass(self) -> None:
    """
    Tests that self.Number is a subclass of itself.
    """
    self.assertTrue(issubclass(self.Number, self.Number))
