"""
TestPreClass tests the PreClass class from the static module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.static import PreClass
from worktoy.mcls import AbstractMetaclass
from worktoy.waitaminute import MissingVariable, TypeException

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestPreClass(TestCase):
  """
  TestPreClass tests the PreClass class.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_bad_type(self) -> None:
    """
    Tests that PreClass raises TypeException when passed wrong types.
    """
    badType = lambda: None
    with self.assertRaises(TypeException) as context:
      _ = PreClass(badType)
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.varName, 'arg')
    self.assertEqual(e.actualObject, badType)
    self.assertEqual(e.actualType, type(badType))
    self.assertEqual(
        e.expectedTypes,
        (str, int, type, tuple, list),
    )

  def test_instance_check(self) -> None:
    """
    Tests that PreClass instances are instances of type.
    """

    class Foo(metaclass=AbstractMetaclass):
      @classmethod
      def __class_hash__(cls, ) -> int:
        return 69420

      def __hash__(self) -> int:
        return 69420

    Pre = PreClass('Bar', 69420, type)
    foo = Foo()
    self.assertTrue(isinstance(Foo, Pre))
    self.assertIsInstance(Foo, Pre)
    self.assertEqual(hash(Foo()), 69420)

  def test_bad_hash(self) -> None:
    """
    Tests that a PreClass instance handles no hash correctly.
    """
    Pre = PreClass('Sus', )
    with self.assertRaises(MissingVariable) as context:
      _ = isinstance('breh', Pre)
    e = context.exception
    self.assertEqual(e.varName, '__hash_value__')
    self.assertEqual(e.varType, int)

  def test_wrong_type_hash(self) -> None:
    """
    Tests that a PreClass instance handles wrong type hash correctly.
    """
    Pre = PreClass('Sus', )
    setattr(Pre, '__hash_value__', 'smoke w**d everyday!')
    with self.assertRaises(TypeException) as context:
      _ = isinstance('breh', Pre)
    e = context.exception
    self.assertEqual(e.varName, '__hash_value__')
    self.assertEqual(e.actualObject, 'smoke w**d everyday!')
    self.assertEqual(e.actualType, str)
    self.assertEqual(e.expectedTypes, (int,))

  def test_meta_class(self) -> None:
    """
    Tests that a PreClass instantiated with a non-strict subclass of type
    correctly returns that metaclass when the '__class__' attribute on an
    instance of it is accessed.
    """
    breh = PreClass('Breh', 69420, AbstractMetaclass)
    self.assertIs(breh.__class__, AbstractMetaclass)
