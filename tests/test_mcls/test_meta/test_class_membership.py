"""
TestClassMembership tests the __class_len__, __class_bool__ and
__class_contains__ methods.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations
from unittest import TestCase

from worktoy.mcls import AbstractMetaclass

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Iterator, Any


class LenClass(metaclass=AbstractMetaclass):
  """
  LenClass defines '__class_len__'.
  """

  @classmethod
  def __class_len__(cls) -> int:
    return 5


class IterClass(metaclass=AbstractMetaclass):
  """
  IterClass provides iterable contents but no explicit length.
  """

  @classmethod
  def __class_iter__(cls) -> Iterator[int]:
    yield from [1, 2, 3, 4]


class VoidClass(metaclass=AbstractMetaclass):
  """
  VoidClass defines nothing special.
  """


class BoolClass(metaclass=AbstractMetaclass):
  """
  BoolClass defines '__class_bool__' explicitly.
  """

  @classmethod
  def __class_bool__(cls) -> bool:
    return False


class ContainClass(metaclass=AbstractMetaclass):
  """
  ContainClass defines a custom contains hook.
  """

  @classmethod
  def __class_contains__(cls, item: Any) -> bool:
    return item in {'foo', 'bar', 'baz'}


class TestClassLenBoolContains(TestCase):
  """
  Tests for '__class_len__', '__class_bool__', and '__class_contains__'.
  """

  def testExplicitClassLen(self) -> None:
    """
    Tests class with defined '__class_len__'.
    """
    self.assertEqual(len(LenClass), 5)

  def testFallbackLenFromIter(self) -> None:
    """
    Fallback to '__class_iter__' when '__class_len__' is missing.
    """
    self.assertEqual(len(IterClass), 4)

  def testClassLenTypeError(self) -> None:
    """
    Tests that len(VoidClass) raises TypeError.
    """
    with self.assertRaises(TypeError) as context:
      _ = len(VoidClass)
    info = str(context.exception)
    self.assertIn('object has no len()', info)

  def testExplicitClassBool(self) -> None:
    """
    Tests that '__class_bool__' overrides truth value.
    """
    self.assertFalse(bool(BoolClass))

  def testClassBoolFallbackToLen(self) -> None:
    """
    Fallback to '__class_len__' for truthiness.
    """
    self.assertTrue(bool(LenClass))

  def testClassBoolFallbackToIter(self) -> None:
    """
    Fallback to '__class_iter__' for truthiness.
    """
    self.assertTrue(bool(IterClass))

  def testClassBoolDefault(self) -> None:
    """
    VoidClass should fallback to default metaclass truth.
    """
    self.assertTrue(bool(VoidClass))  # Depends on your default

  def testExplicitClassContains(self) -> None:
    """
    Test that '__class_contains__' is respected.
    """
    self.assertIn('foo', ContainClass)
    self.assertNotIn('nope', ContainClass)

  def testContainsFallbackToIter(self) -> None:
    """
    IterClass uses fallback to '__class_iter__' for containment.
    """
    self.assertIn(3, IterClass)
    self.assertNotIn(999, IterClass)

  def testContainsTypeError(self) -> None:
    """
    VoidClass should raise TypeError on containment check.
    """
    with self.assertRaises(TypeError) as context:
      _ = 'foo' in VoidClass
    info = str(context.exception)
    self.assertIn('is not iterable', info)
