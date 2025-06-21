"""
TestClassInstanceCheck tests the functionality of the
'__class_instancecheck__' hook.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.attr import Field
from worktoy.parse import maybe
from worktoy.static import AbstractObject
from worktoy.mcls import AbstractMetaclass
from worktoy.text import stringList
from worktoy.waitaminute import TypeException

from .. import ComplexNumber

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any


class Number(ComplexNumber):
  """
  Number is a simple class that can be used to test the
  '__class_instancecheck__' hook.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_instancecheck__(cls, instance: Any) -> bool:
    """
    Check if the instance is an instance of the class.
    """
    if type(instance) is cls:
      return True
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


class SusNumber:
  """
  This is not a number. It just pretends to be one.
  """

  pass


class TestClassInstanceCheck(TestCase):
  """
  TestClassInstanceCheck tests the functionality of the
  '__class_instancecheck__' hook.
  """

  def testDirectInstance(self) -> None:
    """
    Tests that a direct instance of Number passes isinstance.
    """
    self.assertTrue(isinstance(Number(), Number))

  def testBuiltinInt(self) -> None:
    """
    Tests that a built-in int passes as instance of Number.
    """
    self.assertTrue(isinstance(7, Number))

  def testBuiltinFloat(self) -> None:
    """
    Tests that a built-in float passes as instance of Number.
    """
    self.assertTrue(isinstance(3.14, Number))

  def testBuiltinComplex(self) -> None:
    """
    Tests that a built-in complex passes as instance of Number.
    """
    self.assertTrue(isinstance(1 + 2j, Number))

  def testFakeNumber(self) -> None:
    """
    Tests that a non-numeric class does not pass as instance of Number.
    """
    self.assertFalse(isinstance(SusNumber(), Number))

  def testWrongTypeSubclass(self) -> None:
    """
    Tests that passing a non-type to issubclass raises.
    """
    with self.assertRaises(TypeException):
      issubclass(3.14, Number)

  def testBuiltinIntSubclass(self) -> None:
    """
    Tests that int is accepted as subclass of Number.
    """
    self.assertTrue(issubclass(int, Number))

  def testFakeNumberSubclass(self) -> None:
    """
    Tests that a fake numeric class with no magic methods fails.
    """
    self.assertFalse(issubclass(SusNumber, Number))

  def testDuckTypedSubclass(self) -> None:
    """
    Tests that a class with __float__ counts as a Number subclass.
    """

    class Floaty:
      def __float__(self) -> float:
        return 42.0

    self.assertTrue(issubclass(Floaty, Number))
